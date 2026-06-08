#!/bin/bash

# --- Definir Arrays ---
# Los arrays en bash son unidireccionales y se indexan desde 0

frutas=("Manzana" "Banana" "Naranja" "Uva")

# --- Acceder a Elementos ---
echo "Primera fruta: ${frutas[0]}"
echo "Segunda fruta: ${frutas[1]}"

# --- Acceder a Todos los Elementos ---
echo "Todas las frutas (@): ${frutas[@]}"
echo "Todas las frutas (*): ${frutas[*]}"

# --- Longitud del Array ---
echo "Número total de frutas: ${#frutas[@]}"

# --- Iterar sobre un Array ---
echo "--- Lista de Frutas ---"
for fruta in "${frutas[@]}"; do
    echo "- $fruta"
done

# --- Añadir Elementos ---
frutas+=("Kiwi")
echo "Ahora con Kiwi: ${frutas[@]}"

# --- Eliminar Elementos ---
unset frutas[1] # Elimina Banana (índice 1)
echo "Sin Banana: ${frutas[@]}"
# Nota: Los índices no se reordenan automáticamente
echo "Índice 1 tras borrar: '${frutas[1]}'" # Estará vacío

# --- NIVEL 2: Arrays Asociativos (Diccionarios) ---
# Requieren el uso de 'declare -A'

declare -A usuario

usuario["nombre"]="Pepe"
usuario["edad"]=30
usuario["puesto"]="Administrador"

echo "Nombre del usuario: ${usuario["nombre"]}"

# Ver todas las claves
echo "Claves disponibles: ${!usuario[@]}"

# Iterar sobre claves y valores
echo "--- Datos del Usuario ---"
for clave in "${!usuario[@]}"; do
    echo "$clave: ${usuario[$clave]}"
done

