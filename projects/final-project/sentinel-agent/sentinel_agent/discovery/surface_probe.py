"""
Probe de superficie: puertos expuestos (bind no-loopback) vs solo-loopback,
derivado de los listeners descubiertos. Da al triage la priorización que hoy
no tiene (un puerto en 0.0.0.0 es atacable; en 127.0.0.1 no).
"""

from __future__ import annotations

from typing import List, Tuple


def build_surface(services: List[dict]) -> dict:
    """Lógica pura: clasifica los puertos de los listeners por exposición."""
    exposed = sorted({s["port"] for s in services if s.get("exposed") and s.get("port")})
    loopback = sorted({s["port"] for s in services if s.get("loopback") and s.get("port")})
    # Un puerto puede estar en ambos (IPv4 wildcard + IPv6 loopback); prioriza expuesto.
    loopback = [p for p in loopback if p not in exposed]
    return {
        "exposed_ports": exposed,
        "loopback_only": loopback,
        "internet_facing": len(exposed) > 0,
    }


def collect(services: List[dict]) -> Tuple[dict, list]:
    return {"surface": build_surface(services)}, []
