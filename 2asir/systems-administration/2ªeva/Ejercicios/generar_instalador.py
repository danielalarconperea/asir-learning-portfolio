#!/bin/bash
cat << 'EOF' > install_scripts.sh
#!/bin/bash

mkdir -p "1-Ejercicios basicos"

echo "Creando 1-Ejercicios basicos/10_tama_dir.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/10_tama_dir.sh"
#!/bin/bash
# Ejercicio 10: tama_dir.sh
# Pide un usuario y muestra el tamaño de su directorio de conexión.

read -p "Introduce el nombre del usuario: " USUARIO

# Buscamos el home del usuario en /etc/passwd por si no está en /home/
HOMEDIR=$(grep "^$USUARIO:" /etc/passwd | cut -d: -f6)

if [ -z "$HOMEDIR" ]; then
    echo "El usuario $USUARIO no existe."
elif [ ! -d "$HOMEDIR" ]; then
    echo "El directorio $HOMEDIR no existe."
else
    echo "Calculando el tamaño de $HOMEDIR..."
    du -sh "$HOMEDIR"
fi

SH_EOF
chmod +x "1-Ejercicios basicos/10_tama_dir.sh"

echo "Creando 1-Ejercicios basicos/11_grupos_usu.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/11_grupos_usu.sh"
#!/bin/bash
# Ejercicio 11: grupos_usu.sh
# Pide un usuario y muestra los grupos a los que pertenece (uno en cada línea).

read -p "Introduce el nombre del usuario: " USUARIO

if id "$USUARIO" >/dev/null 2>&1; then
    echo "Grupos del usuario $USUARIO:"
    groups "$USUARIO" | cut -d: -f2 | tr ' ' '\n' | grep -v '^$'
else
    echo "El usuario $USUARIO no existe."
fi

SH_EOF
chmod +x "1-Ejercicios basicos/11_grupos_usu.sh"

echo "Creando 1-Ejercicios basicos/12_usu_grupo.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/12_usu_grupo.sh"
#!/bin/bash
# Ejercicio 12: usu_grupo.sh
# Pide un grupo y muestra los usuarios que pertenecen a él (separados por ';').

read -p "Introduce el nombre del grupo: " GRUPO

# Obtenemos los usuarios secundarios del archivo /etc/group
USUARIOS=$(grep "^$GRUPO:" /etc/group | cut -d: -f4 | tr ',' ';')

if [ -z "$(grep "^$GRUPO:" /etc/group)" ]; then
    echo "El grupo $GRUPO no existe."
elif [ -z "$USUARIOS" ]; then
    echo "El grupo $GRUPO no tiene usuarios secundarios definidos."
else
    echo "Usuarios en el grupo $GRUPO: $USUARIOS"
fi

SH_EOF
chmod +x "1-Ejercicios basicos/12_usu_grupo.sh"

echo "Creando 1-Ejercicios basicos/13_nuevos.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/13_nuevos.sh"
#!/bin/bash
# Ejercicio 13: nuevos.sh
# Pide un número de días y muestra archivos modificados en ese periodo (posteriores a ese día).

read -p "Introduce el número de días (ficheros modificados en los últimos N días): " DIAS

echo "Buscando ficheros modificados en los últimos $DIAS días en el directorio actual..."
find . -maxdepth 2 -mtime -"$DIAS" -type f

SH_EOF
chmod +x "1-Ejercicios basicos/13_nuevos.sh"

echo "Creando 1-Ejercicios basicos/14_cron_usuario.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/14_cron_usuario.sh"
#!/bin/bash
# Ejercicio 14: cron_usuario.sh
# Pide un usuario y muestra su crontab. Requiere permisos para ver crontabs de otros.

read -p "Introduce el nombre del usuario: " USUARIO

if id "$USUARIO" >/dev/null 2>&1; then
    echo "Mostrando crontab de $USUARIO:"
    sudo crontab -u "$USUARIO" -l 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "No se ha podido leer el crontab (puede que no tenga o falten permisos de sudo)."
    fi
else
    echo "El usuario $USUARIO no existe."
fi

SH_EOF
chmod +x "1-Ejercicios basicos/14_cron_usuario.sh"

echo "Creando 1-Ejercicios basicos/15_calc_para.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/15_calc_para.sh"
#!/bin/bash
# Ejercicio 15: calc_para.sh
# Recibe dos números por parámetro y muestra resultados.

if [ $# -ne 2 ]; then
    echo "Uso: $0 numero1 numero2"
    exit 1
fi

NUM1=$1
NUM2=$2

echo "Suma: $((NUM1 + NUM2))"
echo "Resta: $((NUM1 - NUM2))"
echo "Multiplicación: $((NUM1 * NUM2))"
[ $NUM2 -ne 0 ] && echo "División: $((NUM1 / NUM2))" || echo "División: Error"

SH_EOF
chmod +x "1-Ejercicios basicos/15_calc_para.sh"

echo "Creando 1-Ejercicios basicos/15_hola_para.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/15_hola_para.sh"
#!/bin/bash
# Ejercicio 15: hola_para.sh
# Recibe un nombre por parámetro.

if [ -z "$1" ]; then
    echo "Uso: $0 nombre"
    exit 1
fi

echo "¡Hola $1!"

SH_EOF
chmod +x "1-Ejercicios basicos/15_hola_para.sh"

echo "Creando 1-Ejercicios basicos/16_pon_numeros.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/16_pon_numeros.sh"
#!/bin/bash
# Ejercicio 16: pon_numeros.sh
# Recibe un fichero y muestra sus líneas numeradas.

if [ -z "$1" ] || [ ! -f "$1" ]; then
    echo "Uso: $0 nombre_fichero"
    exit 1
fi

nl -ba "$1"
# O alternativamente: cat -n "$1"

SH_EOF
chmod +x "1-Ejercicios basicos/16_pon_numeros.sh"

echo "Creando 1-Ejercicios basicos/17_busca_fichero.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/17_busca_fichero.sh"
#!/bin/bash
# Ejercicio 17: busca_fichero.sh
# Recoge un nombre de fichero y lo busca en todo el sistema.

if [ -z "$1" ]; then
    echo "Uso: $0 nombre_fichero"
    exit 1
fi

echo "Buscando '$1' en todo el sistema (puede tardar y mostrar errores de permisos)..."
find / -name "$1" 2>/dev/null

SH_EOF
chmod +x "1-Ejercicios basicos/17_busca_fichero.sh"

echo "Creando 1-Ejercicios basicos/18_ejecutar.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/18_ejecutar.sh"
#!/bin/bash
# Ejercicio 18: ejecutar.sh
# Añade permisos de ejecución a un fichero pasado por parámetro.

if [ -z "$1" ] || [ ! -e "$1" ]; then
    echo "Uso: $0 nombre_fichero"
    exit 1
fi

chmod +x "$1"
echo "Permisos de ejecución añadidos a '$1'."
ls -l "$1"

SH_EOF
chmod +x "1-Ejercicios basicos/18_ejecutar.sh"

echo "Creando 1-Ejercicios basicos/1_config_path.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/1_config_path.sh"
#!/bin/bash
# Ejercicio 1: Añadir PATH a .bashrc
# Este script añade el directorio de ejercicios al PATH en .bashrc para que los scripts 
# se puedan ejecutar desde cualquier lugar.

EJERCICIOS_DIR="$HOME/ejercicios"

# Comprobamos si ya está en el .bashrc
if grep -q "$EJERCICIOS_DIR" "$HOME/.bashrc"; then
    echo "El directorio ya está en el PATH de .bashrc"
else
    echo "export PATH=\$PATH:$EJERCICIOS_DIR" >> "$HOME/.bashrc"
    echo "Directorio añadido al PATH en .bashrc. Reinicia la shell o ejecuta 'source ~/.bashrc'"
fi

SH_EOF
chmod +x "1-Ejercicios basicos/1_config_path.sh"

echo "Creando 1-Ejercicios basicos/2_usuarios.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/2_usuarios.sh"
#!/bin/bash
# Ejercicio 2: usuarios.sh
# Muestra la lista de usuarios reales (no del sistema).
# Normalmente los usuarios reales tienen un UID >= 1000.

echo "Usuarios reales en el sistema (UID >= 1000):"
awk -F: '$3 >= 1000 && $1 != "nobody" {print $1}' /etc/passwd

SH_EOF
chmod +x "1-Ejercicios basicos/2_usuarios.sh"

echo "Creando 1-Ejercicios basicos/3_quiensoy.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/3_quiensoy.sh"
#!/bin/bash
# Ejercicio 3: quiensoy.sh
# Muestra el usuario actual, su HOME y datos de caducidad.

USUARIO=$(whoami)
echo "Usuario actual: $USUARIO"
echo "Directorio de conexión: $HOME"

# chage -l requiere permisos de root para ver otros, o siendo el propio usuario para verse a sí mismo.
echo "Datos de caducidad de la contraseña y del usuario:"
chage -l "$USUARIO"

SH_EOF
chmod +x "1-Ejercicios basicos/3_quiensoy.sh"

echo "Creando 1-Ejercicios basicos/4_dimecron.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/4_dimecron.sh"
#!/bin/bash
# Ejercicio 4: dimecron.sh
# Muestra las configuraciones activas del cron del usuario actual, sin comentarios.

echo "Tareas programadas en CRON (activas):"
crontab -l 2>/dev/null | grep -v '^#' | grep -v '^$'
if [ $? -ne 0 ]; then
    echo "No hay tareas programadas o el comando crontab no está disponible."
fi

SH_EOF
chmod +x "1-Ejercicios basicos/4_dimecron.sh"

echo "Creando 1-Ejercicios basicos/5_numusu.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/5_numusu.sh"
#!/bin/bash
# Ejercicio 5: numusu.sh
# Muestra cuántos usuarios hay conectados en el sistema actualmente.

TOTAL=$(who | wc -l)
echo "Actualmente hay $TOTAL usuarios conectados al sistema."

SH_EOF
chmod +x "1-Ejercicios basicos/5_numusu.sh"

echo "Creando 1-Ejercicios basicos/6_masmemoria.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/6_masmemoria.sh"
#!/bin/bash
# Ejercicio 6: masmemoria.sh
# Muestra los 3 procesos que más memoria consumen.

echo "Top 3 procesos con más consumo de memoria:"
ps aux --sort=-%mem | head -n 4 | tail -n 3
# Usamos head -n 4 para incluir la cabecera y los 3 primeros, luego tail -n 3 para descartar la cabecera si se desea solo los datos.

SH_EOF
chmod +x "1-Ejercicios basicos/6_masmemoria.sh"

echo "Creando 1-Ejercicios basicos/7_modi_cron.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/7_modi_cron.sh"
#!/bin/bash
# Ejercicio 7: modi_cron.sh
# Muestra cuántas veces se ha modificado el cron y las fechas/horas.
# Nota: Esto busca en los logs del sistema, los cuales suelen requerir permisos de root.

LOG_FILE="/var/log/syslog"
[ ! -f "$LOG_FILE" ] && LOG_FILE="/var/log/cron"

if [ ! -r "$LOG_FILE" ]; then
    echo "Error: No se puede leer el archivo de log ($LOG_FILE). ¿Tienes permisos?"
    exit 1
fi

MODS=$(grep "crontab" "$LOG_FILE" | grep -E "REPLACE|EDIT" | wc -l)
echo "El cron se ha modificado $MODS veces desde el último rotado de logs."
echo "Detalle de las modificaciones:"
grep "crontab" "$LOG_FILE" | grep -E "REPLACE|EDIT" | awk '{print $1, $2, $3}'
# Dependiendo del sistema, el formato del log puede variar.
# Este script asume un formato estándar de syslog.

SH_EOF
chmod +x "1-Ejercicios basicos/7_modi_cron.sh"

echo "Creando 1-Ejercicios basicos/8_hola.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/8_hola.sh"
#!/bin/bash
# Ejercicio 8: hola.sh
# Pide un nombre de usuario por teclado y lo saluda.

read -p "Introduce tu nombre: " NOMBRE
echo "¡Hola $NOMBRE! Bienvenido al sistema."

SH_EOF
chmod +x "1-Ejercicios basicos/8_hola.sh"

echo "Creando 1-Ejercicios basicos/9_calc.sh..."
cat << 'SH_EOF' > "1-Ejercicios basicos/9_calc.sh"
#!/bin/bash
# Ejercicio 9: calc.sh
# Pide dos números y muestra resultados de suma, resta, multiplicación y división.

read -p "Introduce el primer número: " NUM1
read -p "Introduce el segundo número: " NUM2

echo "Suma: $((NUM1 + NUM2))"
echo "Resta: $((NUM1 - NUM2))"
echo "Multiplicación: $((NUM1 * NUM2))"

if [ $NUM2 -ne 0 ]; then
    echo "División: $((NUM1 / NUM2))"
else
    echo "División: Error (división por cero)"
fi

SH_EOF
chmod +x "1-Ejercicios basicos/9_calc.sh"

mkdir -p "2-Ejercicios avanzados"

echo "Creando 2-Ejercicios avanzados/10_check_bin.sh..."
cat << 'SH_EOF' > "2-Ejercicios avanzados/10_check_bin.sh"
#!/bin/bash
# Ejercicio 10 Avanzado: Comprobar ~/bin y añadir al PATH.

BIN_DIR="$HOME/bin"

if [ ! -d "$BIN_DIR" ]; then
    echo "El directorio $BIN_DIR no existe. Creándolo..."
    mkdir -p "$BIN_DIR"
else
    echo "El directorio $BIN_DIR ya existe."
fi

# Comprobar si ya está en el PATH
if [[ ":$PATH:" == *":$BIN_DIR:"* ]]; then
    echo "El directorio ya está en el PATH."
else
    echo "Añadiendo $BIN_DIR al PATH en .bashrc..."
    echo 'export PATH="$HOME/bin:$PATH"' >> "$HOME/.bashrc"
    echo "Añadido. Abre una nueva shell para aplicar los cambios."
fi

SH_EOF
chmod +x "2-Ejercicios avanzados/10_check_bin.sh"

echo "Creando 2-Ejercicios avanzados/11_donde_esta.sh..."
cat << 'SH_EOF' > "2-Ejercicios avanzados/11_donde_esta.sh"
#!/bin/bash
# Ejercicio 11 Avanzado: Buscar ficheros y mostrar rutas absolutas de sus directorios.

if [ $# -eq 0 ]; then
    echo "Uso: $0 fichero1 fichero2..."
    exit 1
fi

for FICHERO in "$@"; do
    echo "Buscando '$FICHERO'..."
    RUTAS=$(find / -name "$FICHERO" 2>/dev/null)
    
    if [ -z "$RUTAS" ]; then
        echo "El archivo ordinario $FICHERO no se encuentra en el sistema."
    else
        echo "El archivo ordinario $FICHERO se encuentra en los directorios:"
        for RUTA in $RUTAS; do
            DIRNAME=$(dirname "$RUTA")
            # Convertimos a ruta absoluta si no lo es (aunque find / ya da absolutas)
            readlink -f "$DIRNAME"
        done
    fi
    echo ""
done

SH_EOF
chmod +x "2-Ejercicios avanzados/11_donde_esta.sh"

echo "Creando 2-Ejercicios avanzados/12_calendario.sh..."
cat << 'SH_EOF' > "2-Ejercicios avanzados/12_calendario.sh"
#!/bin/bash
# Ejercicio 12 Avanzado: Script calendario.

DIA=$(date +%d)
MES=$(date +%m)
ANIO=$(date +%Y)

if [ $# -eq 0 ]; then
    cal
    exit 0
fi

if [ $# -ne 1 ]; then
    echo "Sólo se admite un parámetro."
    exit 1
fi

case $1 in
    -c|--corta)
        echo "$DIA/$MES/$ANIO"
        ;;
    -l|--larga)
        echo "Hoy es el día '$DIA' del mes '$MES' del año '$ANIO'."
        ;;
    *)
        echo "Opción incorrecta."
        exit 2
        ;;
esac

SH_EOF
chmod +x "2-Ejercicios avanzados/12_calendario.sh"

echo "Creando 2-Ejercicios avanzados/13_citas.sh..."
cat << 'SH_EOF' > "2-Ejercicios avanzados/13_citas.sh"
#!/bin/bash
# Ejercicio 13 Avanzado: Gestión de citas médicas.
# Archivo de datos: citas_db.txt

DB="citas_db.txt"
[ ! -f "$DB" ] && touch "$DB"

mostrar_ayuda() {
    echo "Uso: $0 [OPCIÓN]"
    echo "  -h, --help    Muestra esta ayuda."
    echo "  -a, --add H_INI H_FIN NOMBRE  Añade una cita."
    echo "  -s, --search PATRON           Busca pacientes por patrón."
    echo "  -i, --init H_INI              Busca citas por hora de inicio."
    echo "  -e, --end H_FIN               Busca citas por hora de fin."
    echo "  -n, --name                    Lista citas ordenadas por nombre."
    echo "  -o, --hour                    Lista citas ordenadas por hora."
}

if [ $# -eq 0 ]; then mostrar_ayuda; exit 0; fi

case $1 in
    -h|--help) mostrar_ayuda ;;
    -a|--add)
        if [ $# -ne 4 ]; then echo "Error: Faltan parámetros."; exit 1; fi
        H_INI=$2; H_FIN=$3; NOMBRE=$4
        
        # Validar horas
        if ! [[ "$H_INI" =~ ^[0-9]{2}$ ]] || ! [[ "$H_FIN" =~ ^[0-9]{2}$ ]]; then echo "Error: Formato HORA incorrecto (00-23)."; exit 1; fi
        if [ "$H_INI" -lt 0 ] || [ "$H_INI" -gt 23 ] || [ "$H_FIN" -lt 0 ] || [ "$H_FIN" -gt 23 ]; then echo "Error: Hora fuera de rango."; exit 1; fi
        
        # Comprobar nombre repetido
        if grep -q ":$NOMBRE$" "$DB"; then echo "Error: El paciente ya tiene una cita."; exit 1; fi
        
        # Comprobar solapamiento
        # Formato: start:end:name
        while IFS=: read -r s e n; do
            if [ "$H_INI" -lt "$e" ] && [ "$H_FIN" -gt "$s" ]; then
                echo "Error: La cita se solapa con la de $n ($s-$e)."
                exit 1
            fi
        done < "$DB"
        
        echo "$H_INI:$H_FIN:$NOMBRE" >> "$DB"
        echo "Cita añadida con éxito."
        ;;
    -s|--search)
        grep "$2" "$DB" || echo "No se encontraron resultados."
        ;;
    -i|--init)
        grep "^$2:" "$DB" || echo "No hay citas que empiecen a esa hora."
        ;;
    -e|--end)
        grep ":$2:" "$DB" || echo "No hay citas que terminen a esa hora."
        ;;
    -n|--name)
        sort -t: -k3 "$DB" | tr ':' '\t'
        ;;
    -o|--hour)
        sort -t: -k1 "$DB" | tr ':' '\t'
        ;;
    *)
        echo "Opción no reconocida."
        mostrar_ayuda
        ;;
esac

SH_EOF
chmod +x "2-Ejercicios avanzados/13_citas.sh"

echo "Creando 2-Ejercicios avanzados/14_citas-menu.sh..."
cat << 'SH_EOF' > "2-Ejercicios avanzados/14_citas-menu.sh"
#!/bin/bash
# Ejercicio 14 Avanzado: Menú interactivo para el script de citas.

SCRIPT="./citas.sh"

while true; do
    echo "--- MENÚ DE CITAS MÉDICAS ---"
    echo "1. Añadir cita nueva"
    echo "2. Buscar por nombre de paciente"
    echo "3. Buscar por hora inicial"
    echo "4. Buscar por hora final"
    echo "5. Listar citas por nombre"
    echo "6. Listar citas por hora"
    echo "7. Salir"
    read -p "Opción: " OPC

    case $OPC in
        1)
            read -p "Hora inicio (00-23): " HI
            read -p "Hora fin (00-23): " HF
            read -p "Nombre paciente: " NOM
            bash $SCRIPT --add "$HI" "$HF" "$NOM"
            ;;
        2)
            read -p "Patrón a buscar: " PAT
            bash $SCRIPT --search "$PAT"
            ;;
        3)
            read -p "Hora de inicio: " HI
            bash $SCRIPT --init "$HI"
            ;;
        4)
            read -p "Hora de fin: " HF
            bash $SCRIPT --end "$HF"
            ;;
        5)
            bash $SCRIPT --name
            ;;
        6)
            bash $SCRIPT --hour
            ;;
        7)
            break
            ;;
        *)
            echo "Opción no válida."
            ;;
    esac
    echo ""
done

SH_EOF
chmod +x "2-Ejercicios avanzados/14_citas-menu.sh"

echo "Creando 2-Ejercicios avanzados/1_control_params.sh..."
cat << 'SH_EOF' > "2-Ejercicios avanzados/1_control_params.sh"
#!/bin/bash
# Ejercicio 1 Avanzado: Calculadora con control de parámetros.
# Si no se pasan parámetros, los pide por teclado.

NUM1=$1
NUM2=$2

if [ -z "$NUM1" ]; then
    read -p "No indicaste el primer número. Introdúcelo ahora: " NUM1
fi

if [ -z "$NUM2" ]; then
    read -p "No indicaste el segundo número. Introdúcelo ahora: " NUM2
fi

# Validar que son números
if ! [[ "$NUM1" =~ ^[0-9]+$ ]] || ! [[ "$NUM2" =~ ^[0-9]+$ ]]; then
    echo "Error: Ambos parámetros deben ser números."
    exit 1
fi

echo "Suma: $((NUM1 + NUM2))"
echo "Resta: $((NUM1 - NUM2))"
echo "Multiplicación: $((NUM1 * NUM2))"
[ $NUM2 -ne 0 ] && echo "División: $((NUM1 / NUM2))" || echo "División: Error"

SH_EOF
chmod +x "2-Ejercicios avanzados/1_control_params.sh"

echo "Creando 2-Ejercicios avanzados/2_comparar.sh..."
cat << 'SH_EOF' > "2-Ejercicios avanzados/2_comparar.sh"
#!/bin/bash
# Ejercicio 2 Avanzado: Comparar dos números.

read -p "Número 1: " N1
read -p "Número 2: " N2

if [ "$N1" -eq "$N2" ]; then
    echo "Los números son iguales."
elif [ "$N1" -gt "$N2" ]; then
    echo "$N1 es mayor que $N2."
else
    echo "$N2 es mayor que $N1."
fi

SH_EOF
chmod +x "2-Ejercicios avanzados/2_comparar.sh"

echo "Creando 2-Ejercicios avanzados/3_existe_usuario.sh..."
cat << 'SH_EOF' > "2-Ejercicios avanzados/3_existe_usuario.sh"
#!/bin/bash
# Ejercicio 3 Avanzado: Comprobar si un usuario existe.

USUARIO=$1
if [ -z "$USUARIO" ]; then
    read -p "Introduce el nombre del usuario a comprobar: " USUARIO
fi

if id "$USUARIO" >/dev/null 2>&1; then
    echo "El usuario '$USUARIO' SÍ existe en el sistema."
else
    echo "El usuario '$USUARIO' NO existe."
fi

SH_EOF
chmod +x "2-Ejercicios avanzados/3_existe_usuario.sh"

echo "Creando 2-Ejercicios avanzados/4_grupos_compartidos.sh..."
cat << 'SH_EOF' > "2-Ejercicios avanzados/4_grupos_compartidos.sh"
#!/bin/bash
# Ejercicio 4 Avanzado: Grupos comunes a varios usuarios.
# Uso: ./grupos_compartidos.sh user1 user2 user3...

if [ $# -lt 2 ]; then
    echo "Se necesitan al menos 2 usuarios para comparar."
    exit 1
fi

# Inicializamos con los grupos del primer usuario
COMUNES=$(id -Gn "$1" | tr ' ' '\n')

shift # Pasamos al siguiente

for USU in "$@"; do
    if ! id "$USU" >/dev/null 2>&1; then
        echo "Usuario $USU no existe. Saltando..."
        continue
    fi
    GRUPOS_USU=$(id -Gn "$USU" | tr ' ' '\n')
    # Actualizamos la intersección
    COMUNES=$(echo -e "$COMUNES\n$GRUPOS_USU" | sort | uniq -d)
done

if [ -z "$COMUNES" ]; then
    echo "No hay grupos comunes entre los usuarios indicados."
else
    echo "Grupos compartidos por todos los usuarios:"
    echo "$COMUNES"
fi

SH_EOF
chmod +x "2-Ejercicios avanzados/4_grupos_compartidos.sh"

echo "Creando 2-Ejercicios avanzados/5_menu_usuarios.sh..."
cat << 'SH_EOF' > "2-Ejercicios avanzados/5_menu_usuarios.sh"
#!/bin/bash
# Ejercicio 5 Avanzado: Menú de gestión de usuarios y grupos.

while true; do
    echo "--- MENÚ DE USUARIOS ---"
    echo "1. Listar usuarios de mi grupo"
    echo "2. Usuarios de mi grupo + directorio Home"
    echo "3. Listado de grupos y número de usuarios"
    echo "4. Salir"
    read -p "Opción: " OPCION

    MI_GRUPO_ID=$(id -g)
    MI_GRUPO_NOMBRE=$(id -gn)

    case $OPCION in
        1)
            echo "Usuarios del grupo $MI_GRUPO_NOMBRE:"
            grep ":$MI_GRUPO_ID:" /etc/passwd | cut -d: -f1
            ;;
        2)
            echo "Usuarios del grupo $MI_GRUPO_NOMBRE y sus Homes:"
            grep ":$MI_GRUPO_ID:" /etc/passwd | cut -d: -f1,6 | tr ':' '\t'
            ;;
        3)
            echo "Listado de grupos y cantidad de usuarios:"
            while IFS=: read -r gname gpass gid gmembers; do
                # Usuarios primarios (en /etc/passwd)
                C1=$(grep -c ":$gid:" /etc/passwd)
                # Usuarios secundarios (en /etc/group)
                if [ -n "$gmembers" ]; then
                    C2=$(echo "$gmembers" | tr ',' '\n' | wc -l)
                else
                    C2=0
                fi
                echo "Grupo: $gname - Usuarios: $((C1 + C2))"
            done < /etc/group
            ;;
        4)
            echo "Saliendo..."
            break
            ;;
        *)
            echo "Opción no válida."
            ;;
    esac
    echo ""
done

SH_EOF
chmod +x "2-Ejercicios avanzados/5_menu_usuarios.sh"

echo "Creando 2-Ejercicios avanzados/6_hasta_fin.sh..."
cat << 'SH_EOF' > "2-Ejercicios avanzados/6_hasta_fin.sh"
#!/bin/bash
# Ejercicio 6 Avanzado: Leer hasta "fin" y mostrar todo.

TEXTOS=""

echo "Introduce textos (escribe 'fin' para terminar):"
while true; do
    read -p "> " LINEA
    if [ "$LINEA" == "fin" ]; then
        break
    fi
    TEXTOS="$TEXTOS$LINEA\n"
done

echo -e "\nTextos introducidos:"
echo -e "$TEXTOS"

SH_EOF
chmod +x "2-Ejercicios avanzados/6_hasta_fin.sh"

echo "Creando 2-Ejercicios avanzados/7_permisos_texto.sh..."
cat << 'SH_EOF' > "2-Ejercicios avanzados/7_permisos_texto.sh"
#!/bin/bash
# Ejercicio 7 Avanzado: Permisos de un fichero en texto legible.

if [ -z "$1" ] || [ ! -e "$1" ]; then
    echo "Uso: $0 fichero"
    exit 1
fi

PERMS=$(ls -l "$1" | cut -c 2-10)

echo "Fichero: $1"
echo "Permisos: $PERMS"

# Desglose
echo "Propietario:"
[[ ${PERMS:0:1} == 'r' ]] && echo "- Lectura"
[[ ${PERMS:1:1} == 'w' ]] && echo "- Escritura"
[[ ${PERMS:2:1} == 'x' ]] && echo "- Ejecución"

echo "Grupo:"
[[ ${PERMS:3:1} == 'r' ]] && echo "- Lectura"
[[ ${PERMS:4:1} == 'w' ]] && echo "- Escritura"
[[ ${PERMS:5:1} == 'x' ]] && echo "- Ejecución"

echo "Otros:"
[[ ${PERMS:6:1} == 'r' ]] && echo "- Lectura"
[[ ${PERMS:7:1} == 'w' ]] && echo "- Escritura"
[[ ${PERMS:8:1} == 'x' ]] && echo "- Ejecución"

SH_EOF
chmod +x "2-Ejercicios avanzados/7_permisos_texto.sh"

echo "Creando 2-Ejercicios avanzados/8_menu_permisos.sh..."
cat << 'SH_EOF' > "2-Ejercicios avanzados/8_menu_permisos.sh"
#!/bin/bash
# Ejercicio 8 Avanzado: Menú para añadir o quitar permisos.

if [ -z "$1" ] || [ ! -e "$1" ]; then
    echo "Uso: $0 fichero"
    exit 1
fi

FICHERO=$1

while true; do
    echo "--- GESTIÓN DE PERMISOS: $FICHERO ---"
    ls -l "$FICHERO"
    echo "1. Añadir permiso de ejecución (+x)"
    echo "2. Quitar permiso de ejecución (-x)"
    echo "3. Añadir permiso de escritura (+w)"
    echo "4. Quitar permiso de escritura (-w)"
    echo "5. Salir"
    read -p "Opción: " OPC

    case $OPC in
        1) chmod +x "$FICHERO" ;;
        2) chmod -x "$FICHERO" ;;
        3) chmod +w "$FICHERO" ;;
        4) chmod -w "$FICHERO" ;;
        5) break ;;
        *) echo "Opción no válida." ;;
    esac
done

SH_EOF
chmod +x "2-Ejercicios avanzados/8_menu_permisos.sh"

echo "Creando 2-Ejercicios avanzados/9_menu_red.sh..."
cat << 'SH_EOF' > "2-Ejercicios avanzados/9_menu_red.sh"
#!/bin/bash
# Ejercicio 9 Avanzado: Menú de configuración de red.
# Nota: Modificar la red requiere privilegios de root.

validar_ip() {
    local ip=$1
    local stat=1
    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        OIFS=$IFS
        IFS='.'
        ip=($ip)
        IFS=$OIFS
        [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
        stat=$?
    fi
    return $stat
}

while true; do
    echo "--- CONFIGURACIÓN DE RED ---"
    echo "a. Mostrar configuración IP"
    echo "b. Modificar IP y máscara (Temporal)"
    echo "c. Modificar Gateway (Temporal)"
    echo "d. Modificar DNS"
    echo "s. Salir"
    read -p "Opción: " OPC

    case $OPC in
        a)
            ip addr show
            ;;
        b)
            read -p "Introduce interfaz (ej. eth0): " INT
            read -p "Introduce nueva IP: " NIP
            read -p "Introduce máscara (ej. 24): " MASK
            if validar_ip "$NIP"; then
                sudo ip addr add "$NIP/$MASK" dev "$INT"
                echo "IP añadida."
            else
                echo "IP no válida."
            fi
            ;;
        c)
            read -p "Introduce Gateway: " GW
            if validar_ip "$GW"; then
                sudo ip route add default via "$GW"
                echo "Gateway configurado."
            else
                echo "IP no válida."
            fi
            ;;
        d)
            read -p "Introduce DNS: " DNS
            if validar_ip "$DNS"; then
                echo "nameserver $DNS" | sudo tee /etc/resolv.conf > /dev/null
                echo "DNS configurado."
            else
                echo "IP no válida."
            fi
            ;;
        s) break ;;
        *) echo "Opción no válida." ;;
    esac
    echo ""
done

SH_EOF
chmod +x "2-Ejercicios avanzados/9_menu_red.sh"

echo '¡Todos los scripts han sido creados!'
EOF