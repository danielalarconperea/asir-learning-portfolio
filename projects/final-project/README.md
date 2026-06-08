# Final Project - Distributed IoT Security Architecture

Proyecto final basado en una arquitectura de seguridad IoT distribuida usando Raspberry Pi y AWS IoT Core.

## Resumen

La idea principal es conectar dos nodos fisicos mediante mensajeria segura:

- Raspberry Pi 4 como nodo protegido.
- AWS IoT Core como punto central de comunicacion MQTT/TLS.
- Raspberry Pi 5 como nodo coordinador, con API, base de datos, dashboard y logica de respuesta.

## Partes principales

| Area | Contenido |
| --- | --- |
| Infraestructura | Raspberry Pi, Docker y servicios Linux. |
| Seguridad | MQTT/TLS, monitorizacion, auditoria y simulacion de ataque. |
| Backend | API, gestion de eventos, base de datos y dashboard. |
| Documentacion | Arquitectura, despliegue, pruebas y guias de uso. |

## Estructura

```text
final-project/
+-- docs/                  # Documentacion tecnica
+-- PI-5/                  # Nodo coordinador
+-- pi4-felix/             # Nodo protegido
+-- docker-compose.yml
+-- simulador_ataque.py
+-- CHANGELOG.md
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

## Contenido

La carpeta recoge el codigo, la documentacion y las pruebas principales del TFG.
