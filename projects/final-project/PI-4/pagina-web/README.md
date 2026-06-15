# pagina-web — Honeypot web "CyberGuard / SentinelIT" (objetivo de demostración)

Aplicación web **deliberadamente vulnerable** que corre en el nodo PI-4 y hace de
**superficie de ataque** del proyecto: es el escenario donde se generan los
ataques (SQLi, XSS, *session hijacking*) que el SOC (PI-5) detecta, analiza con
IA y mitiga bajo control humano (HITL).

> **Es un objetivo de demostración, no "el objetivo" del SOC.** El sistema es
> genérico —el sensor `sentinel-agent` se autoconfigura en cualquier servidor—;
> este honeypot es solo un *target* de ejemplo para ver el flujo completo
> ataque → detección → respuesta de extremo a extremo.

## Qué demuestra

| Vector | Dónde | Qué dispara en el SOC |
|--------|-------|------------------------|
| **SQL Injection** | login y formularios de búsqueda | evento `SQLi` → triage IA → propuesta de bloqueo (HITL) |
| **XSS** | campos reflejados/almacenados | evento `XSS` → triage IA |
| **Session hijacking** | robo de cookie de sesión PHP | cierre remoto de la sesión comprometida vía [`cerrar_sesion_admin.php`](cerrar_sesion_admin.php) |
| **Fuerza bruta** | login / SSH / FTP del host | detección por ventana deslizante en el sensor |

> ⚠️ **Inseguro a propósito.** Pensado para laboratorio/demo. No lo expongas a
> internet con datos reales ni reutilices sus credenciales.

## Stack

PHP (7.4+) + Bootstrap + Bootstrap Icons, sobre MySQL/MariaDB. Sin framework: las
páginas se componen con *includes* (`header`/`navbar`/`footer`).

## Estructura

```
pagina-web/
├── index.php, servicios.php, como-funciona.php, tecnologias.php,
│   equipo.php, contacto.php, sugerencias.php   # sitio público (marketing)
├── login.php, logout.php, panel.php            # área de cliente
├── admin.php, admin_logs.php                   # panel de administración
├── cerrar_sesion_admin.php                     # cierre remoto de sesiones (anti-hijacking)
├── includes/                                   # header, navbar, footer, logger, session_control
├── css/main.css, js/{main,charts}.js           # estilos y gráficas
├── db.php                                       # conexión PDO (ajustar credenciales)
└── schema.sql                                   # tablas (eventos, usuarios, ajustes) + datos de prueba
```

## Relación con el SOC

La tabla `eventos` de esta app es su **propio** registro (para el panel de
administración). El **monitoreo del SOC es independiente**: el sensor
`sentinel-agent` instalado en PI-4 lee los logs del host (Apache/vsftpd/SSH),
detecta los ataques y los publica **por MQTT/mTLS a AWS IoT Core → PI-5**. La web
no envía nada al SOC; es el objetivo, no el sensor.

## Despliegue

Pasos detallados en [`guia_despliegue.md`](guia_despliegue.md).
