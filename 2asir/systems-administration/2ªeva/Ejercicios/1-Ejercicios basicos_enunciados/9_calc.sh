#!/bin/bash
# Ejercicio 9: Pide dos números y muestra el resultado de las 4 operaciones básicas.

read -p "Introduce el primer número: " num1
read -p "Introduce el segundo número: " num2

suma=$(($num1 + $num2))
resta=$(($num1 - $num2))
multiplicacion=$(($num1 * $num2))
division=$(($num1 / $num2))


echo "Suma: $suma"
echo "Resta: $resta"
echo "Multiplicación: $multiplicacion"
echo "División: $division"
