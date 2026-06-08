# **Apuntes CCNA 2 - Módulo 1: Configuración Básica del Dispositivo**  
**Integración con módulos anteriores y estructura para futuros temas**  

---

# 1. Configuración Básica de Dispositivos

## 1.1 Secuencia de Arranque y Carga del Sistema

- **Proceso de arranque en un switch Cisco**  
  Tras encender el dispositivo, se ejecuta una secuencia de cinco pasos:
  - **Paso 1:** Se ejecuta el POST (Power-On Self Test) desde la ROM para verificar la CPU, la memoria DRAM y la memoria flash.
  - **Paso 2:** Se carga el cargador de arranque (boot loader) desde la ROM.
  - **Paso 3:** El boot loader inicializa registros de la CPU y asigna la memoria física.
  - **Paso 4:** Se inicializa el sistema de archivos en la memoria flash.
  - **Paso 5:** Se localiza y carga la imagen del sistema operativo IOS, transfiriéndole el control al IOS.  

- **Comandos clave:**  
  ```bash
  boot system flash:/ruta/ios.bin  # Define la imagen de arranque.
  show boot                        # Muestra la configuración de arranque.
  ```  

## 1.2 Indicadores LED y Recuperación del Sistema
![Indicadores LED de un switch](..\IMG\LED.png)
- **Indicadores LED:**  
  Cada LED en un switch ofrece información sobre el estado del sistema y de los puertos:
  - **LED SYST:** Indica que el sistema recibe alimentación.
  - **LED RPS:** Indica el estado de la fuente de alimentación redundante.
  - **LED STAT:** Muestra el estado operativo del puerto.
  - **LED DUPLX y SPEED:** Indican respectivamente el modo dúplex y la velocidad configurada.
  - **LED PoE:** Presente en switches compatibles con PoE para indicar el estado de alimentación de los puertos.
  
- **Recuperación tras un bloqueo:**  

  En caso de fallo en el sistema operativo (por falta o daño de archivos), el boot loader permite acceder a la consola de recuperación para formatear la flash, reinstalar el IOS o recuperar contraseñas. Se requiere conexión por consola y la pulsación del botón Mode al reiniciar.

## 1.3 Configuración de Acceso Remoto

- **Acceso mediante SVI (Switch Virtual Interface):**  
  Para la administración remota se debe asignar una dirección IP a una interfaz virtual (SVI).  
  - **Ejemplo de configuración de SVI:**  
    - Asignar una IP y máscara a la interfaz VLAN (por ejemplo, VLAN 99).  
    - Configurar un gateway predeterminado para que el switch sea accesible desde redes remotas.  
    - Verificar la configuración con comandos como `show ip interface brief` y `show ipv6 interface brief`.  
  - **Consideraciones:**  
    - Por defecto, todos los puertos están en VLAN 1, por lo que se recomienda utilizar una VLAN de administración distinta (ej. VLAN 99).  
    - La configuración IPv6 requiere habilitar la función en el switch (en algunos casos, mediante el comando `sdm prefer dual-ipv4-and ipv6 default` y un reinicio).
  
- **Acceso Remoto Seguro:**  
  Se recomienda evitar Telnet, ya que transmite credenciales en texto plano.  
  - **Telnet:** Usa el puerto TCP 23 y resulta vulnerable a interceptaciones (Wireshark puede capturar usuario y contraseña).  
  - **SSH:** Utiliza el puerto TCP 22 y cifra la comunicación.  
    - **Pasos para configurar SSH en un switch:**
      1. Verificar compatibilidad con el comando `show ip ssh`.
      2. Configurar un nombre de dominio con `ip domain-name [nombre_dominio]`.
      3. Generar pares de claves RSA con `crypto key generate rsa`.
      4. Configurar autenticación de usuario local con `username [nombre] secret [password]`.
      5. Habilitar SSH en las líneas VTY con `transport input ssh` y `login local`.
      6. Forzar el uso de SSH versión 2 mediante `ip ssh version 2`.  
  - Se puede verificar la configuración y el estado de SSH con `show ip ssh`.  
  citeturn0file0

## 1.4 Configuración Básica de Routers

Aunque los routers y switches comparten muchas similitudes en su configuración inicial, en los routers se deben considerar aspectos particulares:

- **Parámetros básicos:**
  - Asignar un nombre único al dispositivo.
  - Configurar contraseñas y banners de advertencia (por notificaciones legales de acceso no autorizado).
  - Guardar la configuración activa para evitar pérdida de parámetros tras un reinicio.
  
- **Configuración de Interfaces:**
  - Las interfaces deben configurarse con una dirección IP y, de ser necesario, una descripción para facilitar la identificación.  
    - Ejemplo:  
      ```
      interface GigabitEthernet0/0
       ip address [ip-address] [subnet-mask]
       no shutdown
       description Conexión a [destino]
      ```
  - **Interfaz Loopback:**  
    - Se configura con el comando `interface loopback [número]` y se le asigna una dirección IP.  
    - Es útil para pruebas internas y para simular enlaces a Internet en entornos de laboratorio.  
  - **Verificación de conectividad y estado:**  
    - Comandos como `show ip interface brief`, `show running-config interface [interface-id]` y `show ip route` permiten validar que las interfaces estén activas y correctamente configuradas.
  
- **Topología Dual Stack:**  
  - Se ilustra la coexistencia de direccionamiento IPv4 e IPv6 en la configuración de interfaces, destacándose la necesidad de asignar direcciones globales y link-local en IPv6.  
  citeturn0file0

---

# 2. Conceptos de Switching

Aunque el documento se centra en la configuración básica, se extraen conceptos fundamentales del switching para entender el funcionamiento de los switches en redes Cisco.

## 2.1 Fundamentos del Switching

- **Comunicación Dúplex:**  
  - **Dúplex Completo:** Permite la transmisión y recepción simultánea de datos, eliminando dominios de colisión en puertos conectados individualmente a un dispositivo.  
  - **Semidúplex:** La comunicación se produce en una sola dirección a la vez, pudiendo generar colisiones.  
  - En puertos Gigabit y 10 Gb, se requiere operar en dúplex completo para aprovechar el ancho de banda.  

## 2.2 Configuración de Puertos

- **Parámetros de Puertos en la Capa Física:**  
  - Los puertos pueden configurarse manualmente para establecer velocidad y modo dúplex utilizando los comandos `speed` y `duplex`.  
  - La configuración predeterminada en switches modernos es la negociación automática, aunque para conexiones a dispositivos fijos (servidores, PC) se recomienda configurar estos parámetros de forma manual para evitar incompatibilidades.
  
- **Auto-MDIX:**  
  - Esta función permite que la interfaz detecte y configure automáticamente el tipo de cable (directo o cruzado) requerido, facilitando la interconexión entre dispositivos sin preocuparse por el tipo de cable.
  - Se habilita mediante el comando `mdix auto` y requiere que la velocidad y el modo dúplex estén configurados en modo `auto`.  
  citeturn0file0

---

# 3. VLANs

Aunque el material se centra en la configuración básica, se incluyen aspectos importantes sobre el uso de VLANs en la administración de switches.

## 3.1 Uso de VLAN en la Administración

- **VLAN Predeterminada y VLAN de Administración:**
  - Por defecto, todos los puertos están asignados a la VLAN 1.
  - Se recomienda crear una VLAN exclusiva para la administración (por ejemplo, VLAN 99) para mejorar la seguridad.
  
- **Configuración de SVI para VLAN:**
  - La asignación de una dirección IP a la SVI (Switch Virtual Interface) se realiza en el modo de configuración de interfaz VLAN.
  - Se debe configurar la dirección IP y la máscara, además del gateway predeterminado para el acceso remoto.  
  - La SVI no permite enrutar paquetes de Capa 3; su función es exclusiva para la administración remota.  
  citeturn0file0

---

# 4. Enrutamiento Inter-VLAN

Aunque el documento no profundiza en el enrutamiento entre VLANs, se hace mención de los siguientes puntos:

- **Opciones de Enrutamiento:**
  - La configuración de SVI en switches de Capa 2 permite la administración, pero para el enrutamiento entre VLANs es necesario utilizar un router (configuración “router-on-a-stick”) o switches de Capa 3.
  
- **Conceptos Básicos:**
  - Se debe tener en cuenta que la segmentación mediante VLANs requiere la interconexión de diferentes dominios de difusión mediante enrutamiento, lo cual se suele practicar en fases posteriores del curso.  
  *(Información ampliable en documentos posteriores del conjunto CCNA 2)*

---

# 5. EtherChannel

El material de esta parte no cubre la agrupación de enlaces (EtherChannel). Este tema se abordará en documentos posteriores que forman parte del temario completo de CCNA 2.

---

# 6. DHCPv4

La configuración y funcionamiento del protocolo DHCP para IPv4 no se detalla en este módulo, correspondiendo a temas que se desarrollarán en documentos posteriores del curso.

---

# 7. SLAAC y DHCPv6

## 7.1 Asignación de Direcciones en IPv6

- **Direcciones Link-Local y Global:**
  - Al configurar IPv6 en una interfaz, se asigna automáticamente una dirección link-local (prefijo FE80).
  - Es posible asignar manualmente una dirección global para la administración y conectividad.
  
- **Verificación:**
  - Se utiliza el comando `show ipv6 interface brief` para observar las direcciones asignadas y el estado de la interfaz, mostrando tanto la dirección de unidifusión global como la link-local.  
  citeturn0file0

---

# 8. Conceptos FHRP (First Hop Redundancy Protocols)

El documento no aborda directamente los protocolos de redundancia de primer salto (como HSRP). Este tema se incluirá en módulos posteriores donde se traten estrategias de alta disponibilidad y redundancia en la puerta de enlace.

---

# 9. Conceptos de Seguridad en LAN

## 9.1 Amenazas en el Acceso Remoto

- **Telnet vs SSH:**
  - **Telnet:** Opera en el puerto TCP 23 y envía datos sin cifrar, lo que puede ser interceptado.
  - **SSH:** Opera en el puerto TCP 22, ofreciendo conexiones cifradas y autenticación segura.
  
- **Buenas Prácticas:**
  - Se recomienda utilizar SSH en lugar de Telnet para la administración remota.
  - Verificar la compatibilidad del dispositivo con características criptográficas (por ejemplo, mediante la presencia de “k9” en el nombre del IOS).  
  citeturn0file0

---

# 10. Configuración de Seguridad en Switches

Aunque el documento se centra en la configuración básica, se pueden extraer algunas pautas de seguridad:

- **Acceso Remoto Seguro:**  
  - Uso de SSH en lugar de Telnet.
  - Configuración de contraseñas seguras y banners de advertencia.
  
- **Consideraciones Adicionales (a desarrollar en módulos posteriores):**
  - Implementación de Port Security.
  - Configuración de BPDU Guard y otras medidas para mitigar ataques internos.

---

# 11. Conceptos de WLAN y 12. Configuración de WLAN

Estos temas no se abordan en el material presentado. Se tratarán en módulos específicos dedicados a redes inalámbricas dentro del temario oficial CCNA 2.

---

# 13. Conceptos de Enrutamiento

## 13.1 Funcionamiento de Routers y Tablas de Enrutamiento

- **Interconexión de Redes:**
  - Los routers pueden interconectar redes LAN y WAN, soportando diversas interfaces (Gigabit Ethernet, interfaces seriales, DSL, etc.).
  
- **Configuración de Interfaces:**
  - Cada interfaz debe configurarse con una dirección IP y activarse con el comando `no shutdown`.
  
- **Verificación:**
  - Uso de comandos como `show ip interface brief` y `show ip route` para validar la conectividad.
  
- **Interfaz Loopback:**
  - Una interfaz lógica interna que siempre se mantiene en estado “up” y se utiliza para pruebas y administración.  
  citeturn0file0

---

# 14. Enrutamiento Estático

## 14.1 Configuración y Verificación

- **Configuración de Rutas Estáticas:**
  - Se pueden configurar rutas estáticas y rutas por defecto utilizando el comando  
    `ip route [red_destino] [máscara] [ip_del_siguiente_salto]`  
  - Es esencial guardar la configuración para mantener las rutas tras reinicios.
  
- **Verificación:**
  - Comandos como `show ip route` permiten verificar la presencia de rutas conectadas directamente y rutas estáticas.
  
- **Ejemplos Prácticos:**
  - La salida de `show ip route` incluye entradas marcadas con “C” para redes conectadas y “L” para rutas locales del router.  
  citeturn0file0

---

# 15. Resolución de Problemas en Rutas Estáticas y Predeterminadas

## 15.1 Herramientas y Comandos de Diagnóstico

- **Comandos de Verificación:**
  - `show interfaces` muestra el estado, estadísticas y posibles errores (errores de entrada/salida, colisiones, CRC, etc.).
  - `show running-config interface [interface-id]` muestra la configuración aplicada a una interfaz específica.
  - `show ip interface brief` y `show ipv6 interface brief` permiten revisar rápidamente el estado de las interfaces.
  
- **Filtrado de Salida:**
  - Uso del operador pipe (`|`) para filtrar la salida de comandos:  
    - `include`: muestra solo líneas que contienen el término de búsqueda.
    - `exclude`: descarta líneas con el término especificado.
    - `begin` y `section`: para mostrar secciones específicas.
  
- **Historial de Comandos:**
  - Se puede acceder al historial con las teclas de flecha (↑ y ↓) o con `show history` para repasar comandos recientes y ayudar en la solución de problemas.
  
- **Ejemplos Prácticos de Troubleshooting:**
  - Si una interfaz está “up” pero el protocolo está “down”, podría indicar problemas de configuración en el otro extremo o errores físicos.
  - El análisis de errores como “input errors”, “CRC errors”, “runt frames” y “giants” ayuda a identificar problemas en el cableado o incompatibilidades en el modo dúplex.  
  citeturn0file0

---

# Conclusión

Este documento extrae y organiza de manera coherente la información fundamental del Módulo 1 – Configuración Básica del Dispositivo – para CCNA 2. Se abordan aspectos críticos de la inicialización y configuración de dispositivos, el funcionamiento básico del switching, la administración de VLAN para la gestión, los fundamentos de enrutamiento en routers y procedimientos de verificación y troubleshooting. Temas más avanzados (como EtherChannel, DHCP, FHRP, y WLAN) se desarrollarán en las partes sucesivas del conjunto de documentos, integrándose de manera coherente en el temario oficial.

La información aquí presentada se apoya en conceptos prácticos, ejemplos de configuración y comandos esenciales, ofreciendo una base sólida para avanzar en la comprensión y práctica de la administración de redes Cisco.

---

Esta estructura organizada y detallada facilitará el estudio y la comprensión, cumpliendo con el objetivo de extraer toda la información relevante del material disponible.  
citeturn0file0