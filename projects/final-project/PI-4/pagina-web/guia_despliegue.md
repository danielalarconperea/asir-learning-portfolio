# Guía de Despliegue - SentinelIT

Esta guía explica los pasos necesarios para instalar y poner en marcha el panel web de SentinelIT y preparar la base de datos.

> ⚠️ **Honeypot deliberadamente vulnerable.** Esta web es el **objetivo de demostración** del proyecto (SQLi, XSS, *session hijacking*); ver [`README.md`](README.md). Despliégala solo en laboratorio/demo, nunca expuesta a internet con datos reales. Las credenciales por defecto son débiles a propósito.

## 1. Requisitos Previos
* **Servidor Web:** Apache o Nginx
* **PHP:** Versión 7.4 o superior (con extensión PDO_MySQL habilitada)
* **Base de Datos:** MySQL o MariaDB

## 2. Configuración de la Base de Datos
1. Inicia sesión en tu gestor de base de datos (por ejemplo, phpMyAdmin o mediante la consola de MySQL/MariaDB).
2. Crea una nueva base de datos llamada `SentinelIT` (o el nombre que prefieras).
3. Importa el archivo `schema.sql` proporcionado en el código fuente.
   - *Por consola:* `mysql -u root -p SentinelIT < schema.sql`
4. Este script creará las tablas necesarias (`eventos`, `usuarios`, `ajustes`) e insertará algunos datos de prueba.

## 3. Configuración del Proyecto Web
1. Mueve a la carpeta pública de tu servidor web (por ejemplo, `htdocs` en XAMPP, `www` en AppServ o `/var/www/html` en Linux) todos los archivos del proyecto.
2. Abre el archivo `db.php` con un editor de texto o código.
3. Verifica y ajusta las credenciales de conexión según tu entorno local:
   ```php
   $host = 'localhost';
   $db   = 'SentinelIT'; // El nombre de tu base de datos
   $user = 'root';       // Tu usuario de MySQL/MariaDB
   $pass = '';           // Tu contraseña de MySQL/MariaDB
   ```

## 4. Acceso al Panel
1. Abre tu navegador y dirígete a `http://localhost/SentinelIT-web` (o la ruta donde hayas colocado el proyecto).
2. Accede a la sección de **Iniciar Sesión**.
3. Las credenciales de prueba por defecto (si no has modificado los hashes en la base de datos) son:
   - **Administrador:** admin@SentinelIT.com / admin123
   - **Clientes:** cliente1@SentinelIT.com o cliente2@SentinelIT.com / cliente123

## 5. Relación con el SOC (monitorización)

El panel de esta web es **independiente del SOC**: su tabla `eventos` es solo el registro interno de la propia aplicación. La monitorización de seguridad la realiza el sensor [`sentinel-agent`](../../sentinel-agent/README.md) instalado en la Raspberry Pi, que lee los logs del host (Apache, vsftpd, SSH), detecta los ataques y los publica **por MQTT/mTLS a AWS IoT Core → PI-5** (el coordinador SOC). No hay que insertar registros a mano ni habilitar endpoints de recepción en esta web.

