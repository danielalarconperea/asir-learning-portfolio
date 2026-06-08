# Docker 07: Casos Prácticos Completos

En esta sección unimos todo lo aprendido para desplegar sistemas reales.

---

## Proyecto A: Despliegue de WordPress + MariaDB
Este es el ejercicio clásico de administración de sistemas. Necesitamos:
1. Una red común.
2. Persistencia para la base de datos.
3. Persistencia para los archivos de WordPress (temas, imágenes).

### Solución con Docker Compose:
```yaml
version: '3.3'

services:
  db:
    image: mariadb:10.5
    container_name: wordpress_db
    volumes:
      - db_data:/var/lib/mysql
    environment:
      MYSQL_ROOT_PASSWORD: password_maestra
      MYSQL_DATABASE: wordpress
      MYSQL_USER: user_wp
      MYSQL_PASSWORD: password_wp
    networks:
      - wp_net

  wordpress:
    depends_on:
      - db
    image: wordpress:latest
    container_name: wordpress_app
    ports:
      - "8000:80"
    environment:
      WORDPRESS_DB_HOST: db:3306
      WORDPRESS_DB_USER: user_wp
      WORDPRESS_DB_PASSWORD: password_wp
      WORDPRESS_DB_NAME: wordpress
    volumes:
      - wp_files:/var/www/html
    networks:
      - wp_net

volumes:
  db_data:
  wp_files:

networks:
  wp_net:
```

## Proyecto B: Stack MEAN (o similar) con Dockerfile propio
Imagina que tienes una aplicación Node.js personalizada.

1. **Dockerfile (./app/Dockerfile)**:
```dockerfile
FROM node:14-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

2. **docker-compose.yml**:
```yaml
services:
  frontend:
    build: ./app
    ports:
      - "3000:3000"
    environment:
      - MONGO_URL=mongodb://database:27017/miapp
  database:
    image: mongo:latest
```

---

## Consejos para el Examen / Práctica
- **Orden de encendido**: Si el servicio A usa al servicio B, asegúrate de que B tenga los puertos o nombres correctos.
- **Limpieza**: No dejes volúmenes "huérfanos". Usa `docker system prune` de vez en cuando (borra todo lo que no se esté usando: contenedores parados, redes vacías, imágenes sin tag).
- **Rutas**: En Windows, cuidado con las rutas de los Bind Mounts. Usa `/c/Users/...` si estás en Git Bash o rutas completas entre comillas.

---
*Siguiente tema: [08_Conceptos_Avanzados.md](08_Conceptos_Avanzados.md)*
