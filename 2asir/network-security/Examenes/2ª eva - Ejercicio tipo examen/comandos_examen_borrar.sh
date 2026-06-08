
# ==========================================================
# CONFIGURACIÓN POR DISPOSITIVO - EXAMEN SEGURIDAD
# (Con referencias a los apartados del enunciado)
# ==========================================================

# ----------------------------------------------------------
# 1. CORE (Switch Multicapa - Núcleo)
# ----------------------------------------------------------
enable
configure terminal

# [Apartado 3: Usuarios locales]
username admin privilege 15 secret cisco123
username supervisor privilege 7 secret cisco456
privilege exec level 7 ping
privilege exec level 7 traceroute
privilege exec level 7 show

# [Apartado 4: AAA]
aaa new-model
aaa authentication login default local
aaa authentication login CONSOLE_AUTH local enable

# [Apartado 4: AAA - Aplicación en Consola]
line con 0
 login authentication CONSOLE_AUTH
exit

# [Apartado 5: SSH]
ip domain-name examen.local
crypto key generate rsa (2048)
ip ssh version 2

# [Apartado 12: ACL de Gestión (VTY)]
ip access-list standard ACL_VTY
 permit 192.168.4.10
exit

# [Apartado 12: Restricción de acceso VTY]
line vty 0 4
 transport input ssh
 access-class ACL_VTY in
exit

# [Apartado 1: VLANs y Direccionamiento]
vlan 20
 name Datos_VLAN20
vlan 50
 name Servidores_VLAN50
vlan 99
 name Nativa_Gestion

interface vlan 20
 ip address 192.168.20.1 255.255.255.0
interface vlan 50
 ip address 192.168.50.1 255.255.255.0
interface vlan 99
 ip address 192.168.99.1 255.255.255.0

# [Apartado 1: Puertos de Interconexión (Enrutados)]
interface g1/0/1
 no switchport
 ip address 192.168.1.2 255.255.255.0

interface g1/0/21
 no switchport
 ip address 192.168.4.2 255.255.255.0

# [Apartado 9: Servidor DHCP]
ip dhcp excluded-address 192.168.20.1 192.168.20.10
ip dhcp excluded-address 192.168.50.1 192.168.50.10

ip dhcp pool VLAN_20
 network 192.168.20.0 255.255.255.0
 default-router 192.168.20.1

ip dhcp pool VLAN_50
 network 192.168.50.0 255.255.255.0
 default-router 192.168.50.1

# [Apartado 2: Etherchannel (LACP)]
interface range f0/1 - 2
 channel-group 1 mode active
interface port-channel 1
 switchport mode trunk
 switchport trunk native vlan 99

# [Apartado 6: Spanning-Tree Root]
spanning-tree vlan 1,20,50,99 root primary

# [Apartado 11: Enrutamiento OSPF]
router ospf 1
 router-id 1.1.1.1
 network 192.168.1.0 0.0.0.255 area 0
 network 192.168.4.0 0.0.0.255 area 0
 network 192.168.20.0 0.0.0.255 area 0
 network 192.168.50.0 0.0.0.255 area 0
 passive-interface default
 no passive-interface g1/0/1

# [Apartado 13: Filtro VLAN 50 (ACL Extended)]
ip access-list extended FILTRO_VLAN50
 permit tcp 192.168.50.0 0.0.0.255 host 192.168.4.10 eq 80
 permit tcp 192.168.50.0 0.0.0.255 host 192.168.4.10 eq 443
 permit udp 192.168.50.0 0.0.0.255 host 192.168.4.10 eq 53
 deny ip 192.168.50.0 0.0.0.255 host 192.168.4.10
 permit ip 192.168.50.0 0.0.0.255 any

# [Apartado 14: Filtro VLAN 20 (Bloqueo Rango)]
ip access-list standard BLOQUEO_VLAN20
 deny 192.168.20.16 0.0.0.15
 permit any

# [Apartado 13 y 14: Aplicación de ACLs en Interfaces]
interface vlan 50
 ip access-group FILTRO_VLAN50 in
interface vlan 20
 ip access-group BLOQUEO_VLAN20 in

# [Apartado 1 y 10: Puertos de Acceso VLAN 20, PortFast y Port-Security en CORE]
interface range g1/0/11 - 15
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation shutdown

# [Apartado 1 y 10: Puertos de Acceso VLAN 50, PortFast y Port-Security en CORE]
interface range g1/0/16 - 20
 switchport mode access
 switchport access vlan 50
 spanning-tree portfast
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation shutdown

# [Apartado 1: Puertos No Usados en CORE]
interface range g1/0/2 - 10, g1/0/22 - 24
 switchport access vlan 99
 shutdown

# [Apartado 7: NTP]
ntp server 192.168.4.10
# [Apartado 8: Syslog]
logging 192.168.4.10
service timestamps log datetime msec
exit

# ----------------------------------------------------------
# 2. SW1 (Switch de Acceso)
# ----------------------------------------------------------
enable
configure terminal

# [Apartado 1: VLANs]
vlan 20,50,99

# [Apartado 1 y 10: Puertos de Acceso VLAN 20, PortFast y Port-Security]
interface range f0/1 - 5
 switchport mode access
 switchport access vlan 20
 spanning-tree portfast
 switchport port-security
 switchport port-security maximum 2
 switchport port-security violation shutdown

# [Apartado 1 y 10: Puertos de Acceso VLAN 50]
interface range f0/6 - 10
 switchport mode access
 switchport access vlan 50
 spanning-tree portfast

# [Apartado 1: Puertos No Usados]
interface range f0/11 - 24
 switchport access vlan 99
 shutdown

# [Apartado 2: Etherchannel LACP]
interface range f0/1 - 2
 channel-group 1 mode active
interface port-channel 1
 switchport mode trunk
 switchport trunk native vlan 99

# [Apartado 1: Gestión SVI]
interface vlan 99
 ip address 192.168.99.2 255.255.255.0
ip default-gateway 192.168.99.1

# [Apartados 3, 4, 5, 7, 8: Gestión igual que CORE]
...

# ----------------------------------------------------------
# 3. R1 (Router de Salida Local)
# ----------------------------------------------------------
enable
configure terminal

# [Apartado 1: Direccionamiento Interfaces]
interface g0/0
 ip address 192.168.1.1 255.255.255.0
 no shutdown

interface s0/0/0
 ip address 10.1.1.2 255.255.255.252
 clock rate 128000
 no shutdown

# [Apartado 11: OSPF]
router ospf 1
 router-id 2.2.2.2
 network 192.168.1.0 0.0.0.255 area 0
 network 10.1.1.0 0.0.0.3 area 0

# [Partes 4 y 5: VPN IPSEC - Fase 1 ISAKMP]
crypto isakmp policy 10
 encryption aes 256
 hash sha
 authentication pre-share
 group 5
 lifetime 86400
crypto isakmp key vpnpa55 address 10.2.2.2

# [Partes 4 y 5: VPN IPSEC - Fase 2 IPsec]
crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac

# [Partes 4 y 5: Tráfico Interesante (ACL 110)]
access-list 110 permit ip 192.168.1.0 0.0.0.255 192.168.3.0 0.0.0.255

# [Partes 4 y 5: Conexión Fase 1 y 2]
crypto map VPN-MAP 10 ipsec-isakmp
 set peer 10.2.2.2
 set transform-set VPN-SET
 match address 110

# [Partes 4 y 5: Aplicación en Interfaz]
interface s0/0/0
 crypto map VPN-MAP

# ----------------------------------------------------------
# 4. R2 (Internet / ISP)
# ----------------------------------------------------------
enable
configure terminal

# [Apartado 1: Direccionamiento]
interface s0/0/0
 ip address 10.1.1.1 255.255.255.252
 no shutdown
interface s0/0/1
 ip address 10.2.2.1 255.255.255.252
 clock rate 128000
 no shutdown
interface g0/0
 ip address 192.168.2.1 255.255.255.0
 no shutdown

# [Apartado 11: OSPF]
router ospf 1
 router-id 3.3.3.3
 network 10.1.1.0 0.0.0.3 area 0
 network 10.2.2.0 0.0.0.3 area 0
 network 192.168.2.0 0.0.0.255 area 0

# ----------------------------------------------------------
# 5. R3 (Router Remoto)
# ----------------------------------------------------------
enable
configure terminal

# [Apartado 1: Direccionamiento]
interface g0/0
 ip address 192.168.3.1 255.255.255.0
 no shutdown
interface s0/0/1
 ip address 10.2.2.2 255.255.255.252
 no shutdown

# [Apartado 11: OSPF]
router ospf 1
 router-id 4.4.4.4
 network 10.2.2.0 0.0.0.3 area 0
 network 192.168.3.0 0.0.0.255 area 0

# [Apartado 15: NAT Overload (PAT)]
access-list 1 permit 192.168.3.0 0.0.0.255
ip nat inside source list 1 interface s0/0/1 overload
interface g0/0
 ip nat inside
interface s0/0/1
 ip nat outside

# [Partes 4 y 5: VPN IPSEC (Símétrico)]
crypto isakmp policy 10
 encryption aes 256
 hash sha
 authentication pre-share
 group 5
 lifetime 86400
crypto isakmp key vpnpa55 address 10.1.1.2

crypto ipsec transform-set VPN-SET esp-aes esp-sha-hmac
access-list 110 permit ip 192.168.3.0 0.0.0.255 192.168.1.0 0.0.0.255

crypto map VPN-MAP 10 ipsec-isakmp
 set peer 10.1.1.2
 set transform-set VPN-SET
 match address 110

interface s0/0/1
 crypto map VPN-MAP
