#!/bin/bash
# Ejercicio 15: Pide un nombre de usuario y muestra un mensaje de saludo para él 
# (usando parámetros en la llamada).

if [ -n "$1" ]; then
    user=$1
else
    read -p "Dime el usuario: " user
fi

echo "Hola $user"
