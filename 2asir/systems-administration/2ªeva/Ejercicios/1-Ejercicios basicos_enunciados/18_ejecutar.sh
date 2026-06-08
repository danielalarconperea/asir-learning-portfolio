#!/bin/bash
# Ejercicio 18: Que recoja un nombre de fichero y le añada permisos de ejecución.

if [ -n "$1" ]; then
    file=$1
else
    read -p "Dime el fichero: " file
fi

if chmod a+x $file > /dev/null; then
    echo "permisos de ejecución añadidos"
else
    echo "No se ha encontrado el archivo con ese nombre"
fi
