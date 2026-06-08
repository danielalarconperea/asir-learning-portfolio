#!/bin/bash

### --- Sección 1: Comando locate (Búsqueda indexada) ---

# ℹ️ El comando 'locate' busca archivos en una base de datos preconstruida (mlocate.db).
# Es mucho más rápido que 'find' porque no recorre el disco en tiempo real,
# pero depende de que la base de datos esté actualizada.

# Sintaxis básica: locate [patrón]
locate mi_archivo
# -> /home/usuario/documentos/mi_archivo.txt
# -> /var/www/html/mi_archivo.config

### --- Sección 2: Opciones de locate (Detalladas) ---

# 🔍 Opción -i (Case Insensitive)
# Ignora la "sensibilidad" a mayúsculas y minúsculas.
# Útil si no recuerdas si el archivo es "Foto.jpg" o "foto.jpg".
locate -i archivo
# -> /home/user/Archivo.txt
# -> /home/user/archivo.bak

# 🔢 Opción -c (Count)
# En lugar de mostrar las rutas, cuenta cuántas coincidencias existen y muestra el número.
locate -c .bashrc
# -> 12 (Indica que hay 12 archivos que coinciden con el patrón)

# 🔗 Opción -A (All / And)
# Permite usar varios patrones. Solo muestra resultados que coincidan con TODOS los patrones dados.
# Útil para filtrar resultados específicos.
locate -A "conf" "apache"
# -> /etc/apache2/apache2.conf
# -> (Solo muestra archivos que tengan "conf" Y "apache" en la ruta)

### --- Sección 3: Comando updatedb (Gestión de la Base de Datos) ---

# ⚙️ El comando 'updatedb' actualiza la base de datos que usa 'locate'.
# Generalmente se ejecuta automáticamente por cron (tarea programada), 
# pero se puede forzar manualmente con permisos de superusuario.
sudo updatedb
# -> (No muestra salida, pero actualiza el índice de archivos en el sistema)

# 📂 Localización de la base de datos
# El archivo binario de la base de datos suele encontrarse en la siguiente ruta:
ls -l /var/lib/mlocate/mlocate.db
# -> -rw-r----- 1 root mlocate 1234567 Nov 25 10:00 /var/lib/mlocate/mlocate.db

### --- Sección 4: Configuración (/etc/updatedb.conf) ---

# 📝 El comportamiento de updatedb se define en el archivo de configuración.
# Aquí explicamos las variables CLAVES que aparecen en tus apuntes.

# Visualizamos el archivo de configuración actual:
cat /etc/updatedb.conf
# -> PRUNE_BIND_MOUNTS="yes"
# -> PRUNEFS="NFS nfs nfs4 rpc_pipefs afs binfmt_misc ..."
# -> PRUNENAMES=".git .hg .svn"
# -> PRUNEPATHS="/tmp /var/spool /media /var/lib/os-prober ..."

# --- Explicación detallada de las variables de configuración ---

# 1. PRUNEFS (Filesystems)
# 🚫 Excluye tipos de sistemas de ficheros completos.
# Ejemplo: Se suele excluir NFS para evitar indexar unidades de red lentas.
# Variable: PRUNEFS="NFS nfs afs proc"

# 2. PRUNENAMES (Nombres de directorios/archivos)
# 🚫 Lista de nombres de directorios o archivos que se excluyen de la indexación.
# Ejemplo: Se excluyen carpetas de control de versiones.
# Variable: PRUNENAMES=".git .svn"

# 3. PRUNEPATHS (Rutas específicas)
# 🚫 Lista de rutas absolutas que se excluyen.
# Ejemplo: Se excluye /tmp porque su contenido es volátil y no merece la pena indexarlo.
# Variable: PRUNEPATHS="/tmp /var/tmp /media"

# 4. PRUNE_BIND_MOUNTS
# 🔗 Define si se excluyen los puntos de montaje enlazados (bind mounts).
# 'yes' significa que no se escanearán, evitando duplicados en la base de datos.
# Variable: PRUNE_BIND_MOUNTS="yes"