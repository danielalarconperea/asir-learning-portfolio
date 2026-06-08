#!/bin/bash

# ==============================================================================
# 📝 IDENTIDAD DE USUARIO Y CONTROL DE SESIONES
# ==============================================================================

### 1. ¿QUIÉN SOY? (IDENTIDAD)
# Muestra UID (usuario), GID (grupo principal) y otros grupos
id

# Info de un usuario específico
id root

# Variables específicas del id
id -u   # Solo el UID (número de usuario)
id -g   # Solo el GID (número de grupo)
id -G   # Todos los GIDs de los grupos a los que pertenece

### 2. CAMBIO DE USUARIO (SU)
# su: Switch User (Cambiar usuario).

# Cambiar a root (pide contraseña de root)
su -

# Cambiar a otro usuario
su - usuario

# Nota: El guion '-' es fundamental para cargar las variables de entorno
# y el HOME del usuario (hace un "login" real).

### 3. SESIONES ACTIVAS
# Quién está conectado al sistema ahora mismo
who

# Versión detallada (qué están haciendo)
w

# Cuándo arrancó el sistema y nivel de ejecución
who -b -r

# Historial de últimos inicios de sesión (logins)
last

# Buscar usuario en la base de datos local
getent passwd sysadmin
grep sysadmin /etc/passwd
