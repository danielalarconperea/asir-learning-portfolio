#!/bin/bash
# Ejercicio 7: modi_cron.sh
# Muestra cuántas veces se ha modificado el cron y las fechas/horas.
# Nota: Esto busca en los logs del sistema, los cuales suelen requerir permisos de root.

LOG_FILE="/var/log/syslog"
[ ! -f "$LOG_FILE" ] && LOG_FILE="/var/log/cron"

if [ ! -r "$LOG_FILE" ]; then
    echo "Error: No se puede leer el archivo de log ($LOG_FILE). ¿Tienes permisos?"
    exit 1
fi

MODS=$(grep "crontab" "$LOG_FILE" | grep -E "REPLACE|EDIT" | wc -l)
echo "El cron se ha modificado $MODS veces desde el último rotado de logs."
echo "Detalle de las modificaciones:"
grep "crontab" "$LOG_FILE" | grep -E "REPLACE|EDIT" | awk '{print $1, $2, $3}'
# Dependiendo del sistema, el formato del log puede variar.
# Este script asume un formato estándar de syslog.
