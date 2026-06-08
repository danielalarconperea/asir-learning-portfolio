#!/bin/bash

# --- Parámetros Posicionales (Argumentos del Script) ---
# Ejecuta este script pasando argumentos, por ejemplo:
# ./08_parameters.sh hola mundo 123

echo "Nombre del script (\$0): $0"
echo "Primer argumento (\$1): $1"
echo "Segundo argumento (\$2): $2"

# Si hay más de 9 argumentos, usa llaves: ${10}, ${11}...

# --- Variables Especiales ---
echo "Número total de argumentos (\$#): $#"
echo "Todos los argumentos como una lista (\$@): $@"
echo "PID del script actual (\$$): $$"
echo "Código de salida del último comando ejecutado (\$?): $?"

# $? es el código de salida del último comando ejecutado
# 0: éxito
# 1: error
# 2: uso incorrecto
# 126: no es ejecutable
# 127: no existe
# 128: error de sintaxis
# 130: interrumpido por Ctrl+C
# 131: interrumpido por Ctrl+\


# --- Ejemplo de Uso ---
if [ $# -lt 1 ]; then
    echo "¡Advertencia! No pasaste ningún argumento."
    echo "Uso: $0 [argumento1] [argumento2] ..."
fi

# Iterar sobre todos los argumentos
echo "--- Iterando argumentos ---"
for arg in "$@"; do
    echo "Arg: $arg"
done

# --- NIVEL 2: Procesamiento Dinámico ---

# 1. El comando 'shift'
# 'shift' desplaza los argumentos a la izquierda.
# El valor de $2 pasa a $1, el de $3 a $2, etc.

echo -e "\n--- Usando shift para procesar argumentos ---"
while [ $# -gt 0 ]; do
    echo "Procesando: $1 (Quedan $# argumentos)"
    shift
done

# Nota: Después de los 'shift', $1, $2, etc. están vacíos.

