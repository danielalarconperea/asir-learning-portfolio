"""
Ejecutor de comandos de mitigación con barrera local de seguridad.

Modelo de confianza en defensa en profundidad:
  1. Firma Ed25519 (origen): el comando viene realmente de PI-5.
  2. Denylist local (contenido): rechaza verbos destructivos AUNQUE la firma
     sea válida. PI-5 puede equivocarse o ser comprometido; esta segunda
     barrera es independiente.

La ejecución sigue siendo como ROOT por defecto (decisión del proyecto): la
denylist no cambia el privilegio, solo añade un filtro de contenido. `run_as`
permite de-escalar en objetivos concretos.
"""

from __future__ import annotations

import logging
import re
import shlex
import subprocess
import time
from typing import Callable, Optional, Tuple

from . import signing

logger = logging.getLogger("sentinel-agent")

# Verbos destructivos rechazados localmente aunque la firma sea válida.
# Mitigaciones legítimas (iptables/nft/ufw/systemctl/php/mysql) NO están aquí.
LOCAL_DENYLIST = {
    "rm", "mkfs", "dd", "shutdown", "reboot", "halt", "poweroff", "init",
    "wipefs", "shred", "userdel", "fdisk", "parted", "mkswap", "telinit",
}

_OUTPUT_MAX = 4000


# Prefijos que envuelven al verbo real (se saltan para hallar el comando).
_WRAPPER_PREFIXES = {"sudo", "env", "nice", "ionice", "doas", "timeout", "stdbuf"}


def is_denied(command: str, denylist=LOCAL_DENYLIST) -> Tuple[bool, list]:
    """
    Lógica pura: True si el comando ejecuta algún verbo destructivo. Combina
    dos escaneos sobre el comando sin su contenido entrecomillado:

      * Verbo de comando de cada segmento (separado por ; && || | &), con split
        por '.' para familias tipo `mkfs.ext4` -> `mkfs`. Salta sudo/env/...
      * Palabras sueltas == verbo destructivo (cubre `ls; rm x`) SIN split por
        '.', para no marcar ficheros como `dd.log`.
    """
    if not command:
        return False, []
    sanitized = re.sub(r"'[^']*'", "", command)
    sanitized = re.sub(r'"[^"]*"', "", sanitized)
    hits = set()

    # 1) Verbo de cada segmento de shell.
    for segment in re.split(r"&&|\|\||[;&|]", sanitized):
        tokens = segment.split()
        i = 0
        while i < len(tokens) and tokens[i].rsplit("/", 1)[-1] in _WRAPPER_PREFIXES:
            i += 1
        if i >= len(tokens):
            continue
        base = tokens[i].rsplit("/", 1)[-1]
        if base in denylist or base.split(".")[0] in denylist:
            hits.add(base.split(".")[0] if base not in denylist else base)

    # 2) Palabras sueltas (verbo destructivo en cualquier posición sin comillas).
    for word in re.findall(r"[a-zA-Z_][a-zA-Z0-9_/-]*", sanitized):
        base = word.rsplit("/", 1)[-1]
        if base in denylist:
            hits.add(base)

    return (len(hits) > 0), sorted(hits)


def run_command(command: str, timeout: float = 30.0, run_as: Optional[str] = None) -> dict:
    """Ejecuta el comando y devuelve {exitcode, stdout, stderr, timed_out}."""
    if run_as:
        argv = ["sudo", "-u", run_as, "bash", "-c", command]
        shell = False
    else:
        argv = command
        shell = True
    try:
        proc = subprocess.run(argv, shell=shell, capture_output=True, text=True, timeout=timeout)
        return {
            "exitcode": proc.returncode,
            "stdout": (proc.stdout or "")[:_OUTPUT_MAX],
            "stderr": (proc.stderr or "")[:_OUTPUT_MAX],
            "timed_out": False,
        }
    except subprocess.TimeoutExpired:
        return {"exitcode": -1, "stdout": "", "stderr": "timeout", "timed_out": True}
    except Exception as e:  # noqa: BLE001
        return {"exitcode": -1, "stdout": "", "stderr": str(e), "timed_out": False}


def process_command(
    payload: dict,
    device_id: str,
    verify: Callable[[dict], Tuple[bool, str]] = signing.verify_payload,
    runner: Callable[..., dict] = run_command,
    run_as: Optional[str] = None,
    now_iso: Optional[str] = None,
) -> dict:
    """
    Orquesta verificación de firma + denylist + ejecución, y devuelve el
    payload de RESPUESTA listo para publicar a seguridad/<device>/respuesta,
    SIEMPRE con eco del log_id (contrato del round-trip HITL de PI-5).
    """
    ts = now_iso or time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    accion = payload.get("accion") or payload.get("action", "")
    comando = payload.get("comando") or payload.get("command", "")
    motivo = payload.get("motivo") or payload.get("reason", "")
    log_id = payload.get("log_id")

    base = {
        "timestamp": ts, "sensor": device_id, "tipo": "RESULTADO_COMANDO",
        "accion": accion, "comando": comando, "motivo": motivo, "log_id": log_id,
    }

    # 1) Firma (origen)
    ok, motivo_firma = verify(payload)
    if not ok:
        logger.error(f"[EXEC] Comando rechazado por firma: {motivo_firma}")
        return {**base, "status": "rejected_signature",
                "resultado": {"error": motivo_firma, "exitcode": -1}}

    # Acciones que no ejecutan shell (p. ej. redescubrir) las maneja el monitor;
    # aquí solo tratamos ejecutar_comando.
    if accion not in ("ejecutar_comando", "execute_command"):
        return {**base, "status": "ignored",
                "resultado": {"error": f"accion no ejecutable: {accion}", "exitcode": -1}}

    if not comando:
        return {**base, "status": "error",
                "resultado": {"error": "no_command", "exitcode": -1}}

    # 2) Denylist local (contenido) — independiente de la firma
    denied, verbs = is_denied(comando)
    if denied:
        logger.error(f"[EXEC] Comando BLOQUEADO por denylist local: {verbs} | {comando}")
        return {**base, "status": "rejected_local_policy",
                "resultado": {"error": f"verbo(s) destructivo(s) bloqueado(s): {', '.join(verbs)}",
                              "exitcode": -1}}

    # 3) Ejecución (root por defecto)
    logger.info(f"[EXEC] Ejecutando ({'root' if not run_as else run_as}): {comando}")
    resultado = runner(comando, run_as=run_as)
    return {**base, "resultado": resultado}
