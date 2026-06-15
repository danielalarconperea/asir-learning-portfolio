"""
Esquema JSON estricto de la salida del enriquecedor LLM (Fase 4).

Draft-07, additionalProperties:false en todos los niveles y enums cerrados para
detectar campos inventados. Cualquier salida del LLM que no valide contra este
esquema se descarta entera (no se persiste nada). Ver docs/diseno_agente_discovery.md.
"""

from __future__ import annotations

# Familias de detección reconocidas por el motor (espejo de mitigation_manual).
DETECTOR_ENUM = (
    "ssh_bruteforce", "ftp_bruteforce", "web_bruteforce", "sqli", "xss",
    "session_hijacking", "defacement", "db_compromise", "port_scan", "recon",
)
INTENT_ENUM = ("diagnostic", "mitigation", "recovery")
CONF_ENUM = ("high", "medium", "low")

ENRICHMENT_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "device", "based_on_profile_hash", "global_confidence",
                 "host_notes", "suggested_log_sources", "suggested_recommendation_overrides"],
    "properties": {
        "schema_version": {"const": 1},
        "device": {"type": "string", "pattern": "^[A-Za-z0-9_-]+$"},
        "based_on_profile_hash": {"type": "string"},
        "global_confidence": {"enum": list(CONF_ENUM)},

        "host_notes": {
            "type": "object", "additionalProperties": False,
            "required": ["summary", "risks"],
            "properties": {
                "summary": {"type": "string", "maxLength": 1200},
                "risks": {
                    "type": "array", "maxItems": 20,
                    "items": {
                        "type": "object", "additionalProperties": False,
                        "required": ["text", "confidence", "evidence"],
                        "properties": {
                            "text": {"type": "string", "maxLength": 400},
                            "severity": {"enum": ["info", "baja", "media", "alta", "critica"]},
                            "confidence": {"enum": list(CONF_ENUM)},
                            "evidence": {"type": "array", "items": {"type": "string"}},
                        },
                    },
                },
            },
        },

        "suggested_log_sources": {
            "type": "array", "maxItems": 30,
            "items": {
                "type": "object", "additionalProperties": False,
                "required": ["id", "service", "source", "parser", "detectors", "confidence", "evidence"],
                "properties": {
                    "id": {"type": "string", "pattern": "^[a-z0-9_]+$"},
                    "service": {"type": "string"},
                    "source": {"enum": ["file", "journald"]},
                    "path": {"type": ["string", "null"]},
                    "unit": {"type": ["string", "null"]},
                    "format": {"type": ["string", "null"]},
                    "parser": {"type": "string", "pattern": "^[a-z0-9_]+$"},
                    "detectors": {"type": "array", "items": {"enum": list(DETECTOR_ENUM)}},
                    "confidence": {"enum": list(CONF_ENUM)},
                    "evidence": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                },
                "allOf": [
                    {"if": {"properties": {"source": {"const": "file"}}},
                     "then": {"required": ["path"], "properties": {"path": {"type": "string"}}}},
                    {"if": {"properties": {"source": {"const": "journald"}}},
                     "then": {"required": ["unit"], "properties": {"unit": {"type": "string"}}}},
                ],
            },
        },

        "suggested_recommendation_overrides": {
            "type": "array", "maxItems": 20,
            "items": {
                "type": "object", "additionalProperties": False,
                "required": ["id", "intent", "severity", "requires", "applies_if", "match",
                             "command", "explanation", "confidence", "evidence"],
                "properties": {
                    "id": {"type": "string", "pattern": "^[a-z0-9-]+$"},
                    "intent": {"enum": list(INTENT_ENUM)},
                    "severity": {"enum": ["baja", "media", "alta", "critica"]},
                    "requires": {"type": "array", "items": {"type": "string"}},
                    "applies_if": {"type": "object"},
                    "match": {
                        "type": "object", "additionalProperties": False,
                        "properties": {
                            "families": {"type": "array", "items": {"type": "string"}},
                            "keywords": {"type": "array", "items": {"type": "string"}},
                        },
                    },
                    "command": {"type": "string"},
                    "revert": {"type": "string"},
                    "placeholders": {"type": "array", "items": {"type": "string"}},
                    "explanation": {"type": "string", "maxLength": 1500},
                    "confidence": {"enum": list(CONF_ENUM)},
                    "evidence": {"type": "array", "minItems": 1, "items": {"type": "string"}},
                    "risk_level": {"enum": ["SAFE_READ", "LOW", "HIGH", "CRITICAL"]},
                    "policy_reasons": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
    },
}


# Orden de confianza para la política "min(LLM, respaldo)".
_CONF_RANK = {"low": 0, "medium": 1, "high": 2}
_RANK_CONF = {0: "low", 1: "medium", 2: "high"}


def min_conf(a: str, b: str) -> str:
    """Devuelve la menor de dos confianzas enum."""
    return _RANK_CONF[min(_CONF_RANK.get(a, 0), _CONF_RANK.get(b, 0))]


def cap_conf(conf: str, ceiling: str) -> str:
    """Limita una confianza a un techo (p. ej. recovery -> medium)."""
    return _RANK_CONF[min(_CONF_RANK.get(conf, 0), _CONF_RANK.get(ceiling, 0))]
