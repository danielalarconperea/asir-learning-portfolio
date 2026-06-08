#!/bin/bash
# Ejercicio 4: Realizar un script que recoja como parámetros cualquier cantidad de nombres 
# de usuario y nos diga aquellos grupos a los que pertenecen todos los usuarios a la vez.

if [ 0 -lt $# ]; then
    for i in $@; do
        if id $i > /dev/null; then
            usuarios+=($i)
        fi
    done
    grupos=$(grep $(echo "${usuarios[@]}" | tr " " ",") /etc/group | sed -d: -f1)
    echo "Todos los usuarios pertenecen a los grupos: $grupos"
else
    echo "No se han introducido usuarios"
fi





#!/bin/bash
# Ejercicio 4: Grupos que pertenecen todos los usuarios a la vez.

# 1. Comprobamos si hay parámetros
if [ $# -eq 0 ]; then
    echo "No se han introducido usuarios."
    exit 1
fi

# 2. Primero, filtramos los usuarios que realmente existen
usuarios_validos=()
for i in "$@"; do
    if id "$i" > /dev/null 2>&1; then
        usuarios_validos+=("$i")
    else
        echo "Aviso: El usuario '$i' no existe y será ignorado."
    fi
done

# 3. Si no hay usuarios válidos, terminamos
if [ ${#usuarios_validos[@]} -eq 0 ]; then
    echo "No hay usuarios válidos para comparar."
    exit 1
fi

# 4. Cogemos los grupos del PRIMER usuario válido como base inicial
# Ponemos cada grupo en una línea (tr) y los ordenamos (sort)
comunes=$(id -Gn "${usuarios_validos[0]}" | tr ' ' '\n' | sort)

# 5. Comparamos con los grupos de los demás usuarios válidos
for (( i=1; i<${#usuarios_validos[@]}; i++ )); do
    # Sacamos los grupos del siguiente usuario
    grupos_actual=$(id -Gn "${usuarios_validos[$i]}" | tr ' ' '\n' | sort)
    
    # Filtramos para quedarnos solo con los que coinciden (grep -Fxf)
    comunes=$(echo "$comunes" | grep -Fxf <(echo "$grupos_actual"))
done

# 6. Mostramos el resultado final
if [ -n "$comunes" ]; then
    echo "Los usuarios [${usuarios_validos[*]}] comparten estos grupos:"
    echo "$comunes" | tr '\n' ' ' # Volvemos a ponerlo en una línea
    echo ""
else
    echo "No tienen ningún grupo en común."
fi