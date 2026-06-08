#!/bin/bash
# Ejercicio 12: Script que admita -c/--corta (fecha corta), -l/--larga (fecha larga) 
# o sin parámetros (calendario del mes).


# Comprobamos si se ha introducido algún parámetro
if [ $# -eq 0 ]; then
    # Si no se ha introducido ningún parámetro, mostramos el calendario del mes actual
    cal 
else
    # Comprobamos si el parámetro es -c o --corta
    if [ "$1" = "-c" ] || [ "$1" = "--corta" ]; then
        # Si el parámetro es -c o --corta, mostramos la fecha corta
        date +"%d-%m-%Y"
    # Comprobamos si el parámetro es -l o --larga
    elif [ "$1" = "-l" ] || [ "$1" = "--larga" ]; then
        # Si el parámetro es -l o --larga, mostramos la fecha larga
        date +"%A %d de %B de %Y"
    else
        # Si el parámetro no es válido, mostramos un mensaje de error
        echo "Error: Parámetro no válido"
    fi
fi