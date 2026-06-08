#!/bin/bash
# Ejercicio 10: Pide el nombre de un usuario y muestre en pantalla el tamaño 
# del directorio de conexión de este.

read -p "Introduce el nombre de un usuario: " usuario

# 1. Es mejor comprobar si el directorio existe antes de calcular
if [ -d "/home/$usuario" ]; then
    
    # 2. Usamos 'du' para calcular el tamaño
    # -s: summary (total de la carpeta, no archivo por archivo)
    # -h: human-readable (en KB, MB o GB automáticamente)
    # cut -f1: nos quedamos solo con la primera columna (el número)
    tamano=$(du -sh "/home/$usuario" | cut -f1)

    echo "El tamaño del directorio de conexión de $usuario es: $tamano"
else
    echo "Error: El usuario o su directorio (/home/$usuario) no existe."
fi