"""
Probe de firewall: reporta el gestor ACTIVO, no solo los binarios presentes.

En Debian 11+/RHEL 8+ `iptables` suele ser iptables-nft conviviendo con
ufw/firewalld como frontend; reglas iptables crudas pueden romperse al
recargar. Por eso interesa el gestor activo, para que el LLM elija
`ufw deny` / `firewall-cmd` / `nft` en vez de `iptables` legacy.
"""

from __future__ import annotations

from typing import Optional, Tuple

from . import _util


def decide_active_manager(
    ufw_status: Optional[str],
    firewalld_active: Optional[str],
    nft_ruleset: Optional[str],
    iptables_save: Optional[str],
    present: dict,
) -> dict:
    """
    Lógica pura: a partir de las salidas crudas decide el gestor activo.
    Orden de preferencia: ufw > firewalld > nftables (con reglas) > iptables.
    """
    managers_present = sorted(k for k, v in present.items() if v)

    if ufw_status and "status: active" in ufw_status.lower():
        return {"active_manager": "ufw", "active": True,
                "backend": "iptables", "managers_present": managers_present}

    if firewalld_active and firewalld_active.strip() == "active":
        return {"active_manager": "firewalld", "active": True,
                "backend": "nftables", "managers_present": managers_present}

    if nft_ruleset and _nft_has_rules(nft_ruleset):
        return {"active_manager": "nftables", "active": True,
                "backend": "nftables", "managers_present": managers_present}

    if iptables_save and _iptables_has_rules(iptables_save):
        backend = "iptables-nft" if present.get("nft") else "iptables-legacy"
        return {"active_manager": "iptables", "active": True,
                "backend": backend, "managers_present": managers_present}

    return {"active_manager": "none", "active": False,
            "backend": "none", "managers_present": managers_present}


def _nft_has_rules(ruleset: str) -> bool:
    # `nft list ruleset` vacío no tiene 'chain'/'rule'.
    return "chain" in ruleset or "rule" in ruleset


def _iptables_has_rules(save: str) -> bool:
    # Más allá de las cadenas por defecto y políticas, ¿hay reglas -A?
    return any(line.startswith("-A") for line in save.splitlines())


def collect() -> Tuple[dict, list]:
    degraded = []
    present = {
        "ufw": bool(_util.which("ufw")),
        "firewalld": bool(_util.which("firewall-cmd")),
        "nft": bool(_util.which("nft")),
        "iptables": bool(_util.which("iptables")),
    }
    if not any(present.values()):
        degraded.append("no_firewall_tool")
        return {"firewall": {"active_manager": "none", "active": False,
                             "backend": "none", "managers_present": []}}, degraded

    ufw_status = _util.run(["ufw", "status"]) if present["ufw"] else None
    firewalld_active = _util.run(["systemctl", "is-active", "firewalld"]) if present["firewalld"] else None
    nft_ruleset = _util.run(["nft", "list", "ruleset"]) if present["nft"] else None
    iptables_save = _util.run(["iptables-save"]) if present["iptables"] else None
    if present["iptables"] and iptables_save is None and not _util.is_root():
        degraded.append("iptables_no_root")

    fw = decide_active_manager(ufw_status, firewalld_active, nft_ruleset, iptables_save, present)
    return {"firewall": fw}, degraded
