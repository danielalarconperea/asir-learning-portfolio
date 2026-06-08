pip install flask

git init
git add .
git commit -m "Initial commit"



# Creación de un proyecto web
# Para crear una aplicación web de inicio, usamos el marco aplicación web de Flask.

# Ejecute los comandos siguientes en Azure Cloud Shell para configurar un entorno virtual e instalar Flask en el perfil:

# Bash

python3 -m venv venv
source venv/bin/activate
pip install flask

# Ejecute estos comandos para crear y cambiar al nuevo directorio de la aplicación web:

# Bash

mkdir ~/BestBikeApp
cd ~/BestBikeApp

# Cree un archivo denominado application.py con una respuesta HTML básica:

# Bash

cat >application.py <<EOL
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "<html><body><h1>Hello Best Bike App!</h1></body></html>\n"
EOL

# Para implementar la aplicación en Azure, debe guardar la lista de requisitos de la aplicación que ha realizado en un archivo requirements.txt. Para ello, ejecute el comando siguiente:

# Bash

pip freeze > requirements.txt
Prueba opcional de la aplicación web

# Puede probar la aplicación localmente en Azure mientras se ejecuta.

# Ejecute los comandos siguientes para iniciar la aplicación web en segundo plano:

# Bash

cd ~/BestBikeApp
export FLASK_APP=application.py
flask run &

# Debería obtener una salida como en el siguiente ejemplo:

# Consola
[1] <process-number>
 * Serving Flask app 'application.py'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
Press CTRL+C to quit
# En la salida, tome nota del valor de <process-number>. Dado que el proceso se ejecuta en segundo plano, no se puede salir con CTRL+C. Deberá detenerlo con su número de proceso.

# Ejecute el siguiente comando para ir a la aplicación web.

# Bash

curl -kL http://localhost:5000/

# Debería obtener la siguiente salida HTML:

# HTML
<html><body><h1>Hello Best Bike App!</h1></body></html>
# Mediante el valor de <process-number> que anotó anteriormente, detenga Flask:

# Azure CLI

kill <process-number>

# Implementación con az webapp up
# A continuación se implementará la aplicación Python con az webapp up. Este comando empaquetará la aplicación y la enviará a la instancia de App Service, donde se compila e implementa.

# En primer lugar, es necesario recopilar información sobre el recurso de aplicación web. Ejecute estos comandos para establecer variables de shell que contengan el nombre de la aplicación, el nombre del grupo de recursos, el nombre del plan, la SKU y la ubicación. Usan otros comandos de az para solicitar la información de Azure; az webapp up necesita estos valores para dirigirse a la aplicación web existente.

# Bash

export APPNAME=$(az webapp list --query [0].name --output tsv)
export APPRG=$(az webapp list --query [0].resourceGroup --output tsv)
export APPPLAN=$(az appservice plan list --query [0].name --output tsv)
export APPSKU=$(az appservice plan list --query [0].sku.name --output tsv)
export APPLOCATION=$(az appservice plan list --query [0].location --output tsv)

# Ahora, ejecute az webapp up con los valores adecuados. Asegúrese de que está en el directorio BestBikeApp antes de ejecutar este comando.

# Bash

cd ~/BestBikeApp
az webapp up --name $APPNAME --resource-group $APPRG --plan $APPPLAN --sku $APPSKU --location "$APPLOCATION"

# La implementación tarda unos minutos, periodo durante el que obtendrá la salida de estado. Un código de estado 202 significa que la implementación se ha realizado correctamente.