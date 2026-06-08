#!/bin/bash
# Ejercicio 2: Que nos muestre la lista de usuarios que no sean del sistema.


sudo awk -F: '$3 > 1000 && 60000 > $3 {print $1}' /etc/passwd

sudo cat /etc/passwd | cut -d: -f1,3 | grep -E ':[0-9]{4,}' | grep -vE ':6[0-9]{3,}' | cut -d: -f1

