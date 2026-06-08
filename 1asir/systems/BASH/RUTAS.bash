# APUNTES SOBRE TIPOS DE ENLACES EN LINUX

# Los enlaces en Linux son una forma de crear "accesos directos" o "punteros" a archivos o directorios.
# Existen dos tipos principales de enlaces: enlaces duros (hard links) y enlaces simbólicos (soft links o symlinks).

# -------------------------
# ENLACES DUROS (HARD LINKS)
# -------------------------

# Un enlace duro es una entrada de directorio que asocia un nombre con un archivo existente en el sistema de archivos.
# Características principales de los enlaces duros:
#   - Todos los enlaces duros a un mismo archivo comparten el mismo número de inodo (identificador único del archivo en el sistema de archivos).
#   - No se puede crear un enlace duro a un directorio (generalmente, aunque algunos sistemas antiguos lo permitían con restricciones).
#   - No se pueden crear enlaces duros entre diferentes sistemas de archivos (particiones).
#   - Si se borra el archivo original, el contenido del archivo sigue accesible a través de los enlaces duros restantes,
#     ya que todos apuntan directamente a los datos en el disco. El archivo solo se elimina realmente del disco cuando se borran todos sus enlaces duros
#     y ningún proceso lo tiene abierto.
#   - Modificar el contenido a través de un enlace duro modifica el archivo original y viceversa, porque son, en esencia, el mismo archivo con diferentes nombres.

# Comando para crear un enlace duro: ln <archivo_existente> <nombre_del_nuevo_enlace_duro>

# Ejemplo de creación de un enlace duro:

# 1. Creamos un archivo de ejemplo:
echo "Contenido original del archivo." > archivo_original.txt
echo "Archivo original creado."

# 2. Mostramos su número de inodo y contenido:
ls -li archivo_original.txt
echo "Contenido:"
cat archivo_original.txt

# 3. Creamos un enlace duro llamado 'enlace_duro.txt' que apunta a 'archivo_original.txt':
ln archivo_original.txt enlace_duro.txt
echo "Enlace duro creado."

# 4. Mostramos el número de inodo y contenido del enlace duro.
#    Notarás que el número de inodo es el mismo que el de 'archivo_original.txt'
#    y el contador de enlaces (segunda columna en 'ls -li') habrá aumentado.
ls -li archivo_original.txt enlace_duro.txt
echo "Contenido del enlace duro:"
cat enlace_duro.txt

# 5. Modificamos el contenido a través del enlace duro:
echo "Contenido modificado a través del enlace duro." > enlace_duro.txt
echo "Contenido modificado vía enlace_duro.txt."

# 6. Verificamos que el archivo original también ha cambiado:
echo "Nuevo contenido del archivo original:"
cat archivo_original.txt
echo "Nuevo contenido del enlace duro:"
cat enlace_duro.txt

# 7. Borramos el archivo original:
rm archivo_original.txt
echo "Archivo original borrado."

# 8. Verificamos que el contenido sigue accesible a través del enlace duro:
echo "Verificando acceso a través del enlace duro después de borrar el original:"
ls -li enlace_duro.txt # El contador de enlaces debería haber disminuido.
cat enlace_duro.txt   # El contenido sigue ahí.

# 9. Limpieza del ejemplo de enlace duro:
rm enlace_duro.txt
echo "Enlace duro borrado."

# -------------------------------
# ENLACES BLANDOS/SIMBÓLICOS (SOFT LINKS)
# -------------------------------

# Un enlace simbólico (o symlink) es un tipo especial de archivo que contiene una ruta a otro archivo o directorio.
# Es similar a un acceso directo en Windows.
# Características principales de los enlaces simbólicos:
#   - Tienen su propio número de inodo, diferente al del archivo o directorio al que apuntan.
#   - Pueden apuntar a archivos o directorios.
#   - Pueden crearse entre diferentes sistemas de archivos (particiones).
#   - Si se borra el archivo o directorio original al que apunta el enlace simbólico, el enlace se rompe
#     (se convierte en un enlace "huérfano") y ya no funcionará.
#   - Modificar el enlace simbólico en sí mismo (por ejemplo, cambiar a dónde apunta) no afecta al archivo original.
#     Sin embargo, acceder y modificar el contenido *a través* del enlace simbólico (si no está roto) sí modifica el archivo original.
#   - Su tamaño es el de la cadena de texto de la ruta a la que apunta.

# Comando para crear un enlace simbólico: ln -s <ruta_al_archivo_o_directorio_original> <nombre_del_nuevo_enlace_simbolico>

# Ejemplo de creación de un enlace simbólico a un archivo:

# 1. Creamos otro archivo de ejemplo:
echo "Este es un archivo para el enlace simbólico." > archivo_destino.txt
echo "Archivo destino para symlink creado."

# 2. Mostramos su información:
ls -li archivo_destino.txt

# 3. Creamos un enlace simbólico llamado 'enlace_simbolico.txt' que apunta a 'archivo_destino.txt':
ln -s archivo_destino.txt enlace_simbolico.txt
echo "Enlace simbólico creado."

# 4. Mostramos la información del enlace simbólico.
#    Notarás que 'enlace_simbolico.txt' tiene su propio número de inodo y permisos especiales (empiezan con 'l').
#    'ls -l' también muestra a dónde apunta el enlace (-> archivo_destino.txt).
ls -li archivo_destino.txt enlace_simbolico.txt
echo "Contenido del archivo destino (vía symlink):"
cat enlace_simbolico.txt

# 5. Modificamos el contenido del archivo original a través del enlace simbólico:
echo "Contenido modificado a través del enlace simbólico." >> enlace_simbolico.txt # Usamos >> para añadir, no sobrescribir.
echo "Contenido modificado vía enlace_simbolico.txt."

# 6. Verificamos que el archivo destino ha cambiado:
echo "Nuevo contenido del archivo destino:"
cat archivo_destino.txt

# 7. Borramos el archivo destino:
rm archivo_destino.txt
echo "Archivo destino borrado."

# 8. Intentamos acceder al contenido a través del enlace simbólico.
#    Esto generalmente resultará en un error "No such file or directory" porque el enlace está roto.
echo "Intentando acceder a través del enlace simbólico roto:"
cat enlace_simbolico.txt # Debería fallar
ls -l enlace_simbolico.txt # 'ls' a menudo lo marca en rojo o indica que está roto.

# 9. Limpieza del ejemplo de enlace simbólico:
rm enlace_simbolico.txt
echo "Enlace simbólico borrado."

# Ejemplo de creación de un enlace simbólico a un directorio:

# 1. Creamos un directorio de ejemplo:
mkdir directorio_original
echo "Contenido dentro del directorio." > directorio_original/fichero_en_directorio.txt
echo "Directorio original y fichero interno creados."

# 2. Creamos un enlace simbólico llamado 'enlace_directorio' que apunta a 'directorio_original':
ln -s directorio_original enlace_directorio
echo "Enlace simbólico a directorio creado."

# 3. Listamos el contenido. 'enlace_directorio' aparecerá como un enlace:
ls -l
ls -li enlace_directorio # Muestra información sobre el enlace en sí

# 4. Podemos usar el enlace simbólico como si fuera el directorio original:
echo "Listando contenido del directorio original a través del enlace:"
ls -l enlace_directorio/
cat enlace_directorio/fichero_en_directorio.txt

# 5. Si borramos el directorio original, el enlace simbólico se romperá:
# rm -r directorio_original # Descomentar para probar, luego borrar enlace_directorio
# ls -l enlace_directorio/  # Esto fallaría

# 6. Limpieza del ejemplo de enlace a directorio:
rm -r directorio_original
rm enlace_directorio
echo "Directorio original y enlace a directorio borrados."

# ---------------------------------------------
# RESUMEN DE DIFERENCIAS CLAVE Y CUÁNDO USARLOS
# ---------------------------------------------

# Enlace Duro:
#   - Apunta al inodo (contenido) del archivo.
#   - No ocupa espacio adicional significativo (solo una entrada de directorio).
#   - No puede enlazar directorios.
#   - No puede cruzar sistemas de archivos.
#   - El archivo original puede ser borrado y los datos persisten si quedan otros enlaces duros.
#   - Útil para tener múltiples nombres para el mismo archivo dentro del mismo sistema de archivos,
#     o como una forma de "backup" que no se rompe si el nombre original se mueve (dentro del mismo FS) o borra.

# Enlace Simbólico:
#   - Apunta al nombre/ruta de otro archivo o directorio.
#   - Ocupa un pequeño espacio para almacenar la ruta.
#   - Puede enlazar directorios.
#   - Puede cruzar sistemas de archivos.
#   - Si el archivo/directorio original es borrado o movido, el enlace se rompe.
#   - Muy útil para crear accesos directos convenientes, para apuntar a versiones de software,
#     o para organizar archivos sin duplicarlos físicamente.

# Comando para ver el número de inodo: ls -i <archivo>
# Comando para ver información detallada incluyendo tipo de archivo y a dónde apunta un symlink: ls -l <archivo>

# Fin de los apuntes sobre enlaces en Linux.
echo "Apuntes finalizados. Ejecuta los comandos paso a paso para entenderlos mejor."