# Docker 02: Primeros Pasos con la CLI

En este módulo aprenderás a manejar el ciclo de vida de los contenedores usando la línea de comandos.

---

## 1. Comandos de Información y Estado
Antes de empezar, es vital saber qué está pasando en nuestro sistema.

- `docker version`: Muestra la versión del cliente y del servidor.
- `docker info`: Información detallada sobre la instalación (contenedores totales, imágenes, drivers).
- `docker ps`: Lista los contenedores **en ejecución**.
- `docker ps -a`: Lista **todos** los contenedores (incluyendo los detenidos).

## 2. Ciclo de Vida del Contenedor
El comando rey es `docker run`. Este comando combina `docker create` y `docker start`.

### Sintaxis básica:
`docker run [OPTIONS] IMAGE [COMMAND] [ARG...]`

### Ejemplos prácticos:
1. **Modo Interactivo**:
   `docker run -it ubuntu /bin/bash`
   - `-i`: Interactivo.
   - `-t`: Terminal (TTY).
   
2. **Modo Destacado (Background)**:
   `docker run -d nginx`
   - `-d`: Detached mode. El contenedor corre en segundo plano.

3. **Asignar Nombre**:
   `docker run --name mi-servidor -d nginx`

## 3. Gestión de Contenedores (CRUD)
- **Detener**: `docker stop <ID_o_Nombre>`
- **Iniciar**: `docker start <ID_o_Nombre>`
- **Reiniciar**: `docker restart <ID_o_Nombre>`
- **Eliminar contenedor**: `docker rm <ID_o_Nombre>` (Debe estar detenido).
- **Eliminar forzado**: `docker rm -f <ID_o_Nombre>`

## 4. Inspección y Logs
Cuando algo falla, necesitamos "mirar dentro":
- `docker logs <ID>`: Muestra la salida estándar del contenedor.
- `docker logs -f <ID>`: Logs en tiempo real (follow).
- `docker inspect <ID>`: Devuelve un JSON con TODA la configuración del contenedor.
- `docker stats`: Monitorización de CPU, RAM y Red en tiempo real.

## 5. Entrar en un contenedor en ejecución
Si tienes un servidor (ej. Nginx) corriendo en segundo plano y quieres entrar a su terminal:
`docker exec -it <nombre_contenedor> bash`

---

## Laboratorio rápido
Intenta realizar esta secuencia de comandos para practicar:
1. Descarga y ejecuta un contenedor `hello-world`.
2. Ejecuta un contenedor `nginx` llamado "web1" en segundo plano.
3. Lista los contenedores activos.
4. Detén "web1".
5. Borra todos los contenedores de tu sistema (Cuidado: `docker rm $(docker ps -aq)`).

---
*Siguiente tema: [03_Imagenes_Dockerfile.md](03_Imagenes_Dockerfile.md)*
