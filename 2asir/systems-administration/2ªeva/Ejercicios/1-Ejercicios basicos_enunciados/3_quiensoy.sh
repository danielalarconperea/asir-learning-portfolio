#!/bin/bash
# Ejercicio 3: Que nos muestre el usuario que lo está ejecutando, su directorio de conexión 
# y los datos referentes a fecha de caducidad de la contraseña y del usuario.


echo -n "Usuario actual: "
whoami

echo "Directorio de conexión: $HOME"

echo "Datos de caducidad de la contraseña y del usuario:"
echo "$(chage -l "$USER")" | grep "Password expires"
echo "$(chage -l "$USER")" | grep "Account expires"
