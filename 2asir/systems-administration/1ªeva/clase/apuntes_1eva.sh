#!/bin/bash

# ==============================================================================
# 📚 APUNTES GENERALES - 1ª EVALUACIÓN: ADMINISTRACIÓN DE SISTEMAS
# ==============================================================================
# Objetivo: Guía rápida y ejemplos prácticos de los comandos básicos de terminal.

### --- PARTE 1: VISUALIZACIÓN Y MANIPULACIÓN BÁSICA ---

# 📄 CAT, HEAD, TAIL (Ver contenido)
cat -n archivo.txt              # Ver todo el archivo numerado
head -n 5 archivo.txt           # Ver las primeras 5 líneas
tail -n 20 archivo.txt          # Ver las últimas 20 líneas
tail -f access.log              # Monitorizar un log en tiempo real

# 🗣️ ECHO y TEE (Salida de datos)
echo -e "Línea 1\nLínea 2"      # Imprimir con saltos de línea (\n)
ls | tee log.txt                # Ver el resultado y guardarlo en un archivo a la vez

# ⏱️ TOUCH y RM (Gestión de archivos)
touch nuevo.txt                 # Crear archivo vacío o actualizar fecha
rm -ri carpeta/                 # Borrar directorio preguntando antes de cada archivo
rm -rf /                        # ⚠️ NUNCA USAR (Borra todo el sistema sin preguntar)

### --- PARTE 2: FILTRADO Y PROCESAMIENTO (EL CORAZÓN DE LINUX) ---

# 🔍 GREP (Búsqueda de patrones)
grep -i "error" syslog          # Buscar ignorando mayúsculas/minúsculas
grep -v "^#" config.conf        # Ver archivo ignorando líneas de comentario (#)
grep -E "word1|word2" file      # Buscar una palabra O la otra (Regex extendido)
grep -r "texto" /etc/           # Buscar texto en todos los archivos de una carpeta

# ✂️ CUT y AWK (Columnas)
cut -d":" -f1 /etc/passwd       # Ver solo la primera columna (usuarios)
ls -l | cut -c1-10              # Ver solo los permisos (primeros 10 caracteres)
awk -F: '{print $1, $6}' /etc/passwd # Extraer Usuario y su Home

# 🔄 TR y SED (Transformación)
echo "hola" | tr 'a-z' 'A-Z'    # Convertir a MAYÚSCULAS
tr -d ' ' < archivo.txt         # Borrar todos los espacios
sed 's/antiguo/nuevo/g' file    # Reemplazar texto en la salida
sed -i 's/A/B/g' archivo.txt    # Reemplazar y GUARDAR el cambio en el archivo

### --- PARTE 3: ORGANIZACIÓN Y ESTADÍSTICAS ---

# 📊 SORT y UNIQ (Orden y duplicados)
sort -n lista.txt               # Ordenar numéricamente (1, 2, 10...)
sort -t: -k3n /etc/passwd       # Ordenar usuarios por su UID (3ª columna)
sort archivo.txt | uniq -c      # Contar cuántas veces se repite cada línea

# 🔢 WC (Contadores)
wc -l archivo.txt               # Contar cuántas líneas tiene
ls | wc -l                      # Contar cuántos archivos hay en la carpeta

### --- PARTE 4: HERRAMIENTAS AVANZADAS ---

# 👷 XARGS (El pegamento)
# Convierte la salida de un comando en argumentos para otro.
cat lista_borrar.txt | xargs rm # Borrar todos los archivos listados en el txt

# 🖇️ PASTE y JOIN (Unir archivos)
paste -d";" lista1.txt lista2.txt # Unir archivos horizontalmente (CSV)
join -t: file1.txt file2.txt      # Unir por un campo común (como en SQL)

# 🔪 SPLIT (Dividir archivos grandes)
split -b 100M video.iso parte_  # Dividir un archivo en trozos de 100MB

### --- PARTE 5: INFORMACIÓN DEL SISTEMA ---

# 🗓️ DATE y UNAME
date +"%d-%m-%Y"                # Fecha en formato día-mes-año
uname -a                        # Información completa del Kernel y Sistema
history | grep "ssh"            # Buscar en el historial de comandos usados



sudo ls -lh /var/log | sort -k5hr | head -n 10
sudo ls -l /var/log | sort -k5nr | head -n 10
# con awk seria: 
