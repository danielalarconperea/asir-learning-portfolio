#!/bin/bash
# Ejercicio 9: calc.sh
# Pide dos números y muestra resultados de suma, resta, multiplicación y división.

read -p "Introduce el primer número: " NUM1
read -p "Introduce el segundo número: " NUM2

echo "Suma: $((NUM1 + NUM2))"
echo "Resta: $((NUM1 - NUM2))"
echo "Multiplicación: $((NUM1 * NUM2))"

if [ $NUM2 -ne 0 ]; then
    echo "División: $((NUM1 / NUM2))"
else
    echo "División: Error (división por cero)"
fi
