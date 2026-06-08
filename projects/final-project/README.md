# Final Project - Distributed IoT Security Architecture

Proyecto final centrado en una arquitectura de seguridad IoT distribuida entre dos nodos Raspberry Pi y AWS IoT Core.

## Resumen

El sistema plantea dos nodos fisicos conectados mediante mensajeria segura:

- Raspberry Pi 4 como nodo protegido/sensor.
- AWS IoT Core como capa central de comunicacion segura mediante MQTT/TLS.
- Raspberry Pi 5 como nodo coordinador, con API, base de datos, dashboard y agente de respuesta.

## Valor tecnico

| Area | Trabajo realizado |
| --- | --- |
| Infraestructura | Despliegue en Raspberry Pi, Docker y servicios Linux. |
| Seguridad | Comunicacion MQTT/TLS, monitorizacion, auditoria y simulacion de ataque. |
| Backend | API, gestion de eventos y base de datos. |
| Documentacion | Guias de uso, despliegue, arquitectura y pruebas. |

## Estructura

```text
final-project/
├── docs/                  # Documentacion tecnica y guias
├── PI-5/                  # Nodo coordinador Raspberry Pi 5
├── pi4-felix/             # Nodo protegido Raspberry Pi 4
├── docker-compose.yml     # Orquestacion del entorno
├── simulador_ataque.py    # Simulacion de ataque para pruebas
└── CHANGELOG.md
```

## Documentacion principal

| Documento | Enlace |
| --- | --- |
| Arquitectura | [docs/02_Arquitectura.md](./docs/02_Arquitectura.md) |
| Despliegue GitOps | [docs/02_Despliegue_GitOps.md](./docs/02_Despliegue_GitOps.md) |
| Plan de pruebas | [docs/03_Plan_de_Pruebas_y_Fase_Ataque.md](./docs/03_Plan_de_Pruebas_y_Fase_Ataque.md) |
| Despliegue con Docker y logs | [docs/05_Despliegue_Docker_y_Logs.md](./docs/05_Despliegue_Docker_y_Logs.md) |
| Guia de despliegue | [docs/guia_despliegue.md](./docs/guia_despliegue.md) |
| Guia de uso | [docs/guia_uso.md](./docs/guia_uso.md) |

## Estado

Proyecto en desarrollo y usado como trabajo final. La carpeta conserva codigo, documentacion, pruebas y material de despliegue.

