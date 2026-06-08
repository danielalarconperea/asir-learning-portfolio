#!/bin/bash
# Ejercicio 13 Avanzado: Gestión de citas médicas.
# Archivo de datos: citas_db.txt

DB="citas_db.txt"
[ ! -f "$DB" ] && touch "$DB"

mostrar_ayuda() {
    echo "Uso: $0 [OPCIÓN]"
    echo "  -h, --help    Muestra esta ayuda."
    echo "  -a, --add H_INI H_FIN NOMBRE  Añade una cita."
    echo "  -s, --search PATRON           Busca pacientes por patrón."
    echo "  -i, --init H_INI              Busca citas por hora de inicio."
    echo "  -e, --end H_FIN               Busca citas por hora de fin."
    echo "  -n, --name                    Lista citas ordenadas por nombre."
    echo "  -o, --hour                    Lista citas ordenadas por hora."
}

if [ $# -eq 0 ]; then mostrar_ayuda; exit 0; fi

case $1 in
    -h|--help) mostrar_ayuda ;;
    -a|--add)
        if [ $# -ne 4 ]; then echo "Error: Faltan parámetros."; exit 1; fi
        H_INI=$2; H_FIN=$3; NOMBRE=$4
        
        # Validar horas
        if ! [[ "$H_INI" =~ ^[0-9]{2}$ ]] || ! [[ "$H_FIN" =~ ^[0-9]{2}$ ]]; then echo "Error: Formato HORA incorrecto (00-23)."; exit 1; fi
        if [ "$H_INI" -lt 0 ] || [ "$H_INI" -gt 23 ] || [ "$H_FIN" -lt 0 ] || [ "$H_FIN" -gt 23 ]; then echo "Error: Hora fuera de rango."; exit 1; fi
        
        # Comprobar nombre repetido
        if grep -q ":$NOMBRE$" "$DB"; then echo "Error: El paciente ya tiene una cita."; exit 1; fi
        
        # Comprobar solapamiento
        # Formato: start:end:name
        while IFS=: read -r s e n; do
            if [ "$H_INI" -lt "$e" ] && [ "$H_FIN" -gt "$s" ]; then
                echo "Error: La cita se solapa con la de $n ($s-$e)."
                exit 1
            fi
        done < "$DB"
        
        echo "$H_INI:$H_FIN:$NOMBRE" >> "$DB"
        echo "Cita añadida con éxito."
        ;;
    -s|--search)
        grep "$2" "$DB" || echo "No se encontraron resultados."
        ;;
    -i|--init)
        grep "^$2:" "$DB" || echo "No hay citas que empiecen a esa hora."
        ;;
    -e|--end)
        grep ":$2:" "$DB" || echo "No hay citas que terminen a esa hora."
        ;;
    -n|--name)
        sort -t: -k3 "$DB" | tr ':' '\t'
        ;;
    -o|--hour)
        sort -t: -k1 "$DB" | tr ':' '\t'
        ;;
    *)
        echo "Opción no reconocida."
        mostrar_ayuda
        ;;
esac
