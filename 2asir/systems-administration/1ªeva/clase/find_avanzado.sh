#!/bin/bash

# ==============================================================================
# 🚀 FIND AVANZADO: TRUCOS Y CASOS DE USO REALES
# ==============================================================================
# Complemento a find.sh para usuarios que necesitan exprimir el comando.

### 1. FORMATEO DE SALIDA CON -PRINTF
# El comando -printf permite personalizar totalmente la salida sin usar awk.
# %p: ruta del archivo.
# %u: nombre del dueño.
# %g: nombre del grupo.
# %s: tamaño en bytes.
# %m: permisos en octal.
# %TY: año de modificación.

# Listar archivos con dueño, permisos y tamaño formateado
find . -type f -printf "Archivo: %p | Dueño: %u | Permisos: %m | Tamaño: %s bytes\n"

### 2. BUSCAR POR COMPARACIÓN (-newer)
# Busca archivos modificados después de que un archivo de referencia fuera modificado.

# Buscar archivos más recientes que 'config.old'
find . -newer config.old

### 3. USO DE EXPRESIONES REGULARES (-regex)
# A diferencia de -name (que usa wildcards de shell), -regex busca en toda la ruta.

# Buscar archivos que terminen en .jpg o .png de forma insensible
find . -regex ".*\(.jpg\|.png\)"

### 4. FILTROS DE PERMISOS AVANZADOS
# -perm /modo : Al menos uno de los bits de permisos está activo.
# -perm -modo : Todos los bits de permisos indicados están activos.

# Buscar archivos que tengan ALGÚN permiso de ejecución (dueño, grupo u otros)
find . -perm /111

# Buscar archivos donde el dueño tenga lectura Y escritura (indiferente al resto)
find . -perm -600

### 5. ENCONTRAR ENLACES ROTOS
# Muy útil para limpieza de sistemas.

# Buscar enlaces simbólicos que apuntan a archivos que ya no existen
find . -xtype l

### 6. IGNORAR DIRECTORIOS ESPECÍFICOS (-prune)
# Evita entrar en subcarpetas que no nos interesan (como .git o node_modules).

# Buscar archivos .js ignorando la carpeta node_modules
find . -path "./node_modules" -prune -o -name "*.js" -print

### 7. CASOS DE USO REALES (ADMINISTRACIÓN)

# A) Encontrar archivos de más de 50MB y moverlos a /tmp/grandes
# find /home -type f -size +50M -exec mv {} /tmp/grandes/ \;

# B) Cambiar el dueño solo a los directorios (no a los archivos)
# find /var/www/html -type d -exec chown www-data:www-data {} \;

# C) Buscar archivos modificados en las últimas 24h y comprimirlos
# find . -mtime -1 -type f -print0 | xargs -0 tar -rvf backup_reciente.tar

# D) Buscar archivos que pertenecen a un usuario que YA NO EXISTE en el sistema
# (Archivos que tienen un UID numérico pero no un nombre de usuario asociado)
find / -nouser

# E) Buscar archivos con el bit SUID activo (potencial riesgo de seguridad)
find /usr/bin -perm /4000
