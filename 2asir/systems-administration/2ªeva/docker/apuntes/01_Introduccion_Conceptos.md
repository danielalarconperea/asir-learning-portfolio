# Docker 01: Introducción y Conceptos Fundamentales

Este archivo contiene la base teórica necesaria para entender qué es Docker y por qué revolucionó el despliegue de software.

---

## 1. ¿Qué es un Contenedor?
Un contenedor es una unidad estándar de software que empaqueta el código y todas sus dependencias para que la aplicación se ejecute de forma rápida y confiable de un entorno informático a otro.

### Conceptos Clave:
- **Aislamiento**: Los contenedores están aislados entre sí y del sistema anfitrión (host).
- **Portabilidad**: "Si funciona en mi máquina, funciona en la tuya".
- **Ligereza**: Comparten el kernel del sistema operativo host, lo que los hace mucho más eficientes que las VMs.

## 2. Contenedores vs Máquinas Virtuales (VM)

| Característica | Máquina Virtual (VM) | Contenedor (Docker) |
| :--- | :--- | :--- |
| **Arquitectura** | Incluye SO completo (Guest OS) | Comparte el Kernel del Host |
| **Velocidad de Inicio** | Minutos | Segundos |
| **Tamaño** | GBs | MBs |
| **Aislamiento** | Nivel de Hardware (Hipervisor) | Nivel de Proceso (OS) |
| **Eficiencia** | Menor (Duplica recursos) | Alta (Uso óptimo de RAM/CPU) |

## 3. Arquitectura de Docker (Client-Server)
Docker utiliza una arquitectura de cliente-servidor:
1.  **Docker Client**: La herramienta de línea de comandos (`docker`) con la que interactuamos.
2.  **Docker Host (Daemon)**: El proceso de fondo (`dockerd`) que gestiona objetos como imágenes, contenedores, redes y volúmenes.
3.  **Registry**: Lugar donde se almacenan las imágenes (ej. Docker Hub).

## 4. Los 3 Pilares de Docker
Para estudiar Docker, debes diferenciar claramente estos tres conceptos:

1.  **Dockerfile**: El "plano" o receta (archivo de texto).
2.  **Image (Imagen)**: El "paquete" ejecutable construido a partir del Dockerfile. Es estática.
3.  **Container (Contenedor)**: La "instancia" en ejecución de una imagen. Es dinámica.

> [!TIP]
> Piensa en la **Imagen** como una **Clase** en programación, y el **Contenedor** como un **Objeto** (una instancia de esa clase).

---

## Ejercicios de Autoevaluación
1. ¿Por qué un contenedor de Linux no puede ejecutarse nativamente en un Kernel de Windows?
2. Si borro un contenedor, ¿se borra la imagen de la que proviene?
3. ¿Qué componente de la arquitectura es el responsable de descargar imágenes del Docker Hub?

---
*Siguiente tema: [02_Primeros_Pasos_CLI.md](02_Primeros_Pasos_CLI.md)*
