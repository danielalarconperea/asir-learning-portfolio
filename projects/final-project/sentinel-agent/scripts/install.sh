#!/bin/bash
# ==============================================================================
#  Instalador del sensor genérico Sentinel-IT (sentinel-agent)
# ==============================================================================
#  Prepara un host Linux para ejecutar el sensor:
#    - comprueba privilegios de root
#    - instala dependencias del sistema (python3, pip, firewall) y de Python
#    - crea /etc/sentinel/ y /etc/sentinel/certs/
#    - avisa (sin fallar en silencio) si faltan los certificados mTLS o la
#      clave pública de firma — NO los genera; han de colocarse a mano
#    - copia sentinel.local.yml si se proporciona uno
#    - instala, habilita y arranca la unit de systemd
#
#  NO genera certificados ni claves: sigue docs/Onboarding_Sensor.md (§4 y §5)
#  para crear el Thing, descargar el cert X.509 y distribuir la clave pública.
#
#  Uso:
#    sudo ./scripts/install.sh [ruta/a/sentinel.local.yml]
#
#  Si no pasas un sentinel.local.yml, deberás colocarlo a mano en
#  /etc/sentinel/sentinel.local.yml antes de que el servicio arranque sano.
# ==============================================================================

set -euo pipefail

# --- Rutas (relativas al repo, sin asumir rutas absolutas) -------------------
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"   # .../sentinel-agent/scripts
AGENT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"                  # .../sentinel-agent

# Destino convencional del paquete (coincide con WorkingDirectory de la unit).
INSTALL_DIR="/opt/sentinel-agent"
ETC_DIR="/etc/sentinel"
CERTS_DIR="${ETC_DIR}/certs"

UNIT_SRC="${AGENT_DIR}/deploy/sentinel-agent.service"
UNIT_DST="/etc/systemd/system/sentinel-agent.service"
REQS="${AGENT_DIR}/requirements.txt"

# Argumento opcional: ruta a un sentinel.local.yml a instalar.
LOCAL_CONFIG_SRC="${1:-}"
LOCAL_CONFIG_DST="${ETC_DIR}/sentinel.local.yml"

echo "==========================================="
echo "   Instalador - Sensor Sentinel-IT"
echo "==========================================="

# --- 1. Comprobación de privilegios ------------------------------------------
if [ "$(id -u)" -ne 0 ]; then
  echo "[ERROR] Ejecuta este script como root (sudo ./scripts/install.sh)" >&2
  exit 1
fi

# --- 2. Dependencias del sistema ---------------------------------------------
echo "[*] Comprobando dependencias del sistema..."

if ! command -v python3 >/dev/null 2>&1; then
  echo "[-] python3 no encontrado. Instalando..."
  apt-get update && apt-get install -y python3 python3-pip
else
  echo "[OK] python3 detectado."
fi

# pip puede venir aparte de python3 en algunas distros.
if ! command -v pip3 >/dev/null 2>&1; then
  echo "[-] pip3 no encontrado. Instalando..."
  apt-get update && apt-get install -y python3-pip
else
  echo "[OK] pip3 detectado."
fi

# Firewall: el executor aplica los verbos de bloqueo. Avisamos si no hay ninguno.
if command -v iptables >/dev/null 2>&1; then
  echo "[OK] iptables detectado."
elif command -v nft >/dev/null 2>&1; then
  echo "[OK] nftables (nft) detectado."
else
  echo "[!] AVISO: no se ha encontrado iptables ni nftables."
  echo "    El sensor no podrá aplicar mitigaciones de firewall hasta instalarlo."
fi

# --- 3. Dependencias de Python -----------------------------------------------
echo "[*] Instalando dependencias de Python desde requirements.txt..."
if [ -f "${REQS}" ]; then
  # --break-system-packages: necesario en distros con PEP 668 (Debian 12+).
  pip3 install -r "${REQS}" --break-system-packages
  echo "[OK] Dependencias de Python instaladas."
else
  echo "[ERROR] No se encuentra ${REQS}" >&2
  exit 1
fi

# --- 4. Despliegue del paquete -----------------------------------------------
echo "[*] Desplegando el paquete del sensor en ${INSTALL_DIR}..."
mkdir -p "${INSTALL_DIR}"
# Copiamos el paquete Python para que 'python3 -m sentinel_agent' lo encuentre
# desde el WorkingDirectory de la unit.
cp -r "${AGENT_DIR}/sentinel_agent" "${INSTALL_DIR}/"
cp -f "${AGENT_DIR}/requirements.txt" "${INSTALL_DIR}/" 2>/dev/null || true
echo "[OK] Paquete copiado a ${INSTALL_DIR}."

# --- 5. Directorios de configuración -----------------------------------------
echo "[*] Creando ${ETC_DIR} y ${CERTS_DIR}..."
mkdir -p "${CERTS_DIR}"
chmod 700 "${CERTS_DIR}"
echo "[OK] Directorios de configuración listos."

# --- 6. Comprobación de certificados mTLS (no se generan aquí) ---------------
echo "[*] Comprobando certificados mTLS en ${CERTS_DIR}..."
MISSING_CERTS=0
for f in device.cert.pem device.private.key root-CA.crt; do
  if [ ! -f "${CERTS_DIR}/${f}" ]; then
    echo "[!] AVISO: falta ${CERTS_DIR}/${f}"
    MISSING_CERTS=1
  fi
done
if [ "${MISSING_CERTS}" -eq 0 ]; then
  echo "[OK] Certificados mTLS presentes."
else
  echo "    -> El sensor NO podrá conectar a AWS IoT hasta colocarlos."
  echo "    -> Sigue docs/Onboarding_Sensor.md (§4) para crearlos y descargarlos."
fi

# --- 7. Comprobación de la clave pública de firma (no se genera aquí) --------
echo "[*] Comprobando la clave pública de firma Ed25519..."
SIGNING_PUB="${ETC_DIR}/sentinel_pi5_signing.pub"
MISSING_SIGNING=0
if [ -f "${SIGNING_PUB}" ]; then
  echo "[OK] Clave pública de firma presente (${SIGNING_PUB})."
else
  echo "[!] AVISO: falta ${SIGNING_PUB}"
  echo "    -> Sin la clave pública de PI-5 el sensor NO arrancará (no puede verificar firmas)."
  echo "    -> Cópiala según docs/Onboarding_Sensor.md (§5)."
  MISSING_SIGNING=1
fi

# --- 8. Configuración del sensor ---------------------------------------------
MISSING_CONFIG=0
if [ -n "${LOCAL_CONFIG_SRC}" ]; then
  if [ -f "${LOCAL_CONFIG_SRC}" ]; then
    echo "[*] Instalando sentinel.local.yml desde ${LOCAL_CONFIG_SRC}..."
    cp "${LOCAL_CONFIG_SRC}" "${LOCAL_CONFIG_DST}"
    chmod 600 "${LOCAL_CONFIG_DST}"
    echo "[OK] Configuración instalada en ${LOCAL_CONFIG_DST}."
  else
    echo "[ERROR] No se encuentra el fichero de configuración: ${LOCAL_CONFIG_SRC}" >&2
    exit 1
  fi
elif [ -f "${LOCAL_CONFIG_DST}" ]; then
  echo "[OK] Ya existe ${LOCAL_CONFIG_DST}; se conserva."
else
  echo "[!] AVISO: no hay ${LOCAL_CONFIG_DST} y no se ha proporcionado uno."
  echo "    -> Copia sentinel.local.example.yml a ${LOCAL_CONFIG_DST} y rellénalo"
  echo "       (device_id, aws.*, signing.*) antes de que el servicio arranque sano."
  MISSING_CONFIG=1
fi

# --- 9. Instalación de la unit de systemd ------------------------------------
echo "[*] Instalando el servicio systemd (sentinel-agent.service)..."
if [ ! -f "${UNIT_SRC}" ]; then
  echo "[ERROR] No se encuentra la unit: ${UNIT_SRC}" >&2
  exit 1
fi

cp "${UNIT_SRC}" "${UNIT_DST}"
systemctl daemon-reload
systemctl enable sentinel-agent.service

# No arrancar el servicio si faltan prerequisitos: el sensor entraria en
# crash-loop (config.load() lanza ValueError sin device_id/signing/aws, y sin
# certs la conexion mTLS no levanta). Con Restart=on-failure + RestartSec=10
# eso es un bucle de reinicio cada 10s. Mejor dejarlo habilitado, sin arrancar.
if [ "${MISSING_CERTS}" -ne 0 ] || [ "${MISSING_SIGNING}" -ne 0 ] || [ "${MISSING_CONFIG}" -ne 0 ]; then
  echo "[!] Servicio instalado y habilitado, pero NO arrancado: faltan prerequisitos"
  echo "    (certificados mTLS, clave de firma y/o sentinel.local.yml — ver avisos arriba)."
  echo "    Colócalos y arranca con: sudo systemctl start sentinel-agent"
else
  systemctl start sentinel-agent.service
  echo "[OK] Servicio sentinel-agent instalado, habilitado y arrancado."
fi

echo
echo "==========================================="
echo " Instalación completada."
echo "==========================================="
echo "Estado del servicio:  sudo systemctl status sentinel-agent"
echo "Logs en vivo:         sudo journalctl -u sentinel-agent -f"
echo "Verificación rápida:  python3 -m sentinel_agent --config ${LOCAL_CONFIG_DST} --discover-only"
echo
echo "Si algún AVISO anterior señaló certificados o clave de firma ausentes,"
echo "colócalos y reinicia con: sudo systemctl restart sentinel-agent"
