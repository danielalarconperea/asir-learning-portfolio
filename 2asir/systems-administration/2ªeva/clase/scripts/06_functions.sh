#!/bin/bash

# --- Definición de Funciones ---

# Forma 1 (más común)
mi_funcion() {
    echo "¡Hola desde mi_funcion!"
}

# Forma 2 (usando la palabra clave function)
function otra_funcion {
    echo "¡Hola desde otra_funcion!"
}

# --- Llamar a las funciones ---
mi_funcion
otra_funcion

# --- Argumentos en Funciones ---
# Las funciones acceden a los argumentos con $1, $2, etc., igual que los scripts
saludar() {
    local nombre=$1 # 'local' hace que la variable solo exista dentro de la función
    echo "Hola, $nombre"
}

saludar "Carlos"
saludar "Ana"

# --- Retorno de Valores ---
# Bash no tiene 'return' como otros lenguajes para devolver datos.
# 'return' en bash solo devuelve un código de estado (0-255).
# 0 significa éxito, cualquier otro número es error.

comprobar_par() {
    if (( $1 % 2 == 0 )); then
        return 0 # Éxito/True
    else
        return 1 # Fallo/False
    fi
}

echo "Comprobando si 4 es par..."
if comprobar_par 4; then
    echo "Sí, es par."
else
    echo "No, es impar."
fi

# Para "devolver" datos reales, usamos echo y captura de comando
obtener_fecha() {
    date "+%Y-%m-%d"
}

fecha_hoy=$(obtener_fecha)
echo "La fecha de hoy es: $fecha_hoy"

# --- NIVEL 2: Funciones Avanzadas ---

# 1. Variables Globales vs Locales
var_global="Soy global"

modificar_variables() {
    var_global="He sido modificada globalmente"
    local var_local="Solo existo aquí dentro"
    echo "Dentro: $var_local"
}

echo "Antes: $var_global"
modificar_variables
echo "Después: $var_global"
# echo "Fuera: $var_local" # Esto no imprimiría nada

# 2. Recursividad (Una función que se llama a sí misma)
# Ejemplo: Factorial de un número
factorial() {
    if [ $1 -le 1 ]; then
        echo 1
    else
        local anterior=$(factorial $(( $1 - 1 )))
        echo $(( $1 * anterior ))
    fi
}

echo "El factorial de 5 es: $(factorial 5)"

