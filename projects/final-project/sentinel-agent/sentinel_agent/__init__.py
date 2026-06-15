"""
sentinel-agent — sensor genérico auto-configurable de Sentinel-IT.

Se autodescubre en cualquier servidor Linux (servicios, puertos, logs,
firewall, capacidades), publica un System Profile a PI-5 y ejecuta comandos
de mitigación firmados (Ed25519) tras una barrera local de seguridad.

Ver docs/diseno_agente_discovery.md.
"""

__version__ = "0.1.0"
AGENT_NAME = f"sentinel-agent/{__version__}"
