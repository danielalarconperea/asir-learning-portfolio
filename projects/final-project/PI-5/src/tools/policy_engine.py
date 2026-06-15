"""
Policy Engine — Sentinel-IT (PI-5)

Sustituye la blacklist por substring de iot_tools.py por una clasificacion de
comandos en cuatro niveles de riesgo (SAFE_READ / LOW / HIGH / CRITICAL).

Filosofia:
    * Lectura pura se ejecuta sin friccion (incluso `sudo cat /var/log/...`).
    * Escritura acotada pasa por HITL con etiqueta de nivel.
    * Solo lo destructivo no reversible exige doble confirmacion explicita
      desde el dashboard (CRITICAL).
    * Lo desconocido NO se deniega automaticamente: cae a LOW y llega al
      humano. Esto es deliberado para no entorpecer al agente IA.

Capas adicionales:
    * Firma Ed25519 en el envio y verificacion preventiva en PI-4.
    * audit(...)  -> escritura inmutable en la tabla `audit_log`.
"""

from __future__ import annotations

import logging
import os
import re
import shlex
import sqlite3
import time
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Optional

import yaml

logger = logging.getLogger("CoordinatorSOC")

# ---------------------------------------------------------------------------
# Configuracion (ruta a la BD)
# ---------------------------------------------------------------------------
_BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
_CONFIG_PATH = os.path.join(_BASE_DIR, 'config.yml')
try:
    with open(_CONFIG_PATH, "r") as _f:
        _config = yaml.safe_load(_f)
    DB_PATH = os.path.join(_BASE_DIR, _config['database']['db_path'])
except Exception:
    DB_PATH = os.path.join(_BASE_DIR, "soc_data.db")


# ---------------------------------------------------------------------------
# Niveles
# ---------------------------------------------------------------------------
class RiskLevel(IntEnum):
    SAFE_READ = 0
    LOW = 1
    HIGH = 2
    CRITICAL = 3

    def label(self) -> str:
        return self.name


@dataclass
class Classification:
    level: RiskLevel
    parsed_verb: str
    reasons: list = field(default_factory=list)
    is_executable_via_interpreter: bool = False

    def to_dict(self) -> dict:
        return {
            "level": self.level.label(),
            "verb": self.parsed_verb,
            "reasons": list(self.reasons),
            "interpreter": self.is_executable_via_interpreter,
        }


@dataclass
class Decision:
    allow_direct: bool          # True solo para SAFE_READ
    classification: Classification

    @property
    def level(self) -> RiskLevel:
        return self.classification.level


# ---------------------------------------------------------------------------
# Catalogos de verbos (heuristica, no whitelist cerrada)
# ---------------------------------------------------------------------------
_READ_VERBS = {
    "cat", "ls", "ll", "grep", "egrep", "fgrep", "ss", "netstat", "ps",
    "journalctl", "tail", "head", "less", "more", "id", "whoami", "uname",
    "df", "du", "free", "uptime", "who", "w", "last", "stat", "file", "wc",
    "hostname", "dig", "host", "nslookup", "ping", "traceroute", "tracepath",
    "awk", "cut", "sort", "uniq", "tr", "env", "printenv", "true", "echo",
    "date", "lsblk", "lsof", "lspci", "lsusb", "iostat", "vmstat", "mpstat",
    "tcpdump", "find",  # solo lectura aunque sea sudo, salvo flags mutantes
}

_BOUNDED_WRITE_VERBS = {
    "iptables", "ip6tables", "ufw", "nft", "firewall-cmd",
}

_BROAD_WRITE_VERBS = {
    "systemctl", "service", "kill", "pkill", "mount", "umount",
    "chmod", "chown", "useradd", "usermod", "passwd", "iptables-restore",
    "ip", "tc", "sysctl", "modprobe", "rmmod",
}

_DESTRUCTIVE_VERBS = {
    "rm", "dd", "mkfs", "shutdown", "reboot", "halt", "poweroff",
    "userdel", "fdisk", "parted", "wipefs", "shred", "init",
}

_INTERPRETER_VERBS = {"bash", "sh", "zsh", "dash", "ash", "php", "python",
                     "python3", "perl", "ruby", "node", "lua", "eval", "exec"}
_INTERPRETER_EXEC_FLAGS = {"-c", "-e", "-r", "--command", "-x"}  # ejecucion en linea

_SHELL_METACHARS = (";", "&&", "||", "`", "$(", ">", "|")  # presencia cruda en str
# (las pipes legitimas dentro de un solo verbo de lectura son frecuentes y se
#  tratan especial en la deteccion)

_SENSITIVE_WILDCARD_PATHS = ("/etc/", "/boot/", "/sys/", "/proc/", "/var/lib/",
                            "/dev/sd", "/dev/nvme", "/dev/disk", "/root/")

# Constructos que ejecutan codigo aunque vivan DENTRO de comillas. Un verbo
# de lectura con uno de estos en sus argumentos deja de ser lectura pura:
# `awk 'BEGIN{system("rm -rf /")}'` o `grep "$(malicioso)" f` no deben
# auto-ejecutarse jamas. (_detect_shell_metachars ignora lo entrecomillado a
# proposito; esta lista cubre ese hueco para el caso critico de SAFE_READ.)
_EMBEDDED_EXEC_PATTERNS = ("$(", "`", "system(", "popen(", "exec(", "<(")

_IP_REGEX = re.compile(r"^\d{1,3}(\.\d{1,3}){3}$")

# IP IPv4 como SUBCADENA (cubre `--add-source=1.2.3.4` y rich-rules, donde la IP
# no es un token completo y _IP_REGEX no la ve). Solo IPv4: las reglas IPv6 caen
# a HIGH (fail-safe, van igualmente a HITL).
_IP_SUBSTR = re.compile(r"\b\d{1,3}(?:\.\d{1,3}){3}\b")
# Redes comodin muy amplias (/0../7 = >=16M hosts): NO cuentan como "IP concreta".
_WILDCARD_NET = re.compile(r"\d{1,3}(?:\.\d{1,3}){3}/[0-7]\b")


def _has_ip(flat: str) -> bool:
    """
    True si hay una IPv4 CONCRETA en `flat`. Ignora la IP que aparezca tras
    `comment` (texto libre de nft, no un selector) y descarta redes comodin
    amplias (0.0.0.0/0): una regla `accept 0.0.0.0/0` abre el firewall y NO debe
    bajar a LOW por contener una "IP".
    """
    scan = flat.split(" comment ", 1)[0]
    matches = list(_IP_SUBSTR.finditer(scan))
    if not matches:
        return False
    concretas = [m for m in matches if not _WILDCARD_NET.match(scan[m.start():])]
    return bool(concretas)


# Veredictos de nft que confirman una regla de filtrado (no solo estructura).
_NFT_VERDICTS = ("drop", "accept", "reject", "queue", "dnat", "snat", "masquerade")


def _has_verdict(flat: str) -> bool:
    toks = flat.split()
    return any(v in toks for v in _NFT_VERDICTS)


# Flags de firewall-cmd que mutan estado (para distinguir lectura de escritura).
_FW_MUTATING_PREFIXES = ("--add", "--remove", "--change", "--set", "--new",
                         "--delete", "--panic-on", "--reload", "--runtime-to-permanent")


def _has_mutating_flag(args: list) -> bool:
    return any(a.split("=")[0].startswith(_FW_MUTATING_PREFIXES) for a in args)


# ---------------------------------------------------------------------------
# Clasificador
# ---------------------------------------------------------------------------
def classify(cmd: str) -> Classification:
    """
    Devuelve una Classification con el nivel inferido del comando.

    No lanza excepciones: cualquier fallo de parseo se traduce a HIGH con la
    razon documentada. La idea es que el humano siempre pueda decidir.
    """
    raw = (cmd or "").strip()
    if not raw:
        return Classification(
            level=RiskLevel.HIGH,
            parsed_verb="",
            reasons=["comando vacio: tratado como HIGH para forzar revision"],
        )

    reasons: list = []

    # Saltos de linea = separador de comandos (shlex los trata como whitespace y
    # fusionaria 'cat x\nsystemctl restart y' en un solo verbo de lectura). Se
    # clasifica cada linea por separado: SAFE_READ solo si TODAS lo son.
    newline_segments = _split_unquoted_newlines(raw)
    if len(newline_segments) > 1:
        seg_classes = [classify(s) for s in newline_segments]
        if all(seg.level == RiskLevel.SAFE_READ for seg in seg_classes):
            return Classification(
                level=RiskLevel.SAFE_READ,
                parsed_verb=" / ".join(seg.parsed_verb for seg in seg_classes),
                reasons=["comando multilinea: todos los tramos son lectura",
                         *[r for seg in seg_classes for r in seg.reasons]],
            )
        highest = max(seg.level for seg in seg_classes)
        return Classification(
            level=max(RiskLevel.HIGH, highest),
            parsed_verb=seg_classes[0].parsed_verb,
            reasons=["comando multilinea con tramo mutante",
                     *[r for seg in seg_classes for r in seg.reasons]],
        )

    pipe_segments = _split_unquoted_pipe(raw)
    if len(pipe_segments) > 1:
        segment_classes = [classify(segment) for segment in pipe_segments]
        if all(seg.level == RiskLevel.SAFE_READ for seg in segment_classes):
            joined_verbs = " | ".join(seg.parsed_verb for seg in segment_classes)
            return Classification(
                level=RiskLevel.SAFE_READ,
                parsed_verb=joined_verbs,
                reasons=[
                    "pipeline compuesto solo por comandos de lectura",
                    *[reason for seg in segment_classes for reason in seg.reasons],
                ],
            )
        highest = max(seg.level for seg in segment_classes)
        return Classification(
            level=max(RiskLevel.HIGH, highest),
            parsed_verb=segment_classes[0].parsed_verb if segment_classes else "",
            reasons=[
                "pipeline contiene tramo no clasificado como lectura pura",
                *[reason for seg in segment_classes for reason in seg.reasons],
            ],
        )

    # --- 1) Tokenizacion con shlex (modo POSIX) ---
    try:
        tokens = shlex.split(raw, posix=True)
    except ValueError as exc:
        # Comillas mal cerradas, escapes raros... Mejor llega al humano.
        return Classification(
            level=RiskLevel.HIGH,
            parsed_verb=raw.split()[0] if raw else "",
            reasons=[f"shlex no pudo parsear: {exc}"],
        )

    if not tokens:
        return Classification(
            level=RiskLevel.HIGH,
            parsed_verb="",
            reasons=["sin tokens tras parseo"],
        )

    # --- 2) Saltar sudo y env ---
    sudo_present = False
    while tokens and tokens[0] in ("sudo", "env"):
        if tokens[0] == "sudo":
            sudo_present = True
        tokens.pop(0)
    if not tokens:
        return Classification(
            level=RiskLevel.HIGH,
            parsed_verb="sudo" if sudo_present else "",
            reasons=["sudo/env aislado, sin verbo siguiente"],
        )

    verb_full = tokens[0]
    verb = os.path.basename(verb_full)  # admite /usr/bin/php o php
    args = tokens[1:]

    # --- 3) Nivel base por verbo ---
    if verb in _READ_VERBS:
        level = RiskLevel.SAFE_READ
        reasons.append(f"verbo de lectura: {verb}")
    elif verb in _DESTRUCTIVE_VERBS:
        level = RiskLevel.CRITICAL
        reasons.append(f"verbo destructivo: {verb}")
    elif verb in _BROAD_WRITE_VERBS:
        level, sub_reasons = _classify_broad_write(verb, args)
        reasons.extend(sub_reasons)
    elif verb in _BOUNDED_WRITE_VERBS:
        level, sub_reasons = _classify_bounded_write(verb, args)
        reasons.extend(sub_reasons)
    elif verb in _INTERPRETER_VERBS:
        level = RiskLevel.LOW
        reasons.append(f"interprete: {verb}")
    else:
        # Desconocido: NUNCA DENY automatico. Cae a LOW. (Respuesta a L63
        # del doc futuras_mejoras.md.)
        level = RiskLevel.LOW
        reasons.append(f"verbo desconocido '{verb}': tratado como LOW")

    if sudo_present:
        reasons.append("ejecucion con sudo")

    # --- 4) Modificadores (escalan nivel) ---
    is_interp = False
    if verb in _INTERPRETER_VERBS:
        # interprete con flag de ejecucion -c / -e / -r -> +2
        if any(a in _INTERPRETER_EXEC_FLAGS for a in args):
            is_interp = True
            level = _bump(level, 2)
            reasons.append("interprete con ejecucion en linea (-c/-e/-r): +2")

    # Metacaracteres en la cadena original (no en tokens, porque shlex los
    # consume). Un `|` o `>` cruzando un solo comando ya es senal de algo
    # mas complejo que conviene escalar.
    extra = _detect_shell_metachars(raw)
    if extra:
        level = _bump(level, 1)
        reasons.append(f"metacaracteres de shell detectados: {', '.join(extra)}")

    # Wildcards en paths sensibles
    if _hits_sensitive_wildcard(args):
        level = _bump(level, 1)
        reasons.append("wildcard sobre path sensible (/etc, /boot, /dev/sd...): +1")

    # Constructos de ejecucion embebidos (incluso entre comillas): un comando
    # clasificado como lectura pura pierde la auto-ejecucion si los contiene.
    if level == RiskLevel.SAFE_READ:
        embedded = [p for p in _EMBEDDED_EXEC_PATTERNS if p in raw]
        if embedded:
            level = RiskLevel.HIGH
            reasons.append(
                f"constructo de ejecucion embebido en comando de lectura: {', '.join(embedded)}"
            )

    # Heuristica especifica: `find ... -delete` o `find ... -exec` con verbo destructivo
    if verb == "find":
        if "-delete" in args:
            level = max(level, RiskLevel.HIGH)
            reasons.append("find con -delete")
        exec_flags = [f for f in ("-exec", "-execdir", "-ok", "-okdir") if f in args]
        if exec_flags:
            level = max(level, RiskLevel.HIGH)
            reasons.append(f"find con {', '.join(exec_flags)}")
    # `tcpdump -z` ejecuta un comando en cada rotacion; `-w` escribe ficheros
    if verb == "tcpdump":
        if "-z" in args:
            level = max(level, RiskLevel.HIGH)
            reasons.append("tcpdump con -z (ejecuta comando post-rotacion)")
        if "-w" in args:
            level = max(level, RiskLevel.HIGH)
            reasons.append("tcpdump con -w (escribe capturas a disco)")
    # `sed -i` muta archivos
    if verb == "sed" and any(a == "-i" or a.startswith("-i") for a in args):
        level = max(level, RiskLevel.HIGH)
        reasons.append("sed con -i (modificacion in-place)")

    # Verbo destructivo en cualquier posicion del comando (cubre encadenamientos
    # tipo `ls /tmp; rm /tmp/foo` o `cmd && shutdown`).
    extra_destructive = _scan_destructive_anywhere(raw, primary=verb)
    if extra_destructive:
        level = RiskLevel.CRITICAL
        reasons.append(
            f"verbo destructivo encadenado: {', '.join(extra_destructive)}"
        )

    return Classification(
        level=level,
        parsed_verb=verb,
        reasons=reasons,
        is_executable_via_interpreter=is_interp,
    )


def _classify_bounded_write(verb: str, args: list) -> tuple[RiskLevel, list]:
    """
    Despacha la clasificacion por gestor de firewall. Cada familia tiene su
    propia sintaxis (iptables/ip6tables, ufw, nft, firewall-cmd); clasificarlas
    con el parser de iptables daria niveles erroneos (p.ej. `ufw status` -> HIGH).
    """
    if verb in ("iptables", "ip6tables"):
        return _classify_iptables(verb, args)
    if verb == "ufw":
        return _classify_ufw(verb, args)
    if verb == "nft":
        return _classify_nft(verb, args)
    if verb == "firewall-cmd":
        return _classify_firewalld(verb, args)
    return RiskLevel.HIGH, [f"{verb} no clasificado: HIGH"]  # inalcanzable


def _classify_iptables(verb: str, args: list) -> tuple[RiskLevel, list]:
    """
    Casos especiales de iptables/ip6tables:
        -L / -S / --list / --check   -> SAFE_READ
        -F / --flush sin tabla       -> CRITICAL
        -A / -I / -D INPUT -s <IP>   -> LOW
        cualquier otra cosa          -> HIGH
    """
    reasons: list = []
    if not args:
        reasons.append(f"{verb} sin argumentos: HIGH por defecto")
        return RiskLevel.HIGH, reasons

    flat = " ".join(args)
    # Solo-lectura
    read_flags = ("-L", "-S", "--list", "--check", "-V", "--version")
    if any(a in read_flags for a in args):
        reasons.append(f"{verb} en modo lectura ({flat})")
        return RiskLevel.SAFE_READ, reasons

    # Flush global (peligroso)
    if "-F" in args or "--flush" in args:
        # Si va seguido de un nombre de cadena especifica (INPUT/FORWARD/OUTPUT)
        idx = args.index("-F" if "-F" in args else "--flush")
        target = args[idx + 1] if idx + 1 < len(args) else ""
        if target in ("INPUT", "OUTPUT", "FORWARD"):
            reasons.append(f"{verb} flush de cadena especifica: HIGH")
            return RiskLevel.HIGH, reasons
        reasons.append(f"{verb} flush sin cadena: CRITICAL")
        return RiskLevel.CRITICAL, reasons

    # Append/insert/delete contra una IP
    if any(f in args for f in ("-A", "-I", "-D", "--append", "--insert", "--delete")):
        # Comprobamos que haya una IP en los args (parametro -s <ip>)
        has_ip = any(_IP_REGEX.match(a) for a in args)
        if has_ip:
            reasons.append(f"{verb} regla contra IP concreta: LOW")
            return RiskLevel.LOW, reasons
        reasons.append(f"{verb} regla sin IP concreta: HIGH")
        return RiskLevel.HIGH, reasons

    reasons.append(f"{verb} con flags no clasificados ({flat}): HIGH")
    return RiskLevel.HIGH, reasons


def _classify_nft(verb: str, args: list) -> tuple[RiskLevel, list]:
    """
    nftables por subcomando:
        list/export/monitor/describe       -> SAFE_READ
        -f <fichero> (carga ruleset)        -> CRITICAL
        flush ruleset / delete|destroy table-> CRITICAL (borra TODO el firewall)
        flush/delete chain|set|map          -> HIGH
        add|insert|replace rule + IP + verdict -> LOW (bloqueo de una IP)
        add table/chain/...                 -> HIGH
    """
    if not args:
        return RiskLevel.HIGH, ["nft sin args: HIGH"]
    flat = " ".join(args)
    sub = args[0]
    if sub in ("list", "export", "monitor", "describe"):
        return RiskLevel.SAFE_READ, [f"nft lectura ({flat})"]
    if "-f" in args or sub in ("-f", "--file"):
        return RiskLevel.CRITICAL, ["nft -f carga ruleset desde fichero: CRITICAL"]
    if sub == "flush":
        obj = args[1] if len(args) > 1 else ""
        if obj == "ruleset":
            return RiskLevel.CRITICAL, ["nft flush ruleset borra TODO el firewall: CRITICAL"]
        return RiskLevel.HIGH, [f"nft flush {obj}: HIGH"]
    if sub in ("delete", "destroy"):
        obj = args[1] if len(args) > 1 else ""
        if obj == "table":
            return RiskLevel.CRITICAL, ["nft delete table elimina cadenas y reglas: CRITICAL"]
        if obj in ("chain", "set", "map", "flowtable"):
            return RiskLevel.HIGH, [f"nft delete {obj}: HIGH"]
        if obj in ("rule", "element"):
            if _has_ip(flat):
                return RiskLevel.LOW, ["nft delete rule contra IP concreta: LOW"]
            return RiskLevel.HIGH, ["nft delete rule sin IP: HIGH"]
        return RiskLevel.HIGH, [f"nft delete {obj}: HIGH"]
    if sub in ("add", "insert", "replace"):
        obj = args[1] if len(args) > 1 else ""
        if obj == "rule":
            if _has_ip(flat) and _has_verdict(flat):
                return RiskLevel.LOW, ["nft add/insert rule contra IP con verdict: LOW"]
            return RiskLevel.HIGH, ["nft add rule sin IP/verdict claros: HIGH"]
        if obj == "element":
            lvl = RiskLevel.LOW if _has_ip(flat) else RiskLevel.HIGH
            return lvl, [f"nft add element: {lvl.label()}"]
        if obj in ("table", "chain", "set", "map", "flowtable"):
            return RiskLevel.HIGH, [f"nft add {obj} (estructura): HIGH"]
        return RiskLevel.HIGH, [f"nft add {obj}: HIGH"]
    return RiskLevel.HIGH, [f"nft subcomando '{sub}' no acotado: HIGH"]


def _classify_firewalld(verb: str, args: list) -> tuple[RiskLevel, list]:
    """
    firewall-cmd por flag:
        --list/--get/--query/--state/...    -> SAFE_READ
        --panic-on (corta TODO el trafico)  -> CRITICAL
        --add-rich-rule/--add-source + IP   -> LOW
        --reload / --runtime-to-permanent   -> LOW
        --set-default-zone / cambios de zona-> HIGH
    """
    if not args:
        return RiskLevel.HIGH, ["firewall-cmd sin args: HIGH"]
    flat = " ".join(args)
    if "--panic-on" in args:
        return RiskLevel.CRITICAL, ["firewall-cmd --panic-on corta TODO el trafico: CRITICAL"]
    if "--panic-off" in args:
        return RiskLevel.HIGH, ["firewall-cmd --panic-off reabre todo: HIGH"]

    # --direct/--passthrough inyectan reglas iptables/nft CRUDAS y arbitrarias:
    # NUNCA pueden ser SAFE_READ aunque el comando lleve un flag de lectura
    # (p. ej. `firewall-cmd --query-panic --direct --passthrough ipv4 -F`).
    # Se delega el cuerpo del passthrough en el clasificador de iptables, que ya
    # distingue flush global (CRITICAL), flush de cadena (HIGH) y regla+IP (LOW).
    if "--passthrough" in args:
        idx = args.index("--passthrough")
        pt = args[idx + 1:]
        if pt and pt[0] in ("ipv4", "ipv6", "eb"):
            pt = pt[1:]
        if pt:
            lvl, sub = _classify_iptables("iptables", pt)
            return lvl, [f"firewall-cmd --passthrough delega en iptables: {lvl.label()}"] + sub
        return RiskLevel.HIGH, ["firewall-cmd --passthrough sin cuerpo: HIGH"]
    if "--direct" in args:
        return RiskLevel.HIGH, [f"firewall-cmd --direct manipula reglas crudas ({flat}): HIGH"]

    read_prefixes = ("--list", "--get", "--query", "--info", "--state",
                     "--version", "--help", "--check-config")
    if any(a.startswith(read_prefixes) for a in args) and not _has_mutating_flag(args):
        return RiskLevel.SAFE_READ, [f"firewall-cmd lectura ({flat})"]
    broad = ("--set-default-zone", "--set-target", "--new-zone",
             "--delete-zone", "--set-log-denied", "--set-policy")
    if any(a.split("=")[0] in broad for a in args):
        return RiskLevel.HIGH, [f"firewall-cmd cambio amplio de zona/politica ({flat}): HIGH"]
    # Flags mutantes de estado que no empiezan por _FW_MUTATING_PREFIXES.
    if any(a.split("=")[0].startswith(("--lockdown", "--load")) for a in args):
        return RiskLevel.HIGH, [f"firewall-cmd flag mutante de estado ({flat}): HIGH"]
    if "--reload" in args or "--complete-reload" in args:
        return RiskLevel.LOW, ["firewall-cmd reload: LOW"]
    if "--runtime-to-permanent" in args:
        return RiskLevel.LOW, ["firewall-cmd runtime-to-permanent persiste estado actual: LOW"]
    rule_flags = ("--add-rich-rule", "--remove-rich-rule", "--add-source", "--remove-source")
    if any(a.split("=")[0] in rule_flags for a in args):
        if _has_ip(flat):
            return RiskLevel.LOW, ["firewall-cmd regla/source contra IP concreta: LOW"]
        return RiskLevel.HIGH, ["firewall-cmd regla sin IP concreta: HIGH"]
    if _has_mutating_flag(args):
        return RiskLevel.HIGH, [f"firewall-cmd escritura no acotada a IP ({flat}): HIGH"]
    # Solo modificadores vacios (p. ej. `--`) sin flag real -> HIGH (como "sin args").
    if not any(a.startswith("-") and a.strip("-") != "" for a in args):
        return RiskLevel.HIGH, [f"firewall-cmd sin flag real (solo modificadores) ({flat}): HIGH"]
    return RiskLevel.LOW, [f"firewall-cmd flags no catalogados ({flat}): LOW"]


def _classify_ufw(verb: str, args: list) -> tuple[RiskLevel, list]:
    """
    ufw por accion posicional:
        status/show/version  -> SAFE_READ
        reset                -> CRITICAL (borra todas las reglas)
        disable/enable/default-> HIGH (politica global)
        deny/allow/... + IP  -> LOW
    """
    if not args:
        return RiskLevel.HIGH, ["ufw sin args: HIGH"]
    flat = " ".join(args)
    positional = [a for a in args if not a.startswith("-")]  # salta --force/--dry-run
    action = positional[0] if positional else ""
    if action in ("status", "show", "version"):
        return RiskLevel.SAFE_READ, [f"ufw lectura ({flat})"]
    if action == "reset":
        return RiskLevel.CRITICAL, ["ufw reset borra TODAS las reglas: CRITICAL"]
    if action == "disable":
        return RiskLevel.HIGH, ["ufw disable desactiva el firewall: HIGH"]
    if action == "enable":
        return RiskLevel.HIGH, ["ufw enable cambia politica global: HIGH"]
    if action == "reload":
        return RiskLevel.LOW, ["ufw reload: LOW"]
    if action == "default":
        return RiskLevel.HIGH, ["ufw default cambia politica global: HIGH"]
    if action in ("deny", "allow", "reject", "limit", "insert", "route", "delete"):
        if _has_ip(flat):
            return RiskLevel.LOW, [f"ufw {action} contra IP concreta: LOW"]
        return RiskLevel.HIGH, [f"ufw {action} sin IP (afecta puerto/servicio): HIGH"]
    if action == "":
        return RiskLevel.HIGH, [f"ufw sin accion posicional (solo modificadores) ({flat}): HIGH"]
    return RiskLevel.LOW, [f"ufw accion '{action}' no catalogada: LOW"]


def _classify_broad_write(verb: str, args: list) -> tuple[RiskLevel, list]:
    """Subcomandos de solo estado dentro de herramientas normalmente mutantes."""
    if verb == "systemctl" and args:
        read_subcommands = {"status", "show", "is-active", "is-enabled", "list-units"}
        if args[0] in read_subcommands:
            return RiskLevel.SAFE_READ, [f"{verb} {args[0]} es consulta de estado"]
    if verb == "service" and len(args) >= 2 and args[1] == "status":
        return RiskLevel.SAFE_READ, ["service status es consulta de estado"]
    return RiskLevel.HIGH, [f"verbo de escritura amplia: {verb}"]


def _detect_shell_metachars(raw: str) -> list:
    """
    Devuelve la lista de metacaracteres relevantes encontrados.

    Las pipes se clasifican antes por tramos. Aqui quedan metacaracteres que
    introducen control de flujo, sustitucion o escritura de salida.
    """
    hits = []
    # Quitar contenido entre comillas simples/dobles para no leer metacaracteres
    # que el shell trataria como literales.
    sanitized = re.sub(r"'[^']*'", "''", raw)
    sanitized = re.sub(r'"[^"]*"', '""', sanitized)
    for token in (";", "&&", "||", "`", "$("):
        if token in sanitized:
            hits.append(token)
    # `>` y `>>` escriben estado aunque el verbo principal sea de lectura.
    redirect = re.search(r">>?\s*(\S+)", sanitized)
    if redirect:
        target = redirect.group(1)
        hits.append(f"> {target}")
    return hits


def _split_unquoted_newlines(raw: str) -> list:
    """Divide por saltos de linea/retorno de carro que esten FUERA de comillas."""
    segments = []
    current = []
    quote = None
    escaped = False
    for ch in raw:
        if escaped:
            current.append(ch)
            escaped = False
            continue
        if ch == "\\":
            current.append(ch)
            escaped = True
            continue
        if ch in ("'", '"'):
            current.append(ch)
            if quote is None:
                quote = ch
            elif quote == ch:
                quote = None
            continue
        if ch in ("\n", "\r") and quote is None:
            seg = "".join(current).strip()
            if seg:
                segments.append(seg)
            current = []
            continue
        current.append(ch)
    final = "".join(current).strip()
    if final:
        segments.append(final)
    return segments if segments else [raw]


def _split_unquoted_pipe(raw: str) -> list:
    """Split on shell pipes outside quotes; keep logical OR for metachar handling."""
    if "||" in raw:
        return [raw]

    segments = []
    current = []
    quote = None
    escaped = False

    for ch in raw:
        if escaped:
            current.append(ch)
            escaped = False
            continue
        if ch == "\\":
            current.append(ch)
            escaped = True
            continue
        if ch in ("'", '"'):
            current.append(ch)
            if quote is None:
                quote = ch
            elif quote == ch:
                quote = None
            continue
        if ch == "|" and quote is None:
            segment = "".join(current).strip()
            if not segment:
                return [raw]
            segments.append(segment)
            current = []
            continue
        current.append(ch)

    if quote is not None:
        return [raw]
    if segments:
        final = "".join(current).strip()
        if not final:
            return [raw]
        segments.append(final)
        return segments
    return [raw]


def _scan_destructive_anywhere(raw: str, primary: str) -> list:
    """
    Devuelve los verbos destructivos encontrados como palabra completa en el
    comando bruto, excluyendo el verbo principal (que ya se ha contado).

    Cubre encadenamientos del tipo `ls /tmp; rm foo` o `whoami && shutdown`
    que shlex no separa en clauses independientes.
    """
    hits = []
    # Recorrer cada palabra del comando, ignorando contenido entre comillas
    # (no es metodo perfecto pero suficiente para detectar palabras sueltas).
    sanitized = re.sub(r"'[^']*'", "", raw)
    sanitized = re.sub(r'"[^"]*"', "", sanitized)
    for match in re.finditer(r"\b([a-zA-Z_][a-zA-Z0-9_-]*)\b", sanitized):
        word = match.group(1)
        if word == primary:
            continue
        if word in _DESTRUCTIVE_VERBS:
            hits.append(word)
    return hits


def _hits_sensitive_wildcard(args: list) -> bool:
    for a in args:
        if "*" in a or "?" in a:
            for path in _SENSITIVE_WILDCARD_PATHS:
                if path in a:
                    return True
    return False


def _bump(level: RiskLevel, steps: int) -> RiskLevel:
    new = min(int(level) + steps, int(RiskLevel.CRITICAL))
    return RiskLevel(new)


# ---------------------------------------------------------------------------
# Decision
# ---------------------------------------------------------------------------
def decide(cmd: str) -> Decision:
    """
    Solo SAFE_READ permite ejecucion directa. Todo lo demas exige HITL.
    """
    cl = classify(cmd)
    return Decision(allow_direct=(cl.level == RiskLevel.SAFE_READ), classification=cl)


# ---------------------------------------------------------------------------
# Audit log (append-only) — inmutabilidad asegurada por triggers en BD
# ---------------------------------------------------------------------------
# Nota: la cache reactiva de despachos se elimino al introducir firma Ed25519
# en los comandos enviados a PI-4. Si un
# sensor reporta un comando es porque la firma fue valida en su extremo, de
# modo que el round-trip a posteriori dejo de ser necesario.
def audit(
    event_type: str,
    device: str,
    command: str,
    classification: Optional[Classification] = None,
    decision_reason: str = "",
    related_log_id: Optional[int] = None,
) -> None:
    """
    Inserta una entrada en audit_log. Si la tabla no existe (BD vieja) se
    ignora silenciosamente para no romper el flujo principal.
    """
    cls_label = classification.level.label() if classification else ""
    reasons = ""
    if classification:
        joined = "; ".join(classification.reasons) if classification.reasons else ""
        if decision_reason:
            reasons = f"{decision_reason} | {joined}" if joined else decision_reason
        else:
            reasons = joined
    else:
        reasons = decision_reason

    for attempt in range(3):
        conn = None
        try:
            conn = sqlite3.connect(DB_PATH, timeout=10.0, check_same_thread=False)
            conn.execute('PRAGMA journal_mode=WAL;')
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO audit_log
                    (event_type, device, command, classification, decision_reason, related_log_id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (event_type, device, command, cls_label, reasons, related_log_id),
            )
            conn.commit()
            return
        except sqlite3.OperationalError as e:
            msg = str(e).lower()
            if "no such table" in msg:
                logger.warning("[POLICY] audit_log no existe; saltando entrada.")
                return
            if "locked" in msg and attempt < 2:
                time.sleep(1)
                continue
            logger.error(f"[POLICY] No se pudo escribir audit_log: {e}")
            return
        except Exception as e:
            logger.error(f"[POLICY] Error inesperado escribiendo audit_log: {e}")
            return
        finally:
            if conn:
                conn.close()
