#!/bin/bash
# Ejercicio 9 Avanzado: Menú de configuración de red.
# Nota: Modificar la red requiere privilegios de root.

validar_ip() {
    local ip=$1
    local stat=1
    if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        OIFS=$IFS
        IFS='.'
        ip=($ip)
        IFS=$OIFS
        [[ ${ip[0]} -le 255 && ${ip[1]} -le 255 && ${ip[2]} -le 255 && ${ip[3]} -le 255 ]]
        stat=$?
    fi
    return $stat
}

while true; do
    echo "--- CONFIGURACIÓN DE RED ---"
    echo "a. Mostrar configuración IP"
    echo "b. Modificar IP y máscara (Temporal)"
    echo "c. Modificar Gateway (Temporal)"
    echo "d. Modificar DNS"
    echo "s. Salir"
    read -p "Opción: " OPC

    case $OPC in
        a)
            ip addr show
            ;;
        b)
            read -p "Introduce interfaz (ej. eth0): " INT
            read -p "Introduce nueva IP: " NIP
            read -p "Introduce máscara (ej. 24): " MASK
            if validar_ip "$NIP"; then
                sudo ip addr add "$NIP/$MASK" dev "$INT"
                echo "IP añadida."
            else
                echo "IP no válida."
            fi
            ;;
        c)
            read -p "Introduce Gateway: " GW
            if validar_ip "$GW"; then
                sudo ip route add default via "$GW"
                echo "Gateway configurado."
            else
                echo "IP no válida."
            fi
            ;;
        d)
            read -p "Introduce DNS: " DNS
            if validar_ip "$DNS"; then
                echo "nameserver $DNS" | sudo tee /etc/resolv.conf > /dev/null
                echo "DNS configurado."
            else
                echo "IP no válida."
            fi
            ;;
        s) break ;;
        *) echo "Opción no válida." ;;
    esac
    echo ""
done
