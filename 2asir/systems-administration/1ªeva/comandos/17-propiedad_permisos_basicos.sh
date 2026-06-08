#!/bin/bash

# ==============================================================================
# 📝 PROPIEDAD Y PERMISOS BÁSICOS (CHOWN, CHGRP, CHMOD)
# ==============================================================================

### 1. CAMBIO DE PROPIEDAD (OWNERSHIP)
# Solo root puede cambiar el dueño de un archivo.

# Cambiar Dueño (User)
sudo chown usuario archivo.txt

# Cambiar Dueño y Grupo a la vez
sudo chown usuario:grupo archivo.txt

# Cambiar solo el Grupo
chgrp grupo archivo.txt

# Cambiar de forma recursiva (todo un directorio)
sudo chown -R usuario:grupo carpeta/

### 2. PERMISOS BÁSICOS (CHMOD)
# r (4): Leer | w (2): Escribir | x (1): Ejecutar

# --- Modo Octal (Números) ---
# Suma: 7(rwx), 6(rw-), 5(r-x), 4(r--)
chmod 755 script.sh   # u=rwx, g=r-x, o=r-x
chmod 644 texto.txt    # u=rw-, g=r--, o=r--

# --- Modo Simbólico (Letras) ---
chmod u+x archivo     # Dar ejecución al dueño
chmod g-w archivo     # Quitar escritura al grupo
chmod o=r archivo     # Otros solo pueden leer
chmod a+x archivo     # Todos pueden ejecutar

### 3. LA MÁSCARA (UMASK)
# Define qué permisos NO se darán por defecto.
# Carpetas nacen de 777, Archivos de 666.

# Ver umask actual
umask

# Si umask es 022:
# Carpeta: 777 - 022 = 755 (drwxr-xr-x)
# Archivos: 666 - 022 = 644 (-rw-r--r--)

### 4. INFO DETALLADA (STAT)
# Muestra fecha de acceso, modificación, cambio y el número de Inodo.
stat archivo.txt
