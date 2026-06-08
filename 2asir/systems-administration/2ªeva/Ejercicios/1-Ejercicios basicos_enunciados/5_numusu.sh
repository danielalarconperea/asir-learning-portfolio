#!/bin/bash
# Ejercicio 5: Que muestre cuántos usuarios hay conectados en el sistema.

echo -n "Usuarios conectados: "
who | cut -d' ' -f1 | sort -u | wc -l
