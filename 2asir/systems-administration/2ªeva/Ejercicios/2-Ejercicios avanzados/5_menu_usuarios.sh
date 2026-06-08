#!/bin/bash
# Ejercicio 5 Avanzado: Menú de gestión de usuarios y grupos.

while true; do
    echo "--- MENÚ DE USUARIOS ---"
    echo "1. Listar usuarios de mi grupo"
    echo "2. Usuarios de mi grupo + directorio Home"
    echo "3. Listado de grupos y número de usuarios"
    echo "4. Salir"
    read -p "Opción: " OPCION

    MI_GRUPO_ID=$(id -g)
    MI_GRUPO_NOMBRE=$(id -gn)

    case $OPCION in
        1)
            echo "Usuarios del grupo $MI_GRUPO_NOMBRE:"
            grep ":$MI_GRUPO_ID:" /etc/passwd | cut -d: -f1
            ;;
        2)
            echo "Usuarios del grupo $MI_GRUPO_NOMBRE y sus Homes:"
            grep ":$MI_GRUPO_ID:" /etc/passwd | cut -d: -f1,6 | tr ':' '\t'
            ;;
        3)
            echo "Listado de grupos y cantidad de usuarios:"
            while IFS=: read -r gname gpass gid gmembers; do
                # Usuarios primarios (en /etc/passwd)
                C1=$(grep -c ":$gid:" /etc/passwd)
                # Usuarios secundarios (en /etc/group)
                if [ -n "$gmembers" ]; then
                    C2=$(echo "$gmembers" | tr ',' '\n' | wc -l)
                else
                    C2=0
                fi
                echo "Grupo: $gname - Usuarios: $((C1 + C2))"
            done < /etc/group
            ;;
        4)
            echo "Saliendo..."
            break
            ;;
        *)
            echo "Opción no válida."
            ;;
    esac
    echo ""
done
