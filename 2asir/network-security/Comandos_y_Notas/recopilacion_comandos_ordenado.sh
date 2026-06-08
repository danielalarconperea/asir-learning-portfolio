## 1. Configuraciones Globales

enable
configure terminal
hostname NOMBRE_DISPOSITIVO
no ip domain-lookup
banner motd "Mensaje"
clock set 12:00:00 25 Dec 2025
service timestamps log datetime msec
logging 192.168.4.2
logging host 192.168.4.2
no logging trap
ntp server 192.168.4.2
service password-encryption

# Usuarios y Seguridad
username admin secret cisco
username supervisor privilege 7 secret cisco
privilege exec level 7 ping
privilege exec level 7 traceroute
privilege exec level 7 show
aaa new-model
aaa authentication login default local
aaa authentication login CONSOLE_AUTH local enable
ip domain-name miempresa.local
crypto key generate rsa modulus 1024
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3

# Lineas
line console 0
 password cisco
 login
 login authentication CONSOLE_AUTH
 logging synchronous
 exec-timeout 10 0
 exit
line vty 0 15
 password cisco
 login local
 transport input ssh
 exec-timeout 5 0
 access-class 1 in
 exit

# ACL para Gestión (VTY)
access-list 1 permit 192.168.4.10
access-list 1 deny any


## 2. Switch (Switch Capa 3 - Core/Dist)

# VLANs
vlan 10
 name VENTAS
vlan 20
 name PRODUCCION
vlan 99
 name GESTION_NATIVA
 exit

# Interfaces L3 (SVI)
interface vlan 10
 ip address 172.16.10.1 255.255.255.0
 no shutdown
 ip helper-address 192.168.100.10      # DHCP Relay
 exit

# Puertos L3 (Routed Ports)
interface GigabitEthernet1/0/24
 no switchport
 ip address 192.168.200.1 255.255.255.0
 exit

# Enrutamiento L3
ip routing
ip classless

# Puertos de Acceso
interface Range FastEthernet0/1 - 10
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast
 exit

# Puertos Trunk
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk native vlan 99
 switchport trunk allowed vlan 10,20,99
 switchport nonegotiate
 exit

# VTP
vtp mode server
vtp domain midominio
vtp password miclave
vtp version 2

# EtherChannel
interface range GigabitEthernet0/1 - 2
 channel-group 1 mode active
 exit
interface port-channel 1
 switchport mode trunk
 switchport trunk native vlan 99
 exit

# Spanning Tree
spanning-tree mode pvst
spanning-tree vlan 1,10,20 root primary
spanning-tree vlan 1,10,20 root secondary
spanning-tree portfast default
spanning-tree bpduguard enable
spanning-tree portfast bpduguard default

# Seguridad L2
interface FastEthernet0/1
 switchport port-security
 switchport port-security maximum 2
 switchport port-security mac-address sticky
 switchport port-security violation shutdown
 switchport port-security aging time 10
 switchport port-security aging type inactivity
 exit
ip dhcp snooping
ip dhcp snooping vlan 10,20
interface GigabitEthernet0/24
 ip dhcp snooping trust
 exit
interface range FastEthernet0/1 - 20
 ip dhcp snooping limit rate 5
 exit
ip arp inspection vlan 10,20
interface GigabitEthernet0/24
 ip arp inspection trust
 exit


## 3. Router (General)

# Interfaces Físicas
interface GigabitEthernet0/0/1
 description CONEXION_WAN
 ip address 192.168.1.1 255.255.255.0
 duplex auto
 speed auto
 no shutdown
 exit

# Interfaces Loopback
interface Loopback0
 ip address 10.1.1.1 255.255.255.255
 exit

# Subinterfaces (ROAS)
interface GigabitEthernet0/0/0.10
 encapsulation dot1Q 10
 ip address 192.168.10.1 255.255.255.0
 exit

# Rutas Estáticas
ip route 192.168.20.0 255.255.255.0 10.1.1.2
ip route 192.168.30.0 255.255.255.0 Serial0/0/0
ip route 0.0.0.0 0.0.0.0 209.165.200.225
ip route 0.0.0.0 0.0.0.0 10.1.1.2 10

# OSPF
router ospf 1
 router-id 1.1.1.1
 auto-cost reference-bandwidth 1000
 network 192.168.10.0 0.0.0.255 area 0
 network 10.1.1.0 0.0.0.3 area 0
 network 172.20.10.0 0.0.1.255 area 0
 passive-interface GigabitEthernet0/0
 passive-interface default
 no passive-interface GigabitEthernet0/1
 default-information originate
 interface Loopback0
  ip ospf network point-to-point
 interface GigabitEthernet0/0
  ip ospf cost 50
 exit
clear ip ospf process
show ip ospf neighbor

# DHCP Server
ip dhcp excluded-address 192.168.10.1 192.168.10.10
ip dhcp pool LAN_POOL
 network 192.168.10.0 255.255.255.0
 default-router 192.168.10.1
 dns-server 8.8.8.8
 domain-name empresa.com
 exit

# DHCP Client
interface GigabitEthernet0/1
 ip address dhcp
 exit

# ACLs
access-list 10 deny host 192.168.1.50
access-list 10 permit 192.168.1.0 0.0.0.255
access-list 10 permit any
ip access-list extended FILTRO_WEB
 permit tcp 192.168.10.0 0.0.0.255 any eq 80
 permit tcp 192.168.10.0 0.0.0.255 any eq 443
 permit udp any any eq 53
 deny tcp any any eq 23
 deny ip any any log
 exit
interface GigabitEthernet0/0
 ip access-group FILTRO_WEB in
 exit


## 4. IPv6 & VPN (Router Avanzado)

# IPv6
ipv6 unicast-routing
interface GigabitEthernet0/0
 ipv6 address 2001:db8:acad:1::1/64
 ipv6 address fe80::1 link-local
 no shutdown
ipv6 route ::/0 2001:db8:acad:2::2
ipv6 route 2001:db8:acad:3::/64 2001:db8:acad:2::2
ipv6 route ::/0 2001:db8:acad:2::3 10

# DHCPv6
ipv6 dhcp pool POOL_STATELESS
 dns-server 2001:4860:4860::8888
 domain-name ejemplo.com
 exit
interface GigabitEthernet0/0
 ipv6 nd other-config-flag
 ipv6 dhcp server POOL_STATELESS
 exit
ipv6 dhcp pool POOL_STATEFUL
 address prefix 2001:db8:acad:1::/64
 dns-server 2001:4860:4860::8888
 exit
interface GigabitEthernet0/0
 ipv6 nd managed-config-flag
 ipv6 dhcp server POOL_STATEFUL
 exit

# VPN IPsec
crypto isakmp policy 10
 encryption aes 256
 hash sha
 authentication pre-share
 group 5
 lifetime 86400
 exit
crypto isakmp key MITT_SECRETO address 10.2.2.2
crypto ipsec transform-set MI_SET esp-aes esp-sha-hmac
access-list 110 permit ip 192.168.1.0 0.0.0.255 192.168.3.0 0.0.0.255
crypto map MI_MAPA 10 ipsec-isakmp
 set peer 10.2.2.2
 set transform-set MI_SET
 match address 110
 exit
interface Serial0/0/0
 crypto map MI_MAPA
 exit


## 5. Router ISP

# NAT
interface GigabitEthernet0/0
 ip nat inside
interface Serial0/0/0
 ip nat outside
ip nat inside source static 192.168.1.10 209.165.200.226
access-list 1 permit 192.168.0.0 0.0.255.255
ip nat inside source list 1 interface Serial0/0/0 overload
