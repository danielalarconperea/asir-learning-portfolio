#!/bin/bash
# Ejercicio 14 Avanzado: Menú interactivo para el script de citas.

SCRIPT="./citas.sh"

while true; do
    echo "--- MENÚ DE CITAS MÉDICAS ---"
    echo "1. Añadir cita nueva"
    echo "2. Buscar por nombre de paciente"
    echo "3. Buscar por hora inicial"
    echo "4. Buscar por hora final"
    echo "5. Listar citas por nombre"
    echo "6. Listar citas por hora"
    echo "7. Salir"
    read -p "Opción: " OPC

    case $OPC in
        1)
            read -p "Hora inicio (00-23): " HI
            read -p "Hora fin (00-23): " HF
            read -p "Nombre paciente: " NOM
            bash $SCRIPT --add "$HI" "$HF" "$NOM"
            ;;
        2)
            read -p "Patrón a buscar: " PAT
            bash $SCRIPT --search "$PAT"
            ;;
        3)
            read -p "Hora de inicio: " HI
            bash $SCRIPT --init "$HI"
            ;;
        4)
            read -p "Hora de fin: " HF
            bash $SCRIPT --end "$HF"
            ;;
        5)
            bash $SCRIPT --name
            ;;
        6)
            bash $SCRIPT --hour
            ;;
        7)
            break
            ;;
        *)
            echo "Opción no válida."
            ;;
    esac
    echo ""
done
