#!/bin/bash

# ==============================================================================
# 💿 TEMA: GESTIÓN DE DISCOS Y PARTICIONES CON FDISK
# ==============================================================================
# Objetivo: Aprender a crear, eliminar y gestionar particiones MBR en Linux.
#           Comprender el ciclo de vida del almacenamiento: Particionar -> Formatear -> Montar.
#
# NOTA: Estos apuntes están optimizados para leerse en VSCode.

### 1. CONCEPTOS PREVIOS
# ------------------------------------------------------------------------------
# FDISK es una utilidad interactiva basada en menús para manipular tablas de particiones.
# Soporta principalmente el esquema MBR (Master Boot Record).

# > Dispositivos:
#   - /dev/sda, /dev/sdb... (Discos SATA/SCSI físicos o virtuales)
#   - /dev/nvme0n1...       (Discos SSD NVMe modernos)
#
# > Esquemas de Particionamiento:
#   - MBR (fdisk): Estándar antiguo. Máx 4 particiones primarias. Máx 2TB.
#   - GPT (gdisk): Estándar moderno (UEFI). Ilimitadas particiones. Zettabytes.

# ------------------------------------------------------------------------------
# LISTAR DISCOS Y PARTICIONES
# ------------------------------------------------------------------------------
# El flag -l (list) muestra todas las particiones detectadas en el sistema.

sudo fdisk -l

### 2. MODO INTERACTIVO
# ------------------------------------------------------------------------------
# Para modificar un disco, entramos en su menú interactivo. NADA SE APLICA
# INMEDIATAMENTE; los cambios se guardan en memoria hasta confirmar con 'w'.

# Sintaxis:
# sudo fdisk <ruta_al_disco>
sudo fdisk /dev/sdb

### 3. CHEAT SHEET DE COMANDOS (DENTRO DE FDISK)
# ------------------------------------------------------------------------------
# Una vez dentro, usa estas letras:
#
# m  -> Muestra el menú de ayuda.
# p  -> (Print) Muestra la tabla de particiones actual. Úsalo a menudo.
# n  -> (New) Crea una nueva partición. Te pedirá:
#       1. Tipo (p=primaria, e=extendida).
#       2. Número (1-4).
#       3. Primer sector (Enter para default).
#       4. Tamaño (+1G, +500M...).
# d  -> (Delete) Borra una partición.
# t  -> (Type) Cambia el ID del sistema de archivos (ej. de Linux a Swap o NTFS).
#       - 83: Linux (Default)
#       - 82: Linux Swap
#       - b:  W95 FAT32
# w  -> (Write) Escribe cambios al disco y SALE. (Punto de no retorno).
# q  -> (Quit) Sale SIN guardar cambios.

### 4. FLUJO COMPLETO: DE DISCO A CARPETA
# ------------------------------------------------------------------------------
# Paso 1: Particionar (como vimos arriba con fdisk)
# ------------------------------------------------------------------------------

# Paso 2: Formatear (Crear sistema de archivos)
# ------------------------------------------------------------------------------
# Una vez creada la partición (ej. /dev/sdb1), hay que darle formato.
# No formateamos el disco (/dev/sdb), sino la partición (/dev/sdb1).

sudo mkfs.ext4 /dev/sdb1        # Estándar Linux
sudo mkfs.xfs /dev/sdb1         # Estándar RHEL/CentOS
sudo mkfs.fat -F32 /dev/sdb1    # Compatible Windows/USB
sudo mkswap /dev/sdb1           # Para memoria de intercambio (Swap)

# Paso 3: Montar (Hacerla accesible)
# ------------------------------------------------------------------------------
# Creamos un punto de montaje (carpeta vacía)
sudo mkdir -p /mnt/datos

# Montaje temporal (se pierde al reiniciar)
sudo mount /dev/sdb1 /mnt/datos

# Montaje permanente (editar /etc/fstab)
# Añadir la línea:
# /dev/sdb1    /mnt/datos    ext4    defaults    0    2

# Para Swap:
# sudo swapon /dev/sdb1

### 5. EJERCICIO PRÁCTICO
# ------------------------------------------------------------------------------
# 1. Añade un disco virtual de 1GB a tu máquina virtual.
# 2. Usa 'fdisk' para crear dos particiones de 300MB.
# 3. Cambia el tipo de la segunda a 'Swap' (código 82).
# 4. Formatea la primera en ext4 y móntala en /media/datos.
# 5. Activa la swap con 'swapon'.
