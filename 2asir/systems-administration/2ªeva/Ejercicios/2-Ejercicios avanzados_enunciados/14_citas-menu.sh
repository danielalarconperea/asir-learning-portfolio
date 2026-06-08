#!/bin/bash
# Ejercicio 14: Interfaz de menú para el script de citas con opciones para añadir, buscar y listar.

CITAS_FILE="citas.txt"

# Asegurar que el archivo existe
if [ ! -f "$CITAS_FILE" ]; then
    touch "$CITAS_FILE"
fi

# Función para añadir una cita de forma interactiva
menu_añadir() {
    echo -e "\n--- AÑADIR NUEVA CITA ---"
    read -p "Nombre de la persona: " nombre
    read -p "Fecha (YYYY-MM-DD): " fecha
    read -p "Hora de inicio (HH:MM): " h_ini
    read -p "Hora de fin (HH:MM): " h_fin

    # Validaciones básicas
    if [[ ! "$fecha" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
        echo "Error: Formato de fecha incorrecto."
        return
    fi
    if [[ ! "$h_ini" =~ ^[0-9]{2}:[0-9]{2}$ || ! "$h_fin" =~ ^[0-9]{2}:[0-9]{2}$ ]]; then
        echo "Error: Formato de hora incorrecto."
        return
    fi
    if [[ "$h_ini" > "$h_fin" ]]; then
        echo "Error: La hora de inicio no puede ser posterior a la de fin."
        return
    fi

    echo "$nombre | $fecha | $h_ini | $h_fin" >> "$CITAS_FILE"
    echo "Cita añadida con éxito."
}

# Función para buscar
menu_buscar() {
    echo -e "\n--- BUSCAR CITAS ---"
    read -p "Introduce el patrón de búsqueda (nombre, fecha...): " patron
    echo "----------------------------------------------------"
    grep -i "$patron" "$CITAS_FILE" || echo "No se encontraron coincidencias."
    echo "----------------------------------------------------"
}

# Función para listar
menu_listar() {
    echo -e "\n--- LISTAR CITAS ---"
    echo "1. Ordenar por nombre"
    echo "2. Ordenar por hora"
    read -p "Selecciona una opción: " opt_list
    
    echo "----------------------------------------------------"
    case $opt_list in
        1) sort -t'|' -k1 "$CITAS_FILE" ;;
        2) sort -t'|' -k3 "$CITAS_FILE" ;;
        *) echo "Opción no válida." ;;
    esac
    echo "----------------------------------------------------"
}

# Bucle principal del menú
while true; do
    echo -e "\n===== GESTIÓN DE CITAS ====="
    echo "1. Añadir cita"
    echo "2. Buscar cita"
    echo "3. Listar citas"
    echo "4. Salir"
    read -p "Elige una opción: " opcion

    case $opcion in
        1) menu_añadir ;;
        2) menu_buscar ;;
        3) menu_listar ;;
        4) echo "¡Adiós!"; exit 0 ;;
        *) echo "Opción no válida." ;;
    esac
done

