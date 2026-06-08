#!/bin/bash
# Ejercicio 13: Sistema de gestión de citas con opciones para ayuda, añadir, buscar por patrón, 
# hora inicio/fin, listar por nombre o por hora, validando solapamientos y formatos.


# Función para mostrar la ayuda
mostrar_ayuda() {
    echo "Uso: $0 [opción] [argumentos]"
    echo "Opciones:"
    echo "  -a, --añadir <nombre> <fecha> <hora_inicio> <hora_fin>    Añadir una cita"
    echo "  -b, --buscar <patrón>                                     Buscar citas por patrón"
    echo "  -i, --hora_inicio <hora>                                  Buscar citas por hora de inicio"
    echo "  -f, --hora_fin <hora>                                     Buscar citas por hora de fin"
    echo "  -l, --listar [nombre|hora]                                Listar citas por nombre o hora"
    echo "  -h, --help                                               Mostrar esta ayuda"
}

# Función para añadir una cita
añadir_cita() {
    local nombre="$1"
    local fecha="$2"
    local hora_inicio="$3"
    local hora_fin="$4"

    # Validar formato de fecha y hora
    if ! [[ "$fecha" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo "Error: Fecha inválida. Formato correcto: YYYY-MM-DD"
        return 1
    fi
    if ! [[ "$hora_inicio" =~ ^[0-9]{2}:[0-9]{2}$ ]]; then
        echo "Error: Hora de inicio inválida. Formato correcto: HH:MM"
        return 1
    fi
    if ! [[ "$hora_fin" =~ ^[0-9]{2}:[0-9]{2}$ ]]; then
        echo "Error: Hora de fin inválida. Formato correcto: HH:MM"
        return 1
    fi

    # Validar solapamientos
    if [[ "$hora_inicio" > "$hora_fin" ]]; then
        echo "Error: Hora de inicio no puede ser mayor que hora de fin"
        return 1
    fi

    # Añadir la cita al archivo
    echo "$nombre $fecha $hora_inicio $hora_fin" >> citas.txt
    echo "Cita añadida correctamente: $nombre $fecha $hora_inicio $hora_fin"
}

# Función para buscar citas por patrón
buscar_cita() {
    local patron="$1"
    grep -i "$patron" citas.txt
}


# Función para buscar citas por hora de inicio
buscar_por_hora_inicio() {
    local hora="$1"
    grep -w "$hora" citas.txt | awk '{print $1, $2, $3, $4}'
}


# Función para buscar citas por hora de fin
buscar_por_hora_fin() {
    local hora="$1"
    grep -w "$hora" citas.txt | awk '{print $1, $2, $3, $4}'
}


# Función para listar citas por nombre
listar_por_nombre() {
    sort -k1 citas.txt
}


# Función para listar citas por hora
listar_por_hora() {
    sort -k3 citas.txt
}


# Procesar argumentos
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        -a|--añadir)
            añadir_cita "$2" "$3" "$4" "$5"
            shift 5
            ;;
        -b|--buscar)
            buscar_cita "$2"
            shift 2
            ;;
        -i|--hora_inicio)
            buscar_por_hora_inicio "$2"
            shift 2
            ;;
        -f|--hora_fin)
            buscar_por_hora_fin "$2"
            shift 2
            ;;
        -l|--listar)
            if [[ "$2" == "nombre" ]]; then
                listar_por_nombre
            elif [[ "$2" == "hora" ]]; then
                listar_por_hora
            else
                echo "Error: Opción de listado inválida. Use 'nombre' o 'hora'."
                mostrar_ayuda
                exit 1
            fi
            shift 2
            ;;
        -h|--help)
            mostrar_ayuda
            exit 0
            ;;
        *)
            echo "Error: Opción inválida. Use --help para ver las opciones disponibles."
            exit 1
            ;;
    esac
done
