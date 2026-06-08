#!/bin/bash

# --- Bucle FOR ---

# 1. Iterar sobre una lista de elementos explícita
echo "--- Lista Explícita ---"
for color in rojo verde azul; do
    echo "Color: $color"
done

# 2. Iterar sobre un rango (tipo secuencia)
echo -e "\n--- Rango {1..5} ---"
for i in {1..5}; do
    echo "Contando: $i"
done

# 3. Iterar sobre un rango con saltos {inicio..fin..salto}
echo -e "\n--- Rango con saltos {0..10..2} ---"
for i in {0..10..2}; do
    echo "Par: $i"
done

# 4. Estilo C/Java (útil para índices)
echo -e "\n--- Estilo C ((i=0; i<3; i++)) ---"
for ((i=0; i<3; i++)); do
    echo "Índice C: $i"
done

# --- Bucle WHILE ---
# Se ejecuta mientras la condición sea verdadera
echo -e "\n--- Bucle WHILE ---"
contador=1
while [ $contador -le 3 ]; do
    echo "While: $contador"
    ((contador++))
done

# --- Bucle UNTIL ---
# Se ejecuta hasta que la condición sea verdadera (inverso de while)
echo -e "\n--- Bucle UNTIL ---"
contador=1
until [ $contador -gt 3 ]; do
    echo "Until: $contador"
    ((contador++))
done

# --- Control de Bucles ---
# break: Sali del bucle inmediatamente
# continue: Salta a la siguiente iteración

echo -e "\n--- Break y Continue ---"
for i in {1..5}; do
    if [ $i -eq 2 ]; then
        continue # Salta el 2
    fi
    if [ $i -eq 4 ]; then
        break # Termina en el 4 (no imprime 4, ni llega a 5)
    fi
    echo "Número: $i"
done

# --- NIVEL 2: Bucles Avanzados ---

# 1. Iterar sobre archivos (Globbing)
echo -e "\n--- Listando archivos .sh ---"
for archivo in *.sh; do
    echo "Encontrado script: $archivo"
done

# 2. Leer un archivo línea a línea
# Creamos un archivo temporal para el ejemplo
echo -e "Línea 1\nLínea 2\nLínea 3" > temp.txt

echo -e "\n--- Leyendo archivo temp.txt ---"
while IFS= read -r linea; do
    echo "Contenido: $linea"
done < temp.txt

rm temp.txt

# 3. Bucles Infinitos (Controlados)
echo -e "\n--- Bucle Infinito (Ejemplo concepto) ---"
# while true; do
#    echo "Presiona Ctrl+C para parar"
#    sleep 1
# done

