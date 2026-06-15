"""
CLI del operador para el enriquecedor LLM offline (Fase 4).

Uso (desde PI-5/):
  python scripts/enrich_profile.py --device <id> [--generate]      # genera (default)
  python scripts/enrich_profile.py --device <id> --list            # lista pendientes
  python scripts/enrich_profile.py --device <id> --show <enr_id>
  python scripts/enrich_profile.py --device <id> --promote <enr_id> [--item id1,id2]
  python scripts/enrich_profile.py --device <id> --discard <enr_id>
  [--mode api|local --model <m>]   # override del modelo solo para esta corrida

Exit codes: 0 éxito; 1 error genérico (sin perfil/device inseguro/promoción bloqueada);
2 ProviderError (red/429/timeout: reintenta); 3 HallucinationError (revisa modelo/prompt).
"""

import argparse
import json
import os
import re
import sys

_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(_SRC), ".env"))
except Exception:
    pass


def _slug(s: str) -> str:
    return re.sub(r"[^a-z0-9-]+", "-", (s or "").lower()).strip("-")[:40] or "item"


def _draft_to_override_entry(d: dict, device: str, enr_id: int) -> dict:
    entry = {k: d[k] for k in ("intent", "severity", "requires", "applies_if", "match",
                               "command", "explanation") if k in d}
    if d.get("revert"):
        entry["revert"] = d["revert"]
    if d.get("placeholders"):
        entry["placeholders"] = d["placeholders"]
    entry["id"] = f"{device}-enrich-{_slug(d.get('id', 'item'))}"
    entry["source_enrichment"] = enr_id
    entry["notas_correccion"] = f"Promovido por el operador desde enrichment {enr_id}; revisar antes de confiar."
    return entry


def promote_override(device: str, enrichment_id: int, item_ids=None, db_path=None) -> dict:
    """Promueve borradores de un enriquecimiento a recommendations/<device>.json (append atómico)."""
    from tools import db_tools, mitigation_manual, policy_engine

    if not mitigation_manual._SAFE_DEVICE.match(device or ""):
        return {"status": "error", "reason": "device inseguro"}
    enr = db_tools.get_enrichment(enrichment_id, db_path)
    if not enr:
        return {"status": "error", "reason": "enrichment no encontrado"}
    if enr["device"] != device:
        return {"status": "error", "reason": "el enrichment no pertenece a ese device"}

    current = db_tools.get_device_profile(device, db_path)
    # Anti-stale fail-closed: exige que AMBOS hashes existan y coincidan. Un
    # enrichment con profile_hash None/"" (perfil publicado sin hash) NO debe
    # promoverse sobre cualquier inventario; antes el guard se saltaba por ser
    # falsy y promovía a ciegas.
    enr_hash = enr.get("profile_hash")
    cur_hash = current.get("profile_hash")
    if not enr_hash or not cur_hash or enr_hash != cur_hash:
        return {"status": "error", "reason": "perfil ausente o cambiado desde el enrichment; regenéralo (anti-stale)"}

    drafts = enr["enrichment"].get("suggested_recommendation_overrides", [])
    if item_ids:
        wanted = set(item_ids)
        drafts = [d for d in drafts if d.get("id") in wanted]
    if not drafts:
        return {"status": "error", "reason": "no hay borradores que promover (¿item_ids correctos?)"}

    # Re-clasificación de seguridad al promover (defensa en profundidad): aunque
    # ya pasaron el sanitizador al generarse, se re-validan contra el perfil
    # ACTUAL antes de escribir el override (rechaza destructivos/intérpretes).
    from tools import profile_enricher
    for d in drafts:
        verdict, reason = profile_enricher.sanitize_and_classify(dict(d), current)
        if verdict == "REJECT":
            return {"status": "error", "reason": f"borrador '{d.get('id')}' rechazado al re-clasificar: {reason}"}

    path = os.path.join(mitigation_manual.RECS_DIR, f"{device}.json")
    doc = {"version": 1, "device": device, "entries": []}
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                doc = json.load(f)
        except Exception as e:
            return {"status": "error", "reason": f"override existente ilegible: {e}"}
    entries = doc.setdefault("entries", [])

    promoted_ids = []
    for d in drafts:
        entry = _draft_to_override_entry(d, device, enrichment_id)
        entries[:] = [e for e in entries if e.get("id") != entry["id"]]  # upsert por id
        entries.append(entry)
        promoted_ids.append(d.get("id"))

    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(doc, f, ensure_ascii=False, indent=2)
    os.replace(tmp, path)

    mitigation_manual.clear_cache()
    db_tools.set_enrichment_status(enrichment_id, "PROMOTED", promoted_item_ids=promoted_ids, db_path=db_path)
    try:
        policy_engine.audit(event_type="ENRICH_PROMOTE", device=device,
                            command="; ".join(d.get("command", "") for d in drafts),
                            classification=None,
                            decision_reason=f"Operador promovió enrichment {enrichment_id} ({len(drafts)} items)")
    except Exception:
        pass
    return {"status": "success", "promoted": promoted_ids, "path": path}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="enrich_profile")
    parser.add_argument("--device", required=True)
    parser.add_argument("--generate", action="store_true")
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--show", type=int)
    parser.add_argument("--promote", type=int)
    parser.add_argument("--discard", type=int)
    parser.add_argument("--item")  # ids separados por coma
    parser.add_argument("--mode", choices=["api", "local"])
    parser.add_argument("--model")
    args = parser.parse_args(argv)

    if args.mode:
        os.environ["ENRICH_MODE"] = args.mode
    if args.model:
        os.environ["ENRICH_MODEL"] = args.model

    from tools import db_tools

    if args.list:
        for e in db_tools.list_enrichments(args.device, status="PENDING_REVIEW"):
            c = e["enrichment"]
            print(f"[{e['id']}] {e['confidence']} ({e['ai_mode']}/{e['model_used']}) "
                  f"notas={len((c.get('host_notes') or {}).get('risks', []))} "
                  f"logs={len(c.get('suggested_log_sources', []))} "
                  f"overrides={len(c.get('suggested_recommendation_overrides', []))} "
                  f"descartados={len(e['discarded'])}  {e['created_at']}")
        return 0
    if args.show:
        print(json.dumps(db_tools.get_enrichment(args.show), ensure_ascii=False, indent=2))
        return 0
    if args.discard:
        db_tools.set_enrichment_status(args.discard, "DISCARDED")
        print(f"Enrichment {args.discard} descartado.")
        return 0
    if args.promote:
        items = [s.strip() for s in args.item.split(",")] if args.item else None
        res = promote_override(args.device, args.promote, items)
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0 if res.get("status") == "success" else 1

    # default: generar
    from tools import profile_enricher
    try:
        res = profile_enricher.enrich(args.device)
    except profile_enricher.ProviderError as e:
        print(f"[ProviderError:{e.kind}] {e}", file=sys.stderr)
        return 2
    except profile_enricher.HallucinationError as e:
        print(f"[HallucinationError] {e}", file=sys.stderr)
        return 3
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0 if res.get("status") == "success" else 1


if __name__ == "__main__":
    sys.exit(main())
