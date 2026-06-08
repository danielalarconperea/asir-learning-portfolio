#!/bin/bash
# Ejercicio 9: Script con menú para mostrar/modificar IP, máscara, Gateway y DNS, 
# validando los valores con expresiones regulares.

while true; do
    echo -e "\n--- MENÚ DE RED ---"
    echo "1. Mostrar"
    echo "2. Modificar"
    echo "3. Salir"
    read -p "Introduce una opción: " opcion

    case $opcion in
        1)
            echo "1.IP"
            echo "2.Mascara"
            echo "3.Gateway"
            echo "4.DNS"
            read -p "Introduce una opción: " opcion
            case $opcion in
                1)
                    echo "IP: $(hostname -I)"
                    ;;
                2)
                    echo "Mascara: $(ip addr show | grep 'inet ' | awk '{print $2}' | cut -d '/' -f 2)"
                    ;;
                3)
                    echo "Gateway: $(ip route show default | awk '{print $3}')"
                    ;;
                4)
                    echo "DNS: $(cat /etc/resolv.conf | grep 'nameserver' | awk '{print $2}')"
                    ;;
                *)
                    echo "Opción no válida, intenta de nuevo."
                    ;;
            esac
            ;;
        2)
            echo "1.IP"
            echo "2.Mascara"
            echo "3.Gateway"
            echo "4.DNS"
            read -p "Introduce una opción: " opcion
            case $opcion in
                1)
                    read -p "Introduce la IP: " ip
                    if [[ ! $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
                        echo "IP no válida, intenta de nuevo."
                        continue
                    fi
                    ip addr add $ip/24 dev eth0
                    ;;
                2)
                    read -p "Introduce la mascara: " mascara
                    if [[ ! $mascara =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
                        echo "Mascara no válida, intenta de nuevo."
                        continue
                    fi
                    if [[ $ip = "" ]]; then
                        ip=$(hostname -I | awk '{print $1}')
                    fi
                    ip addr add $ip/$mascara dev eth0
                    ;;
                3)
                    read -p "Introduce el gateway: " gateway
                    if [[ ! $gateway =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
                        echo "Gateway no válido, intenta de nuevo."
                        continue
                    fi
                    ip route add default via $gateway
                    ;;
                4)
                    read -p "Introduce el DNS: " dns
                    if [[ ! $dns =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
                        echo "DNS no válido, intenta de nuevo."
                        continue
                    fi
                    sed -i '/nameserver/d' /etc/resolv.conf 2>/dev/null
                    echo "nameserver $dns" >> /etc/resolv.conf
                    ;;
                *)
                    echo "Opción no válida, intenta de nuevo."
                    ;;
            esac
            ;;
        3)
            echo "Saliendo..."
            exit 0
            ;;
        *)
            echo "Opción no válida, intenta de nuevo."
            ;;
    esac
done
    