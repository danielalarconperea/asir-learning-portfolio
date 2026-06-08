## 1. Roles Centrarles y Gestión
- **CORE (L3 Switch):** Centraliza el DHCP, el enrutamiento inter-VLAN y las políticas de firewall (ACLs). Es el cerebro de la red local.
- **R1 y R3:** Actúan como los extremos de la VPN. R1 protege el tráfico que sale hacia la red remota, y R3 hace lo propio desde el otro lado, además de gestionar la NAT para su red local.
- **Servidor (192.168.4.10):** Nodo crítico que provee NTP, Syslog y es la única IP autorizada para gestionar los dispositivos por SSH/VTY.

## 2. Gestión de Accesos y Privilegios
- **AAA:** Implementado en todos los dispositivos para centralizar la autenticación. Se configura `CONSOLE_AUTH` separadamente para garantizar acceso de recuperación.
- **VTY y Autenticación:** Al usar `aaa authentication login default local enable`, todas las líneas (incluidas las VTY) usan esta lista por defecto. Por eso **no es necesario** poner `login local` en las líneas VTY; la configuración de AAA ya se aplica automáticamente a todos los accesos.
- **VTY:** La restricción mediante `access-class` es vital para que solo el administrador desde el servidor pueda configurar los equipos remotamente.

## 2. Seguridad en Capa 2 (Switching)
- **Port Security y PortFast:** Se ha habilitado tanto en el **SW1** como en el **CORE**. 
    - En el **CORE**, se aplica a los puertos donde se conectan PC-A1 y PC-A2.
    - Se limita cada puerto de acceso a un máximo de **2 direcciones MAC** con violación tipo `shutdown`.
- **VLANs:** Se utilizan VLANs separadas para datos (20, 50) y gestión/nativa (99) en ambos switches.

## 3. Filtrado de Tráfico (Firewalling con ACLs)
- **Orden de las Reglas:** En Cisco, las ACLs se procesan secuencialmente. 
    - Para la **VLAN 50**, primero se permiten los servicios específicos (HTTP, HTTPS, DNS) hacia el servidor y luego se bloquea cualquier otro tráfico hacia dicho servidor (`deny ip ... host 192.168.4.10`). Al final hay un `permit any` para que no se bloquee el tráfico a internet u otras redes no restringidas.
- **Bloqueo por Rango:** La denegación del rango `.16 al .31` en la VLAN 20 se realiza mediante una máscara wildcard (`0.0.0.15`), que bloquea exactamente 16 direcciones IPs consecutivas.

- **Enrutamiento OSPF:** 
    - Se configuran Router IDs manuales para mayor control.
    - **Evitar DR/BDR:** En el enlace Ethernet entre el CORE y R1, se configura `ip ospf network point-to-point` para evitar la elección de DR/BDR, acelerando la convergencia y cumpliendo con el apartado 11 del enunciado.
    - **Seguridad:** El uso de `passive-interface default` asegura que no se envíen Hellos hacia las redes de usuarios (VLAN 20, 50, 99).
- **Túnel Site-to-Site:** La VPN protege el tráfico entre la red local (VLAN 20) y la red remota.
- **Fase 1 (ISAKMP):** Utiliza AES-256 para cifrado y SHA para hash, garantizando una negociación segura de las claves.
- **Fase 2 (IPsec):** El `transform-set` define cómo se encapsulará el tráfico real.
- **Tráfico Interesante:** La `access-list 110` define exactamente qué paquetes deben ser cifrados (tráfico entre VLAN 20 y la red 192.168.3.0/24).

## 5. Auditoría y Servicios de Red
- **Sincronización (NTP):** Crucial para que los logs tengan marcas de tiempo correctas y coherentes entre todos los dispositivos.
- **Syslog:** Se envía toda la información de eventos al servidor centralizado (`192.168.4.10`) para su análisis y almacenamiento fuera del dispositivo.
- **DHCP:** El CORE actúa como servidor de red, pero excluye las primeras 10 IPs de cada pool para asignación estática (puertas de enlace, servidores, etc.).

## 6. Notas Técnicas Adicionales
- **Elección de IP de Servidor (.10 vs .2):** Técnicamente, la IP `192.168.4.2` está libre y funcionaría. Sin embargo, se ha elegido la `.10` por coherencia con el diseño del examen (que excluye las primeras 10 IPs) y porque está rotulada así en el diagrama de topología.
- **Sintaxis de Logging:** El comando `logging 192.168.4.10` y `logging host 192.168.4.10` son equivalentes. El router suele aceptar ambos y guardarlos como `logging host` por ser la sintaxis más moderna.
