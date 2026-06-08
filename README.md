<div align="center">

# ASIR Learning Portfolio

Portfolio técnico de Administración de Sistemas Informáticos en Red.

Sistemas, redes, servicios, seguridad, bases de datos, scripting y despliegue web.

<img src="https://skillicons.dev/icons?i=linux,bash,powershell,docker,nginx,mysql,sqlite,html,css,js,php,wordpress,py,git,github,vscode&perline=8" alt="Stack principal">

</div>

## Resumen

Repositorio central con prácticas, apuntes y proyectos desarrollados durante ASIR. El contenido está organizado por cursos y áreas técnicas para facilitar la navegación y mostrar de forma clara el trabajo realizado.

El bloque principal del portfolio corresponde a segundo curso, donde se agrupan administración de sistemas, servicios de red, seguridad, bases de datos, despliegue web, CSS, JavaScript, PHP, WordPress, Docker y scripting.

## Vista rápida

| Sección | Contenido |
| --- | --- |
| [2ASIR](./2asir/) | Administración de sistemas, servicios de red, seguridad, bases de datos y despliegue web. |
| [Sentinel-IT](./projects/final-project/) | Proyecto final: SOC distribuido con Raspberry Pi, MQTT/mTLS, AWS IoT Core, Docker, Python y Flask. |
| [1ASIR](./1asir/) | Base de sistemas, redes, SQL, Python, JavaScript y lenguaje de marcas. |
| [Python Learning Lab](./python-learning-lab/) | Ejercicios y pruebas de aprendizaje en Python. |

## 2ASIR

<img src="https://skillicons.dev/icons?i=linux,bash,powershell,docker,nginx,mysql,html,css,js,php,wordpress,git&perline=6" alt="Stack trabajado en 2ASIR">

Segundo curso reúne la parte más completa del portfolio: administración Linux, scripting, servicios, redes, seguridad, bases de datos y despliegue web.

| Área | Carpeta |
| --- | --- |
| Sistemas y automatización | [systems-administration](./2asir/systems-administration/) |
| Servicios de red | [network-services](./2asir/network-services/) |
| Seguridad de red | [network-security](./2asir/network-security/) |
| Bases de datos | [database-administration](./2asir/database-administration/) |
| Despliegue web, CSS y JavaScript | [web-deployment](./2asir/web-deployment/) |
| Ciberseguridad | [cybersecurity](./2asir/cybersecurity/) |

## Proyecto destacado

<a href="./projects/final-project/">
  <img src="./projects/final-project/assets/portada.png" alt="Sentinel-IT" width="100%">
</a>

### Sentinel-IT

SOC autónomo y distribuido montado sobre dos nodos Raspberry Pi. El sistema recoge telemetría desde un nodo expuesto, la envía por MQTT/mTLS a AWS IoT Core y la analiza desde un nodo coordinador con dashboard Flask, SQLite y apoyo de IA para triage de eventos.

<img src="https://skillicons.dev/icons?i=raspberrypi,linux,docker,py,flask,sqlite,aws,bash&perline=8" alt="Stack de Sentinel-IT">

[Ver proyecto](./projects/final-project/)

## Estructura

```text
asir-learning-portfolio/
|-- 1asir/
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
```

## Tipo de contenido

El repositorio combina prácticas completas, apuntes, ejercicios de clase, laboratorios y proyecto final. No todo el contenido representa aplicaciones terminadas; está organizado como portfolio académico y técnico.
