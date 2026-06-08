#!/bin/bash

# ==============================================================================
# 📝 SOLUCIÓN EXAMEN - OCTUBRE 2025 (1ª EVALUACIÓN)
# ==============================================================================

# 1) Generar archivos_grandes.txt con los 10 ficheros más grandes de /var/log
# Buscamos archivos (-type f), imprimimos tamaño y nombre, ordenamos de mayor a menor,
# nos quedamos con los 10 primeros, extraemos solo el nombre y unimos con ";"
find /var/log -type f -printf "%s %p\n" 2>/dev/null | sort -rn | head -10 | awk '{print $2}' | tr '\n' ';' | sed 's/;$/\n/' > archivos_grandes.txt

# 2) Generar ip.txt con la dirección IP del sistema (solo el número)
# Usamos hostname -I que devuelve las IPs y cogemos la primera con awk
hostname -I | awk '{print $1}' > ip.txt

# 3) Cuántos usuarios no preinstalados (humanos) hay y sus nombres
# Los usuarios humanos suelen empezar en el UID 1000.
echo "Usuarios creados en el sistema:"
awk -F: '$3 >= 1000 && $3 < 60000 {print $1}' /etc/passwd
echo -n "Total: "
awk -F: '$3 >= 1000 && $3 < 60000 {print $1}' /etc/passwd | wc -l

# 4) Crear carpeta TEMPORAL en el HOME y copiar /etc completo
mkdir ~/TEMPORAL
cp -r /etc ~/TEMPORAL/

# 5) Empaquetar /etc en empaquetado.tar y crear enlace blando
# -C cambia al directorio para que la ruta dentro del tar sea relativa
tar -cvf ~/TEMPORAL/empaquetado.tar -C ~/TEMPORAL etc
ln -s ~/TEMPORAL/empaquetado.tar ~/TEMPORAL/enlace_al_tar

# 6) Comprimir con bzip2 generando empaquetado.tar.bzip
# Nota: La extensión estándar es .bz2, pero usamos .bzip por el enunciado
bzip2 -c ~/TEMPORAL/empaquetado.tar > ~/TEMPORAL/empaquetado.tar.bzip

# 7) Mostrar número de archivos que contiene el fichero comprimido
echo "Número de archivos en el paquete:"
tar -tvf ~/TEMPORAL/empaquetado.tar.bzip | wc -l

# 8) Mostrar ficheros modificados HOY con formato: Nombre Tamaño Fecha
# -mtime 0 busca archivos modificados en las últimas 24h
echo -e "Nombre\tTamaño\tFecha"
find . -maxdepth 1 -type f -mtime 0 -printf "%f\t%s\t%t\n"

# 9) Borrar todo el directorio TEMPORAL
rm -rf ~/TEMPORAL
echo "Directorio TEMPORAL eliminado."
