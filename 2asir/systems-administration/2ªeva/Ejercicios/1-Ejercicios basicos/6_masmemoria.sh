#!/bin/bash
# Ejercicio 6: masmemoria.sh
# Muestra los 3 procesos que más memoria consumen.

echo "Top 3 procesos con más consumo de memoria:"
ps aux --sort=-%mem | head -n 4 | tail -n 3
# Usamos head -n 4 para incluir la cabecera y los 3 primeros, luego tail -n 3 para descartar la cabecera si se desea solo los datos.
