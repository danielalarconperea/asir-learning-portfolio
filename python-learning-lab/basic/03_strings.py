# Clase en vídeo: https://youtu.be/Kp4Mvapo5kc?t=8643

### Strings ###

my_string = "Mi String"
my_other_string = 'Mi otro String'

print(len(my_string))
print(len(my_other_string))
print(my_string + " " + my_other_string)

my_new_line_string = "Este es un String\ncon salto de línea"
print(my_new_line_string)

my_tab_string = "\tEste es un String con tabulación"
print(my_tab_string)


my_scape_string = "\\tEste es un String \\n escapado"
print(my_scape_string)

# Formateo

name, surname, age = "Brais", "Moure", 35
print("Mi nombre es {} {} y mi edad es {}".format(name, surname, age))
print("Mi nombre es %s %s y mi edad es %d" % (name, surname, age))
print("Mi nombre es " + name + " " + surname + " y mi edad es " + str(age))
print(f"Mi nombre es {name} {surname} y mi edad es {age}")

# Desempaqueado de caracteres

language = "python"
a, b, c, d, e, f = language
print(a)
print(e)

# División

language_slice = language[1:3]
print(language_slice) # yt -- toma una subcadena desde el índice 1 hasta el índice 2 (el índice final no se incluye)

language_slice = language[1:]
print(language_slice) # ython

language_slice = language[-2]
print(language_slice) # o -- toma el segundo carácter desde el final de la cadena

language_slice = language[0:6:2]
print(language_slice) # pto -- toma una subcadena desde el índice 0 hasta el índice 5 (el índice final no se incluye) saltando cada 2 caracteres

"""
La sintaxis general para el slicing es [start:stop:step]
0: Es el índice de inicio. Comienza desde el primer carácter de la cadena.
6: Es el índice de parada. Se detiene antes de llegar a este índice (no incluye el carácter en el índice 6).
2: Es el paso. Selecciona cada segundo carácter desde el inicio hasta el índice de parada.
"""
# Reverse

reversed_language = language[::-1]
print(reversed_language)

# Funciones del lenguaje

print(language.capitalize())
print(language.upper())
print(language.count("t"))
print(language.isnumeric()) #El método isnumeric() en Python se utiliza para verificar si todos los caracteres de una cadena son numéricos.
print("1".isnumeric())
print(language.isalnum())  #Te ayuda a asegurarte de que una cadena solo contenga caracteres alfabéticos o numéricos, sin espacios ni símbolos de puntuación.
print(language.lower())
print(language.lower().isupper()) #El método .isupper() en Python se utiliza para verificar si todos los caracteres alfabéticos de una cadena están en mayúsculas.
print(language.startswith("Py"))
print("Py" == "py")  # No es lo mismo

#----------------------------------------------------------------------------------------------------------
'''
Ejercicio 1: Informador de Cadenas
Objetivo: Crear un programa que analice una cadena de texto proporcionada por el usuario y muestre información sobre la misma.

Pide al usuario que introduzca una cadena de texto.

Muestra la longitud de la cadena.

Muestra la cadena en mayúsculas y minúsculas.

Muestra si la cadena comienza con una determinada subcadena (por ejemplo, "Hola").

Muestra el número de veces que aparece un carácter específico en la cadena (por ejemplo, la letra "a").
'''
def inf_cadenas(cadenas):
    print(len(cadenas))  # Correct usage of len
    print(cadenas.upper())  # Correct usage of upper
    print(cadenas.lower())  # Correct usage of lower
    
    # Check if the string starts with "Hola"
    if cadenas.startswith("Hola"):
        print('La cadena empieza por "Hola"')
    
    # Print the first character of the string
    print(cadenas.count('Hola'))

# Test the function
inf_cadenas('Hola buenas noches')

# Ejercicio 1: Informador de Cadenas

# Pedir al usuario que introduzca una cadena de texto
# my_string = input("Introduce una cadena de texto: ")

# Mostrar la longitud de la cadena
print(f"La longitud de la cadena es: {len(my_string)}")

# Mostrar la cadena en mayúsculas y minúsculas
print(f"En mayúsculas: {my_string.upper()}")
print(f"En minúsculas: {my_string.lower()}")

# Verificar si la cadena comienza con una subcadena específica
subcadena = "Hola"
print(f"¿Comienza con '{subcadena}'?: {my_string.startswith(subcadena)}")

# Contar el número de veces que aparece un carácter específico
caracter = "a"
print(f"El carácter '{caracter}' aparece {my_string.count(caracter)} veces")


'''
Ejercicio 2: Formateador de Información Personal
Objetivo: Crear un programa que solicite al usuario su nombre, apellido y edad, 
y luego muestre esta información formateada de varias maneras.

Pide al usuario que introduzca su nombre, apellido y edad.

Muestra la información combinada en una frase utilizando diferentes métodos de formateo.
'''

# nombre, apellido, edad=input('dime tu nombre:'), input('dime tu apellido:'), int(input('dime tu edad:'))
nombre='Moure'
apellido='Brais'
edad=3


print(f'Buenos días {nombre} como fue tu cumple nº{edad} con tu familia {apellido}')
print('Buenos días '+nombre+' como fue tu cumple nº'+str(edad)+' con tu familia '+apellido)
print('Buenos días %s como fue tu cumple nº%d con tu familia %s'%(nombre, edad, apellido))
print('Buenos días {} como fue tu cumple nº{} con tu familia {}'.format(nombre, edad, apellido))

# Diferentes tipos de formateo utilizando el operador % en Python

# Variables de ejemplo
nombre = "Brais"
apellido = "Moure"
edad = 35
altura = 1.75
numero_hex = 255

# %s - Formato de cadena (string)
print("Mi nombre es %s %s" % (nombre, apellido))  # Salida: Mi nombre es Brais Moure

# %d - Formato de entero (decimal)
print("Mi edad es %d" % edad)  # Salida: Mi edad es 35

# %f - Formato de número de punto flotante (float)
print("Mi altura es %.2f metros" % altura)  # Salida: Mi altura es 1.75 metros
# .2f indica que se mostrarán 2 decimales

# %x - Formato de número en hexadecimal (lowercase)
print("El número en hexadecimal es %x" % numero_hex)  # Salida: El número en hexadecimal es ff

# %X - Formato de número en hexadecimal (uppercase)
print("El número en hexadecimal es %X" % numero_hex)  # Salida: El número en hexadecimal es FF

# %o - Formato de número en octal
print("El número en octal es %o" % numero_hex)  # Salida: El número en octal es 377

# %e - Formato de notación científica (lowercase)
print("El número en notación científica es %e" % altura)  # Salida: El número en notación científica es 1.750000e+00

# %E - Formato de notación científica (uppercase)
print("El número en notación científica es %E" % altura)  # Salida: El número en notación científica es 1.750000E+00

# %% - Muestra un signo de porcentaje
print("El 100%% de los estudiantes aprobaron.")  # Salida: El 100% de los estudiantes aprobaron.

# Formato de múltiple sustitución
print("Mi nombre es %s %s, tengo %d años, mido %.2f metros y el número hexadecimal es %x" % (nombre, apellido, edad, altura, numero_hex))
# Salida: Mi nombre es Brais Moure, tengo 35 años, mido 1.75 metros y el número hexadecimal es ff

# %c: Formato de carácter único. Toma un entero o un string de longitud 1 y lo convierte a su carácter correspondiente.
print("El carácter ASCII de 65 es: %c" % 65)  # Salida: El carácter ASCII de 65 es: A
print("La inicial es: %c" % 'B')             # Salida: La inicial es: B

# %i: Formato de entero (similar a %d). Acepta enteros decimales, octales (con prefijo 0o) y hexadecimales (con prefijo 0x).
print("Entero: %i" % 42)          # Salida: Entero: 42
print("Entero desde octal: %i" % 0o52) # Salida: Entero desde octal: 42
print("Entero desde hex: %i" % 0x2a)   # Salida: Entero desde hex: 42

# %g: Formato general. Elige entre %f (punto fijo) y %e (notación científica con 'e' minúscula) según la magnitud del número para una representación más compacta.
num_grande = 123456789.0
num_pequeno = 0.0000123
print("Número grande (%g): %g" % (num_grande, num_grande))
# Salida: Número grande (%g): 1.23457e+08
print("Número pequeño (%g): %g" % (num_pequeno, num_pequeno))
# Salida: Número pequeño (%g): 1.23e-05
print("Número normal (%g): %g" % (altura, altura))
# Salida: Número normal (%g): 1.75

# %G: Formato general (similar a %g, pero usa %E - notación científica con 'E' mayúscula si es necesario).
print("Número grande (%G): %G" % (num_grande, num_grande))
# Salida: Número grande (%G): 1.23457E+08

# %r: Formato de representación (repr()). Llama a la función repr() del objeto. Útil para depuración.
mi_lista = [1, 2, 'hola']
print("La representación de la lista es: %r" % mi_lista)
# Salida: La representación de la lista es: [1, 2, 'hola']

# %a: Formato de representación ASCII (ascii()). Similar a %r pero escapa caracteres no ASCII. (Introducido en Python 3).
texto_unicode = "München"
print("Representación ASCII: %a" % texto_unicode)
# Salida: Representación ASCII: 'M\xfcnchen'



# max(iterable, *, key=None, default=None)
# max(arg1, arg2, *args, key=None)

# Con una lista de números
print(max([3, 7, 2, 9, 5]))  # Salida: 9

# Con múltiples argumentos
print(max(10, 5, 8))  # Salida: 10

# Con cadenas (alfabéticamente)
print(max("gato", "perro", "elefante"))  # Salida: perro

# Usando el parámetro key (por longitud de palabra)
print(max(["gato", "perro", "elefante"], key=len))  # Salida: elefante


# min(iterable, *, key=None, default=None)
# min(arg1, arg2, *args, key=None)

# Con una lista de números
print(min([3, 7, 2, 9, 5]))  # Salida: 2

# Con múltiples argumentos
print(min(10, 5, 8))  # Salida: 5

# Con cadenas (alfabéticamente)
print(min("gato", "perro", "elefante"))  # Salida: elefante

# Usando el parámetro key (por longitud de palabra)
print(min(["gato", "perro", "elefante"], key=len))  # Salida: gato

# print(max([]))  # Error: ValueError: max() arg is an empty sequence
# print(min([]))  # Error: ValueError: min() arg is an empty sequence

print(max([], default="No hay datos"))  # Salida: No hay datos

nombres = ["Ana", "Bruno", "Carlos", "Diana"]
print(max(nombres, key=lambda x: x[-1]))  # Ordena según la última letra






# 1. Relleno y Alineación:
'''
<: Alineación a la izquierda (predeterminado para la mayoría de objetos).

>: Alineación a la derecha (predeterminado para números).

^: Alineación centrada.

=: Fuerza a que el relleno se coloque después del signo (si lo hay) pero antes de los dígitos. Solo válido para tipos numéricos. Es útil con 0 para rellenar con ceros (ej. +00012).

[relleno]: Carácter a usar para rellenar el espacio (si se especifica ancho). Debe ir antes del especificador de alineación. Si se omite, se usa espacio.
'''
texto = "Hola"
print(f"'{texto:<10}'")  # Salida: 'Hola      '
print(f"'{texto:>10}'")  # Salida: '      Hola'
print(f"'{texto:^10}'")  # Salida: '   Hola   '
print(f"'{texto:*^10}'") # Salida: '***Hola***'
num = -123
print(f"'{num:=10}'")  # Salida: '-      123' (relleno con espacio)
print(f"'{num:0=10}'") # Salida: '-000000123' (relleno con cero)

# 2. Signo:
'''
+: Indica que siempre se debe mostrar el signo para números positivos y negativos.

-: Indica que solo se debe mostrar el signo para números negativos (predeterminado).

 (espacio): Indica que se debe usar un espacio inicial para números positivos y un signo menos para números negativos.
'''
positivo = 42
negativo = -42
print(f"'{positivo:+}' '{negativo:+}'") # Salida: '+42' '-42'
print(f"'{positivo:-}' '{negativo:-}'") # Salida: '42' '-42' (predeterminado)
print(f"'{positivo: }' '{negativo: }'") # Salida: ' 42' '-42'

# 3. # (Forma Alternativa):
'''
Activa una forma de conversión "alternativa". El efecto depende del tipo:

    Para enteros o, x, X, b: Prefija la salida con 0o, 0x, 0X, 0b respectivamente.

    Para f, F, e, E, g, G: Siempre incluye el punto decimal, incluso si no hay parte fraccionaria.

    Para g, G: No elimina los ceros finales.
'''
num = 255
print(f"{num:#x}")  # Salida: 0xff
print(f"{num:#o}")  # Salida: 0o377
print(f"{num:#b}")  # Salida: 0b11111111
flotante = 12.5
print(f"{flotante:.0f}")   # Salida: 12
print(f"{flotante:#.0f}")  # Salida: 12.

# 4. 0 (Relleno con Ceros):
'''
Equivalente a usar relleno='0' y alineacion='='. Es un atajo conveniente para rellenar números con ceros iniciales respetando el signo.
'''
num = 42
print(f"'{num:05}'") # Salida: '00042'
num_neg = -42
print(f"'{num_neg:05}'") # Salida: '-0042' (Equivalente a f"'{num_neg:0=5}'")

# 5. Ancho (width):
'''
Número entero que especifica el ancho mínimo total del campo. Si el valor formateado es más corto, se rellena según la alineación.
'''
print(f"'{texto:10}'") # Salida: 'Hola      ' (ancho 10, alinea izquierda por defecto)
print(f"'{num:10}'")   # Salida: '        42' (ancho 10, alinea derecha por defecto)

# 6. Agrupación (grouping_option):
'''
,: Usa una coma como separador de miles.

_: Usa un guion bajo como separador de miles (útil en código) o separador para bases b, o, x, X.
'''
numero_grande = 1000000
print(f"{numero_grande:,}")  # Salida: 1,000,000
print(f"{numero_grande:_}")  # Salida: 1_000_000
binario_largo = 0b1101101011011010
print(f"{binario_largo:#_b}") # Salida: 0b_1101_1010_1101_1010

# 7. Precisión (.precision):
'''
Número entero precedido por un punto (.).

Para tipos de punto flotante (f, F, e, E, g, G, %): Número de dígitos después del punto decimal. Para g, G es el número total de dígitos significativos.

Para tipos no numéricos (como s): Longitud máxima del campo (trunca la cadena si es más larga).
'''
pi = 3.14159265
print(f"{pi:.2f}")   # Salida: 3.14
print(f"{pi:.3e}")   # Salida: 3.142e+00
print(f"{pi:.4g}")   # Salida: 3.142 (4 dígitos significativos)
mensaje = "Hola Mundo"
print(f"'{mensaje:.5}'") # Salida: 'Hola ' (trunca a 5 caracteres)

# 8. Tipo (type):
'''
Especifica cómo se debe presentar el objeto. Los más comunes son:
  s: String (predeterminado para objetos string). Llama a str().
  d: Decimal entero.
  b: Binario.
  o: Octal.
  x: Hexadecimal (letras minúsculas).
  X: Hexadecimal (letras mayúsculas).
  n: Número. Similar a d para enteros y g para flotantes, pero usa la configuración regional actual para los separadores. ¡Úsalo con cuidado!
  c: Carácter. Convierte un entero a su carácter Unicode correspondiente.
  f: Punto fijo (notación decimal). Precisión por defecto 6.
  F: Punto fijo. Como f, pero muestra NAN e INF en mayúsculas.
  e: Notación científica (con e minúscula). Precisión por defecto 6.
  E: Notación científica (con E mayúscula). Precisión por defecto 6.
  g: Formato general. Elige entre f y e según la magnitud. Elimina ceros finales insignificantes y el punto decimal si no hay parte fraccionaria (a menos que se use #). Precisión por defecto 6 (dígitos significativos).
  G: Formato general. Como g, pero usa E y muestra NAN, INF en mayúsculas.
  %: Porcentaje. Multiplica el número por 100, lo formatea como f y añade un signo %.
'''
num = 255
flot = 0.75
print(f"{num:d} {num:b} {num:o} {num:x} {num:X}")
# Salida: 255 11111111 377 ff FF
print(f"{65:c}") # Salida: A
print(f"{flot:f} {flot:.1f}") # Salida: 0.750000 0.8
print(f"{flot:e} {flot:E}")   # Salida: 7.500000e-01 7.500000E-01
print(f"{flot:%}")           # Salida: 75.000000%
print(f"{flot:.0%}")         # Salida: 75%