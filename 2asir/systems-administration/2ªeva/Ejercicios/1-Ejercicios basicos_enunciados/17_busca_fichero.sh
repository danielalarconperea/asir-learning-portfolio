#!/bin/bash
# Ejercicio 17: Recoja un nombre de un fichero y lo busque en el sistema.

if [ -n "$1" ]; then
    file=$1
else
    read -p "Dime el fichero: " file
fi

if find / -name "$file" 2>/dev/null; then
    echo "El fichero existe"
else
    echo "El fichero no existe"
fi


#!/bin/bash
# Ejercicio 17: Recoja un nombre de un fichero y lo busque en el sistema.

if [ -n "$1" ]; then
    file=$1
else
    read -p "Dime el fichero: " file
fi

# No comprobamos con -f, dejamos que find lo busque en todo el sistema
echo "Buscando '$file' en el sistema..."
find / -name "$file" 2>/dev/null