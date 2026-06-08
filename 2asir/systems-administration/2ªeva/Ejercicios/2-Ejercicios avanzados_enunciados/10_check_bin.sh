#!/bin/bash
# Ejercicio 10: Script que compruebe si existe un directorio bin en el HOME del usuario; 
# si no existe, crearlo y añadirlo al PATH.

if [ ! -d "$HOME/bin" ]; then
    mkdir "$HOME/bin"
    echo "export PATH=$PATH:$HOME/bin" >> ~/.bashrc
    source ~/.bashrc
fi
