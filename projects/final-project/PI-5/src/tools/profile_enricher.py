"""
Enriquecedor LLM OFFLINE del System Profile (Fase 4).

Toma el perfil DETERMINISTA de un device y propone (vía LLM) notas de riesgo,
fuentes de log y borradores de mitigación. TODO se valida contra un JSON Schema
estricto, se cruza con los hechos crudos del perfil y se etiqueta con confidence;
cada comando sugerido pasa por policy_engine para rechazar lo destructivo. NADA se
auto-aplica: las sugerencias quedan en device_enrichments (status PENDING_REVIEW) y
solo el operador las promueve (scripts/enrich_profile.py --promote).

INVARIANTES (verificados por tests):
  * NO se invoca desde la ruta caliente del triage; este módulo NO importa
    main_coordinator, aws_connector, signing, iot_tools ni google.adk.
  * Honra la dualidad de modelo (AI_MODE/AI_MODEL; override opcional ENRICH_*),
    sin mutar el entorno global.
  * El enriquecedor NUNCA dispara ni publica comandos: policy_engine.classify se
    usa solo para etiquetar/filtrar.
"""

from __future__ import annotations

import html
import json
import logging
import os
import re
import time
from typing import Optional, Tuple

import jsonschema

from tools import enrichment_crosscheck as cc
from tools import mitigation_manual as mm
from tools import policy_engine
from tools.db_tools import get_device_profile, save_enrichment
from tools.enrichment_schema import ENRICHMENT_SCHEMA, cap_conf, min_conf

logger = logging.getLogger("CoordinatorSOC")

_SAFE_DEVICE = re.compile(r"^[A-Za-z0-9_-]+$")
_PROSE_BAD = ("$(", "`", "<(", ">(", "system(", "exec(", "popen(")

SYSTEM_PROMPT = (
    "Eres un normalizador de seguridad OFFLINE para un SOC. Recibes el perfil "
    "DETERMINISTA de un servidor (hechos descubiertos por sondas) y propones "
    "enriquecimientos. REGLAS ESTRICTAS: no inventes hechos que no estén en el "
    "perfil; cada elemento DEBE citar en 'evidence' campos reales del perfil "
    "(p. ej. 'services.proc:nginx', 'capabilities.restic:true'); si dudas, baja "
    "'confidence' o NO lo propongas; los comandos solo pueden usar rutas/servicios/"
    "herramientas presentes en el perfil y los placeholders {ip}/{nombre_usuario} o "
    "los derivables del perfil; nunca propongas comandos destructivos (rm, dd, mkfs, "
    "shutdown). Responde EXCLUSIVAMENTE con un objeto JSON conforme al esquema; sin "
    "texto adicional."
)


class ProviderError(Exception):
    """Fallo del proveedor del modelo (red/HTTP/429/timeout/contexto). Reintentable."""
    def __init__(self, message, kind="unknown"):
        super().__init__(message)
        self.kind = kind


class HallucinationError(Exception):
    """La respuesta llegó pero no parsea o no valida (problema de modelo/prompt)."""
    def __init__(self, message, raw=None):
        super().__init__(message)
        self.raw = raw


# ---------------------------------------------------------------------------
# Selección de modelo (dualidad api/local, sin mutar el entorno global)
# ---------------------------------------------------------------------------
def _resolve_model_config() -> Tuple[str, str, dict]:
    mode = os.environ.get("ENRICH_MODE", os.environ.get("AI_MODE", "local")).strip().lower()
    model = os.environ.get("ENRICH_MODEL", os.environ.get("AI_MODEL", "ollama/gemma4:e2b")).strip()
    if mode == "local":
        api_base = os.environ.get("OLLAMA_API_BASE", "http://local-ai-engine:11434")
        return mode, model, {"api_base": api_base}
    # api (Gemini): clave explícita, sin escribir os.environ.
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ProviderError("AI_MODE/ENRICH_MODE=api pero falta GEMINI_API_KEY", kind="connection")
    return mode, model, {"api_key": key}


def _project_facts(profile: dict) -> dict:
    """Proyecta solo hechos crudos; nunca credenciales ni logins recientes."""
    services = []
    for s in profile.get("services") or []:
        services.append({k: s.get(k) for k in ("unit", "port", "bind", "proc") if k in s})
    return {
        "host": profile.get("host"),
        "package_manager": profile.get("package_manager"),
        "firewall": profile.get("firewall"),
        "web_server": profile.get("web_server"),
        "db_engine": profile.get("db_engine"),
        "capabilities": profile.get("capabilities"),
        "services": services,
        "log_sources": profile.get("log_sources"),
        "surface": profile.get("surface"),
        "degraded": profile.get("degraded"),
    }


def build_prompt(facts: dict) -> str:
    return (
        "PERFIL DETERMINISTA DEL DEVICE (hechos):\n"
        + json.dumps(facts, ensure_ascii=False, indent=2)
        + "\n\nESQUEMA DE SALIDA (responde un objeto JSON que lo cumpla):\n"
        + json.dumps(ENRICHMENT_SCHEMA, ensure_ascii=False)
    )


# ---------------------------------------------------------------------------
# Llamada al LLM (one-shot). _raw_completion es la frontera mockeable.
# ---------------------------------------------------------------------------
def _raw_completion(model: str, messages: list, **kwargs) -> str:
    """Llama a litellm (import perezoso) y devuelve el contenido de texto."""
    import litellm  # import perezoso: el módulo se importa aunque litellm no esté
    resp = litellm.completion(model=model, messages=messages, num_retries=0, **kwargs)
    return resp.choices[0].message.content


_RETRYABLE = {"rate_limit", "timeout", "server"}


def _provider_kind(exc: Exception) -> str:
    name = type(exc).__name__
    if name == "RateLimitError":
        return "rate_limit"
    if name in ("Timeout", "APITimeoutError"):
        return "timeout"
    if name in ("InternalServerError", "ServiceUnavailableError"):
        return "server"
    if name in ("APIConnectionError", "APIError"):
        return "connection"
    if name == "ContextWindowExceededError":
        return "context"
    if name == "ModuleNotFoundError" or name == "ImportError":
        return "dependency"   # litellm no instalado: reintentar no ayuda
    return "unknown"


def _parse_json_robusto(text: Optional[str]) -> Optional[dict]:
    if not text:
        return None
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        pass
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        return None
    candidate = re.sub(r",\s*([}\]])", r"\1", m.group(0))  # trailing commas
    try:
        return json.loads(candidate)
    except (ValueError, TypeError):
        return None


def llm_call(prompt: str, json_schema: dict, mode: str, model: str, extra: dict,
             *, temperature: float = 0.0, max_retries: int = 2, timeout_s: int = 120) -> dict:
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}]
    if mode == "api":
        response_format = {"type": "json_schema",
                           "json_schema": {"name": "enrichment", "schema": json_schema, "strict": True}}
    else:
        response_format = {"type": "json_object"}

    last = None
    for attempt in range(max_retries + 1):
        try:
            text = _raw_completion(model, messages, temperature=temperature, timeout=timeout_s,
                                   response_format=response_format, **extra)
        except Exception as exc:  # noqa: BLE001
            kind = _provider_kind(exc)
            last = ProviderError(f"{type(exc).__name__}: {exc}", kind=kind)
            if kind in _RETRYABLE and attempt < max_retries:
                time.sleep(min(2 ** attempt, 8))
                continue
            raise last
        data = _parse_json_robusto(text)
        if data is None:
            raise HallucinationError("la respuesta del modelo no es JSON parseable", raw=text)
        return data
    raise last  # pragma: no cover


# ---------------------------------------------------------------------------
# Validación + cross-check + sanitización
# ---------------------------------------------------------------------------
def _sanitize_prose(text: str) -> str:
    t = text or ""
    for bad in _PROSE_BAD:
        t = t.replace(bad, "[?]")
    # Escape HTML defensivo: la prosa es review-only, pero así un futuro panel que
    # la pinte con innerHTML no abre un XSS. No afecta a jsonify (re-codifica).
    return html.escape(t, quote=False)


def _invokes_interpreter(resolved: str) -> bool:
    """True si algún tramo del pipeline invoca un intérprete (sh/bash/python/...)."""
    for seg in policy_engine._split_unquoted_pipe(resolved):
        toks = seg.split()
        if toks and os.path.basename(toks[0].strip("'\"`")) in policy_engine._INTERPRETER_VERBS:
            return True
    return False


def sanitize_and_classify(ov: dict, profile: dict) -> Tuple[str, str]:
    """
    Pasa command/revert por policy_engine.classify. REJECT si es destructivo,
    ejecuta código por intérprete (sh -c / curl|bash...) o lleva un salto de línea
    crudo — espejo (y más) de la denylist local del sensor. Anota risk_level.
    """
    for field in ("command", "revert"):
        cmd = ov.get(field) or ""
        if not cmd.strip():
            continue
        if "\n" in cmd or "\r" in cmd:
            return "REJECT", "comando con salto de linea crudo bloqueado"
        resolved, _ = mm.resolve_and_validate(cmd, mm._detect_placeholders(cmd), profile)
        cl = policy_engine.classify(resolved)
        if cl.parsed_verb in policy_engine._DESTRUCTIVE_VERBS or any("destructivo" in r for r in cl.reasons):
            return "REJECT", f"comando destructivo bloqueado ({cl.parsed_verb or 'encadenado'})"
        # Ejecución arbitraria opaca: el cuerpo de `sh -c "..."` escapa al cross-check
        # de rutas/placeholders y a la detección de verbos destructivos.
        if getattr(cl, "is_executable_via_interpreter", False) or _invokes_interpreter(resolved):
            return "REJECT", f"ejecucion por interprete bloqueada ({cl.parsed_verb})"
        if field == "command":
            ov["risk_level"] = cl.level.label()
            ov["policy_reasons"] = cl.reasons
            if cl.level == policy_engine.RiskLevel.CRITICAL:
                ov["confidence"] = cap_conf(ov.get("confidence", "low"), "medium")
    return "KEEP", ""


def _aggregate_confidence(data: dict) -> str:
    confs = [i.get("confidence", "low") for i in data.get("suggested_log_sources", [])]
    confs += [i.get("confidence", "low") for i in data.get("suggested_recommendation_overrides", [])]
    confs += [r.get("confidence", "low") for r in (data.get("host_notes") or {}).get("risks", [])]
    if not confs:
        return "low"   # sin items respaldados, no se hereda el 'high' que declare el LLM
    agg = confs[0]
    for c in confs[1:]:
        agg = min_conf(agg, c)
    return min_conf(agg, data.get("global_confidence", "high"))


def validate_and_crosscheck(data: dict, profile: dict, device: str) -> dict:
    try:
        jsonschema.validate(data, ENRICHMENT_SCHEMA)
    except jsonschema.ValidationError as e:
        raise HallucinationError(f"salida no conforme al esquema: {e.message}")

    # device / hash no se confían al LLM: se sellan con los valores reales.
    data["device"] = device
    data["based_on_profile_hash"] = profile.get("profile_hash", "")

    F = cc.facts(profile)
    discarded = []

    kept_ls = []
    for ls in data.get("suggested_log_sources", []):
        verdict, reason, downs = cc.check_log_source(ls, F)
        if verdict == "DISCARD":
            discarded.append({"item": ls.get("id"), "type": "log_source", "reason": reason})
            continue
        if downs:
            ls["confidence"] = min_conf(ls.get("confidence", "low"), "medium")
        kept_ls.append(ls)
    data["suggested_log_sources"] = kept_ls

    kept_ov = []
    for ov in data.get("suggested_recommendation_overrides", []):
        verdict, reason, downs = cc.check_override(ov, F, profile)
        if verdict == "DISCARD":
            discarded.append({"item": ov.get("id"), "type": "override", "reason": reason})
            continue
        sverdict, sreason = sanitize_and_classify(ov, profile)
        if sverdict == "REJECT":
            discarded.append({"item": ov.get("id"), "type": "override", "reason": sreason})
            continue
        conf = ov.get("confidence", "low")
        if downs:
            conf = min_conf(conf, "medium")
        if ov.get("intent") == "recovery":
            conf = cap_conf(conf, "medium")
        ov["confidence"] = conf
        kept_ov.append(ov)
    data["suggested_recommendation_overrides"] = kept_ov

    notes = data.get("host_notes") or {"summary": "", "risks": []}
    notes["summary"] = _sanitize_prose(notes.get("summary", ""))
    for risk in notes.get("risks", []):
        ceiling = cc.check_note(risk, profile)
        risk["confidence"] = cap_conf(risk.get("confidence", "low"), ceiling)
        risk["text"] = _sanitize_prose(risk.get("text", ""))
    data["host_notes"] = notes

    gconf = _aggregate_confidence(data)
    data["global_confidence"] = gconf
    return {"kept": data, "discarded": discarded, "global_confidence": gconf}


def _counts(kept: dict) -> dict:
    return {
        "host_risks": len((kept.get("host_notes") or {}).get("risks", [])),
        "log_sources": len(kept.get("suggested_log_sources", [])),
        "overrides": len(kept.get("suggested_recommendation_overrides", [])),
    }


# ---------------------------------------------------------------------------
# Entrypoint offline
# ---------------------------------------------------------------------------
def enrich(device: str, db_path: str = None) -> dict:
    if not _SAFE_DEVICE.match(device or ""):
        return {"status": "error", "reason": "device inseguro"}
    profile = get_device_profile(device, db_path)
    if not profile:
        return {"status": "error", "reason": "sin perfil determinista; ejecuta discovery primero"}

    mode, model, extra = _resolve_model_config()   # puede lanzar ProviderError (api sin clave)
    prompt = build_prompt(_project_facts(profile))
    raw = llm_call(prompt, ENRICHMENT_SCHEMA, mode, model, extra)
    res = validate_and_crosscheck(raw, profile, device)

    enr_id = save_enrichment(
        device, profile.get("profile_hash"), profile.get("profile_version"),
        res["kept"], res["discarded"], model_used=model, ai_mode=mode,
        confidence=res["global_confidence"], db_path=db_path,
    )
    logger.info(f"[ENRICH] Device {device}: enrichment id={enr_id} ({mode}/{model}), "
                f"confidence={res['global_confidence']}, descartados={len(res['discarded'])}")
    return {
        "status": "success", "enrichment_id": enr_id,
        "confidence": res["global_confidence"], "counts": _counts(res["kept"]),
        "discarded": len(res["discarded"]),
    }
