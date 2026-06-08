#!/bin/bash

# ==============================================================================
# 📝 CONFIGURACIÓN DE LOGS: RSYSLOG & LOGROTATE
# ==============================================================================
# Objetivo: Configurar cómo se guardan los logs y cómo se gestiona su rotación.

### 1. EL SERVICIO RSYSLOG
# Es el responsable de recoger los mensajes y escribirlos en los archivos.
# Archivo de configuración: /etc/rsyslog.conf
# Directorio de piezas extra: /etc/rsyslog.d/

# Sintaxis de una regla:
# [FACILITY].[PRIORITY]   [DESTINO]

# --- FACILITY (Categoría) ---
# auth/authpriv (seguridad), cron, mail, kern, lpr (impresión), local0-local7.

# --- PRIORITY (Nivel de importancia) ---
# debug (bajo), info, notice, warning, err, crit, alert, emerg (pánico).

# --- EJEMPLOS DE REGLAS ---
# cron.*  /var/log/cron.log             -> Envía TODO de cron a ese archivo.
# *.err   /var/log/todos_los_errores    -> Envía errores de cualquier origen.
# *.info;auth.none /var/log/messages    -> Envía todo nivel info EXCEPTO seguridad.

# Aplicar cambios:
sudo systemctl restart rsyslog

### 2. LOGROTATE: GESTIÓN DE ESPACIO
# Para evitar que los logs llenen el disco, se "rotan" (se comprimen y borran los viejos).
# Archivo de configuración: /etc/logrotate.conf
# Configuraciones específicas: /etc/logrotate.d/

# Estructura de una configuración (ej: para apache):
# /var/log/apache2/*.log {
#     daily             -> Rotar cada día (opciones: weekly, monthly, yearly).
#     size 50M          -> Rotar SIEMPRE que supere 50MB (ignora el tiempo).
#     rotate 7          -> Mantener 7 archivos antiguos antes de borrar.
#     compress          -> Comprimir en .gz para ahorrar espacio.
#     delaycompress     -> No comprimir el archivo rotado más reciente aún.
#     missingok         -> No dar error si el log no existe.
#     notifempty        -> No rotar si el archivo está vacío.
#     create 0640 r adm -> Crear nuevo log con esos permisos/dueño.
#     copytruncate      -> Copiar y truncar (útil para apps que no cierran logs).
#     dateext           -> Usar fecha en el nombre (ej: .20240111) en vez de .1.
#     olddir /backups/  -> Mover logs antiguos a otro directorio.
#     sharedscripts     -> Ejecutar el script UNA VEZ para TODOS los logs.
#     postrotate        -> Ejecutar algo TRAS rotar el log.
#         /usr/sbin/apache2ctl graceful > /dev/null
#     endscript
# }

# Forzar una rotación manualmente (para pruebas):
sudo logrotate -f /etc/logrotate.conf

### 3. ENVÍO DE LOGS A UN SERVIDOR REMOTO
# Rsyslog puede enviar logs a otro servidor centralizador vía red.

# En el cliente (editar /etc/rsyslog.conf):
# *.*  @192.168.1.50   # Enviar todo por UDP al servidor .50
# *.*  @@192.168.1.50  # Enviar todo por TCP al servidor .50

### 4. MONITORIZACIÓN DE LOGS AVANZADA
# Comando 'watch': Repite un comando cada X segundos.
watch -n 1 "tail -n 5 /var/log/auth.log"

# Comando 'multitail': Permite ver varios logs a la vez en ventanas (requiere instalar).
# sudo apt install multitail
# multitail /var/log/syslog /var/log/auth.log
