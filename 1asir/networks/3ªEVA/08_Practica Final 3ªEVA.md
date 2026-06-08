Okay, aquí tienes una guía paso a paso con los comandos necesarios para configurar la topología de Packet Tracer según tus requisitos.

**Notas Previas:**

1.  **Acceso Inicial:** Accede a la CLI (Command Line Interface) de cada dispositivo.
2.  **Modo de Configuración:** La mayoría de los comandos se introducen en el modo de configuración global (`configure terminal` o `conf t`), a menos que se indique lo contrario (modo de interfaz, etc.). Entra con `enable` y, si es necesario, introduce la contraseña de enable (si la has configurado).
3.  **Adaptación de Puertos:** Asegúrate de que los nombres de los puertos (Gig0/0/0, Fa0/1, etc.) coincidan *exactamente* con los de tu topología en Packet Tracer. Los puertos FastEthernet para los PCs se asignarán según el plan de ejemplo; puedes ajustarlos si lo deseas, siempre que cumplas el requisito de al menos 2 puertos por VLAN en cada switch.
4.  **Guardar Configuración:** Después de configurar cada dispositivo, no olvides guardar la configuración con `copy running-config startup-config` o `write memory` desde el modo privilegiado (`#`).

---

**Paso 1: Configuración de VLANs en Todos los Switches (Sw1, Sw2, Sw3)**

En cada uno de los switches (Sw1, Sw2, Sw3), ejecuta los siguientes comandos:

```bash
enable
configure terminal

! Crear VLANs y asignar nombres
vlan 10
 name ATENCION_CLIENTE
vlan 20
 name PLANIFICACION_MERCADO
vlan 30
 name RRHH
vlan 99
 name ADMINISTRATIVA_NATIVA 

exit
```

---

**Paso 2: Configuración de Puertos de Acceso y Asignación de VLANs**

Asignaremos puertos a las VLANs correspondientes en cada switch, asegurando al menos dos por VLAN. También habilitaremos PortFast y BPDU Guard en estos puertos.

**En Sw1:**

```bash
configure terminal

! Puertos para VLAN 10 (Atención Cliente) - PC3 conectado a Fa0/3
interface range Fa0/3 - 4
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security ! Habilitar seguridad
 switchport port-security maximum 3 ! Máximo 3 MAC
 switchport port-security violation shutdown ! Acción por violación
 switchport port-security mac-address sticky ! Opcional: aprender MACs dinámicamente
 shutdown ! Apagar puertos no usados inicialmente
 no shutdown ! Encender SOLO los puertos en uso (Fa0/3)

! Puertos para VLAN 20 (Planificación Mercado) - Sin PC conectado aquí
interface range Fa0/5 - 6
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
 shutdown ! Apagar puertos no usados

! Puertos para VLAN 30 (RRHH) - PC2 conectado a Fa0/1
interface range Fa0/1 - 2
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
 shutdown ! Apagar puertos no usados inicialmente
 no shutdown ! Encender SOLO los puertos en uso (Fa0/1)

exit
```

**En Sw2:**

```bash
configure terminal

! Puertos para VLAN 10 (Atención Cliente) - Sin PC conectado aquí
interface range Fa0/5 - 6
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
 shutdown ! Apagar puertos no usados

! Puertos para VLAN 20 (Planificación Mercado) - PC5 conectado a Fa0/3
interface range Fa0/3 - 4
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
 shutdown ! Apagar puertos no usados inicialmente
 no shutdown ! Encender SOLO los puertos en uso (Fa0/3)

! Puertos para VLAN 30 (RRHH) - PC4 conectado a Fa0/1
interface range Fa0/1 - 2
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
 shutdown ! Apagar puertos no usados inicialmente
 no shutdown ! Encender SOLO los puertos en uso (Fa0/1)

exit
```

**En Sw3:**

```bash
configure terminal

! Puertos para VLAN 10 (Atención Cliente) - PC1 conectado a Fa0/1
interface range Fa0/1 - 2
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
 shutdown ! Apagar puertos no usados inicialmente
 no shutdown ! Encender SOLO los puertos en uso (Fa0/1)

! Puertos para VLAN 20 (Planificación Mercado) - PC0 conectado a Fa0/3
interface range Fa0/3 - 4
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
 shutdown ! Apagar puertos no usados inicialmente
 no shutdown ! Encender SOLO los puertos en uso (Fa0/3)

! Puertos para VLAN 30 (RRHH) - Sin PC conectado aquí
interface range Fa0/5 - 6
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
 shutdown ! Apagar puertos no usados

exit
```

---

**Paso 3: Configuración de EtherChannel y Troncales entre Switches**

Usaremos LACP (protocolo estándar). *Verifica los puertos exactos en tu diagrama. Asumiré los de la imagen 4:*
*   Sw1 <-> Sw3: Gig1/1, Gig3/1
*   Sw2 <-> Sw3: Gig1/1, Gig2/1
*   Sw1 <-> Sw2: Gig1/1, Gig3/1

**En Sw1:**

```bash
configure terminal

! EtherChannel hacia Sw3 (Po1)
interface range Gig1/1, Gig3/1
 channel-group 1 mode active ! LACP activo
 no shutdown

! EtherChannel hacia Sw2 (Po2)
interface range Gig1/1, Gig3/1 ! REVISA SI SON ESTOS LOS PUERTOS CORRECTOS ENTRE SW1 y SW2. Ajusta si es necesario.
 channel-group 2 mode active ! LACP activo
 no shutdown

! Configurar Port-channel 1 como Troncal
interface Port-channel1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,99

! Configurar Port-channel 2 como Troncal
interface Port-channel2
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,99

exit
```

**En Sw2:**

```bash
configure terminal

! EtherChannel hacia Sw3 (Po3)
interface range Gig1/1, Gig2/1
 channel-group 3 mode active ! LACP activo
 no shutdown

! EtherChannel hacia Sw1 (Po2) - Debe coincidir el número de grupo si usas LACP/PAgP, pero aquí usamos LACP 'active' en ambos, así que el número local puede ser diferente. Usaremos Po2 para claridad con Sw1.
interface range Gig1/1, Gig3/1 ! REVISA SI SON ESTOS LOS PUERTOS CORRECTOS ENTRE SW1 y SW2. Ajusta si es necesario.
 channel-group 2 mode active ! LACP activo
 no shutdown

! Configurar Port-channel 3 como Troncal
interface Port-channel3
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,99

! Configurar Port-channel 2 como Troncal
interface Port-channel2
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,99

exit
```

**En Sw3:**

```bash
configure terminal

! EtherChannel hacia Sw1 (Po1)
interface range Gig1/1, Gig3/1
 channel-group 1 mode active ! LACP activo
 no shutdown

! EtherChannel hacia Sw2 (Po3)
interface range Gig1/1, Gig2/1
 channel-group 3 mode active ! LACP activo
 no shutdown

! Configurar Port-channel 1 como Troncal
interface Port-channel1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,99

! Configurar Port-channel 3 como Troncal
interface Port-channel3
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,99

! Configurar Enlace Troncal hacia R1 (Gig0/1)
interface Gig0/1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,99
 no shutdown

exit
```

---

**Paso 4: Configuración de STP - Sw3 como Root Bridge**

**En Sw3:**

```bash
configure terminal

! Establecer Sw3 como root bridge para todas las VLANs (menor prioridad)
spanning-tree vlan 10,20,30,99 priority 4096

exit
```

---

**Paso 5: Configuración del Router R1**

**En R1:**

```bash
enable
configure terminal

! Configurar interfaz hacia Sw3 (Router-on-a-Stick)
interface GigabitEthernet0/0/0
 no shutdown

! Subinterfaz para VLAN 10 (Atención Cliente)
interface GigabitEthernet0/0/0.10
 encapsulation dot1Q 10
 ip address 172.20.1.1 255.255.255.0

! Subinterfaz para VLAN 20 (Planificación Mercado)
interface GigabitEthernet0/0/0.20
 encapsulation dot1Q 20
 ip address 172.20.2.1 255.255.255.0

! Subinterfaz para VLAN 30 (RRHH)
interface GigabitEthernet0/0/0.30
 encapsulation dot1Q 30
 ip address 172.20.3.1 255.255.255.0

! Subinterfaz para VLAN 99 (Nativa/Administrativa)
interface GigabitEthernet0/0/0.99
 encapsulation dot1Q 99 native
 ip address 172.20.0.1 255.255.255.0

! Configurar interfaces hacia Internet
interface GigabitEthernet0/1/0
 description Enlace_Principal_Internet
 ip address 210.1.1.10 255.255.255.252 ! Asumiendo IP .10 en la red .8/30
 no shutdown

interface GigabitEthernet0/1/1
 description Enlace_Backup_Internet
 ip address 210.1.1.14 255.255.255.252 ! Asumiendo IP .14 en la red .12/30
 no shutdown

! Configurar rutas estáticas: Predeterminada y Flotante
! Asumiendo que el siguiente salto para la red principal (.8/30) es .9
! Asumiendo que el siguiente salto para la red backup (.12/30) es .13
ip route 0.0.0.0 0.0.0.0 210.1.1.9 ! Ruta Predeterminada (AD = 1)
ip route 0.0.0.0 0.0.0.0 210.1.1.13 10 ! Ruta Flotante (AD = 10)

! Configurar Servidores DHCP (excluyendo las primeras 5 IP utilizables)
ip dhcp excluded-address 172.20.1.1 172.20.1.5
ip dhcp excluded-address 172.20.2.1 172.20.2.5
ip dhcp excluded-address 172.20.3.1 172.20.3.5
! No excluimos en la .0.0/24 porque no habrá DHCP para la VLAN 99

! Pool DHCP para VLAN 10
ip dhcp pool VLAN10_CLIENTES
 network 172.20.1.0 255.255.255.0
 default-router 172.20.1.1
 dns-server 8.8.8.8 ! Ejemplo de DNS

! Pool DHCP para VLAN 20
ip dhcp pool VLAN20_MERCADO
 network 172.20.2.0 255.255.255.0
 default-router 172.20.2.1
 dns-server 8.8.8.8

! Pool DHCP para VLAN 30
ip dhcp pool VLAN30_RRHH
 network 172.20.3.0 255.255.255.0
 default-router 172.20.3.1
 dns-server 8.8.8.8

exit
```

---

**Paso 6: Configuración de Acceso SSH en Switches (Sw1, Sw2, Sw3)**

Repite estos pasos en **cada uno** de los tres switches (Sw1, Sw2, Sw3), cambiando el `hostname` y la dirección IP de la `interface Vlan99` en cada uno.

```bash
configure terminal

! 1. Establecer Hostname (Ejemplo para Sw1)
hostname Sw1 ! Cambia a Sw2 y Sw3 en los otros switches

! 2. Establecer Nombre de Dominio IP
ip domain-name miempresa.local ! Puedes usar el que quieras

! 3. Generar Claves RSA para SSH (elige un tamaño, ej. 1024)
crypto key generate rsa
  1024

! 4. Crear Usuario Local para SSH
username admin secret TuPasswordSeguro ! Cambia TuPasswordSeguro

! 5. Configurar Líneas VTY para usar SSH y login local
line vty 0 15
 transport input ssh
 login local

! 6. Establecer Contraseña de Enable
enable secret OtraPasswordSegura ! Cambia OtraPasswordSegura

! 7. Configurar Interfaz de Gestión (SVI) para VLAN 99
interface Vlan99
 description Interfaz_Gestion_Switch
 ip address 172.20.0.11 255.255.255.0 ! Usa .12 para Sw2, .13 para Sw3
 no shutdown

! 8. Establecer Gateway Predeterminado para el Switch
ip default-gateway 172.20.0.1 ! La IP de R1 en la VLAN 99

exit
```

---

**Paso 7: Configuración de Seguridad (DHCP Snooping, ARP Inspection) en Switches**

Repite estos pasos en **cada uno** de los tres switches (Sw1, Sw2, Sw3).

```bash
configure terminal

! === DHCP Snooping ===
! Habilitar globalmente
ip dhcp snooping

! Habilitar en las VLANs de usuarios
ip dhcp snooping vlan 10,20,30

! Confiar en los puertos troncales (EtherChannels y enlace a R1)
! En Sw1:
interface Port-channel1
 ip dhcp snooping trust
interface Port-channel2
 ip dhcp snooping trust

! En Sw2:
interface Port-channel2
 ip dhcp snooping trust
interface Port-channel3
 ip dhcp snooping trust

! En Sw3:
interface Port-channel1
 ip dhcp snooping trust
interface Port-channel3
 ip dhcp snooping trust
interface GigabitEthernet0/1 ! Puerto hacia R1
 ip dhcp snooping trust

! (Los puertos de acceso son 'untrusted' por defecto, que es lo correcto)

! === Dynamic ARP Inspection (DAI) ===
! Habilitar DAI en las VLANs de usuarios
ip arp inspection vlan 10,20,30

! Confiar en los puertos troncales (generalmente los mismos que DHCP Snooping trust)
! En Sw1:
interface Port-channel1
 ip arp inspection trust
interface Port-channel2
 ip arp inspection trust

! En Sw2:
interface Port-channel2
 ip arp inspection trust
interface Port-channel3
 ip arp inspection trust

! En Sw3:
interface Port-channel1
 ip arp inspection trust
interface Port-channel3
 ip arp inspection trust
interface GigabitEthernet0/1 ! Puerto hacia R1
 ip arp inspection trust

! (Los puertos de acceso son 'untrusted' por defecto, que es lo correcto)

exit
```

---

**Paso 8: Configuración de los PCs**

*   Ve a la configuración IP de cada PC (PC0 a PC5).
*   Selecciona la opción "DHCP".
*   Deberían obtener automáticamente una dirección IP, máscara de subred, puerta de enlace y servidor DNS del pool DHCP correspondiente configurado en R1.

---

**Paso 9: Verificación (Comandos útiles)**

*   **En Switches:**
    *   `show vlan brief`: Verifica la creación de VLANs y asignación de puertos.
    *   `show interfaces trunk`: Verifica los enlaces troncales y VLAN nativa/permitidas.
    *   `show etherchannel summary`: Verifica el estado de los EtherChannels.
    *   `show spanning-tree vlan <vlan_id>`: Verifica el estado de STP (root bridge, etc.).
    *   `show ip ssh`: Verifica la configuración de SSH.
    *   `show ip dhcp snooping`: Verifica la configuración de DHCP Snooping.
    *   `show ip arp inspection`: Verifica la configuración de DAI.
    *   `show port-security interface <interface_id>`: Verifica la seguridad de puerto.
    *   `show ip interface brief`: Muestra el estado de las interfaces IP (como Vlan99).
*   **En R1:**
    *   `show ip interface brief`: Verifica el estado y las IPs de las interfaces y subinterfaces.
    *   `show ip route`: Verifica la tabla de enrutamiento (rutas conectadas, estáticas).
    *   `show ip dhcp binding`: Muestra las asignaciones de IP hechas por DHCP.
    *   `show ip dhcp pool`: Muestra la configuración de los pools DHCP.
*   **En PCs:**
    *   Usa `ping <gateway_ip>` para probar la conectividad con el router.
    *   Usa `ping <ip_otro_pc_en_otra_vlan>` para probar el enrutamiento inter-VLAN.
    *   Usa `ping 8.8.8.8` (o la IP del 'Internet Cloud' si la conoces) para probar la conectividad a Internet (si el cloud está configurado).

---

¡Listo! Con estos pasos deberías tener la red configurada según los requisitos. Recuerda guardar la configuración en cada dispositivo.