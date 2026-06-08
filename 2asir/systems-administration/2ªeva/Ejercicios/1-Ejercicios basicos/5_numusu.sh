#!/bin/bash
# Ejercicio 5: numusu.sh
# Muestra cuántos usuarios hay conectados en el sistema actualmente.

TOTAL=$(who | wc -l)
echo "Actualmente hay $TOTAL usuarios conectados al sistema."
