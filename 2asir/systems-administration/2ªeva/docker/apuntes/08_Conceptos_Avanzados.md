# Docker 08: Conceptos Avanzados y Buenas Prácticas

Para terminar, veremos conceptos que separan a un usuario básico de un administrador de sistemas experto.

---

## 1. Multi-Stage Builds (Construcción en varias etapas)
Sirve para crear imágenes extremadamente pequeñas. Compilas en una imagen "pesada" y copias el binario resultante a una imagen "ligera".

```dockerfile
# Etapa 1: Compilación
FROM maven:3.6-jdk-11 AS build
COPY src /app/src
COPY pom.xml /app
RUN mvn -f /app/pom.xml clean package

# Etapa 2: Ejecución
FROM openjdk:11-jre-slim
COPY --from=build /app/target/app.jar /usr/local/lib/app.jar
ENTRYPOINT ["java","-jar","/usr/local/lib/app.jar"]
```
*Resultado: Pasamos de una imagen de 600MB (Maven + JDK) a una de 150MB (JRE + App).*

## 2. Limitación de Recursos
Un contenedor puede consumir toda la CPU/RAM del host si falla (DoS accidental).
- `docker run --memory="512m" --cpus="0.5" nginx`
- En Compose:
```yaml
deploy:
  resources:
    limits:
      cpus: '0.50'
      memory: 512M
```

## 3. Seguridad
1. **No usar root**: Por defecto, los procesos en el contenedor corren como root. Es mejor usar la instrucción `USER` en el Dockerfile.
2. **Escaneo de Vulnerabilidades**: `docker scan <imagen>` (o herramientas como Trivy).
3. **Sólo lo necesario**: No instales `vim`, `curl` o `net-tools` en imágenes de producción si no se necesitan.

## 4. Docker Internals: Namespaces y Cgroups
Si en el examen te preguntan cómo hace Docker el aislamiento:
- **Namespaces**: Aíslan lo que el contenedor puede **ver** (Red, Procesos, Usuarios, Mount points).
- **Control Groups (cgroups)**: Limitan lo que el contenedor puede **usar** (CPU, Memoria, I/O).

---

## Reflexión Final
Docker no es una máquina virtual, es un **proceso aislado**. Entender esto es la clave para dominar la administración de contenedores. 

¡Felicidades por completar este set de estudio!

---
*Fin del material de estudio para 2ASIR.*
