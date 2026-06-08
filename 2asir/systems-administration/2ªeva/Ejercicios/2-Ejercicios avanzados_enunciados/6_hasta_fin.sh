#!/bin/bash
# Ejercicio 6: Realizar un script que lea valores desde teclado hasta que se introduzca 
# la cadena "fin". Mostrará todos los textos introducidos y acabará.

while true; do
    read -p "Introduce un valor: " valor
    if [ $valor == "fin" ]; then
        if [ -z $valores ]; then
            echo "Ningun valor registrado"
        else
            echo "Lista de valores introducidos: ${valores[*]}"
        fi
        echo "saliendo del programa..."
        exit 0
    else
        valores+=($valor)
    fi
done