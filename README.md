<div align="center">

# ASIR Learning Portfolio

Portfolio técnico de ASIR: sistemas, redes, servicios, seguridad, bases de datos, scripting y despliegue web.

<img src="https://skillicons.dev/icons?i=linux,bash,powershell,docker,nginx,apache,mysql,sqlite,html,css,js,php,wordpress,py,git,github&perline=8" alt="Stack principal">

</div>

## Qué quiero enseñar aquí

Este repositorio recoge mi trabajo de Administración de Sistemas Informáticos en Red, ordenado para que se pueda ver rápido qué he tocado y en qué contexto.

La parte más importante está en segundo curso: administración de sistemas, servicios de red, seguridad, bases de datos, despliegue web, Docker, scripting y el proyecto final. AWS aparece porque lo usé en Sentinel-IT, pero no es el foco principal del portfolio.

## Vista rápida

| Sección | Contenido |
| --- | --- |
| [2ASIR](./2asir/) | Administración de sistemas, servicios de red, seguridad, bases de datos y despliegue web. |
| [Sentinel-IT](./projects/final-project/) | Proyecto final: SOC distribuido con Raspberry Pi, MQTT/mTLS, AWS IoT Core, Docker, Python y Flask. |
| [1ASIR](./1asir/) | Base de sistemas, redes, SQL, Python, JavaScript y lenguaje de marcas. |
| [Python Learning Lab](./python-learning-lab/) | Ejercicios y pruebas de aprendizaje en Python. |

## 2ASIR

<img src="https://skillicons.dev/icons?i=linux,bash,powershell,docker,nginx,apache,mysql,html,css,js,php,wordpress&perline=6" alt="Stack trabajado en 2ASIR">

Segundo es donde está la parte más completa del portfolio: administración Linux, scripting, servicios, redes, seguridad, bases de datos y despliegue web.

| Área | Carpeta |
| --- | --- |
| Sistemas y automatización | [systems-administration](./2asir/systems-administration/) |
| Servicios de red | [network-services](./2asir/network-services/) |
| Seguridad de red | [network-security](./2asir/network-security/) |
| Bases de datos | [database-administration](./2asir/database-administration/) |
| Despliegue web | [web-deployment](./2asir/web-deployment/) |
| Ciberseguridad | [cybersecurity](./2asir/cybersecurity/) |

## Proyecto destacado

<a href="./projects/final-project/">
  <img src="./projects/final-project/assets/portada.png" alt="Sentinel-IT" width="100%">
</a>

### Sentinel-IT

SOC autónomo y distribuido montado sobre dos nodos Raspberry Pi. El sistema recoge telemetría desde un nodo expuesto, la envía por MQTT/mTLS a AWS IoT Core y la analiza desde un nodo coordinador con dashboard Flask, SQLite y apoyo de IA para triage de eventos.

<img src="https://skillicons.dev/icons?i=raspberrypi,aws,docker,py,flask,sqlite,linux,bash&perline=8" alt="Stack de Sentinel-IT">

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

## Nota

Hay material de distinto tipo: prácticas completas, apuntes, ejercicios de clase y pruebas de aprendizaje. La intención no es presentar todo como producto final, sino dejar el ciclo ordenado y enseñar mejor las áreas técnicas que he trabajado.
