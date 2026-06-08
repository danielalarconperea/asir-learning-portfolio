#!/bin/bash

# ==============================================================================
# � PLANIFICACIÓN DE TAREAS ÚNICAS: AT & BATCH
# ==============================================================================
# Objetivo: Ejecutar comandos una sola vez en un momento determinado.

### 1. REQUISITOS Y SERVICIO
# El demonio 'atd' debe estar en ejecución para procesar las tareas.

# Verificar estado del servicio
systemctl status atd

# Iniciar servicio (requiere root)
sudo systemctl start atd

### 2. COMANDO 'AT' (SINTAXIS Y TIEMPO)
# Formato: echo "comando" | at <tiempo>
# O modo interactivo: at <tiempo> -> escribir comandos -> Ctrl+D para finalizar.

# Ejemplos de formatos de tiempo:
echo "reboot" | at 23:30              # A una hora específica
echo "sh script.sh" | at now + 1 min   # Dentro de 1 minuto
echo "ls -l" | at now + 2 hours        # Dentro de 2 horas
echo "wall 'Aviso'" | at noon          # A mediodía (12:00)
echo "df -h" | at midnight             # A medianoche (00:00)
echo "cp file /tmp" | at teatime       # A la hora del té (16:00)
echo "backup.sh" | at 10:00 AM Mar 20  # Fecha y hora exacta

### 3. OPCIONES COMUNES
# -f: Leer comandos de un archivo en lugar de la entrada estándar.
at -f tareas.txt 22:00

# -m: Enviar un correo al usuario cuando la tarea finalice (útil para logs).
at -m -f backup.sh now + 1 hour

### 4. GESTIÓN DE LA COLA
# atq: Listar trabajos pendientes (ID, Fecha, Hora, Usuario).
atq

# atrm: Eliminar un trabajo de la cola usando su ID.
# Ejemplo: borrar el trabajo número 5
atrm 5

### 5. COMANDO 'BATCH'
# Ejecuta comandos cuando la carga del sistema (CPU load) baja de 0.8.
# No requiere especificar la hora; ideal para procesos pesados que no son urgentes.
echo "sort archivo_gigante.txt" | batch

### 6. CONTROL DE ACCESO
# Archivos en /etc/ para restringir el uso (orden de prioridad):
# 1. /etc/at.allow -> Si existe, SOLO los usuarios aquí listados pueden usar 'at'.
# 2. /etc/at.deny  -> Si existe, los usuarios aquí listados NO pueden usarlo.
# 3. Si ninguno existe, solo root puede usarlo (depende de la distribución).

# Ejemplo: Denegar acceso al usuario 'invitado'
sudo echo "invitado" >> /etc/at.deny