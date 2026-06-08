#!/bin/bash

# ==============================================================================
# 📝 APUNTES DE BASH: CONTROL DE ACCESO Y PRIVILEGIOS (CRON Y AT)
# ==============================================================================
# Este script detalla cómo restringir o permitir el uso de herramientas de
# programación de tareas a usuarios específicos mediante listas de control de acceso.
#
# 💡 Lógica General de Privilegios:
# 1. Si existe el archivo '.allow': SOLO los usuarios listados pueden usar el servicio.
#    (El archivo '.deny' es ignorado en este caso).
# 2. Si NO existe '.allow' pero SÍ existe '.deny': Todos pueden usarlo EXCEPTO los listados.
# 3. Si NO existen NI '.allow' NI '.deny': El comportamiento depende de la distro 
#    (normalmente solo root puede usarlo).
# ==============================================================================

### --- Sección 1: Control de Privilegios para CRON ---
# El servicio cron busca configuraciones en /etc/cron.allow y /etc/cron.deny.
# Formato de archivos: Un nombre de usuario por línea.

# 1.1 Verificar existencia de archivos de control actuales
# 🔍 Usamos 'ls' para ver cuál de los dos archivos existe en el sistema.
ls -l /etc/cron.allow /etc/cron.deny 2>/dev/null
# -> -rw-r--r-- 1 root root 15 Nov 25 10:00 /etc/cron.deny
# -> (Nota: Es común que por defecto solo exista cron.deny vacío o con usuarios especiales).

# 1.2 Ver quién tiene prohibido el uso de cron actualmente
# 🚫 'cat' muestra los usuarios bloqueados explícitamente.
cat /etc/cron.deny
# -> guest
# -> temp_user

# 1.3 Permitir acceso EXCLUSIVO a usuarios específicos (Lista Blanca)
# ⚠️ Al crear 'cron.allow', se bloquea implícitamente a todos los que NO estén en esta lista.
# Creamos el archivo y añadimos al usuario 'juan' y a 'root'.
echo "juan" | sudo tee /etc/cron.allow
echo "root" | sudo tee -a /etc/cron.allow
# -> juan
# -> root

# 1.4 Prohibir acceso a un usuario específico (Lista Negra)
# 🛑 Si borramos 'cron.allow', el sistema vuelve a mirar 'cron.deny'.
# Aquí bloqueamos al usuario 'malicioso' añadiéndolo a deny.
sudo rm /etc/cron.allow
echo "malicioso" | sudo tee -a /etc/cron.deny
# -> malicioso

### --- Sección 2: Control de Privilegios para AT ---
# El comando 'at' (para tareas de ejecución única) sigue la misma lógica que cron.
# Archivos: /etc/at.allow y /etc/at.deny.

# 2.1 Verificar estado de las listas de control para AT
# 📂 Listamos los archivos de configuración.
ls -l /etc/at.allow /etc/at.deny 2>/dev/null
# -> -rw-r--r-- 1 root root 20 Nov 25 10:05 /etc/at.deny

# 2.2 Restringir el uso de AT a un grupo selecto
# 🔒 Creamos/Sobrescribimos 'at.allow'. Solo 'ana' y 'admin' podrán agendar tareas.
# Usamos printf para añadir múltiples líneas de una vez.
printf "ana\nadmin\n" | sudo tee /etc/at.allow
# -> ana
# -> admin

# 2.3 Verificar contenido de la lista blanca de AT
cat /etc/at.allow
# -> ana
# -> admin

### --- Sección 3: Diagnóstico y Verificación de Acceso ---
# Cómo comprobar si la configuración ha surtido efecto intentando acceder como usuario.

# 3.1 Simulación: Usuario bloqueado intentando usar CRON
# 🕵️ Si el usuario 'malicioso' (que está en cron.deny) intenta editar su crontab:
# su - malicioso -c "crontab -e"
# -> You (malicioso) are not allowed to use this program (crontab)
# -> See crontab(1) for more information

# 3.2 Simulación: Usuario bloqueado intentando usar AT
# 🕵️ Si un usuario no autorizado intenta agendar una tarea con 'at':
# su - usuario_no_listado -c "echo 'ls' | at now + 1 minute"
# -> You do not have permission to use at.

# 3.3 Verificación rápida de permisos (Scripting check)
# ✅ Podemos usar un condicional para verificar si el archivo deny contiene un usuario.
usuario="invitado"
if grep -q "^$usuario$" /etc/cron.deny; then
    echo "El usuario $usuario tiene el acceso a CRON denegado."
else
    echo "El usuario $usuario no está explícitamente en cron.deny."
fi
# -> El usuario invitado tiene el acceso a CRON denegado.

### --- Sección 4: Ubicaciones Alternativas y Configuraciones Globales ---
# En algunos sistemas (especialmente derivados de RHEL/CentOS), la configuración
# de seguridad puede estar reforzada por PAM (Pluggable Authentication Modules).

# 4.1 Verificar configuración PAM para crond
# ⚙️ Muestra las reglas de autenticación requeridas.
grep "account" /etc/pam.d/crond
# -> account    required   pam_access.so
# -> account    include    password-auth

# 4.2 Reiniciar servicio (raramente necesario tras cambiar allow/deny, pero recomendable si falla)
# 🔄 Aplicar cambios si el demonio se comporta de forma extraña.
sudo systemctl restart cron
# -> (Sin salida si el comando es exitoso)
# -> (En RHEL/CentOS el servicio se llama 'crond')