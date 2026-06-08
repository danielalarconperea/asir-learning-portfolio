#!/bin/bash
# Ejercicio 12: usu_grupo.sh
# Pide un grupo y muestra los usuarios que pertenecen a él (separados por ';').

read -p "Introduce el nombre del grupo: " GRUPO

# Obtenemos los usuarios secundarios del archivo /etc/group
USUARIOS=$(grep "^$GRUPO:" /etc/group | cut -d: -f4 | tr ',' ';')

if [ -z "$(grep "^$GRUPO:" /etc/group)" ]; then
    echo "El grupo $GRUPO no existe."
elif [ -z "$USUARIOS" ]; then
    echo "El grupo $GRUPO no tiene usuarios secundarios definidos."
else
    echo "Usuarios en el grupo $GRUPO: $USUARIOS"
fi
