#!/bin/bash
# Ejercicio 15: calc_para.sh
# Recibe dos números por parámetro y muestra resultados.

if [ $# -ne 2 ]; then
    echo "Uso: $0 numero1 numero2"
    exit 1
fi

NUM1=$1
NUM2=$2

echo "Suma: $((NUM1 + NUM2))"
echo "Resta: $((NUM1 - NUM2))"
echo "Multiplicación: $((NUM1 * NUM2))"
[ $NUM2 -ne 0 ] && echo "División: $((NUM1 / NUM2))" || echo "División: Error"
