Para llevar a cabo esta práctica de OSPF “from scratch” sigue estos pasos en **cada uno** de tus routers (R1, R2 y R3). El objetivo es levantar un proceso OSPF en área 0 que incluya:

* La LAN local (con sus rangos /23)
* El enlace punto-a-punto a los otros routers (/30)
* La loopback (que nos servirá de router-ID)

---

## 1. Configuración básica en R1

```shell
R1> enable
R1# configure terminal

!— asigna un Router ID único (opcional, si quieres forzarlo):
R1(config)# router ospf 1
R1(config-router)# router-id 1.1.1.1
R1(config-router)# exit

!— habilita OSPF en las redes de R1:
R1(config)# router ospf 1
R1(config-router)# network 172.20.8.0  0.0.1.255 area 0    !–– LAN 172.20.8.0/23
R1(config-router)# network 172.20.10.0 0.0.1.255 area 0    !–– Loopback0 /23
R1(config-router)# network 192.168.255.0 0.0.0.3 area 0    !–– enlace R1–R2 (/30)
R1(config-router)# network 192.168.255.4 0.0.0.3 area 0    !–– enlace R1–R3 (/30)
R1(config-router)# exit

!— (opcional) desactivar resúmenes automáticos:
R1(config)# router ospf 1
R1(config-router)# no auto-summary

R1(config)# end
R1# write memory
```

---

## 2. Configuración básica en R2

```shell
R2> enable
R2# configure terminal

!— router-ID (opcional):
R2(config)# router ospf 1
R2(config-router)# router-id 2.2.2.2
R2(config-router)# exit

!— redes OSPF:
R2(config)# router ospf 1
R2(config-router)# network 172.20.0.0   0.0.1.255 area 0    !–– LAN derecha 172.20.0.0/23
R2(config-router)# network 172.20.2.0   0.0.1.255 area 0    !–– Loopback0 /23
R2(config-router)# network 192.168.255.0 0.0.0.3 area 0    !–– enlace R2–R1 (/30)
R2(config-router)# network 192.168.255.8 0.0.0.3 area 0    !–– enlace R2–R3 (/30)
R2(config-router)# exit

R2(config)# router ospf 1
R2(config-router)# no auto-summary

R2(config)# end
R2# write memory
```

---

## 3. Configuración básica en R3

```shell
R3> enable
R3# configure terminal

!— router-ID (opcional):
R3(config)# router ospf 1
R3(config-router)# router-id 3.3.3.3
R3(config-router)# exit

!— redes OSPF:
R3(config)# router ospf 1
R3(config-router)# network 172.20.4.0   0.0.1.255 area 0    !–– LAN inferior 172.20.4.0/23
R3(config-router)# network 172.20.6.0   0.0.1.255 area 0    !–– Loopback0 /23
R3(config-router)# network 192.168.255.4 0.0.0.3 area 0    !–– enlace R3–R1 (/30)
R3(config-router)# network 192.168.255.8 0.0.0.3 area 0    !–– enlace R3–R2 (/30)
R3(config-router)# exit

R3(config)# router ospf 1
R3(config-router)# no auto-summary

R3(config)# end
R3# write memory
```

---

## 4. Verificación

1. **Vecinos OSPF**

   ```
   show ip ospf neighbor
   ```

   Deberías ver tres adyacencias (R1–R2, R2–R3 y R1–R3).

2. **Tabla de enrutamiento**

   ```
   show ip route ospf
   ```

   Aparecerán las rutas a las loopbacks y a las LAN remotas de los otros routers.

3. **Ping entre loopbacks**
   Desde R1:

   ```
   ping 172.20.2.1   !–– Loopback de R2
   ping 172.20.6.1   !–– Loopback de R3
   ```

4. **Ping PC a PC**
   Finalmente, desde cualquier PC de una LAN, haz ping a las IPs de loopback y a las PCs de otras LANs para demostrar conectividad completa.

---

Con esto tendrás un OSPF de área 0 que interconecta los tres routers y anuncia tanto las redes físicas (/23) como las loopbacks. ¡Éxito en tu práctica!
