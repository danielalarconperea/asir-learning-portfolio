#!/bin/bash
# Ejercicio 2 Avanzado: Comparar dos números.

read -p "Número 1: " N1
read -p "Número 2: " N2

if [ "$N1" -eq "$N2" ]; then
    echo "Los números son iguales."
elif [ "$N1" -gt "$N2" ]; then
    echo "$N1 es mayor que $N2."
else
    echo "$N2 es mayor que $N1."
fi
