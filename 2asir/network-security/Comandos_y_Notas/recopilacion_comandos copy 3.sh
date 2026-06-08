#!/bin/bash
# ==============================================================================
# RECOPILACIÓN DEFINITIVA DE COMANDOS CISCO IOS (1ASIR & 2ASIR)
# ==============================================================================
# Este script agrupa TODOS los comandos encontrados en los apuntes, scripts
# y ejercicios de examen de "Redes" y "Seguridad de Redes".
# ==============================================================================

# ==========================================
# 1. MODOS Y PRIVILEGIOS
# ==========================================
enable                                      # Entrar a modo privilegiado
configure terminal                          # Entrar a configuración global
exit                                        # Salir un nivel
end                                         # Salir al modo privilegiado desde cualquiera
disable                                     # Salir de modo privilegiado

# ==========================================
# 2. GESTIÓN DEL DISPOSITIVO (BÁSICO)
# ==========================================
hostname NOMBRE_DISPOSITIVO                 # Cambiar nombre
no ip domain-lookup                         # Deshabilitar búsqueda DNS errónea
banner motd "Mensaje de Bienvenida/Alerta"  # Banner de inicio

# Gestión de Tiempos y Logs
clock set 12:00:00 25 Dec 2025              # Configurar hora manualmente
service timestamps log datetime msec        # Marcas de tiempo en logs
logging 192.168.4.2                         # Enviar logs a servidor Syslog
logging host 192.168.4.2                    # (Variante) Enviar logs
no logging trap                             # Desactivar traps (o ajustarlos)
ntp server 192.168.4.2                      # Sincronizar reloj con servidor NTP

# Cifrado de contraseñas
service password-encryption                 # Cifrar passwords en texto plano

# Guardado
copy running-config startup-config          # Guardar configuración
write memory                                # (Variante antigua) Guardar

# ==========================================
# 3. USUARIOS Y ACCESO (AAA & SSH)
# ==========================================
# Creación de Usuarios Locales
username admin secret cisco                 # Usuario con clave cifrada
username supervisor privilege 7 secret cisco # Usuario con privilegio específico
# Definir niveles de privilegio
privilege exec level 7 ping
privilege exec level 7 traceroute
privilege exec level 7 show

# Configuración de AAA (Autenticación, Autorización, Contabilidad)
aaa new-model                               # Activar AAA
aaa authentication login default local      # Autenticación predeterminada local
aaa authentication login CONSOLE_AUTH local enable # Lista de aut. para consola

# Configuración de Línea de Consola
line console 0
 password cisco                             # Contraseña (si no se usa AAA)
 login                                      # Activar login simple
 login authentication CONSOLE_AUTH          # Usar lista AAA (si se configuró)
 logging synchronous                        # Evitar que logs corten comandos
 exec-timeout 10 0                          # Timeout de inactividad (min seg)
 exit

# Configuración de SSH (Líneas VTY)
ip domain-name miempresa.local              # Dominio necesario para claves RSA
crypto key generate rsa modulus 1024        # Generar claves (1024 o 2048)
ip ssh version 2                            # Forzar SSHv2
ip ssh time-out 60                          # Tiempo de espera
ip ssh authentication-retries 3             # Intentos permitidos

# Líneas VTY (Acceso Remoto)
line vty 0 15                               # Rango de líneas (0 4 o 0 15)
 password cisco
 login local                                # Usar base de datos local de usuarios
 transport input ssh                        # Permitir solo SSH (bloquear Telnet)
 exec-timeout 5 0                           # Timeout
 access-class 1 in                          # Aplicar ACL estándar para restringir acceso
 exit

# ACL para restringir VTY
access-list 1 permit 192.168.4.10           # Permitir solo IP de gestión
access-list 1 deny any                      # (Implícito, pero explícito es mejor)

# ==========================================
# 4. INTERFACES (L2 & L3)
# ==========================================
# Interfaz Física (Router)
interface GigabitEthernet0/0/1
 description CONEXION_WAN
 ip address 192.168.1.1 255.255.255.0
 duplex auto                                # Duplex automático para 
 speed auto                                 # Velocidad automática
 no shutdown                                # Habilitar interfaz
 exit

# Interface Loopback (Lógica)
interface Loopback0
 ip address 10.1.1.1 255.255.255.255
 exit

# Subinterfaces (Router-on-a-Stick / 802.1Q)
interface GigabitEthernet0/0/0.10
 encapsulation dot1Q 10                     # Tag VLAN 10
 ip address 192.168.10.1 255.255.255.0
 exit

# SVI (Switch Virtual Interface - Interfaz VLAN)
interface vlan 10
 ip address 172.16.10.1 255.255.255.0
 no shutdown
 exit

# Convertir puerto de Switch en Puerto Enrutado (L3)
interface GigabitEthernet1/0/24
 no switchport
 ip address 192.168.200.1 255.255.255.0
 exit

# Habilitar enrutamiento en Switch Multicapa
ip routing
ip classless                                # Permitir subredes (legacy)

# ==========================================
# 5. VLANs y TRUNKING
# ==========================================
# Creación de VLANs
vlan 10
 name VENTAS
vlan 20
 name PRODUCCION
vlan 99
 name GESTION_NATIVA
 exit

# Puertos de Acceso
interface Range FastEthernet0/1 - 10
 switchport mode access
 switchport access vlan 10
 spanning-tree portfast                     # Acelerar convergencia en puertos PC
 exit

# Puertos Trunk (Troncales)
interface GigabitEthernet0/1
 switchport mode trunk
 switchport trunk native vlan 99            # Cambiar VLAN nativa (seguridad)
 switchport trunk allowed vlan 10,20,99     # Filtrar VLANs permitidas
 switchport nonegotiate                     # Deshabilitar DTP (seguridad)
 exit

# VTP (VLAN Trunking Protocol)
vtp mode server                             # o client / transparent
vtp domain midominio
vtp password miclave
vtp version 2

# EtherChannel (Agregación de Enlaces) - LACP
interface range GigabitEthernet0/1 - 2
 channel-group 1 mode active                # LACP (active/passive). PAgP (desirable/auto)
 exit
interface port-channel 1
 switchport mode trunk
 switchport trunk native vlan 99
 exit

# ==========================================
# 6. SPANNING TREE PROTOCOL (STP)
# ==========================================
spanning-tree mode pvst                     # Modo Per-VLAN Spanning Tree
spanning-tree vlan 1,10,20 root primary     # Forzar a ser Root Bridge
spanning-tree vlan 1,10,20 root secondary   # Forzar a ser Backup Root
spanning-tree portfast default              # Activar PortFast por defecto en accesos
spanning-tree bpduguard enable              # (En interfaz) Proteger puerto PortFast
spanning-tree portfast bpduguard default    # (Global) Proteger puertos PortFast

# ==========================================
# 7. ENRUTAMIENTO ESTÁTICO
# ==========================================
# Ruta Estática IPv4
# ip route [RED_DESTINO] [MASCARA] [SIGUIENTE_SALTO / INTERFAZ] [DISTANCIA_ADMIN]
ip route 192.168.20.0 255.255.255.0 10.1.1.2
ip route 192.168.30.0 255.255.255.0 Serial0/0/0

# Ruta Por Defecto (Default Gateway)
ip route 0.0.0.0 0.0.0.0 209.165.200.225

# Ruta Flotante (Respaldo)
ip route 0.0.0.0 0.0.0.0 10.1.1.2 10        # Distancia administrativa 10 (menos preferida)

# ==========================================
# 8. ENRUTAMIENTO DINÁMICO (OSPF)
# ==========================================
router ospf 1
 router-id 1.1.1.1                          # ID único del router
 auto-cost reference-bandwidth 1000         # Ajuste de cálculo de coste (Gbps)
 
 # Declaración de redes (Network Command)
 # network [IP_RED] [WILDCARD] area [AREA_ID]
 network 192.168.10.0 0.0.0.255 area 0      # Red LAN
 network 10.1.1.0 0.0.0.3 area 0            # Enlace WAN
 network 172.20.10.0 0.0.1.255 area 0       # Ejemplo wildcard /23 (Loopback)

 # Interfaces Pasivas (No envían Hello)
 passive-interface GigabitEthernet0/0       # Red LAN donde no hay routers
 passive-interface default                  # Poner todas pasivas por defecto
 no passive-interface GigabitEthernet0/1    # Reactivar donde sí hay vecino

 # Propagación de ruta por defecto
 default-information originate

 # Ajuste tipo de red OSPF
 interface Loopback0
  ip ospf network point-to-point            # Anunciar como /32 o subred real
 interface GigabitEthernet0/0
  ip ospf cost 50                           # Manipular coste manualmente

 exit
 
# Diagnóstico OSPF
clear ip ospf process                       # Reiniciar proceso (útil cambios ID)
show ip ospf neighbor                       # Ver vecinos
show ip ospf interface                      # Ver interfaces OSPF

# ==========================================
# 9. DHCP (CLIENTE Y SERVIDOR)
# ==========================================
# Router como Servidor DHCP
ip dhcp excluded-address 192.168.10.1 192.168.10.10  # Excluir rango de IPs (reservadas)
ip dhcp pool LAN_POOL                                # Crear pool DHCP con nombre
 network 192.168.10.0 255.255.255.0                  # Definir red y máscara a repartir
 default-router 192.168.10.1                         # Puerta de enlace para clientes
 dns-server 8.8.8.8                                  # Servidor DNS principal
 domain-name empresa.com                             # Nombre de dominio de la red
 exit

# Router como Cliente DHCP (WAN)
interface GigabitEthernet0/1
 ip address dhcp                                     # Obtener IP automáticamente del ISP
 exit

# DHCP Relay (Helper Address) - Para reenviar peticiones a otro servidor
interface vlan 10
 ip helper-address 192.168.100.10                    # Reenviar peticiones DHCP a servidor remoto
 exit

# ==========================================
# 10. NAT (TRADUCCIÓN DE DIRECCIONES)
# ==========================================
# Definir zonas Inside/Outside
interface GigabitEthernet0/0
 ip nat inside
interface Serial0/0/0
 ip nat outside

# 1. NAT Estático (Servidor Público)
ip nat inside source static 192.168.1.10 209.165.200.226

# 2. NAT con Sobrecarga (PAT) - Salida a Internet común
access-list 1 permit 192.168.0.0 0.0.255.255           # Tráfico permitido
ip nat inside source list 1 interface Serial0/0/0 overload

# ==========================================
# 11. SEGURIDAD L2 (SWITCH)
# ==========================================
# Port Security
interface FastEthernet0/1
 switchport port-security
 switchport port-security maximum 2
 switchport port-security mac-address sticky           # Aprender MACs dinámicamente
 switchport port-security violation shutdown           # o restrict / protect
 switchport port-security aging time 10                # Tiempo de expiración 10 min
 switchport port-security aging type inactivity        # Expirar por inactividad
 exit

# DHCP Snooping (Evitar Rogue DHCP)
ip dhcp snooping
ip dhcp snooping vlan 10,20
interface GigabitEthernet0/24                          # Puerto Uplink (Router/DHCP real)
 ip dhcp snooping trust                                # Puerto de confianza
 exit
interface range FastEthernet0/1 - 20
 ip dhcp snooping limit rate 5                         # Limitar peticiones DHCP
 exit

# Dynamic ARP Inspection (DAI) (Evitar ARP Spoofing)
ip arp inspection vlan 10,20
interface GigabitEthernet0/24
 ip arp inspection trust
 exit

# ==========================================
# 12. ACLs (LISTAS DE CONTROL DE ACCESO)
# ==========================================
# ACL Estándar (1-99) - Solo origen
access-list 10 deny host 192.168.1.50
access-list 10 permit 192.168.1.0 0.0.0.255
access-list 10 permit any                            # (Opcional, explicito)

# ACL Extendida (100-199 o Nombre) - Origen, Destino, Protocolo, Puerto
ip access-list extended FILTRO_WEB
 permit tcp 192.168.10.0 0.0.0.255 any eq 80         # Permitir HTTP
 permit tcp 192.168.10.0 0.0.0.255 any eq 443        # Permitir HTTPS
 permit udp any any eq 53                            # Permitir DNS
 deny tcp any any eq 23                              # Denegar Telnet
 deny ip any any log                                 # Denegar resto y loguear
 exit

# Aplicar ACL en interfaz
interface GigabitEthernet0/0
 ip access-group FILTRO_WEB in                       # 'in' o 'out'
 exit

# ==========================================
# 13. IPv6 (CONFIGURACIÓN COMPLETA)
# ==========================================
ipv6 unicast-routing                                 # Activar enrutamiento IPv6

# Dirección IPv6 en interfaz
interface GigabitEthernet0/0
 ipv6 address 2001:db8:acad:1::1/64
 ipv6 address fe80::1 link-local                     # Dirección Link-Local manual
 no shutdown

# Rutas Estáticas IPv6
ipv6 route ::/0 2001:db8:acad:2::2                   # Ruta por defecto
ipv6 route 2001:db8:acad:3::/64 2001:db8:acad:2::2   # Ruta específica
ipv6 route ::/0 2001:db8:acad:2::3 10                # Ruta flotante (AD 10)

# DHCPv6 Stateless (SLAAC + DNS)
ipv6 dhcp pool POOL_STATELESS
 dns-server 2001:4860:4860::8888
 domain-name ejemplo.com
 exit
interface GigabitEthernet0/0
 ipv6 nd other-config-flag                           # Bandera 'O' (Other info)
 ipv6 dhcp server POOL_STATELESS
 exit

# DHCPv6 Stateful (Dirección + DNS)
ipv6 dhcp pool POOL_STATEFUL
 address prefix 2001:db8:acad:1::/64
 dns-server 2001:4860:4860::8888
 exit
interface GigabitEthernet0/0
 ipv6 nd managed-config-flag                         # Bandera 'M' (Managed address)
 ipv6 dhcp server POOL_STATEFUL
 exit

# ==========================================
# 14. VPN IPSEC (SITE-TO-SITE)
# ==========================================
# 1. Política ISAKMP (Fase 1)
crypto isakmp policy 10
 encryption aes 256
 hash sha
 authentication pre-share
 group 5
 lifetime 86400
 exit
crypto isakmp key MITT_SECRETO address 10.2.2.2

# 2. Transform Set IPsec (Fase 2)
crypto ipsec transform-set MI_SET esp-aes esp-sha-hmac

# 3. ACL de Tráfico Interesante (VPN)
access-list 110 permit ip 192.168.1.0 0.0.0.255 192.168.3.0 0.0.0.255

# 4. Crypto Map
crypto map MI_MAPA 10 ipsec-isakmp
 set peer 10.2.2.2
 set transform-set MI_SET
 match address 110
 exit

# 5. Aplicar a interfaz WAN
interface Serial0/0/0
 crypto map MI_MAPA
 exit

# ==========================================
# FIN DE LA RECOPILACIÓN
# ==========================================
