#!/bin/bash
# Ejercicio 12 Avanzado: Script calendario.

DIA=$(date +%d)
MES=$(date +%m)
ANIO=$(date +%Y)

if [ $# -eq 0 ]; then
    cal
    exit 0
fi

if [ $# -ne 1 ]; then
    echo "Sólo se admite un parámetro."
    exit 1
fi

case $1 in
    -c|--corta)
        echo "$DIA/$MES/$ANIO"
        ;;
    -l|--larga)
        echo "Hoy es el día '$DIA' del mes '$MES' del año '$ANIO'."
        ;;
    *)
        echo "Opción incorrecta."
        exit 2
        ;;
esac
