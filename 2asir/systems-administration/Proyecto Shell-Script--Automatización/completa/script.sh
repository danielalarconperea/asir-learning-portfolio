
#!/bin/bash
if [ "$#" == "0" ] ;then
#Datos de red del equipo
ip add
#Estado del servicio
systemctl status apache2
fi
#Menu de instalacion
Menu1=""
while [[ "$#" == "0" && "$Menu1" != "Salir" ]]
do
read -p "Opciones del menu del servicio:
    - Instalacion del servicio (Escriba: Descarga)
    - Eliminacion del servicio (Escriba: Borrar)
    - Poner en marcha el servicio (Escriba: Correr)
    - Parar el servicio (Escriba: Parada)
    - Consultar los logs (Escriba: Logs)
    - Salir (Escriba: Salir)
    Escriba lo que desea hacer: " Menu1
#Menu descarga
case $Menu1 in
    "Descarga")
        read -p "Opciones de instalacion:
        - Instalacion mediante comandos (Escriba: Comandos)
        - Instalacion con Docker (Escriba: Docker)
        - Salir (Escriba: Salir)
        Escriba como desea descargarlo: " MenuDescarga
        case $MenuDescarga in
            "Comandos")
                sudo apt install apache2 apache2-doc
            ;;
            "Docker")
            if ! command -v docker &> /dev/null; then sudo apt update && sudo apt install -y docker.io; fi
            if sudo docker ps -a --format '{{.Names}}' | grep -Eq "^apache-container$"; then
                echo "El contenedor 'apache-container' ya existe."
            else
                cat <<EOF > Dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y apache2
CMD ["apachectl", "-D", "FOREGROUND"]
EOF
                sudo docker build -t apache-asir . && sudo docker run -d -p 80:80 --name apache-container apache-asir
            fi
            ;;
            "Salir")
            ;;
            *)
                echo "El valor no es valido"
            ;;
        esac
    ;;
    "Borrar")
        sudo apt remove apache2 apache2-doc && sudo apt autoremove
        sudo docker stop apache-container 2>/dev/null && sudo docker rm apache-container 2>/dev/null
        sudo docker rmi apache-asir 2>/dev/null
    ;;
    "Correr")
        sudo systemctl start apache2
    ;;
    "Parada")
        sudo systemctl stop apache2
    ;;
    "Logs")
        read -p " Opciones de logs:
        - Mostrar logs por fecha (Escriba: Fecha)
        - Mostrar logs por tipo (Escriba: Tipo)
        - Por IP (Escriba: IP)
        - Tiempo real (Escriba: Tiempo)
        - Salir (Escriba: Salir)
        Elija que opcion de logs quiere: " MenuLog
        case $MenuLog in
            "Fecha")
                read -p "Elija de que fecha quiere ver los logs(YYYY-MM-DD):" Fecha
                journalctl -u apache2 --since "$Fecha 00:00:00" --until "$Fecha 23:59:59"
            ;;
            "Tipo")
                read -p "Elija el nivel de detalle:
                - Errores críticos (Escriba: Error)
                - Avisos y advertencias (Escriba: Alerta)
                - Todo el historial (Escriba: Info)
                Seleccione tipo: " TipoLog

                case $TipoLog in
                    "Error")
                        # Nivel 3: Errores que impiden el funcionamiento
                        journalctl -u apache2 -p 3 -b
                    ;;
                    "Alerta")
                        # Nivel 4: Advertencias (warnings)
                        journalctl -u apache2 -p 4 -b
                    ;;
                    "Info")
                        # Muestra todo el log del arranque actual
                        journalctl -u apache2 -b
                    ;;
                    "Salir")
                    ;;
                    *)
                        echo "Tipo no reconocido, mostrando errores por defecto."
                         journalctl -u apache2 -p 3
                    ;;
                esac
            ;;
            "IP")
                read -p "Escriba que IP quiere buscar en los logs: "
                journalctl -u apache2 | grep "$IpBusqueda"
            ;;
            "Tiempo real")
                sudo journalctl -u apache2 -f
            ;;
        esac
    ;;
    "Salir")
    echo "Adios"
    ;;
    *)
        echo "El valor insertado no es valido"
    ;;
esac
done
if [ "$#" != "0" ];then
#!/bin/bash

if [ "$1" == "-install" ];then
 if [ "$2" == "-c" ];then
  sudo apt install apache2 apache2-doc
  elif [ "$2" == "-d" ];then
   if ! command -v docker &> /dev/null; then sudo apt update && sudo apt install -y docker.io; fi
   if sudo docker ps -a --format '{{.Names}}' | grep -Eq "^apache-container$"; then
       echo "El contenedor 'apache-container' ya existe."
   else
       cat <<EOF > Dockerfile
FROM ubuntu:22.04
RUN apt-get update && apt-get install -y apache2
CMD ["apachectl", "-D", "FOREGROUND"]
EOF
       sudo docker build -t apache-asir . && sudo docker run -d -p 80:80 --name apache-container apache-asir
   fi
 elif [ -z "$2" ];then
  echo "Por favor escoja una opción, consulte --help"
 else
  echo "Esa opción no es válida, si necesita ayuda utilice --help al ejecutar el programa"
 fi
elif [ "$1" == "-delete" ];then
 sudo apt remove apache2 apache2-doc && sudo apt autoremove
 sudo docker stop apache-container 2>/dev/null && sudo docker rm apache-container 2>/dev/null
 sudo docker rmi apache-asir 2>/dev/null
elif [ "$1" == "-start" ];then
 sudo systemctl start apache2
elif [ "$1" == "-stop" ];then
 sudo systemctl stop apache2
elif [ "$1" == "-logs" ];then
 case $2 in
  "-f")
   if [ -z "$3" ];then
    echo "Por favor escoja una fecha (YYYY-MM-DD)"
   else
    journalctl -u apache2 --since "$3 00:00:00" --until "$3 23:59:59"
   fi
   ;;
  "-t")
   echo "Elija el nivel de detalle:"
   echo "- Errores críticos (-logs -t -e)"
   echo "- Avisos y advertencias (-logs -t -a)"
   echo "- Todo el historial (-logs -t -i)"
   case $3 in
    "-e")
     # Nivel 3: Errores que impiden el funcionamiento
     journalctl -u apache2 -p 3 -b
     ;;
    "-a")
     # Nivel 4: Advertencias (warnings)
     journalctl -u apache2 -p 4 -b
     ;;
    "-i")
     # Muestra todo el log del arranque actual
     journalctl -u apache2 -b
     ;;
    *)
     echo "Tipo no reconocido, mostrando errores por defecto."
     journalctl -u apache2 -p 3
     ;;
   esac
   ;;
  "-ip")
   journalctl -u apache2 | grep "$3"
   ;;
  "-rt")
   sudo journalctl -u apache2 -f
   ;;
  *)
   echo "Esa opción no es válida, si necesita ayuda utilice --help al ejecutar el programa"
   ;;
 esac
elif [ "$1" == "--help" ];then
 echo "------------------------------------------------------------------------------------"
 echo "-install Instalación del servicio con comandos (-install -c) o Docker (-install -d)"
 echo "------------------------------------------------------------------------------------"
 echo "-delete Eliminación del servicio"
 echo "------------------------------------------------------------------------------------"
 echo "-start Puesta en marcha"
 echo "------------------------------------------------------------------------------------"
 echo "-stop Parada"
 echo "------------------------------------------------------------------------------------"
 echo "-logs Consultar logs:"
 echo "-f por fecha"
 echo "-t por tipo"
 echo "-ip por IP"
 echo "-rt en tiempo real"
 echo "Incluir la fecha(YYYY-MM-DD), el tipo o la IP como tercer parámetro"
 echo "------------------------------------------------------------------------------------"
 elif [ -z "$1" ];then
  echo "Por favor escoja una opción, consulte --help"
else
echo ""
echo "Esa opción no es válida, si necesita ayuda utilice --help al ejecutar el programa"
echo ""
fi
fi
