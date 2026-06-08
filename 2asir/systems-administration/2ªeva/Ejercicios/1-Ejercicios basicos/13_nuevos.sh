#!/bin/bash
# Ejercicio 13: nuevos.sh
# Pide un número de días y muestra archivos modificados en ese periodo (posteriores a ese día).

read -p "Introduce el número de días (ficheros modificados en los últimos N días): " DIAS

echo "Buscando ficheros modificados en los últimos $DIAS días en el directorio actual..."
find . -maxdepth 2 -mtime -"$DIAS" -type f
