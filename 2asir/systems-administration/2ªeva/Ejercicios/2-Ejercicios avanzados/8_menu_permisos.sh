#!/bin/bash
# Ejercicio 8 Avanzado: Menú para añadir o quitar permisos.

if [ -z "$1" ] || [ ! -e "$1" ]; then
    echo "Uso: $0 fichero"
    exit 1
fi

FICHERO=$1

while true; do
    echo "--- GESTIÓN DE PERMISOS: $FICHERO ---"
    ls -l "$FICHERO"
    echo "1. Añadir permiso de ejecución (+x)"
    echo "2. Quitar permiso de ejecución (-x)"
    echo "3. Añadir permiso de escritura (+w)"
    echo "4. Quitar permiso de escritura (-w)"
    echo "5. Salir"
    read -p "Opción: " OPC

    case $OPC in
        1) chmod +x "$FICHERO" ;;
        2) chmod -x "$FICHERO" ;;
        3) chmod +w "$FICHERO" ;;
        4) chmod -w "$FICHERO" ;;
        5) break ;;
        *) echo "Opción no válida." ;;
    esac
done
