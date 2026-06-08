#!/bin/bash
# Ejercicio 13: Pida un día y muestre los ficheros con fecha superior a ese día.

if [ -n "$1" ]; then
    day=$1
else
    read -p "Dime el dia: " day
fi

if $(date -d "$day" > /dev/null 2>&1); then
    find ~ -newermt "$day" 2>/dev/null
else
    echo "El dia es invalido"
fi


#!/bin/bash
# Ejercicio 13: Pida un día y muestre los ficheros con fecha superior a ese día.

if [ -n "$1" ]; then
    day=$1
else
    read -p "Dime el dia: " day
fi

# 1. Si el usuario mete solo un número (del 1 al 31), le añadimos el Año-Mes actual
if [[ "$day" =~ ^[0-9]{1,2}$ ]]; then
    # Construimos la fecha como: 2026-01-26
    day_format="$(date +%Y-%m)-$day"
else
    # Si ha metido una fecha completa, la dejamos tal cual
    day_format="$day"
fi

# 2. Ahora validamos la fecha construida
if date -d "$day_format" > /dev/null 2>&1; then
    echo "Buscando archivos modificados después de: $(date -d "$day_format" '+%d de %B de %Y')"
    echo "---------------------------------------------------"
    find ~ -type f -newermt "$day_format" 2>/dev/null
else
    echo "Error: '$day' no es un día o fecha válida."
fi