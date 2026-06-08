#!/bin/bash

# --- Leer Input del Usuario ---

echo -n "Introduce tu nombre: "
# 'read' guarda lo que escribe el usuario en la variable
read nombre_usuario
echo "Hola, $nombre_usuario"

# Leer con prompt (-p) en la misma línea
read -p "Introduce tu edad: " edad
echo "Tienes $edad años"

# Leer contraseña sin mostrar caracteres (-s)
read -s -p "Introduce una contraseña secreta: " pass
echo # Salto de línea manual porque read -s no lo hace
echo "Contraseña guardada (es: $pass)"

# Leer múltiples variables
echo "Introduce dos números separados por espacio:"
read n1 n2
echo "Número 1: $n1, Número 2: $n2"

# --- Redirección de Output (Básico) ---
# >  : Guarda la salida en un archivo (sobrescribe)
# >> : Añade la salida al final de un archivo (append)

archivo="salida_demo.txt"
echo "Esta es la primera línea" > $archivo
echo "Esta es la segunda línea (añadida)" >> $archivo

echo "Contenido de $archivo:"
cat $archivo

# Limpieza
rm $archivo

# --- NIVEL 2: Entrada/Salida Avanzada ---

# 1. Tuberías (Pipes |)
# Pasa la salida de un comando como entrada de otro
# Ejemplo: listar archivos y contar cuántos hay
echo "Contando archivos en este directorio:"
ls | wc -l

# 2. Here-Documents (<<)
# Útil para escribir bloques grandes de texto en archivos o comandos
cat << EOF > configuracion.txt
USUARIO=$USER
FECHA=$(date)
ESTADO=Activo
EOF
echo "Se ha generado 'configuracion.txt' usando un Here-Doc."
cat configuracion.txt
rm configuracion.txt

# 3. Redirección de Errores
# 2> redirige solo los errores
# &> redirige todo (salida estándar y errores)
ls archivo_que_no_existe.txt 2> errores.log
echo "Se ha guardado el rastro del error en errores.log"
rm errores.log

