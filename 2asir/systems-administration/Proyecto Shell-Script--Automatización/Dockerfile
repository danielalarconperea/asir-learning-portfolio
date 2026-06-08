# ============================================================================
# DOCKERFILE - Servidor Apache sobre Ubuntu 22.04
# Práctica Docker - 2º ASIR
# ============================================================================
#
# Este Dockerfile crea una imagen personalizada de Apache basada en Ubuntu.
# Ventajas de usar Ubuntu en lugar de la imagen httpd:alpine:
#   - Mayor control sobre la configuración
#   - Familiaridad con el sistema de paquetes apt
#   - Mejor compatibilidad con herramientas adicionales
#
# ============================================================================

# Capa 1: Imagen Base
# Usamos Ubuntu 22.04 LTS como base para máxima estabilidad y soporte
FROM ubuntu:22.04

# Evitar prompts interactivos durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Capa 2: Instalación de Paquetes
# Instalamos Apache2 y limpiamos la caché para reducir el tamaño de la imagen
RUN apt-get update && apt-get install -y \
    apache2 \
    tzdata \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configuración de timezone (opcional pero recomendado)
ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Capa 3: Configuración de Apache
# Habilitamos módulos útiles
RUN a2enmod rewrite headers

# Capa 4: Persistencia
# Definimos el volumen para el contenido web
# Este directorio se mapeará al host para persistencia de datos
VOLUME ["/var/www/html"]

# Capa 5: Configuración de Red
# Exponemos el puerto 80 (HTTP estándar)
EXPOSE 80

# Capa 6: Punto de Entrada
# Ejecutamos Apache en primer plano para que Docker pueda monitorearlo
CMD ["apachectl", "-D", "FOREGROUND"]

# ============================================================================
# NOTAS DE USO:
# 
# Construir la imagen:
#   docker build -t mi_apache_ubuntu .
#
# Ejecutar el contenedor:
#   docker run -d -p 80:80 -v $(pwd)/html:/var/www/html --name mi_apache mi_apache_ubuntu
#
# Verificar funcionamiento:
#   curl http://localhost
#
# ============================================================================
