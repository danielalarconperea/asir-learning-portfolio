#!/bin/bash
# Ejercicio 7: Realizar un script que recoja el nombre de un fichero y muestre 
# qué permisos tiene activados mediante texto comprensible.

if [ -n "$1" ]; then
    fichero=$1
else
    read -p "Dame el nombre de un fichero: " fichero
fi

# Validar que el fichero existe
if [ ! -e "$fichero" ]; then
    echo "Error: El fichero no existe."
    exit 1
fi

permisos=$(ls -ld "$fichero" | awk '{print $1}')

if [ "${permisos:0:1}" == "-" ]; then
    echo "El archivo adjunto es un fichero"
elif [ "${permisos:0:1}" == "d" ]; then
    echo "El archivo adjunto es un directorio"
else
    echo "El archivo adjunto es especial"
fi

echo -e "\nEl propietario del fichero es: $(ls -ld "$fichero" | awk '{print $3}')"

if [ "${permisos:1:1}" == "r" ]; then
    echo "Tiene permiso de lectura"
fi

if [ "${permisos:2:1}" == "w" ]; then
    echo "Tiene permiso de escritura"
fi

if [ "${permisos:3:1}" == "x" ]; then
    echo "Tiene permiso de ejecucion"
elif [ "${permisos:3:1}" == "s" ] || [ "${permisos:3:1}" == "S" ]; then
    echo "Tiene permiso de ejecucion con privilegios de usuario (setuid)"
fi

echo -e "\nEl grupo del fichero es: $(ls -ld "$fichero" | awk '{print $4}')"

if [ "${permisos:4:1}" == "r" ]; then
    echo "Tiene permiso de lectura"
fi

if [ "${permisos:5:1}" == "w" ]; then
    echo "Tiene permiso de escritura"
fi

if [ "${permisos:6:1}" == "x" ]; then
    echo "Tiene permiso de ejecucion"
elif [ "${permisos:6:1}" == "s" ] || [ "${permisos:6:1}" == "S" ]; then
    echo "Tiene permiso de ejecucion con privilegios de grupo (setgid)"
fi

echo -e "\nLos demas usuarios del fichero:"

if [ "${permisos:7:1}" == "r" ]; then
    echo "Tiene permiso de lectura"
fi

if [ "${permisos:8:1}" == "w" ]; then
    echo "Tiene permiso de escritura"
fi

if [ "${permisos:9:1}" == "x" ]; then
    echo "Tiene permiso de ejecucion"
elif [ "${permisos:9:1}" == "t" ] || [ "${permisos:9:1}" == "T" ]; then
    echo "Tiene permiso de ejecucion con restricciones (sticky bit)"
fi
