#!/bin/bash

# APUNTES COMPLETOS SOBRE PERMISOS EN LINUX
# ------------------------------------------
# Estos apuntes están diseñados para ser ejecutados en una terminal Bash.
# Cada sección explica un concepto y puede incluir comandos de ejemplo.
# Descomenta las líneas de comandos si quieres probarlos (¡con cuidado!).

echo "========================================================="
echo " CONCEPTOS BÁSICOS DE PERMISOS"
echo "========================================================="

echo "
En Linux, cada archivo y directorio tiene asignados permisos que determinan
quién puede leer, escribir o ejecutarlo. Estos permisos se definen para tres
categorías de usuarios:

1.  Propietario (User/Owner - u): El usuario que creó el archivo o directorio.
2.  Grupo (Group - g): Un conjunto de usuarios que comparten permisos.
3.  Otros (Others - o): Todos los demás usuarios del sistema.

Y existen tres tipos básicos de permisos:

* Leer (Read - r):
    * Para archivos: Permite ver el contenido del archivo.
    * Para directorios: Permite listar el contenido del directorio (nombres de archivos y subdirectorios).
* Escribir (Write - w):
    * Para archivos: Permite modificar o borrar el contenido del archivo.
    * Para directorios: Permite crear, renombrar o borrar archivos y subdirectorios dentro del directorio.
* Ejecutar (Execute - x):
    * Para archivos: Permite ejecutar el archivo (si es un script o un programa).
    * Para directorios: Permite acceder al directorio (entrar en él con 'cd') y acceder a sus metadatos.
"

echo "========================================================="
echo " VISUALIZACIÓN DE PERMISOS: ls -l"
echo "========================================================="

echo "
El comando 'ls -l' muestra información detallada de los archivos, incluyendo sus permisos.
Ejemplo de salida:
-rwxr-xr-- 1 usuario grupo 1024 May 13 10:00 archivo.txt
d--------- 2 root   root  4096 May 13 12:31 directorio_sin_permisos

Interpretación de la primera columna (los permisos):
El primer carácter indica el tipo de archivo:
  - : Archivo regular
  d : Directorio
  l : Enlace simbólico
  c : Dispositivo de caracteres
  b : Dispositivo de bloques
  s : Socket
  p : Tubería (pipe)

Los siguientes nueve caracteres representan los permisos, en tres grupos de tres:
  1.  Propietario (rwx)
  2.  Grupo (rwx)
  3.  Otros (rwx)

Donde:
  r = Leer
  w = Escribir
  x = Ejecutar
  - = Permiso denegado

Ejemplo: '-rwxr-xr--'
  -        : Es un archivo regular.
  rwx      : El propietario (usuario) tiene permisos de leer, escribir y ejecutar.
  r-x      : El grupo tiene permisos de leer y ejecutar, pero no de escribir.
  r--      : Otros tienen permiso de leer, pero no de escribir ni ejecutar.
"

# touch ejemplo_archivo.txt
# mkdir ejemplo_directorio
# ls -l ejemplo_archivo.txt ejemplo_directorio
# rm ejemplo_archivo.txt
# rmdir ejemplo_directorio

echo "========================================================="
echo " CAMBIO DE PERMISOS: chmod"
echo "========================================================="

echo "
El comando 'chmod' (change mode) se utiliza para modificar los permisos de
archivos y directorios. Se puede usar de dos maneras principales:

1.  Método Simbólico:
    Utiliza letras para representar usuarios, operadores y permisos.
    Usuarios:
      u : Propietario (user)
      g : Grupo (group)
      o : Otros (others)
      a : Todos (all - u, g, y o)

    Operadores:
      + : Añade un permiso.
      - : Quita un permiso.
      = : Establece los permisos exactos (sobrescribe los existentes).

    Permisos:
      r : Leer
      w : Escribir
      x : Ejecutar

    Ejemplos:
    # chmod u+x archivo.sh        # Añade permiso de ejecución para el propietario.
    # chmod g-w archivo.txt       # Quita permiso de escritura para el grupo.
    # chmod o=r archivo.conf      # Establece solo permiso de lectura para otros.
    # chmod a+r documento.pdf     # Añade permiso de lectura para todos.
    # chmod u=rwx,g=rx,o=r mi_script # Establece permisos completos para u, rx para g, r para o.

2.  Método Octal (Numérico):
    Representa cada conjunto de permisos (propietario, grupo, otros) con un
    dígito octal (0-7). Cada permiso tiene un valor numérico:
      r = 4
      w = 2
      x = 1
      - = 0

    Se suman los valores para cada categoría de usuario:
      --- = 0 (0+0+0)
      --x = 1 (0+0+1)
      -w- = 2 (0+2+0)
      -wx = 3 (0+2+1)
      r-- = 4 (4+0+0)
      r-x = 5 (4+0+1)
      rw- = 6 (4+2+0)
      rwx = 7 (4+2+1)

    El comando 'chmod' toma un número de tres dígitos:
    El primer dígito es para el propietario.
    El segundo dígito es para el grupo.
    El tercer dígito es para otros.

    Ejemplos:
    # chmod 755 script.sh         # rwxr-xr-x (Propietario: rwx, Grupo: r-x, Otros: r-x)
                                  # Típico para scripts ejecutables y directorios.
    # chmod 644 archivo.txt       # rw-r--r-- (Propietario: rw-, Grupo: r--, Otros: r--)
                                  # Típico para archivos de datos.
    # chmod 700 directorio_privado # rwx------ (Propietario: rwx, Grupo: ---, Otros: ---)
                                  # Típico para directorios privados del usuario.

Opción '-R' (Recursivo):
    # chmod -R 644 mi_directorio/ # Aplica permisos 644 a todos los archivos y
                                  # subdirectorios dentro de mi_directorio.
                                  # ¡Cuidado con esta opción! Es común dar 755 a directorios
                                  # y 644 a archivos. Un 'chmod -R 644' quitaría el permiso
                                  # de ejecución a los subdirectorios, impidiendo el acceso.
                                  # Para aplicar de forma selectiva:
                                  # find ./mi_directorio -type d -exec chmod 755 {} \;
                                  # find ./mi_directorio -type f -exec chmod 644 {} \;
"

# touch mi_archivo_chmod.txt
# echo "Archivo de prueba chmod" > mi_archivo_chmod.txt
# ls -l mi_archivo_chmod.txt
# echo "Aplicando chmod u+x mi_archivo_chmod.txt..."
# chmod u+x mi_archivo_chmod.txt
# ls -l mi_archivo_chmod.txt
# echo "Aplicando chmod 600 mi_archivo_chmod.txt..."
# chmod 600 mi_archivo_chmod.txt
# ls -l mi_archivo_chmod.txt
# rm mi_archivo_chmod.txt

echo "========================================================="
echo " CAMBIO DE PROPIETARIO Y GRUPO: chown y chgrp"
echo "========================================================="

echo "
1.  chown (Change Owner):
    Cambia el propietario y/o el grupo de un archivo o directorio.
    Sintaxis:
      chown [NUEVO_PROPIETARIO] archivo_o_directorio
      chown [NUEVO_PROPIETARIO]:[NUEVO_GRUPO] archivo_o_directorio
      chown :[NUEVO_GRUPO] archivo_o_directorio (solo cambia el grupo)

    Ejemplos (generalmente requieren privilegios de superusuario 'sudo'):
    # sudo chown nuevo_usuario archivo.txt
    # sudo chown usuario_existente:nuevo_grupo documento.doc
    # sudo chown :otro_grupo mi_directorio

    Opción '-R' (Recursivo):
    # sudo chown -R usuario:grupo /ruta/al/directorio

2.  chgrp (Change Group):
    Cambia solo el grupo de un archivo o directorio. Es menos común que
    'chown usuario:grupo' pero existe.
    Sintaxis:
      chgrp [NUEVO_GRUPO] archivo_o_directorio

    Ejemplo (puede requerir 'sudo'):
    # chgrp nuevo_grupo_dev codigo_fuente.c
    # sudo chgrp -R web_editores /var/www/html
"

# echo "Creando archivo para chown/chgrp..."
# sudo touch archivo_prop.txt
# ls -l archivo_prop.txt
# echo "Cambiando propietario a 'nobody' (si existe y tienes sudo)..."
# # sudo chown nobody archivo_prop.txt # Descomentar con precaución
# ls -l archivo_prop.txt
# echo "Cambiando grupo a 'nogroup' (si existe y tienes sudo)..."
# # sudo chown :nogroup archivo_prop.txt # Descomentar con precaución
# ls -l archivo_prop.txt
# sudo rm archivo_prop.txt


echo "========================================================="
echo " PERMISOS POR DEFECTO: umask"
echo "========================================================="

echo "
El comando 'umask' (user file-creation mode mask) controla los permisos
por defecto asignados a los archivos y directorios recién creados.

'umask' especifica los permisos que *NO* se deben asignar.
Se representa como un valor octal.

Permisos base para creación:
  - Archivos: 666 (rw-rw-rw-) - No se da ejecución por defecto por seguridad.
  - Directorios: 777 (rwxrwxrwx) - Se da ejecución para poder acceder.

Cómo funciona 'umask':
Los permisos finales son: (Permisos Base) AND (NOT umask)
O más fácil: Permisos Base MENOS los bits activados en umask.

Ejemplo: umask 022
  - Para archivos:
    Permiso base:      666 (rw-rw-rw-)
    Umask:             022 (-w--w-)
    Permiso resultante: 644 (rw-r--r--)

  - Para directorios:
    Permiso base:      777 (rwxrwxrwx)
    Umask:             022 (-w--w-)
    Permiso resultante: 755 (rwxr-xr-x)

Comandos útiles:
  umask          # Muestra la umask actual en formato octal (e.g., 0022)
  umask -S       # Muestra la umask en formato simbólico (e.g., u=rwx,g=rx,o=rx)
  umask [valor]  # Establece una nueva umask para la sesión actual (e.g., umask 027)

Una umask común es 0022 (o simplemente 22), que resulta en:
  - Archivos: 644 (rw-r--r--)
  - Directorios: 755 (rwxr-xr-x)

Una umask más restrictiva podría ser 0027, que resulta en:
  - Archivos: 640 (rw-r-----)
  - Directorios: 750 (rwxr-x---)

La umask se suele configurar en archivos de inicio de sesión como ~/.bashrc o /etc/profile.
"
echo "Umask actual:"
umask
echo "Umask actual (simbólica):"
umask -S

# echo "Guardando umask actual..."
# OLD_UMASK=$(umask)
# echo "Estableciendo umask 077 (muy restrictiva)..."
# umask 077
# touch archivo_umask_test.txt
# mkdir directorio_umask_test
# ls -ld archivo_umask_test.txt directorio_umask_test/
# echo "Restaurando umask original: $OLD_UMASK"
# umask $OLD_UMASK
# rm archivo_umask_test.txt
# rmdir directorio_umask_test

echo "========================================================="
echo " PERMISOS ESPECIALES"
echo "========================================================="

echo "
Existen tres permisos especiales que otorgan capacidades adicionales:

1.  SetUID (Set User ID - SUID):
    * Aplicable solo a archivos ejecutables.
    * Cuando un archivo con SUID activado es ejecutado, el proceso se ejecuta
        con los privilegios del *propietario* del archivo, no del usuario que lo ejecuta.
    * Representación simbólica: 's' en la posición de ejecución del propietario (rws en lugar de rwx).
        Si el propietario no tiene permiso de ejecución, se muestra como 'S' mayúscula (rwS).
    * Representación octal: Se añade un '4' al principio del número octal (e.g., chmod 4755).
    * Caso de uso: Comandos como 'passwd' (que necesita modificar /etc/shadow, propiedad de root)
        o 'ping' (que necesita abrir sockets raw).
    * ¡Peligroso si se aplica incorrectamente a scripts o programas no seguros!

    # Ejemplo (no ejecutar sin entender las implicaciones):
    # sudo cp /bin/cat /tmp/mycat
    # sudo chown root /tmp/mycat
    # sudo chmod u+s /tmp/mycat  # o sudo chmod 4755 /tmp/mycat
    # ls -l /tmp/mycat # Debería mostrar -rwsr-xr-x ... root ... mycat
    # /tmp/mycat /etc/shadow # Un usuario normal podría ver este archivo (¡peligro!)
    # sudo rm /tmp/mycat

2.  SetGID (Set Group ID - SGID):
    * Para archivos ejecutables:
        * El proceso se ejecuta con los privilegios del *grupo* del archivo.
        * Representación simbólica: 's' en la posición de ejecución del grupo (r-srwx en lugar de r-xrwx).
            Si el grupo no tiene permiso de ejecución, se muestra como 'S' mayúscula (r-Srwx).
        * Representación octal: Se añade un '2' al principio (e.g., chmod 2755).
        * Caso de uso: Programas que necesitan acceder a recursos de un grupo específico.

    * Para directorios:
        * Los nuevos archivos y subdirectorios creados dentro de este directorio
            heredan el grupo del directorio padre (en lugar del grupo primario del usuario que los crea).
        * Si además el SGID está activado en el directorio, los nuevos subdirectorios también
            heredarán el bit SGID.
        * Representación simbólica: 's' en la posición de ejecución del grupo (drwxr-sr-x).
        * Representación octal: Se añade un '2' al principio (e.g., chmod 2775 directorio_colaborativo).
        * Caso de uso: Directorios compartidos donde todos los archivos deben pertenecer a un grupo común.

    # Ejemplo para directorio:
    # mkdir /tmp/proyecto_compartido
    # sudo chgrp desarrolladores /tmp/proyecto_compartido # Asumiendo que 'desarrolladores' es un grupo
    # sudo chmod g+s /tmp/proyecto_compartido # o sudo chmod 2775 /tmp/proyecto_compartido
    # ls -ld /tmp/proyecto_compartido # drwxrwsr-x ... desarrolladores ... proyecto_compartido
    # touch /tmp/proyecto_compartido/nuevo_archivo.txt
    # ls -l /tmp/proyecto_compartido/nuevo_archivo.txt # El archivo pertenecerá al grupo 'desarrolladores'
    # sudo rm -r /tmp/proyecto_compartido

3.  Sticky Bit (Bit Pegajoso):
    * Aplicable principalmente a directorios.
    * Cuando está activado en un directorio, solo el propietario del archivo,
        el propietario del directorio o el usuario root pueden borrar o renombrar
        archivos dentro de ese directorio, incluso si otros usuarios tienen permisos de escritura
        sobre el directorio.
    * Representación simbólica: 't' en la posición de ejecución de otros (rwxrwxrwt).
        Si 'otros' no tienen permiso de ejecución, se muestra como 'T' mayúscula (rwxrwxrwT).
    * Representación octal: Se añade un '1' al principio (e.g., chmod 1777).
    * Caso de uso: Directorios públicos como /tmp o /var/tmp, donde muchos usuarios pueden
        crear archivos, pero no deben poder borrar los archivos de otros.

    # Ejemplo:
    # ls -ld /tmp # Debería mostrar drwxrwxrwt ... root root ... /tmp
    # chmod +t mi_directorio_publico # o chmod 1777 mi_directorio_publico

Combinación de permisos especiales (Octal):
  SUID = 4000
  SGID = 2000
  Sticky Bit = 1000

  chmod 4755 archivo   # SUID
  chmod 2755 archivo   # SGID
  chmod 1777 directorio # Sticky Bit
  chmod 7755 archivo   # SUID + SGID + Sticky Bit (4000+2000+1000 = 7000)
                       # Esto sería rwsrwsrwt si todos los permisos de ejecución base están presentes.
"

echo "========================================================="
echo " SIGNIFICADO DE PERMISOS EN DIRECTORIOS (Resumen)"
echo "========================================================="

echo "
Para un directorio:
* Leer (r): Permite listar el contenido del directorio (ver nombres de archivos y subdirectorios).
    Sin 'r', no puedes hacer 'ls' dentro del directorio.

* Escribir (w): Permite crear, borrar y renombrar archivos y subdirectorios dentro del directorio.
    Requiere también el permiso de ejecución (x) en el directorio.
    Nota: Para borrar un archivo, necesitas permiso de escritura en el *directorio* que lo contiene,
    no necesariamente en el archivo mismo (a menos que el sticky bit esté activado).

* Ejecutar (x): Permite acceder al directorio (hacer 'cd' hacia él) y acceder a los metadatos de
    los archivos dentro del directorio (necesario para 'ls -l', por ejemplo, o para acceder a
    archivos aunque conozcas su nombre). Sin 'x', el directorio es inaccesible, incluso si tienes 'r'.
"

echo "========================================================="
echo " ATRIBUTOS DE ARCHIVO EXTENDIDOS (chattr y lsattr) - AVANZADO"
echo "========================================================="

echo "
Además de los permisos estándar, los sistemas de archivos de Linux (como ext2/3/4)
soportan atributos extendidos que ofrecen un control más fino.

'chattr' (Change Attribute): Modifica atributos.
'lsattr' (List Attributes): Muestra atributos.

Algunos atributos comunes (requieren privilegios de root para modificarse):
  i (immutable):
    Un archivo con el atributo 'i' no puede ser modificado, borrado, renombrado,
    ni se pueden crear enlaces a él. Ni siquiera por root.
    Para modificarlo, primero hay que quitar el atributo 'i'.
    # sudo chattr +i archivo_importante.conf
    # sudo chattr -i archivo_importante.conf

  a (append-only):
    Un archivo con el atributo 'a' solo puede ser abierto en modo de añadir
    (append). No se puede sobrescribir ni borrar su contenido existente.
    Útil para archivos de log.
    # sudo chattr +a /var/log/mi_log_especial.log

  e (extent format): Indica que el archivo usa extents para mapear bloques en disco.

Cómo verlos:
  lsattr archivo_o_directorio

Ejemplo:
# sudo touch /tmp/archivo_seguro.txt
# sudo chattr +i /tmp/archivo_seguro.txt
# lsattr /tmp/archivo_seguro.txt # Debería mostrar ----i-------- /tmp/archivo_seguro.txt
# # Intenta borrarlo: rm /tmp/archivo_seguro.txt # Fallará
# # Intenta escribir en él: echo "test" > /tmp/archivo_seguro.txt # Fallará
# sudo chattr -i /tmp/archivo_seguro.txt
# sudo rm /tmp/archivo_seguro.txt

Estos atributos son independientes de los permisos rwx.
"

echo "========================================================="
echo " FIN DE LOS APUNTES SOBRE PERMISOS EN LINUX"
echo "========================================================="

# Fin del script de apuntes