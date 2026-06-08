# Docker 06: Docker Compose

Docker Compose es una herramienta para definir y ejecutar aplicaciones multi-contenedor. En lugar de escribir 10 comandos de `docker run`, usamos un archivo YAML.

---

## 1. El archivo docker-compose.yml
Es el corazón de Compose. Define servicios, redes y volúmenes.

### Estructura básica:
```yaml
version: '3.8' # Versión del formato

services:
  web: # Nombre del servicio
    image: nginx:alpine
    ports:
      - "8080:80"
    networks:
      - mi-red

  db:
    image: mysql:5.7
    environment:
      MYSQL_ROOT_PASSWORD: root
    volumes:
      - db-data:/var/lib/mysql
    networks:
      - mi-red

networks:
  mi-red:

volumes:
  db-data:
```

## 2. Comandos Principales
Para usar Compose, debes estar en la carpeta donde está el archivo `.yml`.

- `docker-compose up`: Levanta todos los servicios.
- `docker-compose up -d`: Levanta en segundo plano.
- `docker-compose down`: Detiene y **borra** contenedores y redes creadas por el archivo (pero no los volúmenes).
- `docker-compose ps`: Ver estado de los servicios del archivo.
- `docker-compose logs -f`: Ver logs de todos los servicios a la vez.
- `docker-compose exec <servicio> <comando>`: Ejecutar comando en un servicio.

## 3. Ventajas de Compose
1. **Configuración como Código**: Todo el entorno se guarda en un archivo.
2. **Aislamiento**: Crea una red dedicada para los servicios del archivo por defecto.
3. **Escalabilidad**: Podrías hacer `docker-compose up --scale web=3`.

## 4. Variables de Entorno
Puedes usar un archivo `.env` en la misma carpeta para no escribir contraseñas en el YAML:
```yaml
# En docker-compose.yml
services:
  db:
    image: mysql
    environment:
      - MYSQL_ROOT_PASSWORD=${DB_PASSWORD}
```

---

## Desafío de Estudio
Dado el siguiente archivo:
```yaml
services:
  app:
    build: .
    ports: ["5000:5000"]
    depends_on:
      - redis
  redis:
    image: "redis:alpine"
```
1. ¿Qué hace `build: .`?
2. ¿Qué hace `depends_on`? (Advertencia: ¿Significa esto que la app espera a que redis esté *listo* o solo *iniciado*?)

---
*Siguiente tema: [07_Casos_Practicos_Completos.md](07_Casos_Practicos_Completos.md)*
