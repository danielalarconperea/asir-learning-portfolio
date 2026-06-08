#!/bin/bash
# Ejercicio 3: quiensoy.sh
# Muestra el usuario actual, su HOME y datos de caducidad.

USUARIO=$(whoami)
echo "Usuario actual: $USUARIO"
echo "Directorio de conexión: $HOME"

# chage -l requiere permisos de root para ver otros, o siendo el propio usuario para verse a sí mismo.
echo "Datos de caducidad de la contraseña y del usuario:"
echo "$(chage -l "$USUARIO")" | grep "Password expires"
echo "$(chage -l "$USUARIO")" | grep "Account expires"
