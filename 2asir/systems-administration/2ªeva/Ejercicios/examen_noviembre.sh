#!/bin/bash

# ==============================================================================
# 📝 SOLUCIÓN EXAMEN - NOVIEMBRE 2025 (1ª EVALUACIÓN)
# ==============================================================================

# 1) Carpeta /usuarios como base por defecto para nuevos usuarios
sudo mkdir /usuarios
# Cambiamos la configuración por defecto de useradd
sudo sed -i 's/^HOME=.*/HOME=\/usuarios/' /etc/default/useradd

# 2) Registrar cambios de permisos en log_permisos y configurar rotación horaria
sudo apt-get install auditd -y  # Necesario para auditar el sistema

# Crear el archivo si no existe
sudo touch /var/log/log_permisos
sudo chmod 640 /var/log/log_permisos 

# REGISTRO: Decimos al kernel que vigile las llamadas al sistema (syscalls) de cambio de permisos
# -S chmod/fchmod/fchmodat son las funciones que cambian permisos
# -k es un nombre clave para filtrar luego
# -a always,exit es para que se registre siempre que se haga el cambio
sudo auditctl -a always,exit -S chmod -S fchmod -S fchmodat -k cambios_permisos

# 2.1) Activar el envío de auditoría a Syslog
# (Esto hace que los eventos de auditd pasen por rsyslog)
sudo sed -i 's/active = no/active = yes/' /etc/audit/plugins.d/syslog.conf 2>/dev/null || \
sudo sed -i 's/active = no/active = yes/' /etc/audisp/plugins.d/syslog.conf 2>/dev/null

# 2.2) Crear una regla en Rsyslog para filtrar por nuestra clave (-k cambios_permisos)
# Si el mensaje contiene la clave, lo guarda en nuestro archivo y para de procesar (& stop)
sudo bash -c 'cat << EOF > /etc/rsyslog.d/60-permisos.conf
if \$msg contains "cambios_permisos" then /var/log/log_permisos
& stop
EOF'

# 2.3) Reiniciar servicios para aplicar
sudo systemctl restart auditd
sudo systemctl restart rsyslog

# ROTACIÓN: Configuración de Logrotate (Cada hora, 24 copias, comprimido)
sudo bash -c 'cat << EOF > /etc/logrotate.d/log_permisos
/var/log/log_permisos {
    hourly
    rotate 24
    compress
    missingok
    notifempty
    create 0640 root adm
}
EOF'

# 3) Configuraciones por defecto para nuevos usuarios:
# a) Contraseña min 8 caracteres: Editar /etc/login.defs
sudo sed -i 's/^PASS_MIN_LEN.*/PASS_MIN_LEN    8/' /etc/login.defs
# b) Expiren a los 4 años (1461 días):
sudo sed -i 's/^PASS_MAX_DAYS.*/PASS_MAX_DAYS   1461/' /etc/login.defs
# c) Fichero bienvenido.txt en el home (usamos el esqueleto /etc/skel)
echo "Bienvenido al sistema" | sudo tee /etc/skel/bienvenido.txt
# d) Permisos 700 por defecto (solo usuario lee/escribe/ejecuta)
sudo sed -i 's/^UMASK.*/UMASK    077/' /etc/login.defs

# 4) Crear usuario 'pedro' en /jefe, administrador y que no expire
sudo useradd -m -d /jefe -G sudo -K PASS_MAX_DAYS=-1 pedro

# 5) Otros usuarios:
# a) yolanda con contraseña 12345 (usando openssl para el hash)
sudo useradd -m -p $(openssl passwd -1 12345) yolanda
# b) monica: auto-borrado de home al iniciar sesión
sudo useradd -m monica
# Añadimos el comando de borrado a su .bash_profile
echo "rm -rf ~/*" | sudo tee -a /usuarios/monica/.bash_profile

# 6) Carpeta compartida "pactos" en el home de pedro
sudo mkdir /jefe/pactos
# Sticky bit (1) para que no borren archivos ajenos, y permisos totales (777)
sudo chmod 1777 /jefe/pactos
# Para que todos la vean en su home simultáneamente, creamos enlaces simbólicos en el skel
sudo ln -s /jefe/pactos /etc/skel/pactos

# 7) Crear grupo "comisiones" y añadir a todos los usuarios humanos
sudo groupadd comisiones
for user in $(awk -F: '$3>=1000 {print $1}' /etc/passwd); do
    sudo usermod -aG comisiones $user
done

# 8) Mostrar nombres de usuarios del grupo en una línea cada uno
echo "Miembros del grupo comisiones:"
grep "^comisiones:" /etc/group | cut -d: -f4 | tr ',' '\n'
