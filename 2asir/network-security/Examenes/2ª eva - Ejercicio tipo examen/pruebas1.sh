# ------ core

vlan 20
vlan 50
vlan 99
name adm

# 5 puertos por cada vlan, el resto en la vlan 99 desactivados

interface gigabitEthernet1/0/1
switchport mode access
switchport access vlan 50

interface gigabitEthernet1/0/11
switchport mode access
switchport access vlan 20

interface vlan 20
ip address 192.168.20.1 255.255.255.0

interface vlan 50
ip address 192.168.50.1 255.255.255.0

interface vlan 99
ip address 192.168.99.1 255.255.255.0

