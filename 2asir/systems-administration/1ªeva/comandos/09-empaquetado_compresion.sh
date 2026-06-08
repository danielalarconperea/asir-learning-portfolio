#!/bin/bash

# ==============================================================================
# 📝 EMPAQUETADO Y COMPRESIÓN DE ARCHIVOS (TAR, GZIP, BZIP2, XZ, ZIP)
# ==============================================================================

### 1. EL COMANDO TAR (EMPAQUETAR)
# tar no comprime por defecto, solo junta archivos en uno solo (.tar).

# -c: Create (Crear) | -v: Verbose (Ver detalles) | -f: File (Archivo destino)
tar -cvf backup_udev.tar /etc/udev

# -t: List (Listar contenido sin extraer)
tar -tvf backup_udev.tar

# -x: Extract (Extraer el contenido)
tar -xvf backup_udev.tar

# -r: Append (Añadir archivos a un tar ya existente)
tar -rvf backup_udev.tar /etc/hosts

### 2. COMPRESIÓN CON TAR (GZIP, BZIP2, XZ)
# Podemos comprimir directamente al empaquetar usando flags específicas.

# -z: GZIP (.tar.gz) -> El más rápido y común.
tar -zcvf backup.tar.gz /etc/udev

# -j: BZIP2 (.tar.bz2) -> Mejor compresión que gzip, pero más lento.
tar -jcvf backup.tar.bz2 /etc/udev

# -J: XZ (.tar.xz) -> Máxima compresión, el más lento de todos.
tar -Jcvf backup.tar.xz /etc/udev

### 3. COMPRESIÓN INDIVIDUAL DE ARCHIVOS
# Estos comandos actúan sobre un solo archivo y reemplazan el original.

# --- GZIP ---
gzip archivo.txt       # Crea archivo.txt.gz
gunzip archivo.txt.gz  # Descomprime a archivo.txt

# --- BZIP2 ---
bzip2 archivo.txt      # Crea archivo.txt.bz2
bunzip2 archivo.txt.bz2 # Descomprime

# --- XZ ---
xz archivo.txt         # Crea archivo.txt.xz
unxz archivo.txt.xz    # Descomprime

### 4. HERRAMIENTA ZIP (COMPATIBLE CON WINDOWS)
# zip sí comprime por defecto y no borra el archivo original.

# Comprimir archivos
zip backup.zip archivo1 archivo2

# Comprimir un directorio entero (-r: recursivo)
zip -r backup_dir.zip /ruta/al/directorio

# Listar contenido de un zip
unzip -l backup.zip

# Descomprimir
unzip backup.zip
