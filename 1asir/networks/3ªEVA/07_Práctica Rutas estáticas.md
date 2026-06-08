Okay, let's break down the configuration for this Packet Tracer exercise based on the provided topology and instructions.

**1. Análisis de la Topología y Direccionamiento IP**

*   **Red PC0:** 172.17.17.0/24 conectada a R1 (Fa0)
*   **Red PC1:** 172.19.19.0/24 conectada a R3 (Fa0)
*   **Red PC2:** 172.18.18.0/24 conectada a R2 (Gig0)
*   **Enlace R1-R2:** 192.168.255.0/30 (R1: Gig0/0/0, R2: Gig0/0/1)
*   **Enlace R1-R3:** 192.168.255.8/30 (R1: Gig0/0/2, R3: Gig0/0/2) - Marcado como "Ruta Flotante" desde R1.
*   **Enlace R2-R3:** 192.168.255.4/30 (R2: Gig0/0/0, R3: Gig0/0/1)

**Instrucciones de Enrutamiento Estático:**

*   **R1:** Ruta predeterminada (hacia R2) y ruta flotante (hacia R3) para alcanzar las otras redes.
*   **R2:** Rutas de siguiente salto hacia las redes de R1 y R3.
*   **R3:** Rutas totalmente especificadas hacia las redes de R1 y R2.

**2. Asignación de Direcciones IP (Ejemplo)**

Usaremos la primera IP utilizable para un extremo del enlace punto a punto y la segunda para el otro. Usaremos la IP .254 para las interfaces de gateway en las LANs y la .1 para los PCs.

*   **PC0:**
    *   IP: 172.17.17.1
    *   Máscara: 255.255.255.0
    *   Gateway: 172.17.17.254
*   **PC1:**
    *   IP: 172.19.19.1
    *   Máscara: 255.255.255.0
    *   Gateway: 172.19.19.254
*   **PC2:**
    *   IP: 172.18.18.1
    *   Máscara: 255.255.255.0
    *   Gateway: 172.18.18.254
*   **R1:**
    *   Fa0: 172.17.17.254 / 255.255.255.0
    *   Gig0/0/0: 192.168.255.1 / 255.255.255.252
    *   Gig0/0/2: 192.168.255.9 / 255.255.255.252
*   **R2:**
    *   Gig0 (Asumiendo que es Gig0/0/2 como en la imagen): 172.18.18.254 / 255.255.255.0
    *   Gig0/0/1: 192.168.255.2 / 255.255.255.252
    *   Gig0/0/0: 192.168.255.5 / 255.255.255.252
*   **R3:**
    *   Fa0: 172.19.19.254 / 255.255.255.0
    *   Gig0/0/2: 192.168.255.10 / 255.255.255.252
    *   Gig0/0/1: 192.168.255.6 / 255.255.255.252

**3. Configuración en Packet Tracer**

**Paso 1: Configurar PCs**

*   Abre cada PC (PC0, PC1, PC2).
*   Ve a la pestaña `Desktop` -> `IP Configuration`.
*   Introduce la IP, Máscara de Subred y Gateway definidos en el paso 2.

**Paso 2: Configurar Interfaces de Routers**

*   Accede a la CLI de cada router.

    **En R1:**
    ```bash
    enable
    configure terminal
    
    hostname R1
    
    interface GigabitEthernet0/0/1
    description Conexion a LAN PC0
    ip address 172.17.17.254 255.255.255.0
    no shutdown
    
    interface GigabitEthernet0/0/0
    description Enlace a R2
    ip address 192.168.255.1 255.255.255.252
    no shutdown
    
    interface GigabitEthernet0/0/2
    description Enlace a R3 (Backup)
    ip address 192.168.255.9 255.255.255.252
    no shutdown
    
    exit
    ```

    **En R2:**
    ```bash
    enable
    configure terminal
    !
    hostname R2
    !
    ! Asumiendo Gig0 es Gig0/0/2 según la imagen
    !
    interface GigabitEthernet0/0/2
    description Conexion a LAN PC2
    ip address 172.18.18.254 255.255.255.0
    no shutdown
    !
    interface GigabitEthernet0/0/1
    description Enlace a R1
    ip address 192.168.255.2 255.255.255.252
    no shutdown
    !
    interface GigabitEthernet0/0/0
    description Enlace a R3
    ip address 192.168.255.5 255.255.255.252
    no shutdown
    !
    exit
    ```

    **En R3:**
    ```bash
    enable
    configure terminal
    !
    hostname R3
    !
    ! O la interfaz correcta si es diferente
    !
    interface GigabitEthernet0/0/0
    description Conexion a LAN PC1
    ip address 172.19.19.254 255.255.255.0
    no shutdown
    !
    interface GigabitEthernet0/0/2
    description Enlace a R1
    ip address 192.168.255.10 255.255.255.252
    no shutdown
    !
    interface GigabitEthernet0/0/1
    description Enlace a R2
    ip address 192.168.255.6 255.255.255.252
    no shutdown
    !
    exit
    ```

**Paso 3: Configurar Enrutamiento Estático**

*   Vuelve al modo de configuración global (`configure terminal`) en cada router si saliste.

    **En R1:**
    ```bash
    configure terminal
    ! Ruta Predeterminada principal hacia R2
    ! Sintaxis: ip route <red_destino> <mascara_destino> <IP_siguiente_salto> [distancia_administrativa]
    ip route 0.0.0.0 0.0.0.0 192.168.255.2
    !
    ! Ruta Flotante (backup) hacia R3. Se usa una distancia administrativa mayor que 1 (por defecto para estáticas). Usaremos 5.
    ip route 0.0.0.0 0.0.0.0 192.168.255.10 5
    !
    exit
    ```

    **En R2:**
    ```bash
    configure terminal
    ! Rutas hacia las redes conectadas a R1 (LAN PC0 y Enlace R1-R3) via R1
    ip route 172.17.17.0 255.255.255.0 192.168.255.1
    ip route 192.168.255.8 255.255.255.252 192.168.255.1
    !
    ! Ruta hacia la red conectada a R3 (LAN PC1) via R3
    ip route 172.19.19.0 255.255.255.0 192.168.255.6
    !
    exit
    ```

    **En R3:**
    ```bash
    configure terminal
    ! Rutas totalmente especificadas hacia las redes de R1 y R2
    ! Sintaxis: ip route <red_destino> <mascara_destino> <Interfaz_Salida> <IP_siguiente_salto>
    !
    ! Ruta hacia la LAN de R1 (PC0) via R1
    ip route 172.17.17.0 255.255.255.0 GigabitEthernet0/0/2 192.168.255.9
    !
    ! Ruta hacia la LAN de R2 (PC2) via R2
    ip route 172.18.18.0 255.255.255.0 GigabitEthernet0/0/1 192.168.255.5
    !
    ! (Opcional pero recomendable) Ruta hacia el enlace R1-R2 via R2 (camino más corto)
    ! ip route 192.168.255.0 255.255.255.252 GigabitEthernet0/0/1 192.168.255.5
    ! O via R1
    ! ip route 192.168.255.0 255.255.255.252 GigabitEthernet0/0/2 192.168.255.9
    ! Escoge una si necesitas alcanzar específicamente ese segmento desde R3.
    ! Para cumplir estrictamente con "a las redes de R1 y R2", las LANs son lo principal.
    !
    exit
    ```

**Paso 4: Guardar Configuración**

*   En cada router, desde el modo privilegiado (`enable`):
    ```bash
    copy running-config startup-config
    ```
    o simplemente
    ```bash
    wr
    ```

**Paso 5: Verificación**

*   **Comprobar IPs:** En cada router, usa `show ip interface brief` para verificar que las interfaces estén activas ("up", "up") y con las IPs correctas.
*   **Comprobar Rutas:** En cada router, usa `show ip route`.
    *   En R1, deberías ver una ruta estática `S* 0.0.0.0/0 [1/0] via 192.168.255.2`. La ruta flotante no aparecerá a menos que el enlace principal (a R2) falle. Para probarla, puedes apagar la interfaz `Gig0/0/0` de R1 o `Gig0/0/1` de R2.
    *   En R2, deberías ver las rutas estáticas `S` hacia `172.17.17.0/24`, `192.168.255.8/30` (via 192.168.255.1) y `172.19.19.0/24` (via 192.168.255.6).
    *   En R3, deberías ver las rutas estáticas `S` hacia `172.17.17.0/24` (via 192.168.255.9, G0/0/2) y `172.18.18.0/24` (via 192.168.255.5, G0/0/1).
*   **Pruebas de Conectividad:**
    *   Desde PC0, haz ping a PC1 (172.19.19.1) y PC2 (172.18.18.1).
    *   Desde PC1, haz ping a PC0 (172.17.17.1) y PC2 (172.18.18.1).
    *   Desde PC2, haz ping a PC0 (172.17.17.1) y PC1 (172.19.19.1).
    *   Usa `traceroute` (o `tracert` en Windows PC) para ver el camino que siguen los paquetes. Por ejemplo, desde PC0 a PC1, el camino debería ser PC0 -> R1 -> R2 -> R3 -> PC1.

Siguiendo estos pasos, deberías poder configurar la red en Packet Tracer según los requisitos especificados. ¡Suerte!