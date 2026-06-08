# ASIR Learning Portfolio

Repositorio organizado de practicas, apuntes, laboratorios y proyectos realizados durante el ciclo de Administracion de Sistemas Informaticos en Red.

El objetivo de este repo es que el contenido sea facil de navegar y que tambien funcione como portfolio tecnico: sistemas, redes, bases de datos, scripting, seguridad, servicios de red y despliegue web.

## Vista rapida

| Area | Contenido |
| --- | --- |
| [1ASIR](./1asir/) | Bases de SQL, JavaScript, Python, redes, sistemas y lenguaje de marcas. |
| [2ASIR](./2asir/) | Administracion de sistemas, servicios de red, seguridad, BBDD, despliegue web y TFG. |
| [Projects](./projects/) | Proyectos destacados y trabajos con mas valor de portfolio. |
| [Python Learning Lab](./python-learning-lab/) | Ejercicios y pruebas de aprendizaje en Python. |

## Proyectos destacados

| Proyecto | Estado | Tecnologias | Enlace |
| --- | --- | --- | --- |
| Final Project - Distributed IoT Security Architecture | En desarrollo | Raspberry Pi, AWS IoT Core, MQTT/TLS, Docker, Python | [Ver proyecto](./projects/final-project/) |

## Estructura

```text
asir-learning-portfolio/
+-- 1asir/
|   +-- databases-sql/
|   +-- markup-languages/
|   +-- networks/
|   +-- programming-python/
|   +-- systems/
|   +-- web-javascript/
+-- 2asir/
|   +-- cybersecurity/
|   +-- database-administration/
|   +-- final-project/
|   +-- network-security/
|   +-- network-services/
|   +-- systems-administration/
|   +-- web-deployment/
+-- projects/
|   +-- final-project/
|   +-- archive/
+-- python-learning-lab/
    +-- backend-experiments/
    +-- backend-notes/
    +-- basic/
    +-- intermediate/
```

## Criterio de organizacion

- Los contenidos de clase se agrupan por curso y modulo.
- Los proyectos con valor de portfolio viven en `projects/`.
- El TFG se referencia desde `2asir/final-project/`, pero los archivos reales estan en `projects/final-project/` para evitar duplicados.
- Los experimentos de Python y backend se mantienen como laboratorio de aprendizaje, sin presentarlos como producto terminado.

## Notas de limpieza

Este repo evita subir entornos virtuales, caches y archivos generados como `env/`, `venv/`, `__pycache__/` y `*.pyc`.

Los videos pesados se mantienen fuera de Git para que el repositorio sea mas ligero y facil de revisar.
