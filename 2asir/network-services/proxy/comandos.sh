### **1. Gestión del Servicio Squid**

# Instalar el servicio Squid: 
sudo apt-get install squid 


# Comprobar el estado del servicio: 
sudo service squid status 


# Editar el fichero de configuración principal: 
sudo nano /etc/squid/squid.conf 


# Reiniciar el servicio para aplicar cambios: 
sudo service squid restart



### **2. Configuración de Autenticación Básica**

# Para habilitar el acceso mediante usuario y contraseña en el proxy.

# Instalar herramientas de apache2-utils: 
sudo apt-get install apache2-utils 


# Crear el archivo de contraseñas: 
sudo touch /etc/squid/passwd 


# Cambiar la propiedad del archivo al usuario proxy: 
sudo chown proxy: /etc/squid/passwd 


# Agregar un nuevo usuario (ejemplo: usuario1): 
sudo htpasswd /etc/squid/passwd usuario1 



### **3. Instalación de SquidAnalyzer**

Pasos para descargar, compilar e instalar la herramienta de análisis de logs.

# Instalar el servidor web Nginx: 
sudo apt-get install nginx 


# Descargar el paquete de SquidAnalyzer: 
wget https://www.sysadminsdecuba.com/wp-content/uploads/2020/09/squidanalyzer-6.6.tar.gz 


# Extraer el contenido del archivo comprimido: 
tar xvf squidanalyzer-6.6.tar.gz 


# Acceder al directorio extraído: 
cd squidanalyzer-6.6/ 


# Crear carpeta para los archivos HTML generados: 
sudo mkdir /var/www/squidanalyzer 


# Configurar la instalación personalizada (Perl): 
sudo perl Makefile.PL LOGFILE=/var/log/squid/access.log BINDIR=/usr/bin CONFDIR=/etc HTMLDIR=/var/www/squidanalyzer BASEURL=/ MANDIR=/usr/man/man3 DOCDIR=/usr/share/doc/squidanalyzer


# Instalar la herramienta make: 
sudo apt install make 


# Compilar la aplicación: 
sudo make 


# Finalizar la instalación: 
sudo make install



### **4. Automatización y Configuración Web (Nginx)**

# Para programar los informes y habilitar el acceso web a las estadísticas.

# Configurar tarea Cron para generar estadísticas diarias: 
echo "0 2 * * * /usr/local/bin/squid-analyzer > /dev/null 2>&1" | crontab - 


# Eliminar sitios por defecto en Nginx: 
sudo rm /etc/nginx/sites-available/default && sudo rm /etc/nginx/sites-enabled/default 


# Crear nueva configuración para SquidAnalyzer: 
sudo nano /etc/nginx/sites-available/squid-analyzer 


# Validar la sintaxis de configuración de Nginx: 
sudo nginx -t 


# Reiniciar el servicio Nginx: 
sudo systemctl restart nginx.service 


# Crear ficheros externos
sudo touch /etc/squid/ip_sin_internet.txt
sudo touch /etc/squid/url_prohibidas.txt
sudo touch /etc/squid/lista_blanca.txt


# ACA VA LA CONFIGURACIÓN DEL FICHERO /etc/squid/squid.conf

# --- ACLs ---
acl solo_una_ip src 192.168.1.10
acl red_estudios src 192.168.2.0/24
acl rango_excluido src 192.168.1.50-192.168.1.60
acl lista_negra dstdomain "/etc/squid/url_prohibidas.txt"
acl lista_blanca dstdomain "/etc/squid/lista_blanca.txt"
acl archivos_css rep_mime_type text/css
acl archivos_jpg rep_mime_type image/jpeg
acl redes_sociales dstdomain .facebook.com .instagram.com .twitter.com .tiktok.com
acl descargas_exe urlpath_regex -i \.exe \.msi \.bin \.deb \.dmg
acl tipo_exe rep_mime_type application/octet-stream
acl tipo_exe_msdos rep_mime_type application/x-msdos-program
acl anuncios_tracking dstdomain .doubleclick.net .adscore.com .google-analytics.com .zedo.com
acl puertos_web port 80 443
acl protocolo_ftp proto FTP
acl archivos_js rep_mime_type application/javascript application/x-javascript
acl navegadores_moviles browser -i mobile android iphone blackberry
acl multimedia urlpath_regex -i \.mp3$ \.mp4$ \.avi$ \.wav$ \.mov$
acl metodo_post method POST
acl imagenes_pesadas rep_mime_type image/png image/gif

# --- Aplicación de Reglas ---

# A. SEGURIDAD Y PUERTOS
http_access deny !puertos_web        
http_access deny protocolo_ftp       

# B. BLOQUEOS POR ORIGEN
http_access deny rango_excluido      

# C. BLOQUEOS DE CONTENIDO
http_access deny lista_negra         
http_access deny redes_sociales      
http_access deny anuncios_tracking   

# D. BLOQUEOS DE ARCHIVOS Y RECURSOS
http_access deny descargas_exe       
http_reply_access deny tipo_exe      
http_reply_access deny tipo_exe_msdos 
http_access deny multimedia          
http_reply_access deny imagenes_pesadas    
http_access deny navegadores_moviles 
http_reply_access deny archivos_css  
http_reply_access deny archivos_js   

# E. LÍMITES TÉCNICOS Y MÉTODOS
http_access deny metodo_post         

# F. PERMISOS
http_access allow lista_blanca       
http_access allow solo_una_ip        
http_access allow red_estudios       

# G. POLÍTICA FINAL
http_access allow all


## Rellenar ficheros externos con ejemplos

# Rellenar URLs prohibidas (Lista Negra)
echo -e ".poker.com\n.bet365.com\n.juegos.com\n.instagram.com\n.tiktok.com" | sudo tee /etc/squid/url_prohibidas.txt

# Aplicar cambios en Squid
sudo systemctl reload squid
