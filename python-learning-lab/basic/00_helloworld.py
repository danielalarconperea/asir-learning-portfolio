# Clase en vídeo: https://youtu.be/Kp4Mvapo5kc

### Hola Mundo ###

# Nuestro hola mundo en Python
print("Hola Python")
print('Hola Python')

# Esto es un comentario

"""
Este es un
comentario
en varias líneas
"""

'''
Este también es un
comentario
en varias líneas
'''

# Cómo consultar el tipo de dato
print(type("Soy un dato str"))  # Tipo 'str'
print(type(5))  # Tipo 'int'
print(type(1.5))  # Tipo 'float'
print(type(3 + 1j))  # Tipo 'complex'
print(type(True))  # Tipo 'bool'
print(type(print("Mi cadena de texto")))  # Tipo 'NoneType'







"""
EL FAMOSO "FIZZ BUZZ”:
Escribe un programa que muestre por consola (con un print) los
números de 1 a 100 (ambos incluidos y con un salto de línea entre
cada impresión), sustituyendo los siguientes:
- Múltiplos de 3 por la palabra "fizz".
- Múltiplos de 5 por la palabra "buzz".
- Múltiplos de 3 y de 5 a la vez por la palabra "fizzbuzz".
"""

def FIZZBUZZ():
    for index in range(1,101):
        if index % 3 == 0 and index % 5 == 0:
            print('fizzbuzz')
        elif index % 3 == 0:
            print('fizz')
        elif index % 5 == 0:
            print('buzz')
        else:
            print(index)

#FIZZBUZZ()

"""
¿ES UN ANAGRAMA?
Escribe una función que reciba dos palabras (String) y retorne
verdadero o falso (Bool) según sean o no anagramas.
- Un Anagrama consiste en formar una palabra reordenando TODAS
  las letras de otra palabra inicial.
- NO hace falta comprobar que ambas palabras existan.
- Dos palabras exactamente iguales no son anagrama.
"""

def ES_UN_ANAGRAMA(palabra1, palabra2):
    if palabra1.lower() == palabra2.lower():
        return False
    return sorted(palabra1.lower()) == sorted(palabra2.lower())

#print(ES_UN_ANAGRAMA('Mora','roma'))

"""
LA SUCESIÓN DE FIBONACCI
Escribe un programa que imprima los 50 primeros números de la sucesión
de Fibonacci empezando en 0.
- La serie Fibonacci se compone por una sucesión de números en
  la que el siguiente siempre es la suma de los dos anteriores.
  0, 1, 1, 2, 3, 5, 8, 13...
"""
def FIBONACCI():
    anterior=0
    siguiente=1
    for i in range(0,50):
        print(anterior)
        fib=anterior+siguiente
        anterior=siguiente
        siguiente=fib

FIBONACCI() 

"""
¿ES UN NÚMERO PRIMO?
Escribe un programa que se encargue de comprobar si un número es o no primo.
Hecho esto, imprime los números primos entre 1 y 100.
"""

def NÚMERO_PRIMO ():
    for number in range(0,1000000000):

        if number >= 2:
        
            is_divisible = False
        
            for index in range(2, number):
                if number % index == 0:
                    is_divisible = True
                    break
           
            if not is_divisible:
                print(number)
#NÚMERO_PRIMO ()

"""
INVIRTIENDO CADENAS
Crea un programa que invierta el orden de una cadena de texto
sin usar funciones propias del lenguaje que lo hagan de forma automática.
- Si le pasamos "Hola mundo" nos retornaría "odnum aloH"
"""

def invertir(palabra3):
    reverse_palabra3 = palabra3[::-1]
    print(reverse_palabra3)

invertir('casa')


def reverse(text):
    text_len = len(text)
    reversed_text = ""
    for index in range(0, text_len):
        reversed_text += text[text_len - index - 1]
    return reversed_text


print(reverse("Hola mundo"))