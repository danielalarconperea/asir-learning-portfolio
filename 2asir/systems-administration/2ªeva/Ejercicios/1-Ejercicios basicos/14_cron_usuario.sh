#!/bin/bash
# Ejercicio 14: cron_usuario.sh
# Pide un usuario y muestra su crontab. Requiere permisos para ver crontabs de otros.

read -p "Introduce el nombre del usuario: " USUARIO

if id "$USUARIO" >/dev/null 2>&1; then
    echo "Mostrando crontab de $USUARIO:"
    sudo crontab -u "$USUARIO" -l 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "No se ha podido leer el crontab (puede que no tenga o falten permisos de sudo)."
    fi
else
    echo "El usuario $USUARIO no existe."
fi
