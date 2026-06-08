# Proyecto: Shell Script & Automatización de Servicios

Realiza los siguientes apartados utilizando para ello el servicio asignado en clase.

## 🛠️ Apartados del Proyecto

### 1. Gestión de Configuración (Ansible)
*   **Playbook:** Realiza un playbook de instalación completa de tu servicio con **Ansible**.

### 2. Control de Versiones (Git)
*   **Repositorio:** Crea un repositorio de **GIT** donde guardes diferentes versiones de tus ficheros de configuración del servicio implementado y los cambios que realice cada integrante del grupo.

### 3. Contenerización (Docker)
*   **Imagen Personalizada:** Crea una imagen de **Ubuntu** contenerizada con las modificaciones necesarias para implementar tu servicio en otras máquinas.
*   **Dockerización:** Crea un **Dockerfile** que implemente y configure el servicio automáticamente.

---

## 💻 Script de Automatización

Crea un script de automatización para tu servicio que, al arrancar, muestre la siguiente información de forma legible:
*   🌐 **Datos de red** de tu equipo.
*   📊 **Estado actual** del servicio.

### Funcionalidades del Menú
El script debe incluir un menú interactivo con las siguientes acciones:

1.  **Instalación del servicio:**
    *   Mediante comandos directos.
    *   Mediante Ansible.
    *   Mediante Docker.
2.  **Gestión del servicio:**
    *   Eliminación del servicio.
    *   Puesta en marcha (Start).
    *   Parada (Stop).
3.  **Consulta de Logs:**
    *   Filtro por fecha.
    *   Filtro por tipo.
    *   Otras opciones relevantes.
4.  **Configuración:**
    *   Permitir editar las opciones de configuración indicadas por el profesor (según el servicio).

### ⌨️ Ejecución por Parámetros
*   **Importante:** El script debe permitir ejecutar cualquier opción del menú mediante el uso de **parámetros directos** desde la consola (ej: `./script.sh --install --docker`).