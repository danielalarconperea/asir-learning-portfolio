#!/bin/bash
# Ejercicio 5: Realizar un script que muestre un menú: 
# 1. Usuarios de su grupo; 
# 2. Usuarios del grupo y directorio HOME; 
# 3. Listado de grupos y número de usuarios; 
# 4. Salir.

while true; do
    echo -e "\n--- MENÚ DE USUARIOS ---"
    echo "1. Usuarios de su grupo"
    echo "2. Usuarios del grupo y directorio HOME"
    echo "3. Listado de grupos y número de usuarios"
    echo "4. Salir"
    read -p "Introduce una opción: " opcion

    # Obtenemos el nombre y el ID del grupo actual del usuario
    GRUPO_ACTUAL=$(id -gn)
    GID_ACTUAL=$(id -g)

    case $opcion in
        1)
            echo "Usuarios que pertenecen al grupo $GRUPO_ACTUAL:"
            # Buscamos en /etc/passwd los que tengan nuestro GID como principal
            awk -v gid="$GID_ACTUAL" -F: '$4 == gid { print $1 }' /etc/passwd
            ;;
        2)
            echo "Usuarios de $GRUPO_ACTUAL y su directorio HOME:"
            # El campo $1 es el usuario y el $6 es el HOME en /etc/passwd
            awk -v gid="$GID_ACTUAL" -F: '$4 == gid { print "Usuario: " $1 "\t HOME: " $6 }' /etc/passwd
            ;;
        3)
            echo "Listado de todos los grupos y cuántos usuarios tienen (miembros secundarios):"
            while IFS=: read -r gname pass gid members; do
                # Si el campo members está vacío, el conteo es 0
                if [ -z "$members" ]; then
                    count=0
                else
                    # Contamos cuántas comas hay y sumamos 1, o contamos elementos con tr
                    count=$(echo "$members" | tr ',' '\n' | wc -l)
                fi
                echo "Grupo: $gname ($gid) - Usuarios: $count"
            done < /etc/group
            ;;
        4)
            echo "Saliendo..."
            exit 0
            ;;
        *)
            echo "Opción no válida, intenta de nuevo."
            ;;
    esac
done