#!/bin/bash
# Ejercicio 18: ejecutar.sh
# Añade permisos de ejecución a un fichero pasado por parámetro.

if [ -z "$1" ] || [ ! -e "$1" ]; then
    echo "Uso: $0 nombre_fichero"
    exit 1
fi

chmod +x "$1"
echo "Permisos de ejecución añadidos a '$1'."
ls -l "$1"
