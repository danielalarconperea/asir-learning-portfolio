<div align="center">

# ASIR Learning Portfolio

Portfolio de prácticas, apuntes y proyectos de Administración de Sistemas Informáticos en Red.

<p>
  <img src="https://img.shields.io/badge/Linux-222222?style=for-the-badge&logo=linux&logoColor=white" alt="Linux">
  <img src="https://img.shields.io/badge/Bash-4EAA25?style=for-the-badge&logo=gnubash&logoColor=white" alt="Bash">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker">
  <img src="https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
  <img src="https://img.shields.io/badge/AWS_IoT_Core-232F3E?style=for-the-badge&logo=amazonaws&logoColor=white" alt="AWS IoT Core">
</p>

</div>

## Qué hay aquí

Este repositorio recoge mi trabajo de ASIR organizado por cursos y áreas. La idea es que se pueda navegar sin tener que abrir carpetas sueltas sin contexto: sistemas, redes, bases de datos, scripting, seguridad, servicios, despliegue web y el proyecto final.

| Sección | Contenido |
| --- | --- |
| [1ASIR](./1asir/) | Bases de sistemas, redes, SQL, Python, JavaScript y lenguaje de marcas. |
| [2ASIR](./2asir/) | Administración de sistemas, servicios de red, seguridad, bases de datos y despliegue web. |
| [Sentinel-IT](./projects/final-project/) | Proyecto final: SOC distribuido con Raspberry Pi, AWS IoT Core, MQTT/mTLS, Docker, Python y Flask. |
| [Python Learning Lab](./python-learning-lab/) | Ejercicios y pruebas de aprendizaje en Python, incluyendo pequeños labs de backend. |

## Proyecto destacado

<a href="./projects/final-project/">
  <img src="./projects/final-project/assets/portada.png" alt="Sentinel-IT" width="100%">
</a>

### Sentinel-IT

SOC autónomo y distribuido montado sobre dos nodos Raspberry Pi. El sistema recoge telemetría desde un nodo expuesto, la envía por MQTT/mTLS a AWS IoT Core y la analiza desde un nodo coordinador con dashboard Flask, SQLite y apoyo de IA para triage de eventos.

<p>
  <img src="https://img.shields.io/badge/Raspberry_Pi-A22846?style=flat-square&logo=raspberrypi&logoColor=white" alt="Raspberry Pi">
  <img src="https://img.shields.io/badge/MQTT-660066?style=flat-square&logo=mqtt&logoColor=white" alt="MQTT">
  <img src="https://img.shields.io/badge/mTLS-111111?style=flat-square&logo=letsencrypt&logoColor=white" alt="mTLS">
  <img src="https://img.shields.io/badge/Flask-000000?style=flat-square&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white" alt="SQLite">
</p>

[Ver proyecto](./projects/final-project/)

## Estructura

```text
asir-learning-portfolio/
|-- 1asir/
|   |-- databases-sql/
|   |-- markup-languages/
|   |-- networks/
|   |-- programming-python/
|   |-- systems/
|   `-- web-javascript/
|-- 2asir/
|   |-- cybersecurity/
|   |-- database-administration/
|   |-- network-security/
|   |-- network-services/
|   |-- systems-administration/
|   `-- web-deployment/
|-- projects/
|   `-- final-project/
`-- python-learning-lab/
    |-- backend-experiments/
    |-- backend-notes/
    |-- basic/
    `-- intermediate/
```

## Nota

El contenido está pensado como portfolio académico y técnico. Hay proyectos completos, prácticas de clase, apuntes y pruebas de aprendizaje; por eso algunas carpetas son más de laboratorio y otras están más preparadas para enseñarse directamente.
