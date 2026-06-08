# Clase en vídeo: https://youtu.be/TbcEqkabAWU?t=19762

### Regular Expressions ###

import re  # Importa el módulo de expresiones regulares

#-------------------------------------------------------------------------
# match
# Las expresiones regulares permiten buscar patrones específicos dentro de cadenas de texto.

# Define dos cadenas de texto como ejemplos
my_string = "Esta es la lección número 7: Lección llamada Expresiones Regulares"
my_other_string = "Esta no es la lección número 6: Manejo de ficheros"

# re.match busca un patrón específico al comienzo de la cadena
# Busca si la cadena comienza con "Esta es la lección"
match = re.match("Esta es la lección", my_string, re.I)  # El parámetro re.I hace la búsqueda insensible a mayúsculas/minúsculas
print(match)  # Imprime el objeto de coincidencia si se encuentra el patrón
if match: #si hay match el if es igual a true
    start, end = match.span()  # Obtiene las posiciones inicial y final de la coincidencia
    print(my_string[start:end])  # Imprime la parte de la cadena que coincide

# Busca si la cadena comienza con "Esta no es la lección"
match = re.match("Esta no es la lección", my_other_string)
if match is not None:  # Comprueba si se encontró una coincidencia
    print(match)
    start, end = match.span()
    print(my_other_string[start:end])

# Intenta encontrar "Expresiones Regulares" al inicio de la cadena (fallará porque no está al inicio)
print(re.match("Expresiones Regulares", my_string))

#-------------------------------------------------------------------------
# search
# re.search busca el patrón en cualquier parte de la cadena, no solo al inicio
search = re.search("lección", my_string, re.I)  # Busca "lección" en cualquier lugar de la cadena
print(search)  # Imprime el objeto de búsqueda si se encuentra el patrón
if search:
    start, end = search.span()  # Obtiene las posiciones inicial y final de la coincidencia
    print(my_string[start:end])  # Imprime la parte de la cadena que coincide

# Define el patrón de búsqueda (por ejemplo, "número") 
pattern = "número" 
# Realiza la búsqueda en la cadena de texto 
search = re.search(pattern, my_string) 
# Verifica si se encontró una coincidencia y, si es así, imprime la coincidencia 
if search: 
    print('Coincidencia encontrada:', search.group())  
else: 
    print('No se encontró coincidencia')

# SUBGRUPOS
my_string = "Fecha: 2024-11-08" 
pattern = r"(\d{4})-(\d{2})-(\d{2})" 
search = re.search(pattern, my_string) 
if search: 
    print("Fecha completa:", search.group()) # Toda la coincidencia 
    print("Año:", search.group(1)) # Primer subgrupo (año) 
    print("Mes:", search.group(2)) # Segundo subgrupo (mes) 
    print("Día:", search.group(3)) # Tercer subgrupo (día)

#-------------------------------------------------------------------------
my_string = "Esta es la lección número 7: Lección llamada Expresiones Regulares"
# findall
# re.findall busca todas las coincidencias de un patrón y las devuelve en una lista
resultados = re.findall("lección", my_string, re.I)  # Encuentra todas las apariciones de "lección"
print(resultados)  # Imprime todas las coincidencias encontradas

my_string = "Hoy es 2024-11-08. Mañana será 2024-11-09." # Cadena de texto en la que vamos a buscar 
pattern = r"\d{4}-\d{2}-\d{2}" # Patrón de búsqueda para encontrar todas las fechas en formato AAAA-MM-DD
resultados = re.findall(pattern, my_string) # Usamos findall para encontrar todas las coincidencias del patrón 
print(resultados) # Imprimimos la lista de coincidencias encontradas 

#-------------------------------------------------------------------------
# split______str.split(separator, maxsplit)
# re.split divide una cadena en una lista usando un patrón como delimitador
print(re.split(":", my_string))  # Divide la cadena donde aparece ":"

# Definición de varias cadenas de texto para los ejemplos
basic_string = "manzana, pera, plátano, uva"
delimiter_string = "manzana|pera|plátano|uva"
maxsplit_string = "manzana, pera, plátano, uva"
regex_string = "manzana1pera2plátano3uva"
mixed_delimiters_string = "manzana;pera|plátano,uvas"

# 1. Uso básico de split con coma y espacio como delimitador
basic_result = basic_string.split(", ")
print("Uso básico de split:", basic_result)

# 2. Uso de split con un delimitador diferente
delimiter_result = delimiter_string.split("|")
print("Uso de split con diferente delimitador:", delimiter_result)

# 3. Uso de split con maxsplit para limitar el número de divisiones
maxsplit_result = maxsplit_string.split(", ", 2)
print("Uso de split con maxsplit:", maxsplit_result)

# 4. Uso de re.split con expresión regular para dividir por dígitos
regex_result = re.split(r'\d', regex_string)
print("Uso de re.split con expresión regular:", regex_result)

# 5. Uso de re.split con expresión regular para dividir por múltiples delimitadores
mixed_delimiters_result = re.split(r'[;|,]', mixed_delimiters_string)
print("Uso de re.split con múltiples delimitadores:", mixed_delimiters_result)

#-------------------------------------------------------------------------
my_string = "Esta es la lección número 7: Lección llamada Expresiones Regulares"
# sub________re.sub(pattern, repl, string, count=0, flags=0)
'''
pattern: El patrón de expresión regular que se busca.
repl: La cadena con la que se reemplazará cada coincidencia del patrón.
string: La cadena de texto en la que se buscan las coincidencias.
count: (Opcional) El número máximo de sustituciones. Por defecto es 0, lo que significa que se reemplazarán todas las coincidencias.
flags: (Opcional) Modificadores como re.I para ignorar mayúsculas/minúsculas.'''
# re.sub sustituye todas las apariciones de un patrón por otra cadena
print(re.sub("[l|L]ección", "LECCIÓN", my_string))  # Reemplaza "lección" o "Lección" por "LECCIÓN"
print(re.sub("Expresiones Regulares", "RegEx", my_string))  # Reemplaza "Expresiones Regulares" por "RegEx"

# Cadena de texto original
my_string = "Hola mundo! Este es un ejemplo de mundo!"
pattern = "mundo" # Patrón a buscar 
repl = "universo" # Cadena de reemplazo
resultado = re.sub(pattern, repl, my_string)# Realizar la sustitución
print(resultado)

my_string = "Hola mundo! Este es un ejemplo de mundo!" 
pattern = "mundo" 
repl = "universo" 
resultado = re.sub(pattern, repl, my_string, count=1) # Realizar la sustitución, limitando a 1 sustitución 
print(resultado)

# Cadena de texto original
my_string = "La fecha es 2024-11-08."

# Patrón para buscar fechas en formato AAAA-MM-DD y reemplazarlas con un formato más legible
pattern = r"(\d{4})-(\d{2})-(\d{2})"
repl = r"\3/\2/\1"  # Reemplazar con formato DD/MM/AAAA-----usa los subgrupos capturados para reordenar la fecha en formato DD/MM/AAAA.
resultado = re.sub(pattern, repl, my_string)
print(resultado)


# Validación de un correo electrónico utilizando una expresión regular
correo = "example@dominio.com"
if re.match(r'^[\w.-]+@[\w.-]+\.[a-zA-Z]{2,6}$', correo):  # Patrón para validar la estructura de un correo electrónico
    print("Correo válido")
else:
    print("Correo inválido")

# Clase en vídeo (09/11/22): https://www.twitch.tv/videos/1648023317

### Patrones de Expresiones Regulares ###

# Para aprender y validar expresiones regulares: https://regex101.com

# Define la cadena de texto
my_string = "Esta es la lección número 7: Lección llamada Expresiones Regulares. Tel: 123-456-7890, Email: example@dominio.com, Código postal: 28001."

# Encuentra "lección" o "Lección"
pattern = r"[lL]ección"
print(re.findall(pattern, my_string))  # ['lección', 'Lección']

# Encuentra "lección", "Lección" o "Expresiones"
pattern = r"[lL]ección|Expresiones"
print(re.findall(pattern, my_string))  # ['lección', 'Lección', 'Expresiones']

# Encuentra todos los dígitos (números)
pattern = r"[0-9]"
print(re.findall(pattern, my_string))  # ['7', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '2', '8', '0', '0', '1']

# Encuentra todos los dígitos, equivalente a [0-9]
pattern = r"\d"
print(re.findall(pattern, my_string))  # ['7', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '2', '8', '0', '0', '1']

# Encuentra todos los caracteres que no son dígitos
pattern = r"\D"
print(re.findall(pattern, my_string))  # Todos los caracteres que no son dígitos

# Encuentra "l" seguido de cualquier cosa hasta el final de la línea
pattern = r"[l].*"
print(re.findall(pattern, my_string))  # ['la lección número 7: Lección llamada Expresiones Regulares. Tel: 123-456-7890, Email: example@dominio.com, Código postal: 28001.']

# Encuentra todas las palabras (secuencias de caracteres alfanuméricos)
pattern = r"\w+"
print(re.findall(pattern, my_string))  # ['Esta', 'es', 'la', 'lección', 'número', '7', 'Lección', 'llamada', 'Expresiones', 'Regulares', 'Tel', '123', '456', '7890', 'Email', 'example', 'dominio', 'com', 'Código', 'postal', '28001']

# Encuentra todas las secuencias de caracteres no alfanuméricos (espacios, puntuación, etc.)
pattern = r"\W+"
print(re.findall(pattern, my_string))  # [' ', ' ', ' ', ' ', ' ', ' ', ': ', ' ', ' ', ' ', '. ', ' ', ': ', '-', '-', ', ', ': ', '@', '.', ', ', ' ', ': ', '.']

# Encuentra todas las letras minúsculas
pattern = r"[a-z]"
print(re.findall(pattern, my_string))  # Todas las letras minúsculas

# Encuentra todas las letras mayúsculas
pattern = r"[A-Z]"
print(re.findall(pattern, my_string))  # Todas las letras mayúsculas

# Encuentra todas las letras, sin importar si son mayúsculas o minúsculas
pattern = r"[a-zA-Z]"
print(re.findall(pattern, my_string))  # Todas las letras

# Encuentra todos los espacios en blanco (espacios, tabulaciones, saltos de línea)
pattern = r"\s"
print(re.findall(pattern, my_string))  # [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']

# Encuentra todas las secuencias de caracteres que no son espacios en blanco
pattern = r"\S"
print(re.findall(pattern, my_string))  # Todos los caracteres que no son espacios

# Encuentra todas las palabras que empiezan con una letra mayúscula
pattern = r"\b[A-Z][a-z]*\b"
print(re.findall(pattern, my_string))  # ['Esta', 'Lección', 'Expresiones', 'Regulares', 'Tel', 'Email', 'Código']

# Encuentra direcciones de correo electrónico
pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
print(re.findall(pattern, my_string))  # ['example@dominio.com']

# Encuentra números de teléfono en formato XXX-XXX-XXXX
pattern = r"\b\d{3}-\d{3}-\d{4}\b"
print(re.findall(pattern, my_string))  # ['123-456-7890']

# Encuentra fechas en formato AAAA-MM-DD
pattern = r"\b\d{4}-\d{2}-\d{2}\b"
print(re.findall(pattern, my_string))  # ['2024-11-08']


# Validación de un correo electrónico más complejo
email = "mouredev@mouredev.com"
pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z-.]+$"
print(re.match(pattern, email))  # Comprueba si el correo cumple con el patrón
print(re.search(pattern, email))  # Busca el patrón en el correo
print(re.findall(pattern, email))  # Encuentra todas las coincidencias en el correo

email = "mouredev@mouredev.com.mx"
print(re.findall(pattern, email))  # Valida correos con subdominios (ej: .com.mx)

'''
Funciones Principales del Módulo re:
re.compile(pattern, flags=0):
    Compila un patrón de expresión regular en un objeto de expresión regular, que puede ser utilizado para hacer búsquedas más eficientes.

re.match(pattern, string, flags=0):
    Busca una coincidencia del patrón al comienzo de la cadena.

re.search(pattern, string, flags=0):
    Busca la primera ubicación donde el patrón coincide con la cadena.

re.findall(pattern, string, flags=0):
    Encuentra todas las coincidencias del patrón en la cadena y las devuelve como una lista.

re.finditer(pattern, string, flags=0):
    Encuentra todas las coincidencias del patrón en la cadena y las devuelve como un iterador de objetos de coincidencia.

re.fullmatch(pattern, string, flags=0):
    Busca una coincidencia del patrón en toda la cadena.

re.split(pattern, string, maxsplit=0, flags=0):
    Divide la cadena por las ocurrencias del patrón.

re.sub(pattern, repl, string, count=0, flags=0):
    Sustituye las ocurrencias del patrón en la cadena con la cadena repl.

re.subn(pattern, repl, string, count=0, flags=0):
    Sustituye las ocurrencias del patrón en la cadena con la cadena repl y devuelve una tupla (cadena, número de sustituciones).

Métodos de los Objetos de Expresión Regular:
pattern.match(string, pos=0, endpos=9223372036854775807):
    Busca una coincidencia del patrón al comienzo de la cadena dentro de un rango de posiciones.

pattern.search(string, pos=0, endpos=9223372036854775807):
    Busca la primera ubicación donde el patrón coincide con la cadena dentro de un rango de posiciones.

pattern.findall(string, pos=0, endpos=9223372036854775807):
    Encuentra todas las coincidencias del patrón en la cadena dentro de un rango de posiciones.

pattern.finditer(string, pos=0, endpos=9223372036854775807):
    Encuentra todas las coincidencias del patrón en la cadena y las devuelve como un iterador de objetos de coincidencia.

pattern.fullmatch(string, pos=0, endpos=9223372036854775807):
    Busca una coincidencia del patrón en toda la cadena dentro de un rango de posiciones.

pattern.split(string, maxsplit=0):
    Divide la cadena por las ocurrencias del patrón.

pattern.sub(repl, string, count=0):
    Sustituye las ocurrencias del patrón en la cadena con la cadena repl.

pattern.subn(repl, string, count=0):
    Sustituye las ocurrencias del patrón en la cadena con la cadena repl y devuelve una tupla (cadena, número de sustituciones).

Métodos de los Objetos de Coincidencia (Match Objects):
match.group([group1, ...]):
    Devuelve una o más subgrupos de la coincidencia.

match.groups(default=None):
    Devuelve todas las subgrupos de la coincidencia como una tupla.

match.groupdict(default=None):
    Devuelve un diccionario que contiene todos los grupos nombrados.

match.start([group]):
    Devuelve la posición inicial del grupo de la coincidencia.

match.end([group]):
    Devuelve la posición final del grupo de la coincidencia.

match.span([group]):
    Devuelve una tupla (start, end) de la posición del grupo de la coincidencia.

match.pos:
    La posición en la cadena donde comenzó la búsqueda de coincidencias.

match.endpos:
    La posición en la cadena donde terminó la búsqueda de coincidencias.

match.lastindex:
    El índice del último grupo de coincidencias.

match.lastgroup:
    El nombre del último grupo de coincidencias.

match.re:
    El objeto de expresión regular utilizado para hacer la coincidencia.

match.string:
    La cadena que se estaba buscando.
'''