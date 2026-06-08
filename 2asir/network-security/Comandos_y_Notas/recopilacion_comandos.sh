#!/bin/bash
# Recopilación de Comandos de Redes y Seguridad (Cisco IOS)
# Generado a partir de apuntes de 1ASIR y 2ASIR (Revisión Profunda)

# ==========================================
# 1. CONFIGURACIÓN BÁSICA (Routers & Switches)
# ==========================================
enable
configure terminal
hostname SW1
enable secret cisco
no ip domain-lookup
service password-encryption
banner motd "Prohibido el acceso no autorizado"

# Configuración de Reloj y NTP (Nuevo)
clock set [HH:MM:SS] [DIA] [MES] [AÑO]
ntp server 192.168.4.2
service timestamps log datetime msec
logging host 192.168.4.2

# Creación de Usuarios y Privilegios (Nuevo)
username admin secret cisco
username supervisor privilege 7 secret cisco
privilege exec level 7 ping
privilege exec level 7 traceroute
privilege exec level 7 show

# Configuración de Consola
line console 0
 password cisco
 login
 logging synchronous
 exec-timeout 10 0
 exit

# Configuración de VTY (Telnet/SSH) con ACL (Nuevo)
access-list 1 permit 192.168.4.2
access-list 1 deny any
line vty 0 15
 password cisco
 login
 transport input ssh
 exec-timeout 5 0
 access-class 1 in
 exit



# AAA (Nuevo)
aaa new-model
aaa authentication login default local
aaa authentication login CONSOLE_AUTH local enable
line console 0
 login authentication CONSOLE_AUTH # local

# Guardar configuración
copy running-config startup-config
write memory

# ==========================================
# 2. INTERFACES Y ENLACES
# ==========================================
interface GigabitEthernet0/0/1
 description Enlace a Router ISP
 ip address 192.168.1.1 255.255.255.0
 no shutdown
 exit

# Subinterfaces (Router-on-a-Stick)
interface GigabitEthernet0/0/1.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 exit

# interfaces L3 en Switch (SVI)
interface vlan 10
 ip address 172.16.10.1 255.255.255.0
 no shutdown
 exit

# Habilitar enrutamiento en Switch L3
ip routing

# ==========================================
# 3. VLANS Y TRUNKING (Switching)
# ==========================================
# Crear VLANs
vlan 10
 name VENTAS
vlan 99
 name NATIVE
 exit

# Configurar puertos de acceso
interface GigabitEthernet0/1
 switchport mode access
 switchport access vlan 10
 exit

# Configurar puertos Trunk
interface GigabitEthernet0/24
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,99
 switchport nonegotiate
 exit

# Mitigación Salto de VLAN (Nuevo)
# Usar VLAN nativa distinta a la 1 y apagar negociación DTP
switchport nonegotiate
switchport trunk native vlan 999

# VTP (VLAN Trunking Protocol)
vtp mode server
vtp domain miempresa.local
vtp password cisco
vtp version 2

# EtherChannel (LACP)
interface range GigabitEthernet0/1-2
 channel-group 1 mode active
 exit
interface port-channel 1
 switchport mode trunk
 switchport trunk native vlan 99
 exit

# Spanning Tree (Nuevo)
spanning-tree mode pvst
spanning-tree vlan 1,10,20 root primary
spanning-tree portfast default
spanning-tree bpduguard enable

# ==========================================
# 4. ENRUTAMIENTO (Routing)
# ==========================================
# Ruta Estática IPv4
ip route 192.168.20.0 255.255.255.0 10.10.10.2
ip route 192.168.30.0 255.255.255.0 Serial0/0/0
# Ruta Flotante (Respaldo) (Nuevo)
ip route 0.0.0.0 0.0.0.0 10.10.10.2 10

# OSPF (Open Shortest Path First)
router ospf 1
 router-id 1.1.1.1
 network 192.168.10.0 0.0.0.255 area 0
 network 10.1.1.0 0.0.0.3 area 0
 passive-interface GigabitEthernet0/0
 default-information originate
 auto-cost reference-bandwidth 1000
 ip ospf network point-to-point
 exit
# Limpiar proceso OSPF (Nuevo)
clear ip ospf process

# RIPv2
router rip
 version 2
 no auto-summary
 network 192.168.1.0
 passive-interface GigabitEthernet0/1
 default-information originate
 exit

# ==========================================
# 5. SEGURIDAD (ACLs, Port Security, SSH)
# ==========================================
# ACL Estándar (1-99)
access-list 10 permit 192.168.10.0 0.0.0.255
access-list 10 permit any

# ACL Extendida (100-199 o Nombre) - Ejemplos Específicos (Nuevo)
ip access-list extended BLOQUEO_WEB
 permit tcp 192.168.10.0 0.0.0.255 any eq 80
 permit tcp 192.168.10.0 0.0.0.255 any eq 443
 deny tcp any any eq 20
 deny tcp any any eq 21
 deny udp any any eq 69
 permit icmp any any echo-reply
 deny ip any any log
 exit

# Aplicar ACL a interfaz
interface GigabitEthernet0/0
 ip access-group BLOQUEO_WEB in
 exit

# SSH Config
ip domain-name miempresa.local
crypto key generate rsa modulus 1024
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3
username admin privilege 15 secret cisco
line vty 0 4
 transport input ssh
 login local
 exit

# Port Security (Switch)
interface GigabitEthernet0/1
 switchport port-security
 switchport port-security maximum 2
 switchport port-security mac-address sticky
 switchport port-security violation restrict
 # Aging (Nuevo)
 switchport port-security aging time 10
 switchport port-security aging type inactivity
 exit

# DHCP Snooping & ARP Inspection
ip dhcp snooping
ip dhcp snooping vlan 10,20
ip arp inspection vlan 10,20
# Limite de tasa (Nuevo)
interface range f0/1-24
 ip dhcp snooping limit rate 5
 exit
# Puertos de confianza
interface GigabitEthernet0/24
 ip dhcp snooping trust
 ip arp inspection trust
 exit

# ==========================================
# 6. SERVICIOS DE RED (DHCP & NAT)
# ==========================================
# Servidor DHCP
ip dhcp excluded-address 192.168.10.1 192.168.10.10
ip dhcp pool LAN_VENTAS
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 8.8.8.8
 domain-name miempresa.local
 exit

# DHCP Relay (en la interfaz SVI o Router)
interface vlan 10
 ip helper-address 192.168.100.1
 exit

# NAT (Network Address Translation)
# 1. Definir interfaces inside/outside
interface GigabitEthernet0/0
 ip nat inside
interface Serial0/0/0
 ip nat outside

# 2. Crear ACL para tráfico a traducir
access-list 1 permit 192.168.1.0 0.0.0.255

# 3. Habilitar NAT (PAT - Overload)
ip nat inside source list 1 interface Serial0/0/0 overload

# NAT Estático (Port Forwarding o Servidor)
ip nat inside source static 192.168.1.10 209.165.200.225

# ==========================================
# 7. IPV6
# ==========================================
ipv6 unicast-routing

# En interfaz
interface GigabitEthernet0/0
 ipv6 address 2001:db8:acad:1::1/64
 ipv6 address fe80::1 link-local
 ipv6 nd managed-config-flag
 no shutdown

# Ruta estática IPv6
ipv6 route 2001:db8:acad:2::/64 2001:db8:acad:3::2
# Ruta por defecto
ipv6 route ::/0 2001:db8:acad:3::2
# Ruta Flotante IPv6 (Nuevo)
ipv6 route ::/0 2001:db8:acad:3::3 10

# DHCPv6 (Nuevo)
ipv6 dhcp pool STATEFUL_POOL
 address prefix 2001:db8:acad:1::/64
 dns-server 2001:4860:4860::8888
 domain-name ejemplo.com
 exit

# ==========================================
# 8. VERIFICACIÓN Y DIAGNÓSTICO (Show Commands)
# ==========================================
show running-config
show ip interface brief
show ip route
show vlan brief
show interfaces trunk
show ip ospf neighbor
show access-lists
show ip nat translations
show ip dhcp binding
show port-security interface GigabitEthernet0/1
show etherchannel summary
show cdp neighbors
show version
ping 8.8.8.8
traceroute 8.8.8.8
show ntp associations
show clock
show ip dhcp snooping
show ip arp inspection vlan 10
