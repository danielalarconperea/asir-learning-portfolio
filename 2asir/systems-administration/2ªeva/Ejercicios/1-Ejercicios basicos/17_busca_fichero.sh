#!/bin/bash
# Ejercicio 17: busca_fichero.sh
# Recoge un nombre de fichero y lo busca en todo el sistema.

if [ -z "$1" ]; then
    echo "Uso: $0 nombre_fichero"
    exit 1
fi

echo "Buscando '$1' en todo el sistema (puede tardar y mostrar errores de permisos)..."
find / -name "$1" 2>/dev/null
