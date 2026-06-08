#!/bin/bash

# ==============================================================================
# 📝 PLANIFICACIÓN DE TAREAS PERIÓDICAS: CRON & ANACRON
# ==============================================================================
# Objetivo: Ejecutar comandos de forma automática y repetitiva a intervalos regulares.

### 1. GESTIÓN DEL SERVICIO (CROND)
# Cron es un demonio que corre permanentemente en segundo plano.

# Comandos de gestión (requieren sudo):
sudo systemctl status cron    # Verificar estado
sudo systemctl start cron     # Iniciar
sudo systemctl stop cron      # Detener
sudo systemctl restart cron   # Reiniciar (necesario si se cambia /etc/crontab)

### 2. CRONTAB DE USUARIO
# Cada usuario tiene su propio archivo de tareas en /var/spool/cron/crontabs/

crontab -e    # Editar: Abre el editor para añadir/modificar tareas.
crontab -l    # Listar: Muestra las tareas programadas actualmente.
crontab -r    # Eliminar: Borra TODO el crontab del usuario.

# Gestión administrativa (solo root):
sudo crontab -u usuario -l    # Listar tareas de otro usuario.

### 3. SINTAXIS DEL CRONTAB
# Formato de cada línea: 
# [minuto] [hora] [día_mes] [mes] [día_semana] [comando]

# Rangos:
# - Minutos: 0-59
# - Horas: 0-23
# - Día_Mes: 1-31
# - Mes: 1-12
# - Día_Semana: 0-7 (donde 0 y 7 son Domingo)

# Comodines:
# *  -> Todos los valores (ej: cada minuto, cada día)
# ,  -> Lista de valores (1,15,30)
# -  -> Rango de valores (1-5)
# /  -> Incrementos (*/10 = cada 10 minutos)

# Ejemplos:
# 30 04 * 1 1 /bin/backup.sh          -> Lunes de Enero a las 04:30 AM
# 00 22 * * 1-5 /bin/check.sh         -> Lunes a Viernes a las 10:00 PM
# */15 * * * * /bin/status.sh         -> Cada 15 minutos

### 4. ATAJOS (KEYWORDS)
# @reboot   -> Se ejecuta una vez al arrancar el sistema.
# @daily    -> Una vez al día (0 0 * * *).
# @hourly   -> Una vez por hora (0 * * * *).
# @weekly   -> Una vez por semana (0 0 * * 0).

### 5. CRONTAB DEL SISTEMA Y ESTRUCTURA /ETC
# /etc/crontab: Archivo global del sistema. TIENE UN CAMPO EXTRA: EL USUARIO.
# Formato: [min] [hora] [día] [mes] [día_sem] [USUARIO] [comando]

# Directorios de ejecución automática:
# /etc/cron.hourly/   -> Scripts ejecutados cada hora.
# /etc/cron.daily/    -> Scripts ejecutados cada día.
# /etc/cron.weekly/   -> Scripts ejecutados cada semana.
# /etc/cron.monthly/  -> Scripts ejecutados cada mes.
# /etc/cron.d/        -> Tareas específicas de aplicaciones instaladas.

### 6. CONTROL DE ACCESO
# 1. /etc/cron.allow -> Si existe, solo los usuarios listados pueden usar cron.
# 2. /etc/cron.deny  -> Si existe, los usuarios listados tienen prohibido usar cron.
# Si ambos existen, el "allow" tiene prioridad.

### 7. ANACRON (PARA EQUIPOS NO PERMANENTES)
# Ideal para portátiles que no están encendidos 24/7. Asegura que las tareas no realizadas se ejecuten al encender el equipo.
# Configuración en: /etc/anacrontab

# Formato: [periodo_días] [retardo_min] [id_tarea] [comando]
# Ejemplo: 
# 1  5  cron.daily  run-parts /etc/cron.daily  (Diariamente, 5 min tras arranque)

# Comando útil:
sudo anacron -f -n    # Forzar ejecución inmediata de tareas pendientes.