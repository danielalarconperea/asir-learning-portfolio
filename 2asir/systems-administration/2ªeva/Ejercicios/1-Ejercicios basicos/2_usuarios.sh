#!/bin/bash
# Ejercicio 2: usuarios.sh
# Muestra la lista de usuarios reales (no del sistema).
# Normalmente los usuarios reales tienen un UID >= 1000.

echo "Usuarios reales en el sistema (UID >= 1000):"
awk -F: '$3 >= 1000 && $1 != "nobody" {print $1}' /etc/passwd
