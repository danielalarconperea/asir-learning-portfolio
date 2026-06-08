#!/bin/bash
# Ejercicio 4 Avanzado: Grupos comunes a varios usuarios.
# Uso: ./grupos_compartidos.sh user1 user2 user3...

if [ $# -lt 2 ]; then
    echo "Se necesitan al menos 2 usuarios para comparar."
    exit 1
fi

# Inicializamos con los grupos del primer usuario
COMUNES=$(id -Gn "$1" | tr ' ' '\n')

shift # Pasamos al siguiente

for USU in "$@"; do
    if ! id "$USU" >/dev/null 2>&1; then
        echo "Usuario $USU no existe. Saltando..."
        continue
    fi
    GRUPOS_USU=$(id -Gn "$USU" | tr ' ' '\n')
    # Actualizamos la intersección
    COMUNES=$(echo -e "$COMUNES\n$GRUPOS_USU" | sort | uniq -d)
done

if [ -z "$COMUNES" ]; then
    echo "No hay grupos comunes entre los usuarios indicados."
else
    echo "Grupos compartidos por todos los usuarios:"
    echo "$COMUNES"
fi
