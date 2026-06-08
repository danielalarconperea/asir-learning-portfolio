#!/bin/bash
# Ejercicio 11: Busca en el sistema todos los ficheros especificados como argumentos 
# y visualiza su ruta absoluta (sin el nombre del archivo).

for fichero in "$@"; do
    if [ -f "$fichero" ]; then
        find / -name "$fichero" -printf "%h\n" 2>/dev/null
    fi
done
