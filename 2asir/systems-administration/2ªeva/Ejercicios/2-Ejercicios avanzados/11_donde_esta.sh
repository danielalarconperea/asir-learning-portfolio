#!/bin/bash
# Ejercicio 11 Avanzado: Buscar ficheros y mostrar rutas absolutas de sus directorios.

if [ $# -eq 0 ]; then
    echo "Uso: $0 fichero1 fichero2..."
    exit 1
fi

for FICHERO in "$@"; do
    echo "Buscando '$FICHERO'..."
    RUTAS=$(find / -name "$FICHERO" 2>/dev/null)
    
    if [ -z "$RUTAS" ]; then
        echo "El archivo ordinario $FICHERO no se encuentra en el sistema."
    else
        echo "El archivo ordinario $FICHERO se encuentra en los directorios:"
        for RUTA in $RUTAS; do
            DIRNAME=$(dirname "$RUTA")
            # Convertimos a ruta absoluta si no lo es (aunque find / ya da absolutas)
            readlink -f "$DIRNAME"
        done
    fi
    echo ""
done
