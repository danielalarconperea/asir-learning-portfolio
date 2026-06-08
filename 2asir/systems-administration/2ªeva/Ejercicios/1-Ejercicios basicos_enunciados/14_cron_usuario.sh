#!/bin/bash
# Ejercicio 14: Pida un usuario y muestre su crontab.

if [ -n "$1" ]; then
    user=$1
else
    read -p "Dime el usuario: " user
fi

if cat /etc/passwd | grep "$user:" > /dev/null ; then
    crontab -l $user
else
    echo "el usuario no existe"
fi
