#!/bin/bash

# ==============================================================================
# 📝 MONITORIZACIÓN DEL SISTEMA Y GESTIÓN DE PROCESOS
# ==============================================================================

### 1. ESTADO DEL SISTEMA
# Tiempo que lleva encendido y carga media
uptime

# Ver carga media desde el sistema de archivos /proc
cat /proc/loadavg

# Uso de memoria RAM
free -m
free -s 5  # Actualizar cada 5 segundos

### 2. GESTIÓN DE PROCESOS (PS, TOP, HTOP)
# ps: Captura estática de los procesos actuales.
ps aux          # Todos los procesos de todos los usuarios
ps -ef          # Formato estándar de UNIX
ps --forest     # Muestra los procesos en forma de árbol (padres e hijos)
ps -u usuario   # Procesos de un usuario específico

# top: Monitor interactivo en tiempo real.
top             # Pulsar 'q' para salir, 'k' para matar un proceso

# pstree: Árbol de procesos visual
pstree

### 3. CONTROL DE TRABAJOS (JOBS)
# Comandos lanzados desde la terminal actual.

# Lanzar comando en segundo plano (&)
sleep 100 &

# Listar trabajos de la terminal
jobs

# Traer trabajo al primer plano (Foreground)
fg %1

# Mandar trabajo al segundo plano (Background)
bg %1

# Matar procesos
kill -9 1234      # Por PID (identificador de proceso)
kill %1           # Por número de job de la terminal

### 4. LOGS Y MENSAJES DEL SISTEMA
# Ver mensajes del Kernel (drivers, hardware)
dmesg | grep -i usb

# Ver logs gestionados por systemd
journalctl -n 20   # Los últimos 20 mensajes

# Ver últimos intentos de acceso fallidos
sudo lastb

### 5. EL DIRECTORIO /PROC
# Es un sistema de archivos virtual que contiene info del kernel y procesos.
ls /proc        # Cada número es un directorio de un proceso activo
cat /proc/meminfo # Información detallada de la memoria
