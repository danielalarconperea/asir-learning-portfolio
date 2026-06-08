#!/bin/bash

# ==============================================================================
# 📝 GESTIÓN Y VISUALIZACIÓN DE LOGS EN LINUX
# ==============================================================================
# Objetivo: Localizar, filtrar y visualizar los registros del sistema.

### 1. UBICACIÓN PRINCIPAL: /var/log/
# La mayoría de los logs de aplicaciones y del sistema residen aquí.

# Archivos más importantes:
# /var/log/syslog       -> Archivo general de mensajes del sistema (en Debian/Ubuntu).
# /var/log/messages     -> Equivalente al syslog en RHEL/CentOS.
# /var/log/auth.log     -> Intentos de login, uso de sudo, autenticación SSH.
# /var/log/kern.log     -> Mensajes del kernel (drivers, hardware).
# /var/log/apache2/     -> Logs del servidor web Apache (si está instalado).
# /var/log/mysql/       -> Logs de la base de datos MySQL.

### 2. COMANDOS PARA VER LOGS
# Ver el final de un archivo (útil para ver lo más reciente)
tail /var/log/syslog

# Ver en tiempo real (monitorización en vivo)
tail -f /var/log/syslog

# Buscar un error específico
grep "error" /var/log/syslog
grep -i "failed" /var/log/auth.log

# Ver mensajes de arranque del Kernel
dmesg | less

### 3. EL SISTEMA MODERNO: JOURNALCTL
# En sistemas con systemd (Ubuntu, Debian, Fedora), los logs se gestionan con journald.
# Los logs son binarios, por lo que se usa el comando 'journalctl' para leerlos.

# Ver todos los logs (desde el más antiguo)
journalctl

# Ver los logs más recientes (como tail -f)
journalctl -f

# Ver logs de un servicio específico (ej: ssh)
journalctl -u ssh

# Ver logs desde una fecha/hora específica
journalctl --since "2024-01-10 10:00:00"
journalctl --since "1 hour ago"

# Ver logs de errores únicamente
journalctl -p err  # (p es de prioridad: emerg, alert, crit, err, warning, notice, info, debug)

# Ver logs del kernel únicamente
journalctl -k

### 4. CREAR TUS PROPIOS LOGS: LOGGER
# El comando 'logger' permite enviar mensajes al syslog desde la terminal o scripts.

# Ejemplo básico:
logger "Iniciando proceso de backup semanal"

# Especificando la prioridad y etiqueta:
logger -p local0.notice -t [BACKUP_SCRIPT] "Copia de seguridad finalizada con éxito"

# Verificar que se escribió:
tail -n 1 /var/log/syslog
