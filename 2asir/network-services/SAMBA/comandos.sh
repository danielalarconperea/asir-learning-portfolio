# 1. Instalación del servicio
sudo apt update && sudo apt install samba -y

# 2. Creación del sistema de archivos
sudo mkdir -p /samba/publico
sudo mkdir -p /samba/privado

# 3. Creación de usuarios en el sistema (sin acceso a login de shell)
sudo adduser --system --no-create-home --shell /bin/false pepito
sudo adduser --system --no-create-home --shell /bin/false manolito

# 4. Asignación de contraseñas para Samba (te pedirá introducirlas manualmente)
sudo smbpasswd -a pepito
sudo smbpasswd -a manolito

# 5. Configuración de permisos de carpetas
# Público: acceso total para invitados (nobody)
sudo chown -R nobody:nogroup /samba/publico
sudo chmod -R 0777 /samba/publico

# Privado: acceso para el grupo de usuarios de samba
sudo chown -R root:sambashare /samba/privado
sudo chmod -R 0770 /samba/privado

# 6. Edición de la configuración (Añadir los bloques [Publico] y [Privado] al final)
# Puedes usar: sudo nano /etc/samba/smb.conf
# -- Bloque a añadir --
#[global]
#   workgroup = WORKGROUP
#   server string = Servidor Samba
#   map to guest = bad user
#
#[Publico]
#   path = /samba/publico
#   browsable = yes
#   writable = yes
#   guest ok = yes
#   read only = no
#   force user = nobody
#
#[Privado]
#   path = /samba/privado
#   browsable = yes
#   writable = yes
#   guest ok = no
#   valid users = pepito, manolito
# -- Fin del bloque --

# 7. Reinicio de servicios para aplicar cambios
sudo systemctl restart smbd nmbd

# 8. Habilitar el firewall (si está activo)
sudo ufw allow samba








# -------------------------------------------------------------------------







sudo mkdir -p /samba/publico
sudo mkdir -p /samba/privado

sudo chmod -R 777 /samba/publico
sudo chown -R nobody:nogroup /samba/publico

sudo chmod -R 770 /samba/privado

sudo useradd -M -s /sbin/nologin pepito
sudo useradd -M -s /sbin/nologin manolito

sudo smbpasswd -a pepito
sudo smbpasswd -a manolito

sudo groupadd smbgroup
sudo usermod -aG smbgroup pepito
sudo usermod -aG smbgroup manolito
sudo chown -R root:smbgroup /samba/privado

sudo groupadd smbgroup
sudo usermod -aG smbgroup pepito
sudo usermod -aG smbgroup manolito
sudo chown -R root:smbgroup /samba/privado

sudo nano /etc/samba/smb.conf

[Publico]
   path = /samba/publico
   browsable = yes
   writable = yes
   guest ok = yes
   force user = nobody

[Privado]
   path = /samba/privado
   valid users = pepito, manolito
   guest ok = no
   writable = yes
   browsable = yes

sudo systemctl restart smbd nmbd








# -------------------------------------------------------------------------



#!/bin/bash
# Script Simple de Configuración Samba (Sin borrar datos) - 2ASIR Atocha

echo "--- Instalando Samba y creando carpetas ---"
sudo apt update && sudo apt install samba -y
sudo mkdir -p /samba/publico
sudo mkdir -p /samba/privado

echo "--- Creando usuarios y grupo (si no existen) ---"
# Crear usuarios
sudo id -u pepito &>/dev/null || sudo useradd -M -s /sbin/nologin pepito
sudo id -u manolito &>/dev/null || sudo useradd -M -s /sbin/nologin manolito

# Crear grupo y añadir usuarios
sudo getent group smbgroup &>/dev/null || sudo groupadd smbgroup
sudo usermod -aG smbgroup pepito
sudo usermod -aG smbgroup manolito

echo "--- Configurando permisos ---"
sudo chown -R nobody:nogroup /samba/publico
sudo chmod -R 0777 /samba/publico
sudo chown -R root:smbgroup /samba/privado
sudo chmod -R 0770 /samba/privado

echo "--- Estableciendo contraseñas de Samba ---"
sudo smbpasswd -a pepito
sudo smbpasswd -a manolito

echo "--- Aplicando configuración en smb.conf ---"
# Asegurar el map to guest en global
sudo sed -i '/map to guest/d' /etc/samba/smb.conf
sudo sed -i '/\[global\]/a \   map to guest = bad user' /etc/samba/smb.conf

# Añadir recursos al final (sin borrar lo anterior del archivo)
cat <<EOT | sudo tee -a /etc/samba/smb.conf

[Publico]
   path = /samba/publico
   browsable = yes
   writable = yes
   guest ok = yes
   force user = nobody

[Privado]
   path = /samba/privado
   valid users = pepito, manolito
   guest ok = no
   writable = yes
   browsable = yes
EOT

echo "--- Reiniciando servicios ---"
sudo systemctl restart smbd nmbd
sudo ufw allow samba

echo "Configuración simple completada."
