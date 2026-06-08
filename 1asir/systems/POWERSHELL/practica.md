Okay, let's break down this practical exercise step-by-step, assuming you're working in a virtualized environment like VirtualBox or VMware. Replace `XX` with your assigned number or any two digits (e.g., 01, 15).

**Entorno Inicial:**

1.  **Máquina Virtual Servidor:** Windows Server 2022.
2.  **Máquina Virtual Cliente:** Windows 10.
3.  **Configuración de Red Virtual:** Ambas máquinas virtuales conectadas a una "Red Interna" (e.g., llamada `intnet1` en VirtualBox/VMware). El servidor *también* necesitará una segunda interfaz de red conectada a Internet (modo NAT o Bridged en el hipervisor) para poder enrutar el tráfico más adelante.

---

**Manual Paso a Paso: Servicios de Red (1ª parte)**

**Pre-requisitos:**

*   Instalar Windows Server 2022 y Windows 10 en máquinas virtuales.
*   Configurar las interfaces de red de las VMs:
    *   **Servidor:**
        *   Adaptador 1: Red Interna (`intnet1`).
        *   Adaptador 2: NAT o Bridged (para acceso a Internet).
    *   **Cliente:**
        *   Adaptador 1: Red Interna (`intnet1`).
*   Asegúrate de que el nombre del servidor es descriptivo (e.g., `SRV-XX`).
*   Asegúrate de que el nombre del cliente es descriptivo (e.g., `CLI-XX`).
*   Reemplaza `XX` consistentemente en todas las IPs y nombres donde aparezca.

**Paso 1: Configuración IP Estática Inicial del Servidor (Interfaz Interna)**

1.  En el **Servidor Windows Server 2022**, abre "Configuración de Red e Internet" -> "Cambiar opciones del adaptador".
2.  Identifica el adaptador conectado a la "Red Interna". Haz clic derecho -> "Propiedades".
3.  Selecciona "Protocolo de Internet versión 4 (TCP/IPv4)" y haz clic en "Propiedades".
4.  Configura la IP estática:
    *   Dirección IP: `192.168.XX.1`
    *   Máscara de subred: `255.255.255.0`
    *   Puerta de enlace predeterminada: (Dejar en blanco por ahora)
    *   Servidor DNS preferido: `127.0.0.1` (El servidor se resolverá a sí mismo una vez instalado el rol DNS)
5.  Haz clic en "Aceptar" y "Cerrar".

**Paso 2: Instalación de Roles de Servidor**

1.  Abre el **Administrador del Servidor** (Server Manager).
2.  Haz clic en "Administrar" -> "Agregar roles y características".
3.  Sigue el asistente:
    *   Tipo de instalación: "Instalación basada en características o en roles".
    *   Selección del servidor: Selecciona tu servidor local.
    *   Roles de servidor: Marca las casillas para:
        *   **Servidor DHCP** (Añade características si lo pide).
        *   **Servidor DNS** (Añade características si lo pide).
        *   **Servidor Web (IIS)**.
        *   **Acceso Remoto** (Seleccionar este rol).
    *   Características: No se necesitan características adicionales por ahora, a menos que se pidan al seleccionar roles.
    *   Rol Servidor Web (IIS):
        *   En "Servicios de rol", asegúrate de que bajo "Servidor FTP" esté marcado **Servicio FTP**.
        *   Bajo "Desarrollo de aplicaciones", marca **CGI** (necesario para PHP más adelante).
    *   Rol Acceso Remoto:
        *   En "Servicios de rol", marca **Enrutamiento** (Routing).
    *   Confirmación: Revisa las selecciones y haz clic en "Instalar". Reinicia si es necesario después de la instalación.

**Paso 3: Configuración del Servidor DHCP (Parte 1 - Red 192.168.XX.0/24)**

1.  En el **Administrador del Servidor**, ve a "Herramientas" -> "DHCP".
2.  En la consola DHCP, haz clic derecho sobre el nombre del servidor y selecciona **"Autorizar"**. Puede tardar unos segundos (refresca con F5 si es necesario hasta que aparezca una flecha verde).
3.  Expande el nombre del servidor, haz clic derecho sobre "IPv4" y selecciona **"Ámbito nuevo..."**.
4.  Sigue el asistente para crear el ámbito:
    *   Nombre: `1asirXX`
    *   Descripción: (Opcional, e.g., "Ámbito para red interna inicial")
    *   Intervalo de direcciones IP:
        *   Dirección IP inicial: `192.168.XX.100`
        *   Dirección IP final: `192.168.XX.110`
    *   Máscara de subred: `255.255.255.0`
    *   Exclusiones y retraso: (Dejar en blanco por ahora, clic en "Siguiente").
    *   Duración de la concesión: `1` hora.
    *   Configurar opciones DHCP: Selecciona "Sí, deseo configurar estas opciones ahora".
    *   Enrutador (Puerta de enlace predeterminada): Introduce `192.168.XX.1` y haz clic en "Agregar".
    *   Dominio principal y servidores DNS:
        *   Dominio principal: (Dejar en blanco o poner uno si lo tienes).
        *   Servidores DNS: Introduce `192.168.XX.1` (el propio servidor) y haz clic en "Agregar". Luego, introduce `8.8.4.4` y haz clic en "Agregar".
    *   Servidores WINS: Deja en blanco, haz clic en "Siguiente".
    *   Activar ámbito: Selecciona "Sí, deseo activar este ámbito ahora".
5.  Haz clic en "Finalizar". El ámbito debería aparecer activo bajo IPv4.

**Paso 4: Configuración y Prueba del Cliente (Parte 1)**

1.  En la **Máquina Cliente Windows 10**:
    *   Abre "Configuración de Red e Internet" -> "Cambiar opciones del adaptador".
    *   Haz clic derecho en el adaptador de Red Interna -> "Propiedades".
    *   Selecciona "Protocolo de Internet versión 4 (TCP/IPv4)" -> "Propiedades".
    *   Asegúrate de que estén seleccionadas las opciones: **"Obtener una dirección IP automáticamente"** y **"Obtener la dirección del servidor DNS automáticamente"**.
    *   Haz clic en "Aceptar" y "Cerrar".
2.  **Prueba de Concesión:**
    *   Abre un Símbolo del sistema (cmd) en el **Cliente**.
    *   Ejecuta: `ipconfig /release` (Puede dar error si no tenía IP previa, es normal).
    *   Ejecuta: `ipconfig /renew`
    *   Ejecuta: `ipconfig /all`
    *   **Verifica:** Que la Dirección IPv4 esté en el rango `192.168.XX.100` - `192.168.XX.110`, la máscara sea `255.255.255.0`, la Puerta de enlace sea `192.168.XX.1`, y los Servidores DNS sean `192.168.XX.1` y `8.8.4.4`. Anota la **Dirección física (MAC)** del cliente.
3.  **Prueba en el Servidor:**
    *   En la consola DHCP del **Servidor**, ve a "Ámbito [192.168.XX.0] 1asirXX" -> "Concesiones de direcciones".
    *   **Verifica:** Que aparece la concesión otorgada al cliente.
4.  **Reserva de Dirección MAC:**
    *   En la consola DHCP del **Servidor**, dentro del ámbito, haz clic derecho en "Reservas" -> "Reserva nueva...".
    *   Nombre de la reserva: (e.g., `ClienteWin10`)
    *   Dirección IP: `192.168.XX.109`
    *   Dirección MAC: Introduce la MAC del cliente (sin guiones ni dos puntos, o con guiones según pida el formato).
    *   Descripción: (Opcional).
    *   Tipos admitidos: "Ambos" o "Solo DHCP".
    *   Haz clic en "Agregar" y "Cerrar".
5.  **Prueba de Reserva en el Cliente:**
    *   En el **Cliente** (cmd):
        *   `ipconfig /release`
        *   `ipconfig /renew`
        *   `ipconfig /all`
    *   **Verifica:** Que el cliente ahora tiene la dirección IP `192.168.XX.109`.

**Paso 5: Cambio de Direccionamiento de Red y Configuración de Enrutamiento (NAT)**

1.  **Cambiar IP Estática del Servidor (Interfaz Interna):**
    *   En el **Servidor**, vuelve a las propiedades TCP/IPv4 del adaptador de Red Interna.
    *   Cambia la configuración a:
        *   Dirección IP: `10.XX.0.1`
        *   Máscara de subred: `255.255.0.0`
        *   Puerta de enlace predeterminada: (Dejar en blanco)
        *   Servidor DNS preferido: `10.XX.0.1` (Ahora usará su nueva IP interna)
    *   Haz clic en "Aceptar" y "Cerrar".
2.  **Configurar Enrutamiento y Acceso Remoto (RRAS) para NAT:**
    *   En el **Administrador del Servidor**, ve a "Herramientas" -> "Enrutamiento y acceso remoto".
    *   Haz clic derecho en el nombre del servidor (local) -> "Configurar y habilitar Enrutamiento y acceso remoto".
    *   Sigue el asistente:
        *   Selecciona: **"Traducción de direcciones de red (NAT)"**.
        *   Selección de la red pública: Elige la interfaz de red conectada a Internet (la que está en modo NAT/Bridged en el hipervisor).
        *   Selección de la red privada: El asistente debería detectar automáticamente la red `10.XX.0.0/16`. Si no, selecciónala manualmente. Asegúrate de que la interfaz `10.XX.0.1` está seleccionada como la red interna a la que darás servicio NAT.
        *   Finaliza el asistente. El servicio RRAS se iniciará.

**Paso 6: Modificación de la Configuración del Servidor DHCP (Parte 2 - Red 10.XX.0.0/16)**

1.  En la consola DHCP del **Servidor**:
    *   Expande IPv4 -> Haz clic derecho en el ámbito `[192.168.XX.0] 1asirXX` -> "Propiedades".
    *   En la pestaña "General", **cambia el intervalo de direcciones**:
        *   Dirección IP inicial: `10.XX.0.10`
        *   Dirección IP final: `10.XX.0.20`
        *   Máscara de subred: `255.255.0.0` (Asegúrate de que la longitud sea 16).
        *   **NOTA:** El nombre del ámbito no se puede cambiar fácilmente aquí, pero los rangos sí.
    *   Haz clic en "Aplicar". Te advertirá que el rango ha cambiado. Acepta.
    *   Ve a "Ámbito [192...]" -> "Opciones de ámbito".
        *   **003 Enrutador:** Haz doble clic, elimina la IP antigua (`192.168.XX.1`), introduce `10.XX.0.1` y haz clic en "Agregar" y "Aceptar".
        *   **006 Servidores DNS:** Haz doble clic.
            *   **IMPORTANTE:** Para que la resolución interna de `pagina.es` funcione más tarde, DEBES añadir el servidor DNS local PRIMERO.
            *   Elimina las IPs antiguas (`192.168.XX.1`, `8.8.4.4`).
            *   Introduce `10.XX.0.1` y haz clic en "Agregar".
            *   Introduce `208.67.222.222` (OpenDNS) y haz clic en "Agregar".
            *   Introduce `208.67.220.220` (OpenDNS) y haz clic en "Agregar".
            *   Haz clic en "Aceptar".
        *   **051 Tiempo de concesión:** Haz doble clic y cambia la duración a `2` días. Haz clic en "Aceptar".
    *   **Actualizar Reserva:** Ve a "Reservas", haz clic derecho en la reserva del cliente -> "Propiedades". Cambia la Dirección IP asignada a una dentro del nuevo rango (p.ej., `10.XX.0.19`, ya que `109` está fuera del rango `10-20`). Haz clic en "Aceptar". *Opcionalmente, puedes eliminar la reserva si ya no es necesaria.*
    *   Haz clic derecho en el nombre del servidor -> "Todas las tareas" -> "Reiniciar" para asegurarte de que los cambios se aplican.

**Paso 7: Prueba del Cliente (Parte 2 - Nueva Red)**

1.  En el **Cliente Windows 10** (cmd):
    *   `ipconfig /release`
    *   `ipconfig /renew`
    *   `ipconfig /all`
    *   **Verifica:**
        *   Dirección IPv4: En el rango `10.XX.0.10` - `10.XX.0.20` (o la IP reservada si la mantuviste y actualizaste).
        *   Máscara de subred: `255.255.0.0`.
        *   Puerta de enlace predeterminada: `10.XX.0.1`.
        *   Servidores DNS: `10.XX.0.1`, `208.67.222.222`, `208.67.220.220`.
2.  **Prueba de Conectividad a Internet:**
    *   `ping 8.8.8.8` (Debería responder).
    *   Abre un navegador web y visita una página externa (e.g., `google.com`). Debería funcionar gracias al NAT configurado en el servidor.
3.  **Prueba en el Servidor:**
    *   Revisa las "Concesiones de direcciones" en la consola DHCP para confirmar la nueva concesión.

**Paso 8: Instalación y Configuración del Servidor WEB (IIS con PHP)**

1.  **Instalar PHP:**
    *   La forma más fácil en Windows Server es usar el **Instalador de Plataforma Web de Microsoft (Web Platform Installer - WebPI)**.
    *   Descárgalo e instálalo desde el sitio oficial de Microsoft si no está disponible.
    *   Ejecuta WebPI, busca "PHP" (elige una versión reciente como 8.x o 7.4) y haz clic en "Agregar" e "Instalar". Esto debería instalar PHP y configurar IIS para usarlo (incluyendo el módulo CGI/FastCGI).
2.  **Crear Estructuras de Directorios para las Webs:**
    *   Crea carpetas para los sitios:
        *   `C:\inetpub\wwwroot\site1`
        *   `C:\inetpub\wwwroot\site2`
3.  **Crear Contenido Web:**
    *   **Sitio 1 (`site1`):**
        *   Crea un archivo llamado `index.php` dentro de `C:\inetpub\wwwroot\site1`.
        *   Edita `index.php` y añade el siguiente contenido:
            ```php
            <?php
            phpinfo();
            ?>
            ```
    *   **Sitio 2 (`site2`):**
        *   Copia el archivo `index.html` (o los archivos necesarios) de tu proyecto de "Lenguaje de Marcas" a la carpeta `C:\inetpub\wwwroot\site2`. Asegúrate de que haya un `index.html`.
4.  **Configurar los Sitios en IIS:**
    *   Abre el **Administrador de Internet Information Services (IIS)** desde Herramientas en el Administrador del Servidor.
    *   Expande el servidor -> "Sitios".
    *   **Sitio 1 (Predeterminado modificado):**
        *   Selecciona el "Default Web Site".
        *   En el panel derecho, haz clic en "Enlaces..." (Bindings). Edita el enlace existente para el puerto 80. Asegúrate de que esté asignado a la IP `10.XX.0.1` o "Todas las sin asignar".
        *   Haz clic en "Configuración básica..." y cambia la "Ruta de acceso física" a `C:\inetpub\wwwroot\site1`.
        *   Selecciona el sitio en el árbol izquierdo. Haz doble clic en "Documento predeterminado". Asegúrate de que `index.php` esté en la lista y súbelo a la parte superior (o agrégalo si no está).
        *   Selecciona el sitio en el árbol izquierdo. Haz doble clic en "Examen de directorios". Haz clic en "Habilitar" en el panel derecho.
    *   **Sitio 2 (Nuevo sitio en puerto diferente):**
        *   Haz clic derecho en "Sitios" -> "Agregar sitio web...".
        *   Nombre del sitio: `Site2_LM`
        *   Ruta de acceso física: `C:\inetpub\wwwroot\site2`
        *   Enlace:
            *   Tipo: http
            *   Dirección IP: `10.XX.0.1` (o "Todas las sin asignar")
            *   Puerto: `8080`
        *   Haz clic en "Aceptar".
        *   Selecciona el nuevo sitio (`Site2_LM`) en el árbol izquierdo. Haz doble clic en "Documento predeterminado". Asegúrate de que `index.html` esté presente y en la parte superior.
        *   Selecciona el nuevo sitio (`Site2_LM`) en el árbol izquierdo. Haz doble clic en "Examen de directorios". Asegúrate de que esté "Deshabilitado".
5.  **Prueba de los Sitios Web:**
    *   Desde el **Cliente Windows 10**, abre un navegador web:
        *   Visita `http://10.XX.0.1`. Deberías ver la página de información de PHP (`phpinfo`). Intenta navegar a una subcarpeta (si creaste alguna) o directamente a `http://10.XX.0.1/` para ver si el examen de directorios funciona (debería mostrar el contenido de `site1`).
        *   Visita `http://10.XX.0.1:8080`. Deberías ver tu página `index.html` de Lenguaje de Marcas. El examen de directorios no debería funcionar.

**Paso 9: Configuración del Servidor DNS**

1.  En el **Administrador del Servidor**, ve a "Herramientas" -> "DNS".
2.  Expande el nombre del servidor.
3.  Haz clic derecho en "Zonas de búsqueda directa" -> "Zona nueva...".
4.  Sigue el asistente:
    *   Tipo de zona: "Zona principal".
    *   Replicación de zona: (Si estás en un dominio, elige la opción adecuada. Si no, "Almacenar la zona en Active Directory..." estará deshabilitado, simplemente haz clic en Siguiente). **"Almacenar la zona en un archivo..."** (si no hay AD). Nombre de archivo `pagina.es.dns`.
    *   Nombre de zona: `pagina.es`
    *   Actualización dinámica: "No admitir actualizaciones dinámicas" (más seguro para este ejercicio).
    *   Finaliza el asistente.
5.  Selecciona la nueva zona `pagina.es` en el árbol izquierdo.
6.  Haz clic derecho en el panel derecho -> "Host nuevo (A o AAAA)...".
    *   Nombre (usar primario si está en blanco): (Dejar en blanco para que apunte a `pagina.es` o escribir `www` para que apunte a `www.pagina.es`). Usemos en blanco.
    *   Dirección IP: `10.XX.0.1` (La IP interna del servidor donde corre IIS).
    *   Marca "Crear registro de puntero (PTR) asociado" si tienes una zona inversa configurada (no es obligatorio para este ejercicio).
    *   Haz clic en "Agregar host". Acepta la confirmación. Clic en "Realizado".
7.  **(Importante) Configurar Reenvioadores:**
    *   Haz clic derecho en el nombre del servidor DNS -> "Propiedades".
    *   Ve a la pestaña "Reenvioadores".
    *   Haz clic en "Editar". Introduce las IPs de los DNS públicos (e.g., `8.8.8.8`, `8.8.4.4` o los de OpenDNS `208.67.222.222`, `208.67.220.220`) y haz clic en "Agregar".
    *   Haz clic en "Aceptar". Esto permite que tu servidor DNS resuelva nombres externos.
8.  **Prueba de DNS:**
    *   Desde el **Cliente Windows 10** (cmd):
        *   `ipconfig /flushdns` (Limpia la caché de DNS).
        *   `nslookup pagina.es` (Debería resolver a `10.XX.0.1`).
        *   `nslookup www.google.com` (Debería resolver usando los reenviadores).
    *   En el navegador del **Cliente**, visita `http://pagina.es`. Deberías ver la misma página de `phpinfo` que viste al acceder por IP (`http://10.XX.0.1`).

**Paso 10: Configuración del Servidor FTP**

1.  **Crear Usuario para Actualización Web:**
    *   En el **Servidor**, abre "Administración de equipos" (compmgmt.msc).
    *   Ve a "Usuarios y grupos locales" -> "Usuarios".
    *   Haz clic derecho -> "Usuario nuevo...".
        *   Nombre de usuario: `webupdater`
        *   Contraseña: (Elige una contraseña segura).
        *   Desmarca "El usuario debe cambiar la contraseña en el siguiente inicio de sesión".
        *   Marca "La contraseña nunca expira" (para la práctica).
        *   Haz clic en "Crear" y "Cerrar".
2.  **Configurar Permisos de Carpeta Web:**
    *   Ve a la carpeta `C:\inetpub\wwwroot\site1`.
    *   Haz clic derecho -> "Propiedades" -> pestaña "Seguridad" -> "Editar..." -> "Agregar...".
    *   Escribe `webupdater` y haz clic en "Comprobar nombres". Acepta.
    *   Selecciona el usuario `webupdater` y dale permisos de **"Modificar"** (esto incluye leer, escribir, eliminar). Haz clic en "Aplicar" y "Aceptar".
3.  **Configurar Sitio FTP en IIS:**
    *   Abre el **Administrador de IIS**.
    *   Haz clic derecho en "Sitios" bajo tu servidor -> "Agregar sitio FTP...".
    *   Nombre del sitio FTP: `FTPUsers` (o similar).
    *   Ruta de acceso física: Elige una carpeta base para los usuarios FTP. Puede ser una nueva como `C:\FTPRoot` o, si quieres dar acceso a carpetas específicas, necesitarás configurar aislamiento de usuarios o directorios virtuales. Para cumplir el requisito de "carpetas de usuarios creados en las prácticas anteriores", asumamos que tenías carpetas en `C:\Users` o una estructura como `C:\FTPData\User1`, `C:\FTPData\User2`. Para simplificar aquí, usemos `C:\inetpub\ftproot` (crea esta carpeta). *Si el objetivo es SOLO el update web, podríamos apuntar directamente a `site1`, pero el prompt pide acceso a "carpetas de usuarios" Y un usuario de actualización.* Vamos a crear un sitio FTP genérico y luego añadimos un directorio virtual para la web.
        *   Ruta física: `C:\inetpub\ftproot` (crea esta carpeta si no existe).
    *   Enlace y configuración SSL:
        *   Dirección IP: `10.XX.0.1` (o "Todas las sin asignar").
        *   Puerto: `21`.
        *   Marca "Iniciar sitio FTP automáticamente".
        *   Selecciona "Sin SSL". (Para producción, usarías SSL).
    *   Información de autenticación y autorización:
        *   Autenticación: Marca **"Básica"** (envía contraseña en texto plano, ¡cuidado! Adecuado para pruebas internas). Puedes habilitar "Autenticación de Windows" también si usas usuarios del servidor/dominio.
        *   Autorización: Selecciona "Roles o grupos de usuarios especificados". Escribe `Usuarios` (el grupo local estándar) o usuarios específicos que deberían tener acceso a la carpeta base `ftproot`.
        *   Permisos: Marca "Leer" y "Escribir".
    *   Haz clic en "Finalizar".
4.  **Añadir Directorio Virtual para Actualización Web:**
    *   Expande "Sitios" -> Selecciona tu nuevo sitio FTP (`FTPUsers`).
    *   Haz clic derecho -> "Agregar directorio virtual...".
    *   Alias: `web_update`
    *   Ruta de acceso física: `C:\inetpub\wwwroot\site1`
    *   Haz clic en "Aceptar".
    *   Ahora, selecciona el directorio virtual `web_update`. Haz doble clic en "Reglas de autorización de FTP".
    *   Elimina las reglas heredadas si las hay (o añade una más específica).
    *   Haz clic en "Agregar regla de permiso..." en el panel derecho.
    *   Selecciona "Usuarios especificados". Escribe `webupdater`.
    *   Permisos: Marca "Leer" y "Escribir".
    *   Haz clic en "Aceptar".
5.  **(Importante) Firewall de Windows:**
    *   FTP usa el puerto 21 para comandos y puertos adicionales para datos (modo pasivo). La instalación del rol FTP *debería* haber creado reglas de firewall, pero verifícalo.
    *   Abre "Firewall de Windows Defender con seguridad avanzada".
    *   Ve a "Reglas de entrada". Busca reglas como "Servidor FTP" (para tráfico del puerto 21) y "Servidor FTP pasivo". Asegúrate de que estén habilitadas para el perfil de red "Privado" (o "Todos").
6.  **Prueba de FTP:**
    *   Desde el **Cliente Windows 10**, usa un cliente FTP como FileZilla o el Explorador de Windows (escribe `ftp://10.XX.0.1` en la barra de direcciones).
    *   **Prueba 1 (Usuario normal):** Intenta iniciar sesión con una cuenta de usuario estándar del servidor (si la incluiste en la autorización del sitio base). Deberías poder ver el contenido de `C:\inetpub\ftproot` y quizás crear/subir archivos allí.
    *   **Prueba 2 (Actualizador web):** Inicia sesión como `webupdater` con su contraseña.
        *   Deberías poder ver el directorio virtual `web_update`.
        *   Navega dentro de `web_update`. Deberías ver `index.php`.
        *   Intenta subir un archivo de prueba o modificar `index.php` (haz una copia antes). Debería funcionar.
        *   Intenta navegar "hacia arriba" desde `web_update` a la raíz del FTP (si la configuración lo permite) y comprueba si puedes escribir allí (depende de los permisos dados al sitio base y si `webupdater` pertenece al grupo autorizado allí).

---

**Documentación y Comprobaciones Finales:**

*   Para cada paso, haz capturas de pantalla de las configuraciones clave (IPs, DHCP, DNS, IIS, FTP, RRAS) y de los resultados de las pruebas (`ipconfig /all`, `ping`, `nslookup`, navegador web, cliente FTP).
*   Documenta cualquier problema encontrado y cómo lo solucionaste.
*   Asegúrate de que todas las pruebas funcionan como se describe:
    *   Cliente obtiene IP de DHCP (en ambos rangos).
    *   Cliente tiene acceso a Internet vía NAT.
    *   Ambos sitios web son accesibles (uno por IP/puerto 80 y el otro por IP/puerto 8080).
    *   El sitio `pagina.es` es accesible por nombre DNS.
    *   Se puede acceder por FTP y el usuario `webupdater` puede modificar los archivos del sitio web `pagina.es` a través del directorio virtual FTP.

Este manual cubre todos los puntos solicitados en la práctica. ¡Buena suerte!