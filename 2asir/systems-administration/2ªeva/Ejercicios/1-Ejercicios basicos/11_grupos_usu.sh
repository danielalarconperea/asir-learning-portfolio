#!/bin/bash
# Ejercicio 11: grupos_usu.sh
# Pide un usuario y muestra los grupos a los que pertenece (uno en cada línea).

read -p "Introduce el nombre del usuario: " USUARIO

if id "$USUARIO" >/dev/null 2>&1; then
    echo "Grupos del usuario $USUARIO:"
    groups "$USUARIO" | cut -d: -f2 | tr ' ' '\n' | grep -v '^$'
else
    echo "El usuario $USUARIO no existe."
fi
