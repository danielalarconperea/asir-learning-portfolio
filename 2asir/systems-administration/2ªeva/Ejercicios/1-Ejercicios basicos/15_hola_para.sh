#!/bin/bash
# Ejercicio 15: hola_para.sh
# Recibe un nombre por parámetro.

if [ -z "$1" ]; then
    echo "Uso: $0 nombre"
    exit 1
fi

echo "¡Hola $1!"
