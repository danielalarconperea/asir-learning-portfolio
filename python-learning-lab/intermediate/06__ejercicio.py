import os

# Escribir en el archivo
# Abre el archivo en modo escritura ('w'), si no existe, se crea uno nuevo. 
# Si existe, sobrescribe el contenido.
with open('ejemplo.txt', 'w') as file:
    file.write('Primera línea.\n')
    file.write('Segunda línea.\n')
    file.write('Tercera línea.\n')

# Leer el archivo completo
# Abre el archivo en modo lectura ('r') y lee todo el contenido.
with open('ejemplo.txt', 'r') as file:
    contenido = file.read()
    print('Contenido del archivo completo:')
    print(contenido)

# Leer línea por línea
# Abre el archivo en modo lectura ('r') y lee el archivo línea por línea.
with open('ejemplo.txt', 'r') as file:
    print('Leyendo línea por línea:')
    for linea in file:
        print(linea, end='')  # end='' evita que se añada una nueva línea extra

# Añadir más contenido al archivo
# Abre el archivo en modo añadir ('a') para agregar contenido al final sin borrar el existente.
with open('ejemplo.txt', 'a') as file:
    file.write('Añadido al final.\n')

# Leer las líneas como una lista
# Abre el archivo en modo lectura ('r') y usa readlines() para obtener una lista de todas las líneas.
with open('ejemplo.txt', 'r') as file:
    lineas = file.readlines()
    print('\nLíneas del archivo como lista:')
    print(lineas)

# Mover el puntero y leer una parte específica del archivo
# Abre el archivo en modo lectura ('r'), usa seek() para mover el puntero y lee 12 posiciones del archivo.
with open('ejemplo.txt', 'r') as file:
    file.seek(0)  # Mueve el puntero al inicio del archivo.
    print('Leer las primeras 12 posiciones del archivo:')
    print(file.read(12))

# Obtener el tamaño del archivo
# Utiliza getsize() para obtener el tamaño del archivo en bytes.
tamaño = os.path.getsize('ejemplo.txt')
print(f'\nTamaño del archivo: {tamaño} bytes')

# Leer y escribir en modo binario
# Abre un archivo en modo escritura binaria ('wb') y escribe datos binarios.
with open('ejemplo_binario.bin', 'wb') as file:
    file.write(b'This is binary data.')

# Abre el archivo en modo lectura binaria ('rb') y lee los datos binarios.
with open('ejemplo_binario.bin', 'rb') as file:
    datos_binarios = file.read()
    print('Datos binarios leídos del archivo:')
    print(datos_binarios)

# Comprobar si el archivo existe y borrarlo
# Utiliza os.path.exists() para comprobar si el archivo existe y os.remove() para borrarlo.
if os.path.exists('ejemplo.txt'):
    os.remove('ejemplo.txt')
    print('\nArchivo "ejemplo.txt" eliminado.')

if os.path.exists('ejemplo_binario.bin'):
    os.remove('ejemplo_binario.bin')
    print('Archivo "ejemplo_binario.bin" eliminado.')
