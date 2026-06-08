#!/bin/bash
# Ejercicio 1: Añadir PATH a .bashrc
# Este script añade el directorio de ejercicios al PATH en .bashrc para que los scripts 
# se puedan ejecutar desde cualquier lugar.

EJERCICIOS_DIR="$HOME/ejercicios"

# Comprobamos si ya está en el .bashrc
if grep -q "$EJERCICIOS_DIR" "$HOME/.bashrc"; then
    echo "El directorio ya está en el PATH de .bashrc"
else
    echo "export PATH=\$PATH:$EJERCICIOS_DIR" >> "$HOME/.bashrc"
    echo "Directorio añadido al PATH en .bashrc. Reinicia la shell o ejecuta 'source ~/.bashrc'"
fi
