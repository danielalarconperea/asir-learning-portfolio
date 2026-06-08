#!/bin/bash
# Ejercicio 12: Pide el nombre de un grupo y muestre los usuarios que pertenecen 
# a ese grupo (separados por punto y coma).

if [ -n "$1" ]; then
    group=$1
else
    read -p "Dime el nombre de grupo: " group
fi

if cat /etc/group | grep "$group:" > /dev/null ; then
    usuarios=$(cat /etc/group | grep "$group:" | cut -d: -f4 | tr "," ";")
    echo -e "$usuarios"
else
    echo "el grupo no existe"
fi
