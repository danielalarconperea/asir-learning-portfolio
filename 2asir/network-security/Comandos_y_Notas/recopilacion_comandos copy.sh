#!/bin/bash
# Recopilación de Comandos de Redes y Seguridad (Cisco IOS)
# Generado a partir de apuntes de 1ASIR y 2ASIR

# ==========================================
# 1. CONFIGURACIÓN BÁSICA (Routers & Switches)
# ==========================================
enable
configure terminal
hostname [NOMBRE]
enable secret [CONTRASEÑA]
no ip domain-lookup
service password-encryption
banner motd "[MENSAJE]"

# Configuración de Consola
line console 0
 password [CONTRASEÑA]
 login
 logging synchronous
 exec-timeout [MIN] [SEC]
 exit

# Configuración de VTY (Telnet/SSH)
line vty 0 15
 password [CONTRASEÑA]
 login
 transport input ssh
 exec-timeout [MIN] [SEC]
 exit

# Guardar configuración
copy running-config startup-config
# o simplemente:
write memory

# ==========================================
# 2. INTERFACES Y ENLACES
# ==========================================
interface [INTERFAZ]  # Ej: GigabitEthernet0/0/0, Serial0/0/0, Vlan1
 description [DESCRIPCION]
 ip address [IP] [MASCARA]
 no shutdown
 exit

# Subinterfaces (Router-on-a-Stick)
interface [INTERFAZ].[VLAN_ID]
 encapsulation dot1Q [VLAN_ID]
 ip address [IP] [MASCARA]
 exit

# interfaces L3 en Switch (SVI)
interface vlan [ID]
 ip address [IP] [MASCARA]
 no shutdown
 exit

# Habilitar enrutamiento en Switch L3
ip routing

# ==========================================
# 3. VLANS Y TRUNKING (Switching)
# ==========================================
# Crear VLANs
vlan [ID]
 name [NOMBRE]
 exit

# Configurar puertos de acceso
interface [INTERFAZ]
 switchport mode access
 switchport access vlan [ID]
 exit

# Configurar puertos Trunk
interface [INTERFAZ]
 switchport mode trunk
 switchport trunk native vlan [ID]
 switchport trunk allowed vlan [LISTA]
 switchport nonegotiate
 exit

# VTP (VLAN Trunking Protocol)
vtp mode [server|client|transparent]
vtp domain [DOMINIO]
vtp password [PASSWORD]
vtp version 2

# EtherChannel (LACP/PLeAgP)
interface range [INTERFACES]
 channel-group [ID] mode [active|passive|desirable|auto]
 exit

# ==========================================
# 4. ENRUTAMIENTO (Routing)
# ==========================================
# Ruta Estática
ip route [RED_DESTINO] [MASCARA] [NEXT_HOP_IP]
ip route [RED_DESTINO] [MASCARA] [INTERFAZ_SALIDA]
# Ruta por defecto
ip route 0.0.0.0 0.0.0.0 [NEXT_HOP_IP]

# OSPF (Open Shortest Path First)
router ospf [PROCESS_ID]
 router-id [A.B.C.D]
 network [RED] [WILDCARD] area [AREA_ID]
 passive-interface [INTERFAZ]
 default-information originate
 auto-cost reference-bandwidth 1000
 exit

# RIPv2
router rip
 version 2
 no auto-summary
 network [RED_CLASSFUL]
 passive-interface [INTERFAZ]
 default-information originate
 exit

# ==========================================
# 5. SEGURIDAD (ACLs, Port Security, SSH)
# ==========================================
# ACL Estándar (1-99)
access-list [ID] [permit|deny] [IP_ORIGEN] [WILDCARD]
access-list [ID] permit any

# ACL Extendida (100-199 o Nombre)
ip access-list extended [NOMBRE]
 permit tcp [ORIGEN] [WILDCARD] [DESTINO] [WILDCARD] eq [PUERTO]
 deny ip any any log
 exit

# Aplicar ACL a interfaz
interface [INTERFAZ]
 ip access-group [ID/NOMBRE] [in|out]
 exit

# SSH Config
ip domain-name [DOMINIO]
crypto key generate rsa modulus [BITS] # Ej: 1024 o 2048
ip ssh version 2
ip ssh time-out 60
ip ssh authentication-retries 3
username [USUARIO] privilege 15 secret [CONTRASEÑA]
line vty 0 4
 transport input ssh
 login local
 exit

# Port Security (Switch)
interface [INTERFAZ]
 switchport port-security
 switchport port-security maximum [NUM]
 switchport port-security mac-address sticky
 switchport port-security violation [shutdown|restrict|protect]
 exit

# DHCP Snooping & ARP Inspection
ip dhcp snooping
ip dhcp snooping vlan [LISTA_VLANS]
ip arp inspection vlan [LISTA_VLANS]
# En puertos de confianza (Uplinks/Trunks):
interface [INTERFAZ]
 ip dhcp snooping trust
 ip arp inspection trust
 exit

# ==========================================
# 6. SERVICIOS DE RED (DHCP & NAT)
# ==========================================
# Servidor DHCP
ip dhcp excluded-address [IP_INICIO] [IP_FIN]
ip dhcp pool [NOMBRE_POOL]
 network [RED] [MASCARA]
 default-router [GATEWAY]
 dns-server [DNS_IP]
 exit

# DHCP Relay (en la interfaz SVI o Router)
interface vlan [ID]
 ip helper-address [IP_SERVIDOR_DHCP]
 exit

# NAT (Network Address Translation)
# 1. Definir interfaces inside/outside
interface [INT_LAN]
 ip nat inside
interface [INT_WAN]
 ip nat outside

# 2. Crear ACL para tráfico a traducir
access-list [ID] permit [RED_LAN] [WILDCARD]

# 3. Habilitar NAT (PAT - Overload)
ip nat inside source list [ID] interface [INT_WAN] overload

# NAT Estático (Port Forwarding o Servidor)
ip nat inside source static [IP_PRIVADA] [IP_PUBLICA]

# ==========================================
# 7. IPV6
# ==========================================
ipv6 unicast-routing

# En interfaz
interface [INTERFAZ]
 ipv6 address [IPV6_PREFIX]/[LENGTH]
 ipv6 address [LINK_LOCAL] link-local
 no shutdown

# Ruta estática IPv6
ipv6 route [RED_DESTINO]/[LENGTH] [NEXT_HOP_IP]
# Ruta por defecto
ipv6 route ::/0 [NEXT_HOP_IP]

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
show port-security interface [INT]
show etherchannel summary
show cdp neighbors
show version
ping [IP]
traceroute [IP]
