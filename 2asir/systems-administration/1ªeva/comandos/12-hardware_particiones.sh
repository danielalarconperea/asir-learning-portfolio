#!/bin/bash

# ==============================================================================
# 📝 INFORMACIÓN DE HARDWARE Y PARTICIONAMIENTO
# ==============================================================================

### 1. CONSULTA DE HARDWARE
# Ver arquitectura del procesador (x86_64, arm, etc.)
arch

# Información detallada de la CPU
lscpu

# Ver memoria RAM (en Megabytes o Gigabytes)
free -m
free -g

# Listar dispositivos conectados por bus
lspci   # Dispositivos PCI (gráficas, tarjetas de red)
lsusb   # Dispositivos USB conectados

### 2. HERRAMIENTAS DE PARTICIONAMIENTO
# Estas herramientas permiten crear, borrar y modificar particiones.

# --- Modo Texto (Consola) ---
# fdisk   -> El clásico para discos con MBR (aunque ya soporta GPT).
# gdisk   -> Específico para discos GPT.
# parted  -> Potente, admite scripts y maneja particiones de gran tamaño.

# --- Modo Interactivo (Menús) ---
# cfdisk  -> Versión visual de fdisk (muy intuitivo).
# cgdisk  -> Versión visual de gdisk para GPT.

### 3. COMANDOS ÚTILES DE DISCO
# Listar todos los discos y sus particiones
sudo fdisk -l

# Listar dispositivos de almacenamiento específicos (/dev/sd*)
ls /dev/sd*

# Ver información detallada de un disco concreto
sudo fdisk -l /dev/sda
