#!/bin/bash
# Ejercicio 16: Recoja un nombre de fichero y añada una numeración a las líneas de dicho fichero.

if [ -n "$1" ]; then
    file=$1
else
    read -p "Dime el fichero: " file
fi

if [ -f "$file" ]; then
    nl "$file"
else
    echo "El fichero no existe"
fi
