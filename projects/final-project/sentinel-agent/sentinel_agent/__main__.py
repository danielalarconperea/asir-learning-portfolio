"""
Punto de entrada del sensor genérico.

Uso:
  python -m sentinel_agent --config /etc/sentinel/sentinel.local.yml
  python -m sentinel_agent --discover-only [--device <id>]   # imprime el perfil y sale
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys


def _setup_logging(level: str = "INFO", file_path: str = None) -> None:
    handlers = [logging.StreamHandler(sys.stdout)]
    if file_path:
        try:
            handlers.append(logging.FileHandler(file_path))
        except OSError:
            pass
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(prog="sentinel-agent")
    parser.add_argument("--config", default=os.environ.get("SENTINEL_CONFIG", "sentinel.local.yml"))
    parser.add_argument("--discover-only", action="store_true",
                        help="Ejecuta el discovery, imprime el System Profile y sale (sin MQTT)")
    parser.add_argument("--device", default="preview",
                        help="device_id a usar en --discover-only")
    args = parser.parse_args(argv)

    if args.discover_only:
        _setup_logging()
        from . import profile_builder
        sections = profile_builder.discover_sections()
        profile = profile_builder.assemble_core(args.device, sections, _now_iso(), "preview")
        profile, _ = profile_builder.finalize(profile, prev_hash=None, prev_version=0)
        print(json.dumps(profile, indent=2, ensure_ascii=False))
        return 0

    from . import config as cfg_mod
    from .monitor import Monitor
    cfg = cfg_mod.load(args.config)
    log_cfg = cfg.get("logging") or {}
    _setup_logging(log_cfg.get("level", "INFO"), log_cfg.get("file_path"))
    Monitor(cfg).run()
    return 0


def _now_iso() -> str:
    import time
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


if __name__ == "__main__":
    sys.exit(main())
