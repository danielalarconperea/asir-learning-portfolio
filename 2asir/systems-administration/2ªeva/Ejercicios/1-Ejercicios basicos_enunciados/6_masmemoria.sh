#!/bin/bash
# Ejercicio 6: Muestre los 3 procesos que más consumen memoria en el sistema.
echo "---------------------------------------------------------------------------"
echo -e "Procesos con más consumo de memoria:\n" 
top -b -o "%MEM" -n 1 | head -n 10 | tail -n 4
echo "---------------------------------------------------------------------------"