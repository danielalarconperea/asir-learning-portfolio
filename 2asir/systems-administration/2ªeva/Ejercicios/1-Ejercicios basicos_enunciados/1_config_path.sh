#!/bin/bash
# Ejercicio 1: Haz que los scripts puestos en la carpeta ejercicios de tu directorio de conexión 
# se puedan ejecutar desde cualquier ruta sin indicar el directorio. (añadir PATH a .bashrc)

EJERCICIOS_DIR="$HOME/ejercicios"

if grep -q "$EJERCICIOS_DIR" "$HOME/.bashrc"; then
    echo "El directorio ya está en el PATH de .bashrc"
else
    echo "export PATH=\$PATH:$EJERCICIOS_DIR" >> "$HOME/.bashrc"
    echo "Directorio añadido al PATH en .bashrc. Reinicia la shell o ejecuta 'source ~/.bashrc'"
fi
