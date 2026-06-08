#!/bin/bash
# Ejercicio 15: Pide dos números y muestra el resultado de las 4 operaciones básicas 
# (usando parámetros en la llamada).

num1=$1
num2=$2

if [ -z "$num1" ]; then read -p "Número 1: " num1; fi
if [ -z "$num2" ]; then read -p "Número 2: " num2; fi

echo "Suma: $((num1 + num2))"
echo "Resta: $((num1 - num2))"
echo "Multiplicación: $((num1 * num2))"
if [ "$num2" -ne 0 ]; then
    echo "División: $((num1 / num2))"
else
    echo "División: No se puede dividir por cero"
fi