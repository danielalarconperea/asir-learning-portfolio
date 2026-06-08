#!/bin/bash

# ==============================================================================
# 📝 PERMISOS ESPECIALES Y ENLACES (SUID, SGID, STICKY, LINKS)
# ==============================================================================

### 1. PERMISOS ESPECIALES
# Se añaden como un cuarto dígito al principio (4=SUID, 2=SGID, 1=Sticky).

# --- SUID (Set User ID) ---
# El archivo se ejecuta con los permisos del dueño (ej: root).
chmod 4755 archivo
chmod u+s archivo

# --- SGID (Set Group ID) ---
# En carpetas, los archivos nuevos heredan el grupo de la carpeta padre.
chmod 2775 /carpeta/compartida
chmod g+s /carpeta/compartida

# --- STICKY BIT ---
# Solo el dueño puede borrar sus archivos en esa carpeta (ej: /tmp).
chmod 1777 /tmp
chmod +t /tmp

### 2. ENLACES (LINKS)
# Linux usa Inodos para identificar archivos. Los enlaces apuntan a esos Inodos.

# --- Enlaces Duros (Hard Links) ---
# Es el mismo archivo con nombres diferentes. Comparten el mismo Inodo.
# Si borras el original, el enlace duro sigue funcionando.
ln archivo_original enlace_duro

# --- Enlaces Simbólicos/Blandos (Soft Links) ---
# Son como un "Acceso directo" de Windows. Apuntan a la ruta del archivo.
# Si borras el original, el enlace simbólico se "rompe".
ln -s /ruta/archivo_original acceso_directo

### 3. IDENTIFICACIÓN Y BÚSQUEDA
# Ver el número de inodo de un archivo
ls -i archivo.txt

# Buscar todos los nombres que apuntan al mismo Inodo
find / -inum 12345 2>/dev/null
