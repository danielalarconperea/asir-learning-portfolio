#!/bin/bash

# ==============================================================================
# 🔍 BÚSQUEDA AVANZADA DE ARCHIVOS Y DIRECTORIOS: FIND
# ==============================================================================
# Objetivo: Buscar archivos y directorios en una jerarquía basándose en diversos
# criterios y, opcionalmente, realizar acciones sobre ellos.

### 1. SINTAXIS BÁSICA
# find [ruta] [expresión_de_búsqueda] [acción]
# Si no se especifica ruta, usa el directorio actual (.).

# Buscar todo en el directorio actual
find .

# Buscar solo en una ruta específica
find /var/log

### 2. BÚSQUEDA POR NOMBRE Y TIPO
# -name: Busca por nombre (sensible a mayúsculas).
# -iname: Busca por nombre (ignora mayúsculas).
# -type: Filtra por tipo (f=fichero, d=directorio, l=enlace simbólico).

# Buscar un archivo exacto
find . -name "documento.txt"

# Buscar archivos .jpg (ignorar mayúsculas: .JPG, .jpg)
find /home -iname "*.jpg"

# Buscar directorios que se llamen 'config'
find /etc -type d -name "config"

### 3. BÚSQUEDA POR TAMAÑO (-size)
# Unidades: c (bytes), k (kilobytes), M (megabytes), G (gigabytes).
# Prefijos: + (mayor que), - (menor que), (nada) (exactamente).

# Archivos mayores de 100MB
find / -size +100M

# Archivos menores de 50k
find . -size -50k

# Archivos vacíos
find . -empty

### 4. BÚSQUEDA POR TIEMPO (-mtime, -atime, -ctime)
# mtime: Última modificación del contenido.
# atime: Último acceso al archivo.
# ctime: Último cambio en el inodo (metadatos o contenido).
# El valor se da en días (24h). Para minutos usar -mmin, -amin, -cmin.

# Modificados hace exactamente 2 días
find . -mtime 2

# Modificados hace más de 30 días
find /var/backups -mtime +30

# Modificados hace menos de 10 minutos
find . -mmin -10

### 5. BÚSQUEDA POR PERMISOS Y PROPIETARIOS
# -perm: Permisos específicos.
# -user: Archivos de un usuario.
# -group: Archivos de un grupo.

# Permisos exactos 777
find . -perm 777

# Archivos que pertenecen al usuario 'dania'
find /home -user dania

# Archivos que tienen permisos de escritura para el grupo (formato simbólico)
find . -perm -g=w

### 6. OPERADORES LÓGICOS (AND, OR, NOT)
# -and (por defecto): Se deben cumplir ambas condiciones.
# -or: Se debe cumplir una de las dos.
# -not o !: Niega la condición siguiente.

# Archivos .sh Y que sean ejecutables
find . -name "*.sh" -and -perm -u=x

# Archivos que NO sean .txt
find . -not -name "*.txt"

# Buscar archivos .pdf O .doc (usar paréntesis escapados para agrupar)
find . \( -name "*.pdf" -or -name "*.doc" \)

### 7. LIMITAR PROFUNDIDAD (-maxdepth)
# Controla qué tan profundo entra find en las subcarpetas.

# Buscar solo en el directorio actual, sin entrar en subcarpetas
find . -maxdepth 1 -name "*.log"

### 8. ACCIONES SOBRE LOS RESULTADOS (-exec, -delete, -ok)
# -print: Acción por defecto (imprimir ruta).
# -delete: Borra los archivos encontrados (¡PELIGRO!).
# -exec [comando] {} \; : Ejecuta el comando para cada resultado.
# {} : Marcador de posición para el archivo encontrado.
# \; : Finaliza el comando de exec.

# Borrar todos los archivos temporales .tmp
find /tmp -name "*.tmp" -delete

# Cambiar permisos a todos los .sh encontrados
find . -name "*.sh" -exec chmod +x {} \;

# Buscar una palabra dentro los archivos encontrados
find . -type f -name "*.txt" -exec grep "error" {} \;

# -ok es igual que -exec pero pide confirmación antes de ejecutar
find . -name "*.old" -ok rm {} \;

### 9. USO DE XARGS (Alternativa eficiente a -exec)
# Pasa la lista de resultados de find como argumentos a otro comando.
# Es más eficiente para procesar miles de archivos a la vez.

# Contar líneas de todos los archivos .c
find . -name "*.c" | xargs wc -l

# Usar -print0 y xargs -0 para archivos con espacios en el nombre
find . -name "*.txt" -print0 | xargs -0 rm
