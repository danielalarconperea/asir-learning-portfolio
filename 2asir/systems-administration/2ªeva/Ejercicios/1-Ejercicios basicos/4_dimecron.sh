#!/bin/bash
# Ejercicio 4: dimecron.sh
# Muestra las configuraciones activas del cron del usuario actual, sin comentarios.

echo "Tareas programadas en CRON (activas):"
crontab -l 2>/dev/null | grep -v '^#' | grep -v '^$'
if [ $? -ne 0 ]; then
    echo "No hay tareas programadas o el comando crontab no está disponible."
fi
