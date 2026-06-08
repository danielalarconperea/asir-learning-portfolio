#!/bin/bash

# --- Variables ---
# No se ponen espacios alrededor del signo igual

# Definir variables
nombre="Juan"
edad=25
curso="2ASIR"

# Acceder a las variables con $
echo "Me llamo $nombre y tengo $edad años."
echo "Estoy en el curso $curso"

# Otra forma de acceder a las variables es con ${}
# Esto es útil si quieres pegar texto a la variable
echo "Hola, ${nombre}ito"

# Variables de solo lectura (constantes)
readonly PI=3.14159
echo "El valor de PI es $PI"
# PI=3.14  # Esto daría un error

# Borrar una variable (unset)
variable_temporal="Hola"
echo "Variable temporal: $variable_temporal"
unset variable_temporal
# echo "Variable temporal tras unset: $variable_temporal" # No imprime nada

# --- Variables de Entorno Comunes ---
echo "Usuario actual: $USER"
echo "Directorio home: $HOME"
echo "Shell actual: $SHELL"
echo "Directorio de trabajo actual (PWD): $PWD"

# --- NIVEL 2: Expansión de Parámetros ---

# 1. Valores por defecto
# Si 'mi_var' está vacía o no existe, usa "ValorPredeterminado"
echo "Ciudad: ${ciudad:-Madrid}" 

# 2. Longitud de una cadena
mensaje="Hola Mundo"
echo "El mensaje '$mensaje' tiene ${#mensaje} caracteres."

# 3. Recorte de cadenas (Slicing)
# ${var:inicio:longitud}
echo "Primeras 4 letras: ${mensaje:0:4}"
echo "Desde la posición 5: ${mensaje:5}"

# 4. Reemplazo de texto
# ${var/buscar/reemplazar}
echo "Cambiando Mundo por Bash: ${mensaje/Mundo/Bash}"

# 5. Transformación a Mayúsculas/Minúsculas
echo "Todo a MAYÚSCULAS: ${mensaje^^}"
echo "Todo a minúsculas: ${mensaje,,}"

