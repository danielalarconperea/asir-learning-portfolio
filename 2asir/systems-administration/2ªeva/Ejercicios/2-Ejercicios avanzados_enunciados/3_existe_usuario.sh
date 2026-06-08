#!/bin/bash
# Ejercicio 3: Leer un nombre por parámetro, si el usuario no lo introduce pedirlo por teclado. 
# Después mostrar si el usuario existe o no y mostrarlo por pantalla.

if [ -n "$1" ]; then
    user=$1
else
    read -p "Dime el usuario: " user
fi

if id "$user" > /dev/null; then
    echo "El usuario $user existe"
else
    echo "El usuario $user no existe"
fi
