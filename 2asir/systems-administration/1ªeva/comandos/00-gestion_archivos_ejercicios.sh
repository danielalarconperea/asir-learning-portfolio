#!/bin/bash

# ==============================================================================
# 📝 GUÍA DE GESTIÓN DE ARCHIVOS Y DIRECTORIOS (EJERCICIOS)
# ==============================================================================

### 1. OPERACIONES BÁSICAS
# Crear archivos vacíos
touch f1.txt f2.txt f3.txt

# Crear directorios (Absoluto y Relativo)
mkdir $HOME/copias    # Absoluto (usando variable $HOME)
mkdir otro            # Relativo (en la carpeta actual)

# Copiar archivos con cambio de extensión
# Copia f1.txt a copias/f1.doc
cp f1.txt copias/f1.doc

# Mover y Renombrar
mv $HOME/copias/f1.doc $HOME/f1_movido.doc  # Mover
mv $HOME/copias $HOME/copiados              # Renombrar directorio

# Borrar archivos y carpetas
rm copiados/f2.doc          # Borrar archivo
rm -rf otro                 # Borrar directorio y todo su contenido (-r: recursivo, -f: forzar)

### 2. TRABAJO CON USUARIOS DEL SISTEMA (/ETC/PASSWD)
# Ver usuarios y sus shells (campos 1 y 7)
cut -d: -f1,7 /etc/passwd

# Buscar y reemplazar texto en archivos (SED)
# Sustituir 'home' por 'casa' en todo el archivo
sed -i 's/home/casa/g' datos_usuario

# Eliminar o comentar líneas que contengan 'false'
sed -i '/false/c\#LINEA ELIMINADA' datos_usuario

### 3. EMPAQUETADO Y COMPRESIÓN (TAR / ZIP)
# Empaquetar /bin en un .tar
tar -cvf bin.tar /bin

# Empaquetar y comprimir en .tar.gz
tar -czvf bin.tar.gz /bin

# Eliminar archivos del paquete que empiecen por 'p'
tar -f bin.tar.gz --delete --wildcards 'bin/p*'

# Gestión con ZIP
zip -r bin.zip /bin         # Crear
zip -d bin.zip 'bin/p*'     # Borrar archivo interno
unzip -l bin.zip            # Listar contenido

### 4. DIVIDIR Y UNIR ARCHIVOS (SPLIT)
# Dividir un archivo grande en 10 partes
split -n 10 -d bin.tar parte_

# Unir las partes de nuevo
cat parte_* > bin_unido.tar

### 5. MANIPULACIÓN DE TEXTO ÚTIL
# Ver inicio y fin de un archivo
head -n 5 diccionario.txt
tail -n 5 diccionario.txt

# Unir archivos por columnas
paste -d ';' columna1.txt columna2.txt

# Cifrado César simple (sustitución de letras)
tr 'a-z' 'g-za-f' < entrada.txt > salida.txt
