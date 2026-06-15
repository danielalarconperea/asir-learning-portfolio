"""
Genera y rota el par Ed25519 con el que PI-5 firma los comandos al sensor.

Salida (par 'current', el activo):
  PI-5/certificados/sentinel_pi5_signing.key       (privada, gitignored)
  PI-4/firma-iot/sentinel_pi5_signing.pub  (publica, commiteable)

Uso:
  python scripts/generate_signing_keys.py            # crea el par actual
  python scripts/generate_signing_keys.py --force    # sobreescribe el actual (rotacion DESTRUCTIVA, con downtime)
  python scripts/generate_signing_keys.py --next     # crea el par 'next' (rotacion SIN downtime)
  python scripts/generate_signing_keys.py --promote  # asciende 'next' a actual y retira 'next'

Rotacion SIN downtime (recomendada en flota).
IMPORTANTE: PI-5/config.yml SIEMPRE apunta a la ruta ESTABLE (...sentinel_pi5_signing.key);
NUNCA se repunta al .next.key. --promote intercambia el CONTENIDO bajo esa ruta estable, asi
que un restart de PI-5 jamas queda apuntando a un fichero inexistente.
  1. --next   : genera sentinel_pi5_signing.next.{key,pub} SIN tocar el par actual.
  2. Distribuir .next.pub : copiala a cada sensor en signing.next_public_key_path
                (sentinel.local.yml) y reinicia los sensores. Ahora cada sensor acepta
                comandos firmados con la clave actual O con la next.
  3. --promote : asciende el par next a actual: os.replace mueve .next.key -> .key y
                .next.pub -> .pub (la ruta estable .key pasa a CONTENER la clave nueva) y
                elimina el par next. PI-5/config.yml NO se toca.
  4. Reiniciar PI-5 : reinicia el coordinador Y el dashboard para que recarguen el .key.
                Ahora PI-5 firma con la clave nueva, que los sensores YA aceptan (es su
                'next') -> cero rechazos, cero downtime. (Hasta este restart, PI-5 sigue
                firmando con la clave vieja desde memoria; los sensores tambien la aceptan.)
  5. Limpiar sensores : copia la nueva .pub (ya la actual) a signing.public_key_path,
                retira signing.next_public_key_path y reinicia los sensores (vuelta a clave
                unica). La nueva .pub debe estar fisicamente en public_key_path ANTES del
                reinicio: el sensor NO recarga claves en caliente.
"""

import argparse
import os
import sys

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PRIV_DIR = os.path.join(REPO_ROOT, "PI-5", "certificados")
PUB_DIR = os.path.join(REPO_ROOT, "PI-4", "firma-iot")

PRIV_PATH = os.path.join(PRIV_DIR, "sentinel_pi5_signing.key")
PUB_PATH = os.path.join(PUB_DIR, "sentinel_pi5_signing.pub")
PRIV_NEXT_PATH = os.path.join(PRIV_DIR, "sentinel_pi5_signing.next.key")
PUB_NEXT_PATH = os.path.join(PUB_DIR, "sentinel_pi5_signing.next.pub")


def _generate_pair(priv_path: str, pub_path: str, force: bool) -> int:
    for path in (priv_path, pub_path):
        if os.path.exists(path) and not force:
            print(f"[ERROR] Ya existe {path}. Usa --force para sobreescribir.", file=sys.stderr)
            return 1

    os.makedirs(os.path.dirname(priv_path), exist_ok=True)
    os.makedirs(os.path.dirname(pub_path), exist_ok=True)

    private_key = Ed25519PrivateKey.generate()
    priv_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    pub_pem = private_key.public_key().public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    with open(priv_path, "wb") as f:
        f.write(priv_pem)
    try:
        os.chmod(priv_path, 0o600)
    except OSError:
        pass

    with open(pub_path, "wb") as f:
        f.write(pub_pem)

    print(f"[OK] Privada -> {priv_path}")
    print(f"[OK] Publica -> {pub_path}")
    return 0


def _promote() -> int:
    """Asciende el par 'next' a actual (sobreescribe) y elimina el next."""
    for path in (PRIV_NEXT_PATH, PUB_NEXT_PATH):
        if not os.path.exists(path):
            print(f"[ERROR] No existe {path}. Genera primero el par next con --next.",
                  file=sys.stderr)
            return 1
    # os.replace es atomico dentro del mismo sistema de ficheros.
    os.replace(PRIV_NEXT_PATH, PRIV_PATH)
    os.replace(PUB_NEXT_PATH, PUB_PATH)
    try:
        os.chmod(PRIV_PATH, 0o600)
    except OSError:
        pass
    print(f"[OK] Promovido: next -> actual")
    print(f"[OK] Privada -> {PRIV_PATH}")
    print(f"[OK] Publica -> {PUB_PATH}")
    print()
    print("Siguiente paso: PI-5/config.yml NO cambia (sigue apuntando al .key estable, que")
    print("ahora contiene la clave nueva). Reinicia el coordinador Y el dashboard de PI-5")
    print("para que la recarguen. Luego distribuye la nueva .pub a los sensores en")
    print("signing.public_key_path, retira signing.next_public_key_path y reinicialos.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera/rota la clave de firma Ed25519 de PI-5.")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--next", action="store_true",
                       help="Genera el par 'next' (rotacion sin downtime), sin tocar el actual")
    group.add_argument("--promote", action="store_true",
                       help="Asciende el par 'next' a actual y elimina el next")
    parser.add_argument("--force", action="store_true",
                        help="Sobreescribe ficheros existentes")
    args = parser.parse_args()

    if args.promote:
        return _promote()

    if args.next:
        rc = _generate_pair(PRIV_NEXT_PATH, PUB_NEXT_PATH, args.force)
        if rc == 0:
            print()
            print("Distribucion (rotacion):")
            print("  * Copia la .next.pub a cada sensor y apunta signing.next_public_key_path.")
            print("  * Reinicia los sensores; aceptaran la clave actual Y la next.")
            print("  * Cuando todos la acepten, ejecuta --promote y reinicia PI-5")
            print("    (NO se repunta PI-5/config.yml: --promote intercambia el contenido del .key).")
        return rc

    rc = _generate_pair(PRIV_PATH, PUB_PATH, args.force)
    if rc == 0:
        print()
        print("Distribucion:")
        print("  * La privada queda en PI-5 (gitignored). NO la subas a git.")
        print("  * La publica se copia a cada sensor (signing.public_key_path). Es segura para commit.")
    return rc


if __name__ == "__main__":
    sys.exit(main())
