"""Pone el paquete sentinel_agent en el path para los tests del sensor."""
import os
import sys

PKG_DIR = os.path.dirname(__file__)
if PKG_DIR not in sys.path:
    sys.path.insert(0, PKG_DIR)
