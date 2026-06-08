# 🐳 Práctica Apache con Docker - 2º ASIR

## 📋 Descripción

Este proyecto implementa un servidor Apache containerizado usando Docker, con automatización mediante Ansible y un script de gestión interactivo.

## 🏗️ Arquitectura del Sistema

| Componente | Tecnología | Función |
|------------|------------|---------|
| Contenedor | Docker (Ubuntu 22.04) | Aislamiento del servicio Apache |
| Persistencia | Docker Volumes | Mapeo de `/var/www/html` al host |
| Automatización | Ansible Playbook | Configuración idempotente |
| Control de Versiones | Git | Tracking de configuración |
| Interfaz de Control | Bash Script (CLI) | Menú interactivo |

## 📁 Estructura del Proyecto

```
practica con apache/
├── Dockerfile              # Imagen Docker basada en Ubuntu
├── install_apache.yml      # Playbook Ansible
├── manage_service.sh       # Script de automatización
├── .gitignore              # Exclusiones de Git
├── README.md               # Este archivo
└── html/                   # Contenido web (se crea automáticamente)
    └── index.html          # Página de prueba
```

## 🚀 Inicio Rápido

### Opción 1: Menú Interactivo

```bash
chmod +x manage_service.sh
./manage_service.sh
```

### Opción 2: Comando Directo

```bash
# Instalación con Docker
./manage_service.sh install_docker

# Instalación con Ansible (local)
./manage_service.sh install_ansible
```

## 📝 Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `install_docker` | Construir imagen y ejecutar contenedor |
| `install_ansible` | Instalar Apache con Ansible |
| `start` | Iniciar contenedor |
| `stop` | Detener contenedor |
| `restart` | Reiniciar contenedor |
| `logs` | Ver logs del contenedor |
| `status` | Ver estado del contenedor |
| `network` | Ver información de red |
| `shell` | Acceder al shell del contenedor |
| `cleanup` | Eliminar contenedor e imagen |

## 🐋 Docker - Comandos Manuales

```bash
# Construir imagen
docker build -t mi_apache_ubuntu .

# Ejecutar contenedor con volumen persistente
docker run -d -p 80:80 -v $(pwd)/html:/var/www/html --name mi_apache mi_apache_ubuntu

# Ver logs
docker logs mi_apache

# Acceder al contenedor
docker exec -it mi_apache /bin/bash

# Detener y eliminar
docker stop mi_apache && docker rm mi_apache
```

## 📦 Ansible - Comandos Manuales

```bash
# Verificar sintaxis
ansible-playbook install_apache.yml --syntax-check

# Ejecutar playbook
ansible-playbook install_apache.yml --ask-become-pass

# Ejecutar con tags específicos
ansible-playbook install_apache.yml --tags "install" --ask-become-pass
```

## 🔧 Configuración

### Dockerfile

La imagen está basada en **Ubuntu 22.04** e incluye:
- Apache2 con módulos `rewrite` y `headers` habilitados
- Timezone configurada como `Europe/Madrid`
- Volumen definido para `/var/www/html`
- Puerto 80 expuesto

### Playbook Ansible

El playbook es **idempotente** y realiza:
1. Actualización de caché apt
2. Instalación de Apache2
3. Habilitación de módulos
4. Inicio y habilitación del servicio
5. Verificación de funcionamiento

## 🛡️ Restricciones (Anti-Patrones)

> ⚠️ **NO hacer:**
> - Usar la imagen `httpd:alpine` (requerimiento: Ubuntu)
> - Guardar cambios de configuración dentro del contenedor
> - Dejar que el script falle silenciosamente
> - Exponer puertos aleatorios
> - Subir logs o binarios al repositorio

## 📊 Verificación

Una vez instalado, verifica el funcionamiento:

```bash
# Test básico
curl http://localhost

# Ver contenedor
docker ps -f name=mi_apache

# Ver información de red
ip addr show
```

## 📚 Referencias

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Documentación de Apache](https://httpd.apache.org/docs/)
- [Documentación de Ansible](https://docs.ansible.com/)

---

**Curso:** 2º ASIR - Administración de Sistemas  
**Práctica:** Containerización de Apache con Docker
