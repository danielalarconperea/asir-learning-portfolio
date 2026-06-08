#!/bin/bash
# Ejercicio 4: Que nos muestre las configuraciones activas del cron (sin comentarios).

echo "configuraciones del cron sin comentarios:"
echo "-------------------------------------------------------"
crontab -l 2>/dev/null | grep -v "^#" | grep -v "^ *$"
echo "-------------------------------------------------------"
if [ $? -ne 0 ]; then
    echo "No hay tareas programadas o el comando crontab no está disponible."
fi