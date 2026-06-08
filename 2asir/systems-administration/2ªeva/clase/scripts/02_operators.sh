#!/bin/bash

# --- Operadores Aritméticos ---
# Para realizar operaciones matemáticas, necesitamos usar $((...)) o `expr`

num1=10
num2=3

# Suma (+)
suma=$((num1 + num2))
echo "Suma: $num1 + $num2 = $suma"

# Resta (-)
resta=$((num1 - num2))
echo "Resta: $num1 - $num2 = $resta"

# Multiplicación (*)
multi=$((num1 * num2))
echo "Multiplicación: $num1 * $num2 = $multi"

# División (/) - Nota: Bash solo maneja enteros, no decimales
div=$((num1 / num2))
echo "División (entera): $num1 / $num2 = $div"

# Módulo (%) - Resto de la división
mod=$((num1 % num2))
echo "Módulo: $num1 % $num2 = $mod"

# Incremento y Decremento
# Al igual que en C/Java/Python
x=5
((x++)) # Incrementa en 1
echo "x incrementado: $x"

((x+=5)) # Suma 5 a x
echo "x sumado 5: $x"

# --- Operadores de comparación (para números) ---
# -eq : Igual a (equal)
# -ne : No igual a (not equal)
# -gt : Mayor que (greater than)
# -lt : Menor que (less than)
# -ge : Mayor o igual que (greater or equal)
# -le : Menor o igual que (less or equal)

if [ $num1 -gt $num2 ]; then
    echo "$num1 es mayor que $num2"
fi

# --- NIVEL 2: Operaciones Avanzadas ---

# 1. Decimales con 'bc' (Calculadora de precisión)
# Como Bash solo usa enteros, para decimales usamos una tubería a bc
resultado_decimal=$(echo "scale=2; 10 / 3" | bc)
echo "División con 2 decimales: 10 / 3 = $resultado_decimal"

# 2. Comparaciones dentro de (( ))
# Es más intuitivo para programadores (usa >, <, ==, !=, >=, <=)
if (( num1 > num2 )); then
    echo "Usando (( )): $num1 es mayor que $num2"
fi

# 3. Operadores bit a bit (Bitwise)
# AND (&), OR (|), XOR (^), Desplazamiento (<<, >>)
a=2 # 10 en binario
b=1 # 01 en binario
echo "Bitwise AND (2 & 1): $((a & b))" # Resultado: 0
echo "Bitwise OR (2 | 1): $((a | b))"  # Resultado: 3

