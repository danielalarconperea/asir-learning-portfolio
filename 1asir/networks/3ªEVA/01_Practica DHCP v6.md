A continuación encontrarás una guía paso a paso para configurar en Packet Tracer un escenario de DHCPv6 (tanto con estado como sin estado) y SLAAC en routers Cisco. El ejemplo se basa en la topología que muestras en la imagen, donde tenemos varias redes IPv6 y queremos que los PCs obtengan su configuración automáticamente.

---

## 1. Habilitar IPv6 en los routers

1. Entra al **modo de configuración global** de cada router y habilita el enrutamiento IPv6:
   ```bash
   Router(config)# ipv6 unicast-routing
   ```

2. **Asigna direcciones IPv6 a las interfaces** correspondientes. Por ejemplo, si en el Router0 la interfaz G0/0/0 conecta con la red 2001:B:B:B::/64, haz algo así:
   ```bash
   Router0(config)# interface g0/0/0
   Router0(config-if)# ipv6 address 2001:B:B:B::1/64
   Router0(config-if)# ipv6 address FE80::1 link-local
   Router0(config-if)# no shutdown
   ```
   Repite este procedimiento para cada interfaz del router, usando la red IPv6 que corresponda (2001:A:A:A::/64, 2001:C:C:C::/64, etc.) y siempre configurando la **link-local** (FE80::1, por ejemplo).

3. Repite lo mismo en el Router1, si forma parte de la topología, asignando direcciones a sus interfaces según el esquema de red que hayas definido.

---

## 2. Configurar DHCPv6 **con estado** (Stateful)

Supongamos que en el Router0 queremos configurar DHCPv6 con estado para la red 2001:B:B:B::/64. El objetivo es que el PC de esa red reciba **dirección IPv6, DNS y dominio** por DHCPv6.

1. **Crear el pool DHCPv6**:
   ```bash
   Router0(config)# ipv6 dhcp pool DHCPv6_STATEFUL
   Router0(config-dhcpv6)# address prefix 2001:B:B:B::/64  <-- Prefijo que asignará direcciones
   Router0(config-dhcpv6)# dns-server 2001:8888::         <-- DNS IPv6 (ejemplo)
   Router0(config-dhcpv6)# domain-name Salesianos.com     <-- Dominio (ejemplo)
   ```
2. **Activar el DHCPv6 stateful en la interfaz** que conecta al cliente (por ejemplo, G0/0/0):
   - Primero, indicamos que se use DHCPv6 con estado, para lo cual se debe activar la bandera “managed-config-flag”:
     ```bash
     Router0(config)# interface g0/0/0
     Router0(config-if)# ipv6 nd managed-config-flag
     ```
   - Luego, enlazamos la interfaz con el pool DHCPv6 que acabamos de crear:
     ```bash
     Router0(config-if)# ipv6 dhcp server DHCPv6_STATEFUL
     ```
3. Con esto, el **Router0** está listo para ofrecer direcciones IPv6 de manera **con estado** a los clientes en la red 2001:B:B:B::/64.

4. **En el PC** (p.ej. PC0):
   - En la pestaña **Desktop** → **IP Configuration**,
   - Selecciona en la sección de IPv6 “**DHCP**” (o “**DHCPv6**” según la versión de Packet Tracer),
   - Verifica que el PC reciba una dirección en el rango 2001:B:B:B::/64, la DNS 2001:8888:: y el dominio “Salesianos.com”.

---

## 3. Configurar SLAAC + DHCPv6 **sin estado** (Stateless)

Para la red 2001:A:A:A::/64 (por ejemplo, la interfaz G0/0/2 del Router0) vamos a suponer que quieres usar **SLAAC** para la dirección IPv6 pero **DHCPv6 sin estado** para DNS y dominio.

1. **Crear el pool DHCPv6** para la parte de información adicional (DNS, dominio), sin especificar un prefijo, porque la dirección la dará SLAAC:
   ```bash
   Router0(config)# ipv6 dhcp pool DHCPv6_STATELESS
   Router0(config-dhcpv6)# dns-server 2001:4444::
   Router0(config-dhcpv6)# domain-name Salesianos.es
   ```
2. **Configurar la interfaz G0/0/2** (o la que corresponda a la red 2001:A:A:A::/64):
   - Indicamos que el router envíe la información “other-config-flag” (DHCP sin estado), pero no la “managed-config-flag”:
     ```bash
     Router0(config)# interface g0/0/2
     Router0(config-if)# ipv6 nd other-config-flag
     ```
   - Vinculamos esta interfaz con el pool DHCPv6 creado para la parte de DNS:
     ```bash
     Router0(config-if)# ipv6 dhcp server DHCPv6_STATELESS
     ```
   - Asignamos la dirección IPv6 al router:
     ```bash
     Router0(config-if)# ipv6 address 2001:A:A:A::1/64
     Router0(config-if)# ipv6 address FE80::1 link-local
     ```
3. En la **PC** de esa red (p.ej. PC2):
   - En **Desktop** → **IP Configuration**,
   - Selecciona en IPv6 “**Autoconfiguration (SLAAC)**” o “**DHCPv6**” sin estado (depende de la versión de Packet Tracer; a veces basta con “Auto”),
   - Verifica que la dirección IPv6 se forme por **SLAAC** (con el prefijo 2001:A:A:A::/64 y la EUI-64 en la parte final),
   - Y que el PC obtenga la configuración de **DNS** y **dominio** desde el router (por DHCPv6 sin estado).

---

## 4. Configurar SLAAC puro (sin DHCP)

En la red 2001:C:C:C::/64 (por ejemplo, interfaz G0/0/1 del Router0) supongamos que solo quieres SLAAC (sin DHCP). Entonces:

1. **En la interfaz** G0/0/1 (o la que corresponda):
   ```bash
   Router0(config)# interface g0/0/1
   Router0(config-if)# ipv6 address 2001:C:C:C::1/64
   Router0(config-if)# ipv6 address FE80::1 link-local
   Router0(config-if)# no shutdown
   ```
2. Asegúrate de **no configurar** ni `ipv6 dhcp server` ni las banderas “other-config-flag” o “managed-config-flag”. Por defecto, el router enviará el RA (Router Advertisement) con SLAAC habilitado.

3. En el **PC** de esa red, configúralo en modo **Autoconfiguration** (SLAAC). Debería recibir una dirección `2001:C:C:C::xxxx`.

---

## 5. Verificación de la conectividad

1. Desde cada PC, abre la ventana de **Command Prompt** (en la pestaña Desktop) y ejecuta:
   ```bash
   C:\> ipconfig /all
   ```
   Verifica la dirección IPv6 obtenida, el DNS y el dominio (si aplica).

2. Prueba conectividad con **ping**:
   ```bash
   C:\> ping 2001:A:A:A::1
   C:\> ping 2001:B:B:B::1
   C:\> ping 2001:C:C:C::1
   ```
   Y si hay enrutamiento entre routers, prueba pings entre PCs de distintas redes.

3. Si quieres probar la resolución DNS (cuando se configure un servidor DNS real o simulado), podrías hacer pruebas específicas; sin embargo, en Packet Tracer muchas veces se limita a la verificación de la dirección DNS en la configuración del PC.

---

## 6. Resumen de comandos clave en el router

- **Habilitar IPv6**:  
  ```
  ipv6 unicast-routing
  ```
- **Crear pool DHCPv6**:  
  ```
  ipv6 dhcp pool <NOMBRE_POOL>
   address prefix 2001:XXXX:XXXX:XXXX::/64
   dns-server 2001:XXXX::  (opcional)
   domain-name <DOMINIO>   (opcional)
  ```
- **Asignar pool a una interfaz**:  
  ```
  interface <interfaz>
   ipv6 dhcp server <NOMBRE_POOL>
  ```
- **Flags de DHCPv6**:
  - **Stateless**:  
    ```
    ipv6 nd other-config-flag
    ```
  - **Stateful**:  
    ```
    ipv6 nd managed-config-flag
    ```
- **Asignar direcciones a la interfaz**:  
  ```
  interface <interfaz>
   ipv6 address 2001:XXXX:XXXX:XXXX::1/64
   ipv6 address FE80::1 link-local
  ```

---

## 7. Consejos finales

- Asegúrate de que cada **red** (subred /64) tenga una **interfaz** en el router con dirección global unicast y link-local configurada.
- Habilita el **enrutamiento estático o dinámico** (según el escenario) para que los routers puedan llegar a las otras redes (si hay más de un router).
- En los PCs, revisa que en “**Config**” o “**Desktop → IP Configuration**” esté seleccionado el modo adecuado (SLAAC, DHCPv6, etc.).
- Verifica que las banderas **Managed** u **Other** estén configuradas solo cuando corresponda. No las combines incorrectamente (ej. no pongas las dos a la vez si no es necesario).

Con estos pasos deberías tener un escenario funcional de DHCPv6 **con estado**, **sin estado** y SLAAC puro en Cisco Packet Tracer. ¡Éxito con la práctica!

---
---

# DIFERENCIAS que hay entre DHCP con estado, SLAAC y SLAAC y DHCP sin estado

Para entender la diferencia entre estos tres modos de configuración de direcciones IPv6, conviene repasar brevemente cómo funciona el proceso de asignación de direcciones y la información adicional que necesitan los clientes (DNS, dominio, etc.).

---

## 1. SLAAC (Stateless Address Autoconfiguration)

- **Qué es**: SLAAC es el mecanismo por el cual un host (PC, por ejemplo) puede autoconfigurarse una dirección IPv6 global sin necesidad de un servidor DHCP.  
- **Cómo funciona**:  
  - El router envía mensajes _Router Advertisement_ (RA) periódicamente o como respuesta a un _Router Solicitation_ (RS) del host.  
  - Estos RA incluyen el prefijo IPv6 (por ejemplo, 2001:A:A:A::/64) y la información necesaria para que el host se configure su propia dirección, usando EUI-64 o un generador de direcciones aleatorias.  
  - **No** se requiere un servidor DHCP para la dirección en sí.

- **Ventajas**: Es sencillo y no requiere un servidor DHCPv6 para asignar la dirección.  
- **Limitaciones**: Por defecto, SLAAC no proporciona información adicional como DNS o dominio, a menos que se combine con DHCPv6 sin estado (ver siguiente punto).

---

## 2. SLAAC + DHCPv6 **sin estado** (Stateless DHCPv6)

- **Qué es**: Combina la autoconfiguración de direcciones mediante SLAAC con la posibilidad de obtener parámetros adicionales (DNS, dominio, etc.) a través de un servidor DHCPv6.  
- **Cómo funciona**:  
  - El router sigue enviando los RA con el prefijo para que el host se configure su propia dirección vía SLAAC.  
  - En los RA se activa la “_Other Configuration Flag_” (o `other-config-flag`), que le indica al host que debe contactar un servidor DHCPv6 para obtener **otra** información (DNS, dominio…).  
  - El host no obtiene la dirección global del servidor DHCPv6, sino que la obtiene de SLAAC. El DHCPv6 sin estado **solo** sirve para la configuración adicional.

- **Ventajas**: Combina la facilidad de SLAAC para la dirección con la capacidad de DHCPv6 para proveer DNS, dominio, etc.  
- **Limitaciones**: El servidor DHCPv6 no controla la asignación de direcciones (no “lleva el registro” de qué IP se asigna a cada equipo).

---

## 3. DHCPv6 **con estado** (Stateful DHCPv6)

- **Qué es**: Es un servicio DHCP similar a DHCPv4, pero para IPv6. El servidor DHCPv6 proporciona al cliente la dirección IPv6, el DNS, el dominio y cualquier otra opción.  
- **Cómo funciona**:  
  - El router (o servidor DHCPv6 dedicado) mantiene un **pool** de direcciones y va asignando una a cada host.  
  - El router, en sus RA, activa la “_Managed Configuration Flag_” (o `managed-config-flag`), que le indica al host que debe usar DHCPv6 para obtener **la dirección** y otros datos.  
  - El servidor DHCPv6 hace un “seguimiento” o “control” de qué dirección le fue dada a cada cliente (de ahí “con estado”).

- **Ventajas**:  
  - El administrador de red tiene más control sobre las direcciones que se asignan y puede hacer seguimiento de qué dirección obtiene cada cliente.  
  - Facilita la gestión centralizada (similar a DHCPv4).  
- **Limitaciones**:  
  - Es más complejo que SLAAC, requiere un servidor DHCPv6 y configuración adicional.

---

## Resumen de las diferencias

1. **SLAAC (solo)**: El host se autoconfigura completamente su dirección a partir de los RA. No hay servidor DHCPv6 involucrado para la dirección, y por defecto no hay forma de obtener DNS/dominio si no se combina con algo más.

2. **SLAAC + DHCPv6 sin estado**: El host obtiene su **dirección** vía SLAAC, pero usa un servidor DHCPv6 **sin estado** para obtener información adicional (DNS, dominio, etc.). El servidor DHCPv6 no asigna la dirección al host, solo le da parámetros extra.

3. **DHCPv6 con estado**: El host obtiene **dirección, DNS, dominio** y cualquier otro parámetro directamente de un servidor DHCPv6. El servidor mantiene un “estado” o registro de qué dirección ha asignado a cada host.

Cada uno se adapta a diferentes necesidades de la red y nivel de control deseado por el administrador.