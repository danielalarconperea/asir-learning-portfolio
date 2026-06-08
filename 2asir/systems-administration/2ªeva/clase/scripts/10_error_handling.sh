#!/bin/bash

# --- NIVEL 1: Control Básico ---

# 1. set -e: Salir inmediatamente si un comando falla
# Muy útil para evitar que el script siga si algo crítico falla
set -e

echo "Este comando funciona"
ls . > /dev/null

# Si descomentas la línea de abajo, el script se detendrá ahí
# ls archivo_que_no_existe

# 2. set -x: Modo depuración (debug)
# Imprime cada comando antes de ejecutarlo
# set -x
echo "Depuración activada (si descomentas set -x)"
# set +x # Desactiva el modo depuración

# --- NIVEL 2: Gestión de Señales (TRAP) ---

# trap permite ejecutar una función cuando el script recibe una señal
# o cuando termina (EXIT)

limpieza() {
    echo "Ejecutando limpieza antes de salir..."
    rm -f temporal_critico.txt
}

# Ejecutar 'limpieza' al salir del script (por éxito o fallo)
trap limpieza EXIT

touch temporal_critico.txt
echo "Trabajando con archivos temporales..."
sleep 2

# Incluso si forzamos un error, trap EXIT se ejecutará
# false 

echo "Fin del script."
