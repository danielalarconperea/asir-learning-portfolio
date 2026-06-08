#!/bin/bash
# Ejercicio 1 Avanzado: Calculadora con control de parámetros.
# Si no se pasan parámetros, los pide por teclado.

NUM1=$1
NUM2=$2

if [ -z "$NUM1" ]; then
    read -p "No indicaste el primer número. Introdúcelo ahora: " NUM1
fi

if [ -z "$NUM2" ]; then
    read -p "No indicaste el segundo número. Introdúcelo ahora: " NUM2
fi

# Validar que son números
if ! [[ "$NUM1" =~ ^[0-9]+$ ]] || ! [[ "$NUM2" =~ ^[0-9]+$ ]]; then
    echo "Error: Ambos parámetros deben ser números."
    exit 1
fi

echo "Suma: $((NUM1 + NUM2))"
echo "Resta: $((NUM1 - NUM2))"
echo "Multiplicación: $((NUM1 * NUM2))"
[ $NUM2 -ne 0 ] && echo "División: $((NUM1 / NUM2))" || echo "División: Error"
