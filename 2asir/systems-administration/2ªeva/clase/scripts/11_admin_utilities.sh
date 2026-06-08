#!/bin/bash

# En administración de sistemas, Bash se usa para procesar texto
# Aquí vemos las 3 herramientas "reinas" de forma sencilla

# Creamos un archivo de datos (tipo /etc/passwd simplificado)
cat << EOF > usuarios.db
juan:admin:1001
ana:user:1002
pedro:user:1003
marta:admin:1004
EOF

echo "--- Archivo de prueba ---"
cat usuarios.db

# 1. GREP: Buscar texto
echo -e "\n--- Buscando administradores (grep) ---"
grep "admin" usuarios.db

# 2. AWK: Procesar columnas
# Imprimir solo el primer campo (nombre) y el tercero (ID)
# -F: indica el separador (en este caso dos puntos)
echo -e "\n--- Listado de Nombres e IDs (awk) ---"
awk -F: '{ print "Nombre: " $1 " -> ID: " $3 }' usuarios.db

# 3. SED: Editar texto al vuelo
# Cambiar 'user' por 'cliente' solo en la salida
echo -e "\n--- Cambiando 'user' por 'cliente' (sed) ---"
sed 's/user/cliente/g' usuarios.db

# 4. Combinando todo (El poder de la tubería)
# ¿Cuántos usuarios tienen ID mayor a 1002?
echo -e "\n--- Usuarios con ID > 1002 ---"
awk -F: '$3 > 1002 { print $1 }' usuarios.db | wc -l

# Limpieza
rm usuarios.db
