#!/bin/bash

# --- Condicionales IF ---
# IMPORTANTE: Los espacios dentro de [ ... ] son OBLIGATORIOS
# if [ condición ]; then
#     ...
# fi

read -p "Introduce un número: " num

if [ $num -gt 10 ]; then
    echo "El número es mayor que 10"
elif [ $num -eq 10 ]; then
    echo "El número es exactamente 10"
else
    echo "El número es menor que 10"
fi

# --- Comparaciones de Cadenas ---
# =  : Igual
# != : Diferente
# -z : Cadena vacía
# -n : Cadena no vacía

read -p "Confirma escribiendo 'si': " respuesta
if [ "$respuesta" = "si" ]; then
    echo "Confirmado."
else
    echo "Cancelado."
fi

# --- Operadores Lógicos ---
# && : AND (y también)
# || : OR (o bien)

edad=20
tiene_carnet="si"

if [ $edad -ge 18 ] && [ "$tiene_carnet" = "si" ]; then
    echo "Puedes conducir."
else
    echo "No puedes conducir."
fi

# --- Condicional CASE ---
# Útil para muchas opciones

read -p "Elige una opción (A, B, C): " opcion
case $opcion in
    A|a) # Acepta A mayúscula o minúscula
        echo "Elegiste la Opción A"
        ;;
    B|b)
        echo "Elegiste la Opción B"
        ;;
    C|c)
        echo "Elegiste la Opción C"
        ;;
    *)
        echo "Opción no válida"
        ;;
esac

# --- NIVEL 2: Condicionales Avanzados ---

# 1. El uso de [[ ... ]] (Recomendado en Bash moderno)
# Es más potente que [ ... ], no requiere comillas para variables vacías 
# y permite usar && y || dentro directamente.
if [[ $num -gt 5 && $num -lt 15 ]]; then
    echo "El número está entre 5 y 15 (usando [[ ]])"
fi

# 2. Pattern Matching (Comprobación de patrones)
# El operador == dentro de [[ ]] permite usar comodines (*)
archivo="documento.pdf"
if [[ $archivo == *.pdf ]]; then
    echo "Es un archivo PDF"
fi

# 3. Expresiones Regulares (Regex) con =~
# Ejemplo: Comprobar si una variable es un correo electrónico simple
email="test@ejemplo.com"
if [[ $email =~ ^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$ ]]; then
    echo "El formato de email es válido."
else
    echo "Formato de email inválido."
fi

