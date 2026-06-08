# Clase en vídeo: https://youtu.be/TbcEqkabAWU?t=15524

### File Handling ###

import os  # Importa el módulo os para interactuar con el sistema operativo

# Abrir un Archivo
# Se utiliza la función open(). Aquí, 'modo' puede ser:
# 'r': Leer (read), el archivo debe existir.
# 'w': Escribir (write), crea un archivo nuevo o sobrescribe si ya existe.
# 'a': Añadir (append), añade datos al final del archivo.
# 'b': Modo binario, útil para archivos no textuales (como imágenes).
file = open('nombre_del_archivo.txt', 'w')

# Escribir en el archivo
# Escribe texto en el archivo. Sobrescribe el contenido existente.
file.write('Hola, mundo!\n')
file.write('Otra línea.\n')

# Escribir múltiples líneas
# Escribe varias líneas en el archivo usando una lista de strings.
file.writelines(['Línea 1\n', 'Línea 2\n'])

# Cerrar el archivo
# Importante para liberar recursos y asegurar que los datos se guarden correctamente.
file.close()

# Usando 'with' para Manejo Automático
# Asegura que el archivo siempre se cierre, incluso si ocurre un error.
with open('nombre_del_archivo.txt', 'r') as file:
    contenido = file.read()  # Lee todo el contenido del archivo
    print(contenido)  # Imprime el contenido del archivo

# Otros métodos de lectura
# Lee una línea del archivo
with open('nombre_del_archivo.txt', 'r') as file:
    primera_linea = file.readline()
    print(f'Primera línea: {primera_linea}')

# Lee todas las líneas y devuelve una lista
with open('nombre_del_archivo.txt', 'r') as file:
    todas_las_lineas = file.readlines()
    print('Todas las líneas:', todas_las_lineas)

# Leer y escribir en modo binario
# Útil para archivos no textuales, como imágenes.
with open('imagen.jpg', 'rb') as file:
    datos_binarios = file.read()

with open('nueva_imagen.jpg', 'wb') as file:
    file.write(datos_binarios)

# Mover el puntero en el archivo
# Mueve el puntero al inicio del archivo
with open('nombre_del_archivo.txt', 'r') as file:
    file.seek(0)
    contenido = file.read(12)  # Lee las primeras 12 posiciones
    print(f'Primeras 12 posiciones: {contenido}')

# Obtener la posición actual del puntero
with open('nombre_del_archivo.txt', 'r') as file:
    file.seek(0)
    posicion_actual = file.tell()
    print(f'Posición actual del puntero: {posicion_actual}')

# Asegurar la Escritura en Disco
# flush() y os.fsync() aseguran que los datos se escriban físicamente en el disco.
with open('nombre_del_archivo.txt', 'w') as file:
    file.write('Texto importante')
    file.flush()  # Vacía el buffer interno
    os.fsync(file.fileno())  # Asegura la escritura en disco

# Ejemplo Completo que mezcla varias operaciones
with open('archivo.txt', 'w') as file:
    file.write('Primera línea.\n')
    file.write('Segunda línea.\n')

with open('archivo.txt', 'r') as file:
    for linea in file:
        print(linea, end='')  # end='' evita una nueva línea adicional

with open('archivo.txt', 'a') as file:
    file.write('Añadido al final.\n')

# Comprobar si el archivo existe y borrarlo
if os.path.exists('archivo.txt'):
    os.remove('archivo.txt')
    print('Archivo "archivo.txt" eliminado.')

if os.path.exists('nueva_imagen.jpg'):
    os.remove('nueva_imagen.jpg')
    print('Archivo "nueva_imagen.jpg" eliminado.')





import os  # Importa el módulo os para interactuar con el sistema operativo
import xml.etree.ElementTree as ET  # Importa el módulo xml y lo asigna a ET para facilidad de uso

# Crear y escribir un documento XML

# Crear el elemento raíz
# Este es el elemento principal del documento XML.
root = ET.Element('root')

# Añadir subelementos con texto
# child1 y child2 son subelementos de root. Puedes añadir tantos como necesites.
child1 = ET.SubElement(root, 'child1')
child1.text = 'Este es el primer hijo'

child2 = ET.SubElement(root, 'child2')
child2.text = 'Este es el segundo hijo'

# Generar el árbol XML
# Esto convierte la estructura de elementos en un árbol XML que puede ser guardado.
tree = ET.ElementTree(root)

# Guardar el documento XML en un archivo
# Este comando escribe el árbol XML en un archivo llamado 'archivo.xml'.
tree.write('archivo.xml')

# Leer y parsear un documento XML

# Parsear el archivo XML
# Este comando lee y analiza (parsea) el archivo XML.
tree = ET.parse('archivo.xml')
root = tree.getroot()  # Obtiene el elemento raíz del documento XML.

# Iterar sobre los elementos y mostrar su contenido
# Recorre todos los hijos del elemento raíz y muestra su etiqueta (tag) y texto.
for child in root:
    print(f'Elemento: {child.tag}, Texto: {child.text}')

# Modificar un documento XML

# Modificar el texto de un elemento
# Cambia el texto del primer subelemento de root.
root[0].text = 'Texto modificado'

# Añadir un atributo a un elemento
# Añade un atributo llamado 'atributo' con el valor 'valor' al primer subelemento de root.
root[0].set('atributo', 'valor')

# Guardar los cambios en el documento XML
# Escribe los cambios en un nuevo archivo llamado 'archivo_modificado.xml'.
tree.write('archivo_modificado.xml')

# Validar la existencia de los archivos y eliminarlos si existen
# Comprueba si los archivos 'archivo.xml' y 'archivo_modificado.xml' existen y los elimina.
if os.path.exists('archivo.xml'):
    os.remove('archivo.xml')
    print('Archivo "archivo.xml" eliminado.')

if os.path.exists('archivo_modificado.xml'):
    os.remove('archivo_modificado.xml')
    print('Archivo "archivo_modificado.xml" eliminado.')





import csv  # Importa el módulo csv para trabajar con archivos CSV

# Crear y escribir en un archivo CSV

# Definir los encabezados y filas de datos
encabezados = ['Nombre', 'Edad', 'Ciudad']
datos = [
    ['Juan', 28, 'Madrid'],
    ['Ana', 22, 'Barcelona'],
    ['Luis', 35, 'Valencia']
]

# Escribir los datos en un archivo CSV
# 'w' modo de escritura, se crea un archivo nuevo o sobrescribe si ya existe
with open('archivo.csv', 'w', newline='') as archivo_csv:
    writer = csv.writer(archivo_csv)  # Crea un objeto writer
    writer.writerow(encabezados)  # Escribe los encabezados
    writer.writerows(datos)  # Escribe las filas de datos

# Leer un archivo CSV

# Leer el archivo CSV y mostrar su contenido
with open('archivo.csv', 'r') as archivo_csv:
    reader = csv.reader(archivo_csv)  # Crea un objeto reader
    encabezados = next(reader)  # Lee los encabezados
    print(f'Encabezados: {encabezados}')
    for fila in reader:
        print(f'Fila: {fila}')

# Escribir en un archivo CSV usando diccionarios

# Definir los datos como una lista de diccionarios
datos_dict = [
    {'Nombre': 'Juan', 'Edad': 28, 'Ciudad': 'Madrid'},
    {'Nombre': 'Ana', 'Edad': 22, 'Ciudad': 'Barcelona'},
    {'Nombre': 'Luis', 'Edad': 35, 'Ciudad': 'Valencia'}
]

# Escribir los datos en un archivo CSV usando DictWriter
with open('archivo_dict.csv', 'w', newline='') as archivo_csv:
    writer = csv.DictWriter(archivo_csv, fieldnames=encabezados)
    writer.writeheader()  # Escribe los encabezados
    writer.writerows(datos_dict)  # Escribe las filas de datos

# Leer un archivo CSV usando diccionarios

# Leer el archivo CSV y mostrar su contenido
with open('archivo_dict.csv', 'r') as archivo_csv:
    reader = csv.DictReader(archivo_csv)  # Crea un objeto DictReader
    for fila in reader:
        print(f'Fila dict: {fila}')

# Asegurarse de eliminar los archivos creados después de usarlos
# Verifica si los archivos existen y los elimina
if os.path.exists('archivo.csv'):
    os.remove('archivo.csv')
    print('Archivo "archivo.csv" eliminado.')

if os.path.exists('archivo_dict.csv'):
    os.remove('archivo_dict.csv')
    print('Archivo "archivo_dict.csv" eliminado.')






import json  # Importa el módulo json para trabajar con datos JSON

# Crear un Objeto Python que Representa Datos JSON
# Un diccionario que contiene datos de ejemplo
datos = {
    "nombre": "Juan",
    "edad": 28,
    "ciudad": "Madrid",
    "hobbies": ["fútbol", "ajedrez", "lectura"]
}

# Convertir el Objeto Python a una Cadena JSON
# Usa json.dumps() para convertir el diccionario a una cadena JSON
json_string = json.dumps(datos, indent=4)  # 'indent' para una salida más legible
print("Cadena JSON:")
print(json_string)

# Escribir la Cadena JSON en un Archivo
# Abre el archivo en modo escritura ('w') y escribe la cadena JSON en él
with open('datos.json', 'w') as archivo_json:
    json.dump(datos, archivo_json, indent=4)  # 'indent' para una salida más legible en el archivo

# Leer Datos JSON desde un Archivo
# Abre el archivo en modo lectura ('r') y carga los datos JSON desde él
with open('datos.json', 'r') as archivo_json:
    datos_cargados = json.load(archivo_json)  # Convierte la cadena JSON del archivo a un diccionario
    print("\nDatos Cargados desde el Archivo:")
    print(datos_cargados)

# Convertir una Cadena JSON a un Objeto Python
# Usa json.loads() para convertir una cadena JSON a un diccionario Python
cadena_json = '{"nombre": "Ana", "edad": 22, "ciudad": "Barcelona"}'
objeto_python = json.loads(cadena_json)
print("\nObjeto Python desde Cadena JSON:")
print(objeto_python)

# Modificar un Objeto Python y Guardarlo como JSON
# Modifica el diccionario y luego guarda los cambios en un archivo JSON
objeto_python["edad"] = 23  # Modifica la edad
with open('datos_modificados.json', 'w') as archivo_json:
    json.dump(objeto_python, archivo_json, indent=4)

# Validar la Existencia de los Archivos y Eliminarlos
# Verifica si los archivos existen y los elimina
if os.path.exists('datos.json'):
    os.remove('datos.json')
    print('\nArchivo "datos.json" eliminado.')

if os.path.exists('datos_modificados.json'):
    os.remove('datos_modificados.json')
    print('Archivo "datos_modificados.json" eliminado.')







# 1. Abrir aplicaciones de Windows
os.system("start calc")          # Calculadora
os.system("start notepad")       # Bloc de notas
os.system("start mspaint")       # Paint
os.system("start write")         # WordPad
os.system("start explorer")      # Explorador de archivos

# 2. Abrir sitios web en el navegador predeterminado
os.system("start https://www.google.com")       # Abrir Google
os.system("start https://www.cualquierurl.com") # Abrir cualquier URL

# 3. Abrir archivos
os.system("start wordpad.exe C:\\ruta\\al\\archivo.docx")  # Abrir un documento de Word
os.system("start C:\\ruta\\al\\archivo.pdf")              # Abrir un archivo PDF
os.system("start C:\\ruta\\a\\la\\imagen.jpg")            # Abrir una imagen

# 4. Ejecutar comandos de CMD
os.system("dir")                  # Listar directorios
os.system("mkdir nuevo_directorio")  # Crear un directorio
os.system("del archivo.txt")      # Eliminar un archivo

# 5. Abrir programas instalados
os.system("start C:\\ruta\\al\\programa.exe")  # Abrir un programa específico

# 6. Abrir configuraciones de Windows
os.system("start control")              # Panel de control
os.system("start ms-settings:display")  # Configuración de pantalla
os.system("start ms-settings:network")  # Configuración de red

# 7. Abrir herramientas del sistema
os.system("start taskmgr")      # Administrador de tareas
os.system("start eventvwr")     # Visor de eventos
os.system("start devmgmt.msc")  # Administrador de dispositivos

# 8. Abrir consolas especializadas
os.system("start powershell")  # PowerShell
os.system("start wsl")         # Windows Subsystem for Linux (WSL)

# 9. Abrir aplicaciones de Microsoft Office
os.system("start excel")      # Excel
os.system("start winword")    # Word
os.system("start powerpnt")   # PowerPoint

# 10. Abrir aplicaciones de desarrollo
os.system("start code")       # Visual Studio Code
os.system("start git-bash")   # Git Bash

# Nota: Algunos comandos pueden requerir permisos de administrador o rutas específicas.
# Asegúrate de ajustar las rutas y comandos según tu sistema y necesidades.