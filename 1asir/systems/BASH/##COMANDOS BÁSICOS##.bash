#!/bin/bash

# -----------------------------------------------------------------------------
# APUNTES COMPLETOS DE COMANDOS BÁSICOS DE LINUX
# Este script contiene una recopilación de comandos esenciales de Linux,
# con comentarios breves para su comprensión y uso.
# -----------------------------------------------------------------------------

# -------------------------
# NAVEGACIÓN Y LISTADO DE ARCHIVOS
# -------------------------

# pwd (Print Working Directory)
# Muestra la ruta absoluta del directorio actual en el que te encuentras.
pwd

# cd (Change Directory)
# Permite cambiar entre directorios.
# cd [ruta_del_directorio]
cd /home/usuario/documentos # Ejemplo: va al directorio 'documentos' del usuario 'usuario'
cd ..                       # Sube un nivel en la jerarquía de directorios (al directorio padre).
cd ~                        # Va al directorio 'home' del usuario actual.
cd -                        # Vuelve al directorio anterior en el que estuviste.

# ls (List)
# Lista el contenido de un directorio (archivos y subdirectorios).
ls                          # Lista el contenido del directorio actual.
ls /var/log                 # Lista el contenido del directorio /var/log.
ls -l                       # Lista en formato largo, mostrando permisos, propietario, tamaño, fecha de modificación, etc.
ls -a                       # Lista todos los archivos, incluyendo los ocultos (aquellos que empiezan con un punto '.').
ls -lh                      # Lista en formato largo y con tamaños legibles por humanos (KB, MB, GB).
ls -R                       # Lista recursivamente el contenido de los subdirectorios.
ls -t                       # Ordena los archivos por fecha de modificación (los más recientes primero).

# -------------------------
# MANIPULACIÓN DE ARCHIVOS Y DIRECTORIOS
# -------------------------

# touch [nombre_del_archivo]
# Crea un archivo vacío si no existe. Si existe, actualiza su fecha de modificación.
touch mi_archivo.txt

# mkdir (Make Directory)
# Crea uno o más directorios.
# mkdir [nombre_del_directorio]
mkdir nueva_carpeta
mkdir -p ruta/larga/de/varios/directorios # La opción -p crea directorios padres si no existen.

# cp (Copy)
# Copia archivos o directorios.
# cp [origen] [destino]
cp archivo_origen.txt archivo_copiado.txt  # Copia un archivo.
cp archivo.txt ./directorio_destino/      # Copia un archivo a un directorio.
cp -r directorio_origen/ directorio_copiado/ # Copia un directorio recursivamente (incluyendo su contenido).
                                         # La opción -i pregunta antes de sobrescribir.
                                         # La opción -v muestra lo que se está haciendo (verbose).

# mv (Move)
# Mueve o renombra archivos y directorios.
# mv [origen] [destino]
mv archivo_viejo.txt archivo_nuevo.txt    # Renombra un archivo.
mv archivo.txt ./directorio_destino/      # Mueve un archivo a un directorio.
mv directorio_origen/ nuevo_nombre_directorio/ # Renombra un directorio.
mv directorio_origen/ ./otro_lugar/       # Mueve un directorio a otra ubicación.

# rm (Remove)
# Elimina archivos o directorios. ¡USAR CON PRECAUCIÓN! Los archivos eliminados con rm generalmente no se pueden recuperar fácilmente.
# rm [archivo]
rm archivo_a_borrar.txt             # Elimina un archivo.
rm -f archivo_a_borrar.txt          # Fuerza la eliminación sin preguntar (force).
rm -r directorio_a_borrar/          # Elimina un directorio y todo su contenido recursivamente.
rm -rf directorio_a_borrar/         # Fuerza la eliminación recursiva de un directorio. ¡MUY PELIGROSO!

# rmdir (Remove Directory)
# Elimina directorios vacíos.
rmdir carpeta_vacia

# -------------------------
# VISUALIZACIÓN DE ARCHIVOS
# -------------------------

# cat (Concatenate)
# Muestra el contenido de uno o más archivos en la salida estándar (la terminal).
cat mi_archivo.txt
cat archivo1.txt archivo2.txt       # Muestra el contenido de archivo1 seguido de archivo2.
cat -n mi_archivo.txt               # Muestra el contenido con números de línea.

# less
# Muestra el contenido de un archivo página por página. Es más interactivo que 'cat'.
# Permite desplazarse hacia adelante y hacia atrás.
# Presiona 'q' para salir. Usa las flechas, RePág, AvPág para navegar. '/' para buscar.
less mi_largo_archivo.log

# more
# Similar a 'less', pero más antiguo y con menos funcionalidades. Muestra el contenido página por página.
# Presiona la barra espaciadora para avanzar, 'q' para salir.
more mi_otro_archivo.txt

# head
# Muestra las primeras líneas de un archivo (por defecto, las primeras 10).
head mi_archivo.txt
head -n 5 mi_archivo.txt            # Muestra las primeras 5 líneas.

# tail
# Muestra las últimas líneas de un archivo (por defecto, las últimas 10).
tail mi_archivo.txt
tail -n 5 mi_archivo.txt            # Muestra las últimas 5 líneas.
tail -f mi_archivo.log              # Muestra las últimas líneas y sigue mostrando las nuevas líneas que se añaden al archivo en tiempo real (muy útil para logs).

# -------------------------
# BÚSQUEDA DE ARCHIVOS Y TEXTO
# -------------------------

# find [ruta_de_búsqueda] -name "[patrón_nombre_archivo]"
# Busca archivos y directorios según diversos criterios.
find . -name "*.txt"                # Busca todos los archivos .txt en el directorio actual y subdirectorios.
find /home -name "documento.pdf"    # Busca el archivo 'documento.pdf' en /home y subdirectorios.
find / -type d -name "config"       # Busca directorios llamados 'config' desde la raíz.
find . -size +10M                   # Busca archivos mayores a 10MB en el directorio actual.
find . -mtime -7                    # Busca archivos modificados en los últimos 7 días.

# grep (Global Regular Expression Print)
# Busca patrones de texto dentro de archivos.
# grep "[patrón]" [archivo(s)]
grep "error" archivo.log            # Busca la palabra "error" en archivo.log.
grep -i "palabra" mi_archivo.txt    # Busca "palabra" ignorando mayúsculas/minúsculas (-i).
grep -r "texto_a_buscar" /ruta/directorio # Busca "texto_a_buscar" recursivamente (-r) en todos los archivos del directorio.
grep -v "excluir_esto" archivo.txt  # Muestra las líneas que NO contienen "excluir_esto" (-v).
grep -n "patrón" archivo.txt        # Muestra el número de línea donde se encuentra el patrón (-n).
ls -l | grep "drwxr-xr-x"         # Ejemplo de uso con tubería: filtra la salida de 'ls -l' para mostrar solo directorios.

# locate [nombre_archivo]
# Busca archivos utilizando una base de datos preconstruida (suele ser más rápido que 'find' para búsquedas simples por nombre).
# Es posible que necesites actualizar la base de datos con 'sudo updatedb'.
locate mi_documento.odt

# which [comando]
# Muestra la ruta completa del ejecutable de un comando.
which python
which ls

# whereis [comando]
# Localiza el binario, código fuente y página de manual para un comando.
whereis bash

# -------------------------
# PERMISOS DE ARCHIVOS
# -------------------------
# Los permisos en Linux se definen para tres tipos de usuarios:
# Propietario (user - u): El dueño del archivo.
# Grupo (group - g): Usuarios que pertenecen al mismo grupo que el archivo.
# Otros (others - o): Cualquier otro usuario.
# Y para cada tipo, tres tipos de permisos:
# Lectura (read - r): Permiso para leer el contenido del archivo.
# Escritura (write - w): Permiso para modificar el archivo.
# Ejecución (execute - x): Permiso para ejecutar el archivo (si es un script o programa) o acceder al directorio.

# chmod (Change Mode)
# Cambia los permisos de un archivo o directorio.
# Se puede usar notación octal (números) o simbólica (letras).
# Notación Octal: r=4, w=2, x=1. Se suman para cada categoría (propietario, grupo, otros).
# Ejemplo: 755 -> propietario=rwx (4+2+1=7), grupo=r-x (4+0+1=5), otros=r-x (4+0+1=5)
chmod 755 mi_script.sh              # Da permisos rwx para propietario, rx para grupo y otros.
chmod 644 mi_archivo.txt            # Da permisos rw para propietario, r para grupo y otros (común para archivos de texto).
chmod +x mi_script.sh               # Añade permiso de ejecución para todos (propietario, grupo, otros).
chmod u+x mi_script.sh              # Añade permiso de ejecución solo para el propietario.
chmod g-w mi_archivo.txt            # Quita permiso de escritura para el grupo.
chmod o=r mi_archivo.txt            # Establece permisos de solo lectura para otros.
chmod -R 600 ~/.ssh/                # Cambia permisos recursivamente para una carpeta (ej. para claves SSH).

# chown (Change Owner)
# Cambia el propietario y/o grupo de un archivo o directorio.
# chown [nuevo_propietario]:[nuevo_grupo] [archivo/directorio]
# Generalmente requiere privilegios de superusuario (sudo).
sudo chown nuevo_usuario mi_archivo.txt
sudo chown usuario:grupo_desarrollo script.pl
sudo chown -R juan:ventas /home/juan/documentos_ventas # Cambia propietario y grupo recursivamente.

# chgrp (Change Group)
# Cambia el grupo de un archivo o directorio.
# chgrp [nuevo_grupo] [archivo/directorio]
# Generalmente requiere privilegios de superusuario (sudo).
sudo chgrp desarrolladores mi_codigo.c

# -------------------------
# INFORMACIÓN DEL SISTEMA Y PROCESOS
# -------------------------

# uname
# Muestra información del sistema.
uname                       # Muestra el nombre del kernel (Linux).
uname -a                    # Muestra toda la información disponible (kernel, hostname, versión, etc.).
uname -r                    # Muestra la versión del kernel.

# hostname
# Muestra o establece el nombre de host del sistema.
hostname

# df (Disk Free)
# Muestra el espacio utilizado y disponible en los sistemas de archivos.
df
df -h                       # Muestra el espacio en formato legible por humanos (KB, MB, GB).
df -T                       # Muestra el tipo de sistema de archivos.

# du (Disk Usage)
# Muestra el espacio en disco utilizado por archivos y directorios.
du                          # Muestra el uso de disco del directorio actual y sus subdirectorios.
du -sh                      # Muestra el tamaño total del directorio actual en formato legible y resumido (-s).
du -h /var/log              # Muestra el tamaño de /var/log y sus contenidos en formato legible.
du -a                       # Muestra el tamaño de archivos individuales además de directorios.

# free
# Muestra la cantidad de memoria RAM y swap utilizada y disponible.
free
free -h                     # Muestra la memoria en formato legible por humanos.
free -m                     # Muestra la memoria en Megabytes.

# top
# Muestra una lista dinámica y en tiempo real de los procesos en ejecución.
# Es interactivo: 'q' para salir, 'k' para matar un proceso (pide PID), 'h' para ayuda.
top

# ps (Process Status)
# Muestra información sobre los procesos en ejecución.
ps                          # Muestra los procesos del usuario actual en la terminal actual.
ps aux                      # Muestra todos los procesos de todos los usuarios en formato detallado.
ps -ef                      # Similar a 'aux', formato estándar de System V.
ps -u miusuario             # Muestra los procesos del usuario 'miusuario'.
ps ax | grep "nombre_proceso" # Busca un proceso específico por nombre.

# kill [PID_del_proceso]
# Envía una señal a un proceso (por defecto, la señal TERM para terminarlo).
# El PID (Process ID) se puede obtener con 'ps' o 'top'.
kill 1234                   # Envía la señal TERM al proceso con PID 1234.
kill -9 1234                # Envía la señal KILL (SIGKILL), que fuerza la terminación del proceso (usar como último recurso).
kill -l                     # Lista todas las señales disponibles.

# pkill [nombre_del_proceso]
# Mata procesos basándose en su nombre u otros atributos.
pkill firefox

# killall [nombre_del_proceso]
# Mata todos los procesos con un nombre específico.
killall chrome

# jobs
# Muestra los trabajos (procesos) que se están ejecutando en segundo plano o están detenidos en la sesión actual.
# Un trabajo se puede enviar a segundo plano añadiendo '&' al final del comando: `comando &`
# O deteniendo un proceso en primer plano con Ctrl+Z.

# fg (Foreground)
# Trae un trabajo del segundo plano al primer plano.
# fg %[número_de_trabajo]
fg %1                       # Trae el trabajo número 1 al primer plano.

# bg (Background)
# Reanuda un trabajo detenido en segundo plano.
# bg %[número_de_trabajo]
bg %2                       # Reanuda el trabajo detenido número 2 en segundo plano.

# -------------------------
# GESTIÓN DE USUARIOS
# -------------------------

# whoami
# Muestra el nombre de usuario actual.
whoami

# who
# Muestra quién está conectado al sistema.
who
who -b                      # Muestra la hora del último arranque del sistema.

# w
# Muestra quién está conectado y qué está haciendo. Es una versión más detallada de 'who'.
w

# id [usuario]
# Muestra la información de UID (User ID), GID (Group ID) y grupos a los que pertenece un usuario.
id
id nombre_usuario

# su (Switch User)
# Cambia al superusuario (root) o a otro usuario.
# su
# (Pide la contraseña de root)
# su nombre_usuario
# (Pide la contraseña de nombre_usuario)
# su -
# (Cambia a root y carga su entorno completo, como si se hubiera logueado directamente como root)

# sudo [comando]
# Ejecuta un comando como superusuario (root) u otro usuario especificado en el archivo sudoers.
# Permite a usuarios autorizados ejecutar comandos como root sin necesidad de conocer la contraseña de root.
sudo apt update             # Ejemplo: actualiza la lista de paquetes (requiere privilegios de root).
sudo rm /archivo_protegido.txt

# adduser [nuevo_usuario] (Sistemas Debian/Ubuntu)
# Comando interactivo para añadir un nuevo usuario. Crea el directorio home, establece contraseña, etc.
# Requiere privilegios de superusuario.
sudo adduser juan

# useradd [nuevo_usuario] (Más genérico, menos interactivo)
# Añade un nuevo usuario. Puede requerir configurar manualmente el home, contraseña, etc.
# Requiere privilegios de superusuario.
sudo useradd pedro
sudo passwd pedro           # Para establecer la contraseña del nuevo usuario 'pedro'.

# usermod [opciones] [usuario]
# Modifica una cuenta de usuario existente.
# Requiere privilegios de superusuario.
sudo usermod -aG sudo juan  # Añade el usuario 'juan' al grupo 'sudo' (para permitirle usar sudo).
sudo usermod -l nuevo_nombre antiguo_nombre # Cambia el login name.
sudo usermod -d /nuevo/home -m usuario # Cambia el directorio home y mueve el contenido.

# deluser [usuario] (Sistemas Debian/Ubuntu)
# Elimina un usuario.
# Requiere privilegios de superusuario.
sudo deluser juan
sudo deluser --remove-home pedro # Elimina el usuario y su directorio home.

# userdel [usuario] (Más genérico)
# Elimina un usuario.
# Requiere privilegios de superusuario.
sudo userdel ana
sudo userdel -r luis        # Elimina el usuario y su directorio home y buzón de correo.

# passwd [usuario]
# Cambia la contraseña de un usuario.
passwd                      # Cambia la contraseña del usuario actual.
sudo passwd nombre_usuario  # Cambia la contraseña de 'nombre_usuario' (como root).

# -------------------------
# GESTIÓN DE RED
# -------------------------

# ip addr (o ip a)
# Muestra y manipula direcciones IP, interfaces de red. Reemplaza al antiguo 'ifconfig'.
ip addr show
ip a s eth0                 # Muestra información de la interfaz eth0.

# ip link
# Muestra y manipula el estado de las interfaces de red.
ip link show
sudo ip link set eth0 up    # Activa la interfaz eth0.
sudo ip link set eth0 down  # Desactiva la interfaz eth0.

# ip route
# Muestra y manipula la tabla de enrutamiento.
ip route show

# ping [host_o_IP]
# Envía paquetes ICMP ECHO_REQUEST a un host para comprobar la conectividad.
ping google.com
ping 8.8.8.8
ping -c 5 google.com        # Envía 5 paquetes y se detiene.

# netstat
# Muestra conexiones de red, tablas de enrutamiento, estadísticas de interfaces, etc. (puede estar obsoleto, 'ss' es el reemplazo).
netstat -tulnp              # Muestra todos los sockets TCP/UDP que están escuchando y los programas asociados.
                            # -t: TCP, -u: UDP, -l: listening, -n: numérico, -p: programa.

# ss (Socket Statistics)
# Herramienta para investigar sockets. Reemplaza a 'netstat'.
ss -tulnp                   # Similar a 'netstat -tulnp'.
ss -tan                     # Muestra todas las conexiones TCP activas.

# curl [URL]
# Herramienta para transferir datos desde o hacia un servidor, usando protocolos como HTTP, HTTPS, FTP, etc.
curl http://ejemplo.com
curl -O https://ejemplo.com/archivo.zip # Descarga el archivo y lo guarda con el mismo nombre.
curl -o nuevo_nombre.zip https://ejemplo.com/archivo.zip # Descarga y guarda con nombre 'nuevo_nombre.zip'.

# wget [URL]
# Herramienta para descargar archivos de la web de forma no interactiva.
wget https://www.kernel.org/pub/linux/kernel/v5.x/linux-5.10.tar.gz
wget -c [URL]               # Continúa una descarga interrumpida.

# ssh (Secure Shell)
# Permite conectarse de forma segura a un host remoto y ejecutar comandos.
# ssh [usuario]@[host_remoto]
ssh miusuario@192.168.1.100
ssh servidor.ejemplo.com -p 2222 # Conexión a un puerto diferente al 22 (por defecto).

# scp (Secure Copy)
# Copia archivos de forma segura entre hosts utilizando SSH.
# scp [origen] [destino]
scp archivo.txt usuario@host_remoto:/ruta/destino/
scp usuario@host_remoto:/ruta/archivo.txt ./directorio_local/
scp -r directorio/ usuario@host_remoto:/ruta/destino/ # Copia recursiva de un directorio.

# -------------------------
# COMPRESIÓN Y EMPAQUETADO
# -------------------------

# tar (Tape Archive)
# Utilidad para crear y extraer archivos .tar (archivos empaquetados, no necesariamente comprimidos).
# Comúnmente usado junto con gzip o bzip2 para compresión.
# -c : Crear un archivo.
# -x : Extraer de un archivo.
# -v : Modo verboso (muestra los archivos procesados).
# -f : Especifica el nombre del archivo (debe ir justo antes del nombre).
# -z : Comprimir/descomprimir con gzip (.tar.gz o .tgz).
# -j : Comprimir/descomprimir con bzip2 (.tar.bz2 o .tbz2).
# -J : Comprimir/descomprimir con xz (.tar.xz).

# Crear un archivo tar:
tar -cvf mi_archivo.tar /ruta/a/directorio_o_archivos
# Extraer un archivo tar:
tar -xvf mi_archivo.tar
tar -xvf mi_archivo.tar -C /ruta/de_extraccion # Extraer en un directorio específico.

# Crear un archivo tar comprimido con gzip:
tar -czvf mi_archivo.tar.gz /ruta/a/directorio
# Extraer un archivo tar.gz:
tar -xzvf mi_archivo.tar.gz

# Crear un archivo tar comprimido con bzip2:
tar -cjvf mi_archivo.tar.bz2 /ruta/a/directorio
# Extraer un archivo tar.bz2:
tar -xjvf mi_archivo.tar.bz2

# gzip [archivo]
# Comprime archivos usando el algoritmo Lempel-Ziv (LZ77). Crea un archivo .gz.
gzip mi_archivo.txt             # Crea mi_archivo.txt.gz y elimina el original.
gzip -k mi_archivo.txt          # Crea mi_archivo.txt.gz y conserva el original (-k).
gzip -d mi_archivo.txt.gz       # Descomprime mi_archivo.txt.gz (equivale a gunzip).

# gunzip [archivo.gz]
# Descomprime archivos .gz.
gunzip mi_archivo.txt.gz

# zip [archivo.zip] [archivos_a_comprimir]
# Empaqueta y comprime archivos en formato .zip.
zip mi_coleccion.zip archivo1.txt imagen.jpg directorio/
zip -r mi_completo.zip mi_directorio/ # Comprime un directorio recursivamente.

# unzip [archivo.zip]
# Descomprime archivos .zip.
unzip mi_coleccion.zip
unzip mi_archivo.zip -d /ruta/destino # Descomprime en un directorio específico.

# -------------------------
# OTROS COMANDOS ÚTILES
# -------------------------

# man [comando]
# Muestra la página del manual para un comando específico. Es la ayuda más completa.
# Presiona 'q' para salir.
man ls
man grep

# history
# Muestra el historial de comandos ejecutados en la sesión actual.
history
history 20                  # Muestra los últimos 20 comandos.
!n                          # Ejecuta el comando número 'n' del historial.
!!                          # Ejecuta el último comando.
!cadena                     # Ejecuta el último comando que comienza con 'cadena'.
Ctrl+R                      # Búsqueda inversa en el historial.

# alias [nombre_alias="comando"]
# Crea un atajo (alias) para un comando o una serie de comandos.
alias ll="ls -lh"             # Ahora 'll' ejecutará 'ls -lh'.
alias update="sudo apt update && sudo apt upgrade -y"
# Para hacer los alias permanentes, añádelos a ~/.bashrc o ~/.zshrc.
# Escribe 'alias' sin argumentos para ver los alias definidos.

# unalias [nombre_alias]
# Elimina un alias.
unalias ll

# echo "[texto]"
# Muestra una línea de texto o el valor de una variable.
echo "Hola Mundo"
echo $HOME                   # Muestra el valor de la variable de entorno HOME.
echo "El usuario es: $(whoami)" # Ejecuta el comando entre $( ) e inserta su salida.

# clear
# Limpia la pantalla de la terminal.

# exit
# Cierra la sesión actual de la terminal o sale de un script.
exit

# date
# Muestra o establece la fecha y hora del sistema.
date
date +"%Y-%m-%d %H:%M:%S"     # Muestra la fecha y hora en un formato específico.

# cal
# Muestra un calendario del mes actual.
cal
cal 2024                    # Muestra el calendario para el año 2024.
cal 12 2025                 # Muestra el calendario de Diciembre de 2025.

# sleep [segundos]
# Pausa la ejecución durante un número específico de segundos.
echo "Esperando 5 segundos..."
sleep 5
echo "Terminado."

# diff [archivo1] [archivo2]
# Compara dos archivos línea por línea y muestra las diferencias.
diff texto1.txt texto2.txt
diff -u archivo_original.c archivo_modificado.c # Muestra diferencias en formato unificado (útil para parches).

# sort [archivo]
# Ordena las líneas de un archivo de texto.
sort mi_lista.txt
sort -r mi_lista.txt        # Ordena en orden inverso (-r).
sort -n numeros.txt         # Ordena numéricamente (-n).
sort -u mi_lista.txt        # Ordena y elimina líneas duplicadas (-u).

# wc (Word Count)
# Cuenta líneas, palabras y caracteres en un archivo.
wc mi_documento.txt
wc -l mi_documento.txt      # Cuenta solo líneas (-l).
wc -w mi_documento.txt      # Cuenta solo palabras (-w).
wc -c mi_documento.txt      # Cuenta solo bytes (-c).
wc -m mi_documento.txt      # Cuenta solo caracteres (-m, puede diferir de -c con caracteres multibyte).

# tee [archivo]
# Lee de la entrada estándar y escribe tanto en la salida estándar como en uno o más archivos.
# Útil para ver la salida de un comando y guardarla en un archivo al mismo tiempo.
ls -l | tee listado_archivos.txt
echo "Esto es una prueba" | tee prueba.txt
cat archivo_entrada.txt | tee archivo_salida1.txt archivo_salida2.txt > /dev/null # Solo guarda en archivos, no muestra en pantalla.

# uptime
# Muestra cuánto tiempo ha estado funcionando el sistema desde el último arranque,
# el número de usuarios conectados y la carga promedio del sistema.
uptime

# shutdown [opciones] [tiempo] [mensaje]
# Apaga o reinicia el sistema. Requiere privilegios de superusuario.
# sudo shutdown now             # Apaga inmediatamente.
# sudo shutdown -h now          # Similar a 'now', apaga (halt).
# sudo shutdown -r now          # Reinicia inmediatamente.
# sudo shutdown -h +10 "El sistema se apagará en 10 minutos" # Apaga en 10 minutos con un mensaje.
# sudo shutdown -r 22:00        # Reinicia a las 10:00 PM.
# sudo shutdown -c              # Cancela un apagado programado.

# reboot
# Reinicia el sistema. Generalmente es un enlace a 'shutdown -r now'. Requiere privilegios de superusuario.
# sudo reboot

# halt
# Detiene el sistema. Generalmente es un enlace a 'shutdown -h now'. Requiere privilegios de superusuario.
# sudo halt

# poweroff
# Apaga el sistema y corta la energía (si el hardware lo soporta). Requiere privilegios de superusuario.
# sudo poweroff

# -------------------------
# REDIRECCIONES Y TUBERÍAS (PIPES)
# -------------------------

# > (Redirección de salida)
# Redirige la salida estándar (stdout) de un comando a un archivo. Sobrescribe el archivo si existe.
ls -l > lista_archivos.txt

# >> (Redirección de salida - añadir)
# Redirige la salida estándar (stdout) de un comando a un archivo. Añade la salida al final del archivo si existe, o lo crea si no.
echo "Nueva línea de log" >> mi_log.txt

# < (Redirección de entrada)
# Redirige la entrada estándar (stdin) de un comando para que la tome de un archivo en lugar del teclado.
sort < lista_desordenada.txt

# 2> (Redirección de error estándar)
# Redirige la salida de error estándar (stderr) a un archivo. Sobrescribe el archivo si existe.
comando_que_falla 2> errores.txt

# 2>> (Redirección de error estándar - añadir)
# Redirige la salida de error estándar (stderr) a un archivo. Añade la salida al final del archivo si existe.
comando_que_falla_mucho 2>> todos_los_errores.log

# &> (Redirección de stdout y stderr) o >&
# Redirige tanto la salida estándar (stdout) como la salida de error estándar (stderr) al mismo archivo. Sobrescribe.
comando_completo &> salida_y_errores.txt
# Otra forma (más antigua pero común): comando_completo > salida_y_errores.txt 2>&1

# | (Tubería - Pipe)
# Envía la salida estándar (stdout) de un comando como entrada estándar (stdin) de otro comando.
# Permite encadenar comandos para procesar datos de forma secuencial.
ls -l | grep ".txt"             # Lista archivos y filtra solo los que contienen ".txt".
cat /var/log/syslog | grep -i "error" | wc -l # Cuenta cuántas líneas contienen "error" (ignorando caso) en el syslog.
ps aux | sort -nk 3             # Muestra procesos y los ordena por la tercera columna (uso de CPU) numéricamente.

# -------------------------
# VARIABLES DE ENTORNO
# -------------------------

# printenv
# Muestra todas las variables de entorno.
printenv
printenv HOME               # Muestra el valor de la variable HOME.

# export [NOMBRE_VARIABLE="valor"]
# Define una variable de entorno para la sesión actual y para los procesos hijos que se ejecuten desde ella.
export MI_VARIABLE="Hola desde la terminal"
echo $MI_VARIABLE
# Para hacerla permanente, añádela a ~/.bashrc o ~/.profile (o ~/.zshrc si usas zsh).

# unset [NOMBRE_VARIABLE]
# Elimina una variable de entorno de la sesión actual.
unset MI_VARIABLE

# Ejemplos de variables de entorno comunes:
# $HOME: Directorio home del usuario actual.
# $PATH: Lista de directorios donde el shell busca los comandos ejecutables.
# $USER: Nombre del usuario actual.
# $SHELL: El shell por defecto del usuario.
# $PWD: Directorio de trabajo actual.
# $LANG: Configuración regional y de idioma.
# $TERM: Tipo de terminal que se está utilizando.

# -------------------------
# CONTROL DE TRABAJO (Recordatorio de jobs, fg, bg, & y Ctrl+Z)
# -------------------------
# comando &                   # Ejecuta un comando en segundo plano (background).
# Ctrl+Z                      # Detiene (suspende) el proceso que se está ejecutando en primer plano (foreground).
# jobs                        # Lista los trabajos activos (en segundo plano o detenidos).
# fg %[numero_trabajo]        # Trae un trabajo al primer plano. Si no se especifica número, trae el más reciente.
# bg %[numero_trabajo]        # Reanuda un trabajo detenido en segundo plano. Si no se especifica número, reanuda el más reciente.

# -------------------------
# ATAJOS DE TECLADO ÚTILES EN LA TERMINAL (Bash/Zsh)
# -------------------------
# Ctrl+C                      # Termina (interrumpe) el comando actual.
# Ctrl+D                      # Cierra la terminal, o envía EOF (End Of File) si la entrada está vacía.
# Ctrl+L                      # Limpia la pantalla (similar a 'clear').
# Ctrl+A                      # Mueve el cursor al inicio de la línea.
# Ctrl+E                      # Mueve el cursor al final de la línea.
# Ctrl+U                      # Borra desde el cursor hasta el inicio de la línea.
# Ctrl+K                      # Borra desde el cursor hasta el final de la línea.
# Ctrl+W                      # Borra la palabra anterior al cursor.
# Ctrl+Y                      # Pega el texto borrado recientemente (con Ctrl+U, Ctrl+K, Ctrl+W).
# Ctrl+R                      # Búsqueda inversa en el historial de comandos. Empieza a escribir y autocompleta.
# Ctrl+S                      # Pausa la salida a la terminal (XOFF). ¡CUIDADO! Puede parecer que la terminal se congela.
# Ctrl+Q                      # Reanuda la salida a la terminal (XON), después de Ctrl+S.
# Ctrl+Z                      # Suspende el proceso actual (lo envía a segundo plano, detenido). Ver 'jobs', 'fg', 'bg'.
# Tab                         # Autocompleta nombres de comandos, archivos o directorios. Pulsar dos veces muestra opciones.
# Flecha Arriba/Abajo         # Navega por el historial de comandos.
# Alt+B                       # Mueve el cursor una palabra hacia atrás.
# Alt+F                       # Mueve el cursor una palabra hacia adelante.
# Alt+D                       # Borra la palabra siguiente al cursor.
# Shift+RePág (PageUp)        # Desplaza la salida de la terminal hacia arriba.
# Shift+AvPág (PageDown)      # Desplaza la salida de la terminal hacia abajo.

# -------------------------
# FIN DE LOS APUNTES
# -------------------------
# Recuerda que la mejor forma de aprender es practicar.
# Usa 'man [comando]' para obtener información detallada de cada comando.
# ¡Explora y experimenta! (con precaución, especialmente con comandos como 'rm' o 'sudo').