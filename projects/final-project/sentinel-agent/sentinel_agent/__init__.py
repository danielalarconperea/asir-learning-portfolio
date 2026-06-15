"""
sentinel-agent — sensor genérico auto-configurable de Sentinel-IT.

Reemplaza al monolito PI-4/agente_monitor3.py (atado al honeypot) por un
sensor que se autodescubre en cualquier servidor Linux, publica un System
Profile a PI-5 y ejecuta comandos de mitigación firmados con una barrera
local de seguridad.

Ver docs/diseno_agente_discovery.md.
"""

__version__ = "0.1.0"
AGENT_NAME = f"sentinel-agent/{__version__}"
