#!/bin/bash
# Ejercicio 11: Pide el nombre de un usuario y muestre los grupos a los que pertenece (uno en cada línea).

if [ -n "$1" ]; then
    user=$1
else
    read -p "Dime el nombre de usuario: " user
fi

if cat /etc/passwd | grep $user > /dev/null ; then
    gupos=$(id $user | cut -d" " -f3 | cut -d= -f2 | sed "s/,/\n/g") 
    echo -e "\n$gupos"
else
    echo "el usuario no existe"
fi



if id "$user" > /dev/null 2>&1; then
    grupos=$(id -Gn "$user" | tr ' ' '\n')
    echo "Los grupos de $user son:"
    echo "$grupos"
else
    echo "Error: El usuario '$user' no existe en este sistema."
fi