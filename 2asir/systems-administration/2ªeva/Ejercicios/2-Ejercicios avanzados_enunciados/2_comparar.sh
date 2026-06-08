#!/bin/bash
# Ejercicio 2: Leer dos números y mostrar si son iguales o cuál es mayor.

if [ -n "$1" ]; then
    num1=$1
else
    read -p "Dime el primer numero: " num1
fi

if [ -n "$2" ]; then
    num2=$2
else
    read -p "Dime el segundo numero: " num2
fi

if [ $num1 -eq $num2 ]; then
    echo "Los numeros son iguales"
elif [ $num1 -gt $num2 ]; then
    echo "El numero $num1 es mayor"
else
    echo "El numero $num2 es mayor"
fi
