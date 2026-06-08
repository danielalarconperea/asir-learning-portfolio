#!/bin/bash

# ==============================================================================
# 📝 GUÍA DEFINITIVA DE AWK: PROCESAMIENTO DE TEXTO Y COLUMNAS
# ==============================================================================
# Objetivo: Filtrar, extraer y manipular datos estructurados en filas y columnas.

### 1. SINTAXIS BÁSICA
# Formato: awk 'condición { acción }' archivo
# Si no se pone condición, se aplica a todas las líneas.
# Si no se pone acción, por defecto imprime la línea entera ({print $0}).

# Ejemplo: Imprimir la primera columna de un archivo
awk '{print $1}' lista.txt

### 2. VARIABLES DE POSICIÓN ($0, $1, $2...)
# AWK divide cada línea en campos (columnas) usando espacios o tabuladores por defecto.
# $0 -> Representa la LÍNEA COMPLETA.
# $1 -> Primera columna.
# $2 -> Segunda columna... y así sucesivamente.

# Ejemplo: Imprimir usuario y su home desde una salida de comando
ls -l /home | awk '{print "Usuario:", $9, "-> Carpeta:", $3}'

### 3. EL SEPARADOR DE CAMPOS (-F)
# Vital para archivos como /etc/passwd o archivos CSV.
# Por defecto es el espacio, pero con -F lo cambiamos.

# Ejemplo: Ver solo los nombres de usuario del sistema (separador ":")
awk -F: '{print $1}' /etc/passwd

# Ejemplo: Varias columnas con formato
awk -F: '{print "User:", $1, "\tUID:", $3}' /etc/passwd

### 4. VARIABLES INTERNAS (NF, NR, FS)
# NF (Number of Fields): Número de columnas que tiene la línea actual.
# NR (Number of Records): Número de línea actual (empieza en 1).
# FS (Field Separator): El separador actual (se puede ver/cambiar dentro).

# Ejemplo: Imprimir solo líneas que tengan más de 3 columnas
awk 'NF > 3' datos.txt

# Ejemplo: Imprimir el número de línea antes de cada nombre
awk -F: '{print NR, $1}' /etc/passwd

# Ejemplo: Imprimir la ÚLTIMA columna de cada línea (sea cual sea)
awk '{print $NF}' log.txt

### 5. FILTRADO POR PATRONES (BUSCAR COSAS)
# Podemos poner una condición antes de las llaves.

# A) Buscar una palabra exacta:
awk '/root/ {print $0}' /etc/passwd

# B) Comparar una columna específica:
awk -F: '$3 < 100 {print $1}' /etc/passwd    # Usuarios del sistema (UID < 100)

# C) Uso de conectores lógicos (&&, ||, !):
awk -F: '$1 == "root" || $3 > 1000 {print $1}' /etc/passwd

### 6. BLOQUES BEGIN Y END
# BEGIN { ... } -> Se ejecuta UNA VEZ ANTES de leer ninguna línea.
# END   { ... } -> Se ejecuta UNA VEZ DESPUÉS de leer todas las líneas.

# Ejemplo: Crear un informe con cabecera y pie de página
awk -F: 'BEGIN {print "--- LISTA DE USUARIOS ---"} 
         {print $1} 
         END {print "--- TOTAL LINEAS: " NR " ---"}' /etc/passwd

### 7. OPERACIONES MATEMÁTICAS
# AWK puede sumar, contar y promediar valores de columnas.

# Ejemplo: Sumar el tamaño de todos los archivos en el directorio actual
ls -l | awk '{sum += $5} END {print "Total bytes:", sum}'

### 8. EJEMPLO AVANZADO: FILTRAR LOGS
# Imagina un log de acceso: IP Fecha Error
# Queremos contar cuántos errores "404" hay de una IP específica:
# awk '$1 == "192.168.1.1" && $3 == "404" {count++} END {print count}' access.log
