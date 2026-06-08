#!/bin/bash
# Ejercicio 6 Avanzado: Leer hasta "fin" y mostrar todo.

TEXTOS=""

echo "Introduce textos (escribe 'fin' para terminar):"
while true; do
    read -p "> " LINEA
    if [ "$LINEA" == "fin" ]; then
        break
    fi
    TEXTOS="$TEXTOS$LINEA\n"
done

echo -e "\nTextos introducidos:"
echo -e "$TEXTOS"
