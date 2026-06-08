# Clase en vídeo: https://youtu.be/TbcEqkabAWU?t=4142

### Challenges ###

"""
EL FAMOSO "FIZZ BUZZ”:
Escribe un programa que muestre por consola (con un print) los
números de 1 a 100 (ambos incluidos y con un salto de línea entre
cada impresión), sustituyendo los siguientes:
- Múltiplos de 3 por la palabra "fizz".
- Múltiplos de 5 por la palabra "buzz".
- Múltiplos de 3 y de 5 a la vez por la palabra "fizzbuzz".
"""


def fizzbuzz():
    for index in range(1, 101):
        if index % 3 == 0 and index % 5 == 0:
            print("fizzbuz")
        elif index % 3 == 0:
            print("fizz")
        elif index % 5 == 0:
            print("buzz")
        else:
            print(index)


fizzbuzz()

"""
¿ES UN ANAGRAMA?
Escribe una función que reciba dos palabras (String) y retorne
verdadero o falso (Bool) según sean o no anagramas.
- Un Anagrama consiste en formar una palabra reordenando TODAS
  las letras de otra palabra inicial.
- NO hace falta comprobar que ambas palabras existan.
- Dos palabras exactamente iguales no son anagrama.
"""


def is_anagram(word_one, word_two):
    if word_one.lower() == word_two.lower():
        return False
    return sorted(word_one.lower()) == sorted(word_two.lower())


print(is_anagram("Amor", "Roma"))

"""
LA SUCESIÓN DE FIBONACCI
Escribe un programa que imprima los 50 primeros números de la sucesión
de Fibonacci empezando en 0.
- La serie Fibonacci se compone por una sucesión de números en
  la que el siguiente siempre es la suma de los dos anteriores.
  0, 1, 1, 2, 3, 5, 8, 13...
"""


def fibonacci():

    prev = 0
    next = 1

    for index in range(0, 50):
        print(prev)
        fib = prev + next
        prev = next
        next = fib


fibonacci()

"""
¿ES UN NÚMERO PRIMO?
Escribe un programa que se encargue de comprobar si un número es o no primo.
Hecho esto, imprime los números primos entre 1 y 100.
"""


def is_prime():

    for number in range(1, 101):

        if number >= 2:

            is_divisible = False

            for index in range(2, number):
                if number % index == 0:
                    is_divisible = True
                    break

            if not is_divisible:
                print(number)


is_prime()

"""
INVIRTIENDO CADENAS
Crea un programa que invierta el orden de una cadena de texto
sin usar funciones propias del lenguaje que lo hagan de forma automática.
- Si le pasamos "Hola mundo" nos retornaría "odnum aloH"
"""


def reverse(text):
    text_len = len(text)
    reversed_text = ""
    for index in range(0, text_len):
        reversed_text += text[text_len - index - 1]
    return reversed_text


print(reverse("Hola mundo"))


'''
ÁREA DE UN POLÍGONO
Crea una única función (importante que sólo sea una) que sea capaz
de calcular y retornar el área de un polígono.
- La función recibirá por parámetro sólo UN polígono a la vez.
- Los polígonos soportados serán Triángulo, Cuadrado y Rectángulo.
- Imprime el cálculo del área de un polígono de cada tipo.
'''
def area_poligono(poligono, base, altura):
    if poligono == "triangulo":
        area = base * altura / 2
    elif poligono == "cuadrado":
        area = base ** 2
    elif poligono == "rectangulo":
        area = base * altura
    else:
        print('escribe en poligono (rectangulo-cuadrado-triangulo)')
    return print(area)

area_poligono('triangulo', 3,5)

print('-----------------------------------------------------------------------------')

# Definimos una clase base llamada 'Polygon' para representar un polígono
class Polygon:
    
    # Método para calcular el área del polígono, que será sobrescrito por las subclases
    def area(self):
        pass

    # Método para imprimir el área del polígono
    def print_area(self):
        # Utiliza f-string para imprimir el área del polígono, utilizando el nombre de la clase en minúsculas
        print(f"El área del {self.__class__.__name__.lower()} es {self.area()}")

# Definimos una clase 'Triangle' que hereda de 'Polygon'
class Triangle(Polygon):
    
    # Método constructor que inicializa la base y la altura del triángulo
    def __init__(self, base, height):
        self.base = base
        self.height = height

    # Sobrescribimos el método 'area' para calcular el área de un triángulo
    def area(self):
        return (self.base * self.height) / 2

# Definimos una clase 'Rectangle' que hereda de 'Polygon'
class Rectangle(Polygon):
    
    # Método constructor que inicializa la longitud y el ancho del rectángulo
    def __init__(self, length, width):
        self.length = length
        self.width = width

    # Sobrescribimos el método 'area' para calcular el área de un rectángulo
    def area(self):
        return self.length * self.width

# Definimos una clase 'Square' que hereda de 'Polygon'
class Square(Polygon):
    
    # Método constructor que inicializa el lado del cuadrado
    def __init__(self, side):
        self.side = side

    # Sobrescribimos el método 'area' para calcular el área de un cuadrado
    def area(self):
        return self.side * self.side

# Función principal que ejecuta el código
def main():
    # Creamos una lista de polígonos con diferentes instancias de 'Triangle', 'Rectangle' y 'Square'
    polygons = [
        Triangle(10, 5),    # Triángulo con base 10 y altura 5
        Rectangle(5, 7),    # Rectángulo con longitud 5 y ancho 7
        Square(4)           # Cuadrado con lado 4
    ]

    # Iteramos sobre cada polígono en la lista y llamamos al método 'print_area' para imprimir su área
    for polygon in polygons:
        polygon.print_area()

# Condición para asegurarnos de que la función 'main' se ejecute solo si este script se ejecuta directamente
if __name__ == "__main__":
    main()



'''
ASPECT RATIO DE UNA IMAGEN
Crea un programa que se encargue de calcular el aspect ratio de una
imagen a partir de una url.
- Url de ejemplo: https://raw.githubusercontent.com/mouredevmouredev/master/mouredev_github_profile.png
- Por ratio hacemos referencia por ejemplo a los "16:9" de una imagen de 1920*1080px.
'''

# import threading
# from urllib.request import urlopen
# from PIL import Image
# import math

# import threading
# from urllib.request import urlopen
# from PIL import Image

# class Challenge5:

#     def __init__(self):
#         pass

#     def rational_aspect_ratio(self, aspect_ratio):
#         precision = 1.0E-6
#         x = aspect_ratio
#         a = round(x)
#         h1, k1, h, k = 1, 0, a, 1

#         while (x - a > precision * k * k):
#             x = 1.0 / (x - a)
#             a = round(x)
#             h1, k1, h, k = h, k, h1 + a * h, k1 + a * k

#         return h, k

#     def aspect_ratio(self, url):
#         def task():
#             response = urlopen(url)
#             image = Image.open(response)

#             height = image.height
#             width = image.width
#             aspect_ratio = self.rational_aspect_ratio(height / width)
#             aspect_ratio_str = f"{aspect_ratio[1]}:{aspect_ratio[0]}"

#             print(f"El aspect ratio es {aspect_ratio_str}" if aspect_ratio_str else "No se ha podido calcular el aspect ratio")

#         threading.Thread(target=task).start()

# # Ejemplo de uso
# challenge = Challenge5()
# challenge.aspect_ratio("https://example.com/image.jpg")

'''
Crea un programa que cuente cuantas veces se repite cada palabra
y que muestre el recuento final de todas ellas.
Los signos de puntuación no forman parte de la palabra.
Una palabra es la misma aunque aparezca en mayúsculas y minúsculas.
No se pueden utilizar funciones propias del lenguaje que
lo resuelvan automáticamente.
'''

# Texto de ejemplo
texto = 'Hola hola, buenos dias hola'
print(texto)
# Convertir el texto a minúsculas para tratar todas las palabras por igual
texto = texto.lower()

# Eliminar signos de puntuación manualmente
signos_puntuacion = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~'
for signo in signos_puntuacion:
    texto = texto.replace(signo, "")
print(texto)
# Inicializar variables
palabra = ''
diccionario = {}

# Recorrer cada letra en el texto
for letra in texto:
    if letra.isalnum():
        palabra += letra
    else:
        if palabra:
            # Agregar la palabra al diccionario o incrementar su conteo
            if palabra in diccionario:
                diccionario[palabra] += 1
            else:
                diccionario[palabra] = 1
            palabra = ''

# No olvidar la última palabra en el texto
if palabra:
    if palabra in diccionario:
        diccionario[palabra] += 1
    else:
        diccionario[palabra] = 1

# Mostrar el resultado
for palabra, conteo in diccionario.items():
    print(f'{palabra}: {conteo}')


'''
Contar vocales en una cadena:
Escribe un programa que cuente la cantidad de vocales en una cadena.
'''
contadorvocales = 0
texto = input("Dime una cadena de caracteres para ver cuántas vocales tiene: ")

for i in range(len(texto)):
    if texto[i] in ('a', 'e', 'i', 'o', 'u'):
        contadorvocales += 1

print(contadorvocales)

# o mejor

contadorvocales = 0
texto = input("Dime una cadena de caracteres para ver cuántas vocales tiene: ")

for letra in texto:
    if letra in ('a', 'e', 'i', 'o', 'u'):
        contadorvocales += 1

print(contadorvocales)
