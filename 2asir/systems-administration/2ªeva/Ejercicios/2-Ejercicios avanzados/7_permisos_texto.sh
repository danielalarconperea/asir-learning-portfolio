#!/bin/bash
# Ejercicio 7 Avanzado: Permisos de un fichero en texto legible.

if [ -z "$1" ] || [ ! -e "$1" ]; then
    echo "Uso: $0 fichero"
    exit 1
fi

PERMS=$(ls -l "$1" | cut -c 2-10)

echo "Fichero: $1"
echo "Permisos: $PERMS"

# Desglose
echo "Propietario:"
[[ ${PERMS:0:1} == 'r' ]] && echo "- Lectura"
[[ ${PERMS:1:1} == 'w' ]] && echo "- Escritura"
[[ ${PERMS:2:1} == 'x' ]] && echo "- Ejecución"

echo "Grupo:"
[[ ${PERMS:3:1} == 'r' ]] && echo "- Lectura"
[[ ${PERMS:4:1} == 'w' ]] && echo "- Escritura"
[[ ${PERMS:5:1} == 'x' ]] && echo "- Ejecución"

echo "Otros:"
[[ ${PERMS:6:1} == 'r' ]] && echo "- Lectura"
[[ ${PERMS:7:1} == 'w' ]] && echo "- Escritura"
[[ ${PERMS:8:1} == 'x' ]] && echo "- Ejecución"
