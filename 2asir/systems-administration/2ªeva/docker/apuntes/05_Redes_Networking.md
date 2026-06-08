# Docker 05: Redes (Networking)

La comunicación entre contenedores y con el exterior es fundamental. Docker gestiona esto mediante "Drivers" de red.

---

## 1. Drivers Principales

### A. Bridge (Por defecto)
Crea una red virtual privada dentro del host. Los contenedores en la misma red bridge pueden hablar entre sí por IP o nombre.
- **Uso**: Aplicaciones estándar.

### B. Host
El contenedor no tiene IP propia; usa la red del host directamente. No hay aislamiento de red.
- **Uso**: Rendimiento máximo o aplicaciones que necesitan muchos puertos.

### C. None
El contenedor no tiene interfaz de red (solo loopback).
- **Uso**: Procesos aislados que no necesitan red.

### D. Overlay
Permite conectar contenedores en diferentes hosts físicos (usado en Docker Swarm/Clusters).

## 2. Publicación de Puertos (Port Mapping)
Un contenedor en modo bridge está aislado. Para que sea accesible desde fuera del host, debemos mapear un puerto.
- **Sintaxis**: `-p <Puerto_Host>:<Puerto_Contenedor>`
- **Ejemplo**: `docker run -p 8080:80 nginx`
  *(Si entras a localhost:8080 en tu navegador, verás el Nginx que corre en el 80 del contenedor).*

## 3. Gestión de Redes Personalizadas
Es una **mala práctica** usar la red bridge por defecto para producción. Es mejor crear redes propias:
1. `docker network create mi-red`
2. `docker run --network mi-red --name db postgres`
3. `docker run --network mi-red --name web frontend-app`

> [!IMPORTANT]
> En redes personalizadas, Docker incluye un **DNS interno**. El contenedor "web" puede contactar con "db" simplemente usando el nombre `db` como host, sin saber su IP.

## 4. Comandos de Red
- `docker network ls`: Listar redes.
- `docker network inspect <nombre>`: Ver qué contenedores están conectados a esa red.
- `docker network connect <red> <contenedor>`: Conectar un contenedor ya iniciado a otra red.
- `docker network disconnect <red> <contenedor>`: Desconectar.

---

## Laboratorio de Conectividad
1. Crea una red llamada `laboratorio`.
2. Lanza un contenedor `nginx` llamado `srv1` en esa red.
3. Lanza un contenedor `alpine` interactivo en la misma red: 
   `docker run -it --network laboratorio alpine sh`
4. Dentro del alpine, haz: `ping srv1`.
   *¿Funciona? ¿Por qué?*

---
*Siguiente tema: [06_Docker_Compose.md](06_Docker_Compose.md)*
