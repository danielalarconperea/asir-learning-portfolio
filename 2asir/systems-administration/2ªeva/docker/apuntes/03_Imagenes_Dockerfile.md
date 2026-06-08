# Docker 03: Imágenes y Dockerfile

Las imágenes son las plantillas de solo lectura que definen qué contendrá nuestro contenedor. En este archivo aprenderás a crearlas.

---

## 1. ¿Qué es una Imagen?
Una imagen es un conjunto de capas (layers) apiladas. Cada capa representa una instrucción en el Dockerfile. Son **inmutables**; si cambias algo, se crea una nueva capa.

## 2. Comandos de Imágenes
- `docker images`: Lista las imágenes locales.
- `docker pull <imagen>`: Descarga una imagen del Registry.
- `docker rmi <imagen>`: Borra una imagen local.
- `docker tag <imagen_origen> <nuevo_nombre>`: Crea un alias para una imagen.
- `docker build -t <nombre:tag> .`: Construye una imagen a partir de un Dockerfile en el directorio actual (`.`).

## 3. El Dockerfile: Anatomía y Palabras Clave
El Dockerfile es un archivo de texto sin extensión que contiene las instrucciones para montar la imagen.

| Instrucción | Descripción |
| :--- | :--- |
| **FROM** | Define la imagen base (ej. `FROM debian:latest`). **Obligatorio al inicio**. |
| **WORKDIR** | Establece el directorio de trabajo (como un `cd`). |
| **COPY** / **ADD** | Copia archivos del host al contenedor. |
| **RUN** | Ejecuta comandos durante la construcción (ej. `apt upgrade`). |
| **ENV** | Define variables de entorno. |
| **EXPOSE** | Documenta el puerto en el que escucha la aplicación. |
| **CMD** | Comando por defecto al iniciar el contenedor. Solo puede haber uno. |
| **ENTRYPOINT** | Similar a CMD pero más difícil de sobrescribir. |

## 4. Ejemplo Real: Servidor Web Personalizado
Crea un archivo llamado `Dockerfile` con este contenido:
```dockerfile
FROM nginx:alpine
WORKDIR /usr/share/nginx/html
COPY index.html .
ENV APP_VERSION=1.0
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## 5. Optimización de Imágenes
- **Capas**: Cada `RUN`, `COPY` y `ADD` crea una capa. Intenta concatenar comandos:
  `RUN apt update && apt install -y git && rm -rf /var/lib/apt/lists/*`
- **.dockerignore**: Similar a `.gitignore`, evita enviar archivos innecesarios (como `node_modules` o archivos `.git`) al daemon de Docker.
- **Imágenes Alpine**: Usa bases como `python:3.9-alpine` para reducir el tamaño de 900MB a 50MB.

---

## Ejercicio de Estudio
Analiza el siguiente Dockerfile. ¿Qué hace cada línea?
```dockerfile
FROM python:3.9
RUN pip install flask
COPY app.py /app/
WORKDIR /app
CMD ["python", "app.py"]
```
¿Qué pasaría si cambiamos el `COPY` y el `WORKDIR` de orden?

---
*Siguiente tema: [04_Persistencia_Datos.md](04_Persistencia_Datos.md)*
