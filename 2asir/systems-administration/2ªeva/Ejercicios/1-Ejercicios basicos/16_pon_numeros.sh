#!/bin/bash
# Ejercicio 16: pon_numeros.sh
# Recibe un fichero y muestra sus líneas numeradas.

if [ -z "$1" ] || [ ! -f "$1" ]; then
    echo "Uso: $0 nombre_fichero"
    exit 1
fi

nl -ba "$1"
# O alternativamente: cat -n "$1"
