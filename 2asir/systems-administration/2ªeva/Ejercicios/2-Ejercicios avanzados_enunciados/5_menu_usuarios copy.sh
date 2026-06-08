#!/bin/bash
# Ejercicio 5: Realizar un script que muestre un menú: 
# 1. Usuarios de su grupo; 
# 2. Usuarios del grupo y directorio HOME; 
# 3. Listado de grupos y número de usuarios; 
# 4. Salir.

while true; do
    echo "-------------------------------------------"
    echo "1. Usuarios de su grupo." 
    echo "2. Usuarios del grupo y directorio HOME." 
    echo "3. Listado de grupos y número de usuarios." 
    echo "4. Salir."
    echo "-------------------------------------------"
    read -p "Elige una opcion [1-4]: " opcion
    
    user_name=$(id -un)
    group_name=$(id -gn)
    user_gid=$(id -u)
    group_gid=$(id -g)


    case $opcion in
        1)
            echo -e "\n*******************************************"
            echo -n "Los usuarios del grupo $group_name: "
            awk -v "g=$user_gid" -F: '$4 == g {print $1}' /etc/passwd
            echo "*******************************************"
        ;;
        2)
            echo -e "\n*******************************************"
            awk -v g="$group_gid" -F: '$4 == g {print "Usuario: " $1 " Home: " $6}' /etc/passwd
            echo "*******************************************"
        ;;
        3)
            echo -e "\n*******************************************"
            while IFS=: read -r grupo pass gidgroup usuarios;do
                if [ -z "$usuarios" ]; then
                    count=0
                else
                    count=$(echo "$usuarios" | tr "," "\n" | wc -l)
                fi
                echo "Grupo: $grupo - Numero de usuarios: $count"
            done < /etc/group
            echo "*******************************************"
        ;;
        4)
            echo -e "\nsaliendo del programa..."
            exit 0
        ;;
        *)
            echo "el número introducido no es correcto"
        ;;

    esac
done


# -------------------------------------------------------------------------------------------


awk -F: '{ 
    # Si el campo 4 está vacío, el total es 0, si no, contamos las comas y sumamos 1
    # split divide el texto por comas y devuelve cuántos trozos han salido
    n = ($4 == "" ? 0 : split($4, arr, ","))
    print "Grupo: " $1 " (" $3 ") - Usuarios: " n 
}' /etc/group



while read -r linea; do
    nombre_grupo=$(echo "$linea" | cut -d: -f1)
    gid_grupo=$(echo "$linea" | cut -d: -f3)
    miembros=$(echo "$linea" | cut -d: -f4)
    
    echo "Grupo: $nombre_grupo ($gid_grupo) - Miembros: $miembros"
done < /etc/group