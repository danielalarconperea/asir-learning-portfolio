#!/bin/bash

# ==============================================================================
# 📝 GESTIÓN DE PERMISOS EN LINUX (BÁSICOS Y ESPECIALES)
# ==============================================================================
# Objetivo: Controlar quién puede leer, escribir o ejecutar archivos y carpetas.

### 1. PERMISOS BÁSICOS (rwx)
# Se dividen en tres grupos: Usuario (u), Grupo (g) y Otros (o).
# r (4): Lectura | w (2): Escritura | x (1): Ejecución

# --- Representación Octal (Números) ---
# 7 (4+2+1) -> rwx | 6 (4+2) -> rw- | 5 (4+1) -> r-x | 4 -> r--

# Ejemplo: Aplicar permisos 750 (u=rwx, g=r-x, o=---)
chmod 750 archivo.sh

# --- Representación Simbólica ---
chmod u+x archivo      # Añadir ejecución al usuario
chmod g-w archivo      # Quitar escritura al grupo
chmod o=r archivo      # Otros solo pueden leer
chmod a+x archivo      # Añadir ejecución a TODOS (All)

### 2. PROPIEDAD DE ARCHIVOS
# Cambiar dueño (requiere sudo para cambiar a otros)
sudo chown usuario archivo
sudo chown usuario:grupo archivo  # Cambia dueño y grupo a la vez

# Cambiar solo el grupo
chgrp grupo archivo

### 3. LA MÁSCARA (UMASK)
# Define qué permisos NO se dan por defecto al crear un archivo/carpeta.
# Los archivos nacen con 666 y las carpetas con 777 (máximo). El umask se resta de ahí.
# Si umask es 022:
# Carpeta: 777 - 022 = 755 (drwxr-xr-x)
# Archivo: 666 - 022 = 644 (-rw-r--r--)

umask 027    # Establecer nueva máscara para la sesión actual

### 4. PERMISOS ESPECIALES (CRUCIAL EXAMEN) 🚀
# Se añaden como un cuarto dígito al principio (4=SUID, 2=SGID, 1=Sticky).

# --- A) SUID (Set User ID) ---
# El archivo se ejecuta con los permisos del DUEÑO del archivo, no de quien lo lanza.
# Visualización: Aparece una 's' en el lugar de la 'x' del usuario (rws------).
chmod 4755 programa_root
chmod u+s programa_root
# Ejemplo clásico: /usr/bin/passwd (permite a usuarios cambiar su clave siendo root).

# --- B) SGID (Set Group ID) ---
# En archivos: Se ejecuta con los permisos del GRUPO del archivo.
# En carpetas: Los archivos nuevos creados dentro HEREDAN el grupo de la carpeta.
# Visualización: Aparece una 's' en el lugar de la 'x' del grupo (rwxrws---).
chmod 2775 carpeta_compartida
chmod g+s carpeta_compartida

# --- C) STICKY BIT ---
# Solo se aplica a CARPETAS. Evita que usuarios borren archivos de otros.
# Solo el dueño del archivo (o root) puede borrar su propio archivo.
# Visualización: Aparece una 't' al final (rwxrwxrwt).
chmod 1777 /tmp
chmod +t /tmp
# Ejemplo clásico: /tmp (todos escriben, nadie borra lo ajeno).

### 5. CÓMO VERLOS (LS -L)
# drwxr-xr-x -> Directorio normal
# -rwsr-xr-x -> Archivo con SUID (dueño ejecuta como root)
# drwxrwsr-x -> Directorio con SGID (herencia de grupo)
# drwxrwxrwt -> Directorio con Sticky Bit (borrado restringido)

# NOTA: Si la letra es MAYÚSCULA (S o T), significa que el permiso especial está 
# activo pero el permiso de ejecución 'x' básico NO está puesto (error común).
