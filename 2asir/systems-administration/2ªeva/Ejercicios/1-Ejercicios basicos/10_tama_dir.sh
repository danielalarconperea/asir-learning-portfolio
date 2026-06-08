#!/bin/bash
# Ejercicio 10: tama_dir.sh
# Pide un usuario y muestra el tamaño de su directorio de conexión.

read -p "Introduce el nombre del usuario: " USUARIO

# Buscamos el home del usuario en /etc/passwd por si no está en /home/
HOMEDIR=$(grep "^$USUARIO:" /etc/passwd | cut -d: -f6)

if [ -z "$HOMEDIR" ]; then
    echo "El usuario $USUARIO no existe."
elif [ ! -d "$HOMEDIR" ]; then
    echo "El directorio $HOMEDIR no existe."
else
    echo "Calculando el tamaño de $HOMEDIR..."
    du -sh "$HOMEDIR"
fi
