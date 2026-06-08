#!/bin/bash

# --- Operadores de Test de Archivos ---
# -e : Existe (cualquier tipo)
# -f : Es un archivo regular (file)
# -d : Es un directorio (directory)
# -r : Tiene permisos de lectura (readable)
# -w : Tiene permisos de escritura (writable)
# -x : Tiene permisos de ejecución (executable)
# -s : El archivo no está vacío (size > 0)

archivo_test="00_helloworld.sh"
directorio_test="."

echo "Analizando '$archivo_test'..."

if [ -e "$archivo_test" ]; then
    echo "- El archivo existe."
    
    if [ -f "$archivo_test" ]; then
        echo "- Es un archivo regular."
    fi

    if [ -r "$archivo_test" ]; then
        echo "- Se puede leer."
    fi

    if [ -w "$archivo_test" ]; then
        echo "- Se puede escribir."
    fi

    if [ -x "$archivo_test" ]; then
        echo "- Es ejecutable."
    else
        echo "- NO es ejecutable."
    fi
else
    echo "El archivo no existe."
fi

echo "---"
echo "Analizando directorio actual '$directorio_test'..."

if [ -d "$directorio_test" ]; then
    echo "- Es un directorio."
else
    echo "- No es un directorio."
fi

# --- NIVEL 2: Operaciones Avanzadas con Archivos ---

# 1. Comparar fechas de archivos
# -nt : Más nuevo que (newer than)
# -ot : Más viejo que (older than)

touch archivo1.txt
sleep 1
touch archivo2.txt

if [ archivo2.txt -nt archivo1.txt ]; then
    echo "archivo2.txt es más reciente que archivo1.txt"
fi

rm archivo1.txt archivo2.txt

# 2. Creación de archivos temporales seguros
# mktemp crea un archivo con un nombre aleatorio único
temp_file=$(mktemp /tmp/script_demo.XXXXXX)
echo "He creado un archivo temporal en: $temp_file"
echo "Datos sensibles" > "$temp_file"
rm "$temp_file"

# 3. Comprobar si un archivo está vacío
if [ ! -s "archivo_vacio.txt" ]; then
    echo "El archivo 'archivo_vacio.txt' no existe o está vacío."
fi


# -z : El string está vacío
# -n : El string no está vacío

