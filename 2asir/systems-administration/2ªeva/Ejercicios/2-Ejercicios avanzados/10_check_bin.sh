#!/bin/bash
# Ejercicio 10 Avanzado: Comprobar ~/bin y añadir al PATH.

BIN_DIR="$HOME/bin"

if [ ! -d "$BIN_DIR" ]; then
    echo "El directorio $BIN_DIR no existe. Creándolo..."
    mkdir -p "$BIN_DIR"
else
    echo "El directorio $BIN_DIR ya existe."
fi

# Comprobar si ya está en el PATH
if [[ ":$PATH:" == *":$BIN_DIR:"* ]]; then
    echo "El directorio ya está en el PATH."
else
    echo "Añadiendo $BIN_DIR al PATH en .bashrc..."
    echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
    echo "Añadido. Abre una nueva shell para aplicar los cambios."
fi
