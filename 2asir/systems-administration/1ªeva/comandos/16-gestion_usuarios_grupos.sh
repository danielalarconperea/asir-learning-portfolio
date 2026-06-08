#!/bin/bash

# ==============================================================================
# 📝 ADMINISTRACIÓN DE USUARIOS Y GRUPOS
# ==============================================================================

### 1. GESTIÓN DE GRUPOS
# Crear un grupo
sudo groupadd ventas

# Crear un grupo con GID específico (menor a 1000 para sistema)
sudo groupadd -r research

# Modificar nombre de un grupo
sudo groupmod -n comercial ventas

# Eliminar un grupo
sudo groupdel comercial

### 2. CREACIÓN DE USUARIOS (USERADD)
# useradd es el comando de bajo nivel para crear usuarios.

# Crear usuario básico (sin home por defecto)
sudo useradd pedro

# Crear usuario con HOME y shell específica
sudo useradd -m -s /bin/bash juan

# Crear usuario completo (UID, Grupo principal, Grupos secundarios y Comentario)
sudo useradd -u 1050 -g users -G sudo,adm -m -c "Juan Perez" juan

# --- Consultar Configuración por Defecto ---
useradd -D      # Ver qué pasa cuando no pones opciones

### 3. MODIFICACIÓN Y CONTRASEÑAS
# Establecer o cambiar contraseña
sudo passwd juan

# Bloquear / Desbloquear cuenta
sudo passwd -l juan   # Lock (Bloquear)
sudo passwd -u juan   # Unlock (Desbloquear)

# Modificar usuario existente
sudo usermod -aG grupo_nuevo juan  # Añadir a un grupo extra sin borrar los anteriores

### 4. ELIMINACIÓN DE USUARIOS
# Borrar solo la cuenta
sudo userdel juan

# Borrar cuenta Y su carpeta HOME (¡CUIDADO!)
sudo userdel -r juan

### 5. ARCHIVOS CLAVE DEL SISTEMA
# /etc/passwd   -> Usuarios, UIDs, Homes y Shells.
# /etc/shadow   -> Contraseñas cifradas e info de expiración.
# /etc/group    -> Grupos y sus miembros.
# /etc/skel/    -> Esqueleto (lo que se copia al home nuevo).
