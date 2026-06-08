#!/bin/bash
# Ejercicio 3 Avanzado: Comprobar si un usuario existe.

USUARIO=$1
if [ -z "$USUARIO" ]; then
    read -p "Introduce el nombre del usuario a comprobar: " USUARIO
fi

if id "$USUARIO" >/dev/null 2>&1; then
    echo "El usuario '$USUARIO' SÍ existe en el sistema."
else
    echo "El usuario '$USUARIO' NO existe."
fi
