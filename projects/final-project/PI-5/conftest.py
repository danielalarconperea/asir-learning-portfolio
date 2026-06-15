"""
Configuracion compartida de pytest para PI-5.

Anade src/ al sys.path una sola vez, para que los tests importen los modulos
del coordinador (`import dashboard_soc`, `from tools import policy_engine`...)
sin repetir sys.path.append en cada fichero.
"""
import os
import sys

SRC_DIR = os.path.join(os.path.dirname(__file__), "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)
