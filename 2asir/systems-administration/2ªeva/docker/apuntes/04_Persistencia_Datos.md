# Docker 04: Persistencia de Datos

Por defecto, los contenedores son "efímeros". Si borras el contenedor, los datos creados dentro desaparecen. En este archivo aprenderás a evitarlo.

---

## 1. El Sistema de Archivos de Capas (Copy-on-Write)
Los contenedores usan una capa de lectura/escritura superior. Cuando el contenedor se borra, esa capa muere. Para persistir datos, Docker ofrece tres mecanismos:

## 2. Tipos de Montaje

### A. Volumes (Volúmenes) - *Recomendado*
Son gestionados por Docker en una parte del host (`/var/lib/docker/volumes/` en Linux).
- **Ventaja**: Independientes de la estructura del host, fáciles de respaldar.
- **Uso**: `docker volume create mi-data`
- **Montaje**: `docker run -v mi-data:/app/data nginx`

### B. Bind Mounts (Montajes de enlace)
Mapean una carpeta o archivo específico del Host a una carpeta del Contenedor.
- **Ventaja**: Ideal para desarrollo (el código cambia en el host y se ve en el contenedor).
- **Riesgo**: Dependes de la ruta absoluta del host.
- **Uso**: `docker run -v C:\proyectos\web:/usr/share/nginx/html nginx`

### C. Tmpfs Mounts
Almacenan los datos solo en la memoria RAM del Host. Nunca se escriben en disco.
- **Uso**: Datos sensibles o temporales de alta velocidad.

## 3. Comandos de Volúmenes
- `docker volume ls`: Lista volúmenes.
- `docker volume inspect <nombre>`: Ver dónde vive físicamente el volumen.
- `docker volume rm <nombre>`: Borrar un volumen (no debe estar en uso).
- `docker volume prune`: Borrar todos los volúmenes sin uso.

## 4. Sintaxis: -v vs --mount
Hay dos formas de montar datos:
1. **-v (Legacy)**: Corto pero menos claro. `docker run -v mi-vol:/destino nginx`
2. **--mount (moderno)**: Más explícito y recomendado para Docker Swarm.
   `docker run --mount source=mi-vol,target=/destino nginx`

---

## Caso Práctico: Base de Datos con persistencia
Si ejecutas una base de datos sin volumen, al borrar el contenedor pierdes tus tablas:
```bash
# Correcto:
docker run -d \
  --name mi-db \
  -e MYSQL_ROOT_PASSWORD=secreto \
  -v mysql-data:/var/lib/mysql \
  mysql:latest
```
Si ahora haces `docker rm -f mi-db`, y vuelves a crear el contenedor con el mismo `-v`, tus datos seguirán ahí.

---
## Pregunta de Examen
¿Cuál es la diferencia principal entre un Bind Mount y un Volumen a nivel de permisos de sistema operativo?

---
*Siguiente tema: [05_Redes_Networking.md](05_Redes_Networking.md)*
