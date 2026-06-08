¡Claro! Aquí tienes la configuración paso a paso para tu nueva topología, siguiendo una estructura similar a tu ejemplo anterior pero con los datos y requisitos específicos de tu diagrama y lista, incluyendo las configuraciones de seguridad adicionales.

**¡IMPORTANTE! Revisión de Puertos EtherChannel:** La imagen 4 tiene etiquetas de puerto que crean conflictos (el mismo puerto parece usarse para dos EtherChannels diferentes en Sw1 y Sw2). En la configuración de EtherChannel a continuación, usaré los puertos *tal como están etiquetados* en la imagen 4 entre los switches, **pero debes asegurarte de que en Packet Tracer conectas cables a puertos FÍSICAMENTE DISTINTOS** para cada enlace del EtherChannel. Por ejemplo, si Sw1 usa Gig1/1 y Gig3/1 para ir a Sw3, *no puede* usar esos mismos puertos para ir a Sw2. Tendrás que elegir otros puertos disponibles (ej. Gig2/1, Gig4/1) para el EtherChannel entre Sw1 y Sw2 y ajustar los comandos `interface range` correspondientes.

---

**Paso 1: Configuración Básica Inicial (Todos los Switches: Sw1, Sw2, Sw3)**

```bash
enable
configure terminal

! Cambiar el nombre del dispositivo (ejecutar en cada switch cambiando el nombre)
hostname Sw1 ! (O Sw2, Sw3)

! Configurar contraseñas básicas (SSH configurará mejores más adelante)
enable secret cisco ! Cambia 'cisco' por una contraseña segura
line console 0
 password cisco ! Cambia 'cisco' por una contraseña segura
 login
exit

! Configurar un mensaje de banner
banner motd # Acceso restringido. Solo personal autorizado. #

! Guardar configuración inicial (opcional en este punto)
! write memory
```

---

**Paso 2: Creación de VLANs (Todos los Switches: Sw1, Sw2, Sw3)**

```bash
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

**Paso 3: Configuración SVI y Gateway Predeterminado (Todos los Switches: Sw1, Sw2, Sw3)**

*   Usaremos IPs .11, .12, .13 para las interfaces de gestión de los switches en la VLAN 99. R1 usará la .1.

```bash
configure terminal

! Configurar Interfaz Virtual de Switch (SVI) para Gestión (VLAN 99)
interface Vlan99
 description Gestion y Nativa
 ! Asigna una IP única a cada switch:
 ! En Sw1:
 ip address 172.20.0.11 255.255.255.0
 ! En Sw2:
 ! ip address 172.20.0.12 255.255.255.0
 ! En Sw3:
 ! ip address 172.20.0.13 255.255.255.0
 no shutdown
exit

! Configurar Gateway Predeterminado para el tráfico originado por el switch
! La IP es la del Router R1 en la VLAN 99
ip default-gateway 172.20.0.1

exit
```

---

**Paso 4: Asignación de Puertos de Acceso y Seguridad Inicial (Sw1, Sw2, Sw3)**

*   Asignaremos los puertos FastEthernet a las VLANs según los PCs conectados.
*   Habilitaremos PortFast, BPDU Guard y Port Security en los puertos de acceso.

**En Sw1:**

```bash
configure terminal

! PC3 (VLAN 10) en Fa0/3. Asignamos Fa0/3-4 a VLAN 10.
interface range Fa0/3 - 4
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security mac-address sticky ! Opcional
 shutdown ! Apagar puertos no usados en el rango
 no shutdown ! Encender SOLO Fa0/3 (donde está PC3)

! Puertos para VLAN 20 (Naranja) - Sin PC. Asignamos Fa0/5-6.
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

! PC2 (VLAN 30 - Verde) en Fa0/1. Asignamos Fa0/1-2 a VLAN 30.
interface range Fa0/1 - 2
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
 shutdown ! Apagar puertos no usados en el rango
 no shutdown ! Encender SOLO Fa0/1 (donde está PC2)

exit
```

**En Sw2:**

```bash
configure terminal

! Puertos para VLAN 10 (Azul) - Sin PC. Asignamos Fa0/5-6.
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

! PC5 (VLAN 20 - Naranja) en Fa0/3. Asignamos Fa0/3-4 a VLAN 20.
interface range Fa0/3 - 4
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
 shutdown ! Apagar puertos no usados en el rango
 no shutdown ! Encender SOLO Fa0/3 (donde está PC5)

! PC4 (VLAN 30 - Verde) en Fa0/1. Asignamos Fa0/1-2 a VLAN 30.
interface range Fa0/1 - 2
 switchport mode access
 switchport access vlan 30
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
 shutdown ! Apagar puertos no usados en el rango
 no shutdown ! Encender SOLO Fa0/1 (donde está PC4)

exit
```

**En Sw3:**

```bash
configure terminal

! PC1 (VLAN 10 - Azul) en Fa0/1. Asignamos Fa0/1-2 a VLAN 10.
interface range Fa0/1 - 2
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
 shutdown ! Apagar puertos no usados en el rango
 no shutdown ! Encender SOLO Fa0/1 (donde está PC1)

! PC0 (VLAN 20 - Naranja) en Fa0/3. Asignamos Fa0/3-4 a VLAN 20.
interface range Fa0/3 - 4
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 spanning-tree bpduguard enable
 switchport port-security
 switchport port-security maximum 3
 switchport port-security violation shutdown
 switchport port-security mac-address sticky
 shutdown ! Apagar puertos no usados en el rango
 no shutdown ! Encender SOLO Fa0/3 (donde está PC0)

! Puertos para VLAN 30 (Verde) - Sin PC. Asignamos Fa0/5-6.
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

**Paso 5: Configuración de EtherChannel y Troncales (Sw1, Sw2, Sw3)**

*   **¡¡ADVERTENCIA!!** Revisa y ajusta los puertos físicos (`GigX/Y`) en los comandos `interface range` a continuación para que coincidan con los cables *realmente conectados* en tu topología Packet Tracer, asegurando que no haya conflictos de puertos. Los puertos usados aquí se basan en las *etiquetas* de la Imagen 4, que pueden ser conflictivas.

**En Sw1:**

```bash
configure terminal

! EtherChannel hacia Sw3 (Po1) - Usando puertos etiquetados Gig1/1, Gig3/1
interface range Gig1/1, Gig3/1
 shutdown ! Buena practica apagar antes de configurar channel-group
 channel-protocol lacp
 channel-group 1 mode active
 no shutdown

! EtherChannel hacia Sw2 (Po2) - Usando puertos etiquetados Gig1/1, Gig3/1
! *** ¡¡CONFLICTO!! Estos puertos ya se usan para Po1. Debes elegir puertos DIFERENTES en Sw1 para este enlace (ej. Gig2/1, Gig4/1) y ajustar el comando range. ***
interface range Gig1/1, Gig3/1 ! <-- AJUSTA ESTOS PUERTOS
 shutdown
 channel-protocol lacp
 channel-group 2 mode active
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

! EtherChannel hacia Sw3 (Po3) - Usando puertos etiquetados Gig1/1, Gig2/1
interface range Gig1/1, Gig2/1
 shutdown
 channel-protocol lacp
 channel-group 3 mode active
 no shutdown

! EtherChannel hacia Sw1 (Po2) - Usando puertos etiquetados Gig1/1, Gig3/1
! *** ¡¡CONFLICTO!! Gig1/1 ya se usa para Po3. Debes elegir puertos DIFERENTES en Sw2 para este enlace (ej. Gig3/1, Gig4/1 que coincidan con los elegidos en Sw1) y ajustar el comando range. ***
interface range Gig1/1, Gig3/1 ! <-- AJUSTA ESTOS PUERTOS
 shutdown
 channel-protocol lacp
 channel-group 2 mode active
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

! EtherChannel hacia Sw1 (Po1) - Usando puertos etiquetados Gig1/1, Gig3/1
interface range Gig1/1, Gig3/1
 shutdown
 channel-protocol lacp
 channel-group 1 mode active
 no shutdown

! EtherChannel hacia Sw2 (Po3) - Usando puertos etiquetados Gig1/1, Gig2/1
! *** ¡¡CONFLICTO!! Gig1/1 ya se usa para Po1. Debes elegir puertos DIFERENTES en Sw3 para este enlace (ej. Gig2/1, Gig4/1 que coincidan con los elegidos en Sw2) y ajustar el comando range. ***
interface range Gig1/1, Gig2/1 ! <-- AJUSTA ESTOS PUERTOS
 shutdown
 channel-protocol lacp
 channel-group 3 mode active
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

! Configurar Enlace Troncal hacia R1 (Puerto Gig0/1)
interface Gig0/1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,30,99
 no shutdown

exit
```

---

**Paso 6: Configuración de Spanning Tree (STP)**

**En Sw3 (Convertirlo en Root Bridge):**

```bash
configure terminal

! Establecer Sw3 como root bridge para todas las VLANs (menor prioridad)
spanning-tree vlan 10,20,30,99 priority 4096

exit
```

*Nota: PortFast ya fue habilitado en los puertos de acceso en el Paso 4.*

---

**Paso 7: Configuración del Router R1**

```bash
enable
configure terminal

! Habilitar interfaz hacia Sw3 y configurar subinterfaces (Router-on-a-Stick)
interface GigabitEthernet0/0/0
 description Enlace_Troncal_a_Sw3
 no shutdown

interface GigabitEthernet0/0/0.10
 encapsulation dot1Q 10
 description Gateway_VLAN10_Clientes
 ip address 172.20.1.1 255.255.255.0

interface GigabitEthernet0/0/0.20
 encapsulation dot1Q 20
 description Gateway_VLAN20_Mercado
 ip address 172.20.2.1 255.255.255.0

interface GigabitEthernet0/0/0.30
 encapsulation dot1Q 30
 description Gateway_VLAN30_RRHH
 ip address 172.20.3.1 255.255.255.0

interface GigabitEthernet0/0/0.99
 encapsulation dot1Q 99 native
 description Gateway_VLAN99_Admin_Nativa
 ip address 172.20.0.1 255.255.255.0

! Configurar interfaces hacia Internet
interface GigabitEthernet0/1/0
 description Enlace_Principal_Internet_(210.1.1.8/30)
 ip address 210.1.1.10 255.255.255.252
 no shutdown

interface GigabitEthernet0/1/1
 description Enlace_Backup_Internet_(210.1.1.12/30)
 ip address 210.1.1.14 255.255.255.252
 no shutdown

! Configurar rutas estáticas: Predeterminada y Flotante
! Asume que el siguiente salto es .9 para la principal y .13 para la backup
ip route 0.0.0.0 0.0.0.0 210.1.1.9 name Ruta_Predeterminada_Principal
ip route 0.0.0.0 0.0.0.0 210.1.1.13 10 name Ruta_Predeterminada_Flotante

! Configurar Servidor DHCP
! Excluir las primeras 5 IP utilizables de cada pool (.1 a .5) y la IP del router
ip dhcp excluded-address 172.20.1.1 172.20.1.5
ip dhcp excluded-address 172.20.2.1 172.20.2.5
ip dhcp excluded-address 172.20.3.1 172.20.3.5
! No se necesita DHCP para VLAN 99 (IPs fijas)

! Pool DHCP para VLAN 10
ip dhcp pool VLAN10_CLIENTES
 network 172.20.1.0 255.255.255.0
 default-router 172.20.1.1
 dns-server 8.8.8.8 ! Puedes usar otro DNS si prefieres

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

**Paso 8: Configuración de Acceso SSH Seguro (Todos los Switches: Sw1, Sw2, Sw3)**

*   Ejecuta estos comandos en **cada switch**.

```bash
configure terminal

! 1. Establecer Nombre de Dominio IP (Necesario para generar claves RSA)
ip domain-name tuempresa.local ! Usa un nombre de dominio

! 2. Generar Claves RSA para SSH (Usa 1024 bits o más)
crypto key generate rsa modulus 1024

! 3. Crear Usuario Local para SSH
username admin privilege 15 secret TuPasswordSSHSuperSeguro ! Cambia el password

! 4. Configurar Líneas VTY para usar SSH y login local
line vty 0 15
 transport input ssh
 login local
 exit

! 5. (Opcional pero recomendado) Deshabilitar Telnet si solo quieres SSH
! no transport input telnet

! 6. Asegurar la contraseña de enable (si no usaste una fuerte antes)
enable secret TuPasswordEnableSuperSeguro ! Cambia el password

! 7. Habilitar SSH versión 2 (más segura)
ip ssh version 2

exit
```

---

**Paso 9: Configuración de Seguridad Adicional (DHCP Snooping, ARP Inspection)**

*   Ejecuta estos comandos en **cada switch** (Sw1, Sw2, Sw3).

```bash
configure terminal

! === DHCP Snooping ===
! Habilitar globalmente
ip dhcp snooping

! Habilitar en las VLANs de usuarios (donde hay clientes DHCP)
ip dhcp snooping vlan 10,20,30

! Confiar en los puertos troncales (EtherChannels y enlace a R1)
! Revisa los números de Port-channel correctos para CADA switch
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
interface GigabitEthernet0/1 ! Puerto hacia R1 (donde está el servidor DHCP)
 ip dhcp snooping trust

! (Los puertos de acceso son 'untrusted' por defecto, lo cual es correcto)

! === Dynamic ARP Inspection (DAI) ===
! Habilitar DAI en las VLANs de usuarios
ip arp inspection vlan 10,20,30

! Confiar en los puertos troncales (generalmente los mismos que DHCP Snooping trust)
! Revisa los números de Port-channel correctos para CADA switch
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

! (Los puertos de acceso son 'untrusted' por defecto, lo cual es correcto)

exit
```

---

**Paso 10: Configuración de los PCs (PC0 a PC5)**

1.  Abre la configuración IP de cada PC.
2.  Selecciona la opción **DHCP**.
3.  Espera a que obtenga una dirección IP de su VLAN correspondiente desde el router R1.

---

**Paso 11: Guardar Configuración Final y Verificación**

*   **En TODOS los dispositivos (R1, Sw1, Sw2, Sw3):**
    ```bash
    enable
    copy running-config startup-config
    ! o simplemente
    write memory
    ```

*   **Comandos de Verificación Útiles:**
    *   Switches: `show vlan brief`, `show interfaces trunk`, `show etherchannel summary`, `show spanning-tree summary`, `show spanning-tree vlan <id>`, `show ip ssh`, `show ip dhcp snooping`, `show ip arp inspection`, `show port-security interface <id>`, `show ip interface brief`, `ping <ip_router_vlan99>`, `ssh -l admin <ip_otro_switch_vlan99>`
    *   Router R1: `show ip interface brief`, `show ip route`, `show ip dhcp binding`, `show ip dhcp pool`
    *   PCs: `ipconfig /all` (en Command Prompt), `ping <gateway>`, `ping <ip_otro_pc_misma_vlan>`, `ping <ip_otro_pc_otra_vlan>`, `ping 8.8.8.8` (o IP de Internet)

---

¡Listo! Con estos pasos deberías tener la red configurada y asegurada según tus requisitos. Recuerda ajustar los puertos de EtherChannel si es necesario.