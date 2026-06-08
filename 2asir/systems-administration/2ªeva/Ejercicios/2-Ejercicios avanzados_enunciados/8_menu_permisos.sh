#!/bin/bash
# Ejercicio 8: Añada al programa anterior un menú que permita añadir o quitar permisos al fichero.


if [ -n "$1" ]; then
    fichero=$1
else
    read -p "Dame el nombre de un fichero: " fichero
fi

# Validar que el fichero existe
if [ ! -e "$fichero" ]; then
    echo "Error: El fichero no existe."
    exit 1
fi

permisos=$(ls -ld "$fichero" | awk '{print $1}')

if [ "${permisos:0:1}" == "-" ]; then
    echo -e "\nEl archivo adjunto es un fichero"
elif [ "${permisos:0:1}" == "d" ]; then
    echo "El archivo adjunto es un directorio"
else
    echo "El archivo adjunto es especial"
fi

echo -e "\nEl propietario del fichero es: $(ls -ld "$fichero" | awk '{print $3}')"

if [ "${permisos:1:1}" == "r" ]; then
    echo "Tiene permiso de lectura"
fi

if [ "${permisos:2:1}" == "w" ]; then
    echo "Tiene permiso de escritura"
fi

if [ "${permisos:3:1}" == "x" ]; then
    echo "Tiene permiso de ejecucion"
elif [ "${permisos:3:1}" == "s" ] || [ "${permisos:3:1}" == "S" ]; then
    echo "Tiene permiso de ejecucion con privilegios de usuario (setuid)"
fi

echo -e "\nEl grupo del fichero es: $(ls -ld "$fichero" | awk '{print $4}')"

if [ "${permisos:4:1}" == "r" ]; then
    echo "Tiene permiso de lectura"
fi

if [ "${permisos:5:1}" == "w" ]; then
    echo "Tiene permiso de escritura"
fi

if [ "${permisos:6:1}" == "x" ]; then
    echo "Tiene permiso de ejecucion"
elif [ "${permisos:6:1}" == "s" ] || [ "${permisos:6:1}" == "S" ]; then
    echo "Tiene permiso de ejecucion con privilegios de grupo (setgid)"
fi

echo -e "\nLos demas usuarios del fichero:"

if [ "${permisos:7:1}" == "r" ]; then
    echo "Tiene permiso de lectura"
fi

if [ "${permisos:8:1}" == "w" ]; then
    echo "Tiene permiso de escritura"
fi

if [ "${permisos:9:1}" == "x" ]; then
    echo "Tiene permiso de ejecucion"
elif [ "${permisos:9:1}" == "t" ] || [ "${permisos:9:1}" == "T" ]; then
    echo "Tiene permiso de ejecucion con restricciones (sticky bit)"
fi

while true; do
    read -p $'\nQuieres modificar algun permiso [si/no]: ' modificar

    if [ $modificar == "si" -o $modificar == "SI" ]; then
        read -p "Quieres añadir o quitar permisos [añadir/quitar]: " accion
        read -p "A quien quieres modificar los permisos [propietario/grupo/demas/todos]: " sujeto
        read -p "Que permiso quieres modificar [r/w/x/s/t]: " permiso

        case $accion in
            añadir)
                case $sujeto in
                    propietario)
                        case $permiso in
                            r) chmod u+r "$fichero" ;;
                            w) chmod u+w "$fichero" ;;
                            x) chmod u+x "$fichero" ;;
                            s) chmod u+s "$fichero" ;;
                            *) echo "Permiso no válido." ;;
                        esac
                        ;;
                    grupo)
                        case $permiso in
                            r) chmod g+r "$fichero" ;;
                            w) chmod g+w "$fichero" ;;
                            x) chmod g+x "$fichero" ;;
                            s) chmod g+s "$fichero" ;;
                            *) echo "Permiso no válido." ;;
                        esac
                        ;;
                    demas)
                        case $permiso in
                            r) chmod o+r "$fichero" ;;
                            w) chmod o+w "$fichero" ;;
                            x) chmod o+x "$fichero" ;;
                            t) chmod o+t "$fichero" ;;
                            *) echo "Permiso no válido." ;;
                        esac
                        ;;
                    todos)
                        case $permiso in
                            r) chmod a+r "$fichero" ;;
                            w) chmod a+w "$fichero" ;;
                            x) chmod a+x "$fichero" ;;
                            s) chmod a+s "$fichero" ;;
                            t) chmod a+t "$fichero" ;;
                            *) echo "Permiso no válido." ;;
                        esac
                        ;;
                    *) echo "Sujeto no válido." ;;
                esac
                ;;
            quitar)
                case $sujeto in
                    propietario)
                        case $permiso in
                            r) chmod u-r "$fichero" ;;
                            w) chmod u-w "$fichero" ;;
                            x) chmod u-x "$fichero" ;;
                            s) chmod u-s "$fichero" ;;
                            *) echo "Permiso no válido." ;;
                        esac
                        ;;
                    grupo)
                        case $permiso in
                            r) chmod g-r "$fichero" ;;
                            w) chmod g-w "$fichero" ;;
                            x) chmod g-x "$fichero" ;;
                            s) chmod g-s "$fichero" ;;
                            *) echo "Permiso no válido." ;;
                        esac
                        ;;
                    demas)
                        case $permiso in
                            r) chmod o-r "$fichero" ;;
                            w) chmod o-w "$fichero" ;;
                            x) chmod o-x "$fichero" ;;
                            t) chmod o-t "$fichero" ;;
                            *) echo "Permiso no válido." ;;
                        esac
                        ;;
                    todos)
                        case $permiso in
                            r) chmod a-r "$fichero" ;;
                            w) chmod a-w "$fichero" ;;
                            x) chmod a-x "$fichero" ;;
                            s) chmod a-s "$fichero" ;;
                            t) chmod a-t "$fichero" ;;
                            *) echo "Permiso no válido." ;;
                        esac
                        ;;
                    *) echo "Sujeto no válido." ;;
                esac
                ;;
            *) echo "Acción no válida." ;;
        esac
    elif [ $modificar == "no" -o $modificar == "NO" ]; then
        echo "No se ha modificado ningun permiso."
        exit 0
    else
        echo "Opcion no valida."
    fi
done