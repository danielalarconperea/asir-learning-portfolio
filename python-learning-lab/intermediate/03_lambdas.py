# Clase en vídeo: https://youtu.be/TbcEqkabAWU?t=9145

### Lambdas ###

'''
def sum_two_values(first_value, second_value): 
    return first_value + second_value
'''
sum_two_values = lambda first_value, second_value: first_value + second_value

print(sum_two_values(2, 4))

'''
def multiply_values(first_value, second_value): 
    return first_value * second_value - 3
'''
multiply_values = lambda first_value, second_value: first_value * second_value - 3

print(multiply_values(2, 4))


def sum_three_values(value):
    return lambda first_value, second_value: first_value + second_value + value


print(sum_three_values(5)(2, 4))



'''
Las funciones de orden superior en Python son aquellas que aceptan otras funciones como argumentos o retornan una función. 
Las lambdas permiten crear funciones simples de manera rápida y concisa. 
A continuación, te doy algunos ejemplos comunes de uso de lambdas en funciones de orden superior, como map(), filter(), reduce(), y sorted().
'''
# La función map() aplica una función a cada elemento de un iterable (como una lista) y devuelve un nuevo iterable con los resultados.
# Usando map para elevar al cuadrado cada número
numeros = [1, 2, 3, 4, 5]
cuadrados = list(map(lambda x: x ** 2, numeros)) # El itinerable es la lista números y Lo que hace map() es aplicar la función lambda a cada número de la lista numeros
print(cuadrados)  # Salida: [1, 4, 9, 16, 25]

# La función filter() filtra los elementos de un iterable, dejando solo aquellos que cumplan con una condición (una función que retorne True o False).
# Usando filter para obtener números pares de una lista
numeros = [1, 2, 3, 4, 5, 6, 7, 8]
pares = list(filter(lambda x: x % 2 == 0, numeros))
print(pares)  # Salida: [2, 4, 6, 8]

# La función reduce() (del módulo functools) aplica una función acumulativa a los elementos de un iterable. Va reduciendo la lista a un único valor, acumulando los resultados.
from functools import reduce

# Usando reduce para multiplicar todos los números de una lista
numeros = [1, 2, 3, 4, 5]
producto = reduce(lambda x, y: x * y, numeros)
print(producto)  # Salida: 120 (1 * 2 * 3 * 4 * 5)

# La función sorted() se usa para ordenar una lista. Se le puede pasar una función como el argumento key para definir cómo se ordenarán los elementos.
palabras = ["hola", "mundo", "python", "lambda"]
ordenadas = sorted(palabras, key=lambda palabra: palabra[1])
print(ordenadas)  # Salida: ['lambda', 'mundo', 'python', 'hola']

# O

estudiantes = [
    {"nombre": "Ana", "nota": 9},
    {"nombre": "Pedro", "nota": 7},
    {"nombre": "Laura", "nota": 10}
]
ordenado_por_nota = sorted(estudiantes, key=lambda estudiante: estudiante["nota"], reverse=True) # sorted(iterable, key=None, reverse=False)
print(ordenado_por_nota)
# Salida:
# [{'nombre': 'Laura', 'nota': 10}, {'nombre': 'Ana', 'nota': 9}, {'nombre': 'Pedro', 'nota': 7}]

#Las funciones any() y all() reciben un iterable y evalúan si alguno o todos los elementos cumplen con una condición.
numeros = [1, 2, 3, 4, 5, 6, 7]
resultado = any(map(lambda x: x > 5, numeros))
print(resultado)  # Salida: True

# O

numeros = [2, 4, 6, 8]
resultado = all(map(lambda x: x % 2 == 0, numeros))
print(resultado)  # Salida: True

# La función zip() toma varios iterables y los agrupa por índice, devolviendo tuplas. Puedes usar lambdas para procesar esos grupos de datos.
lista1 = [1, 2, 3]
lista2 = [4, 5, 6]
sumas = list(map(lambda x: x[0] + x[1], zip(lista1, lista2)))
print(sumas)  # Salida: [5, 7, 9]



# -------------------------------------------------------------------------------------------



# === Notas completas sobre funciones lambda en Python ===

# 1. Definición básica
# Lambda es una función anónima definida con la palabra clave 'lambda'
# Sintaxis: lambda argumentos: expresión
# Retorna automáticamente el resultado de la expresión

funcion_lambda = lambda x: x**2
print(funcion_lambda(5))  # 25

# 2. Comparación con función tradicional
def funcion_normal(x):
    return x**2

# Equivalente a:
lambda_normal = lambda x: x**2

# 3. Uso básico con funciones de orden superior

# a) map()
numeros = [1, 2, 3, 4]
cuadrados = list(map(lambda x: x**2, numeros))
print(cuadrados)  # [1, 4, 9, 16]

# b) filter()
pares = list(filter(lambda x: x % 2 == 0, numeros))
print(pares)  # [2, 4]

# c) sorted()
usuarios = [{'nombre': 'Juan', 'edad': 30}, {'nombre': 'Ana', 'edad': 25}]
ordenados = sorted(usuarios, key=lambda x: x['edad'])
print(ordenados)  # Ordena por edad ascendente

# 4. Lambdas con condicionales
# Usamos operadores ternarios
clasificador = lambda x: 'par' if x % 2 == 0 else 'impar'
print(clasificador(4))  # 'par'
print(clasificador(5))  # 'impar'

# 5. Lambdas múltiples parámetros
suma = lambda a, b: a + b
print(suma(3, 5))  # 8

# 6. Lambdas anidadas
multiplicador = lambda x: (lambda y: x * y)
doble = multiplicador(2)
print(doble(5))  # 10

# 7. Currying con lambdas
suma_currying = lambda x: lambda y: x + y
suma5 = suma_currying(5)
print('-----------:',suma5(3))  # 8

# 8. Manejo de excepciones (usando función wrapper)
def safe_divide(f):
    def wrapper(x, y):
        try:
            return f(x, y)
        except ZeroDivisionError:
            return "Error: División por cero"
    return wrapper

divide = safe_divide(lambda x, y: x / y)
print(divide(10, 2))  # 5.0
print(divide(10, 0))  # Error

# 9. Lambdas en estructuras de datos
operaciones = {
    'suma': lambda x, y: x + y,
    'resta': lambda x, y: x - y,
    'multiplica': lambda x, y: x * y
}

print(operaciones['suma'](5, 3))  # 8

# 10. Uso con argumentos variables
variable_args = lambda *args: sum(args)
print(variable_args(1, 2, 3))  # 6

# 11. Lambdas con argumentos por defecto
saludo = lambda nombre, mensaje="Hola": f"{mensaje} {nombre}"
print(saludo("Ana"))         # Hola Ana
print(saludo("Pedro", "Adiós"))  # Adiós Pedro

# 12. Uso en expresiones generadoras
generador = ((lambda x: x**2)(i) for i in range(5))
print(list(generador))  # [0, 1, 4, 9, 16]

# 13. Lambdas en closures
def crear_potencia(n):
    return lambda x: x ** n

cuadrado = crear_potencia(2)
cubo = crear_potencia(3)
print(cuadrado(3))  # 9
print(cubo(3))      # 27

# 14. Uso con functools.reduce()
from functools import reduce
producto = reduce(lambda x, y: x * y, [1, 2, 3, 4])
print(producto)  # 24

# 15. Lambdas en interfaces gráficas (ejemplo Tkinter)
"""
import tkinter as tk
root = tk.Tk()
boton = tk.Button(root, text="Click", command=lambda: print("Hola mundo"))
boton.pack()
root.mainloop()
"""

# 16. Uso con pandas (ejemplo)
"""
import pandas as pd
df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
df['c'] = df.apply(lambda row: row['a'] + row['b'], axis=1)
"""

# 17. Lambdas con expresiones complejas (aunque no recomendado)
# Se pueden usar paréntesis para múltiples líneas
complex_lambda = lambda x: (
    x**2 +
    x**3 +
    x % 2
)
print(complex_lambda(3))  # 27 + 9 + 1 = 37

# 18. Lambdas en comprensión de listas
funciones = [(lambda n: lambda: n * i) for i in range(3)]
# for f in funciones:
#     print(f())  # Atención: cuidado con closure tardía!

# Solución correcta para closure:
funciones = [(lambda n: lambda i=i: n * i) for i in range(3)]
for f in funciones:
    print(f(2))  # 0, 2, 4

# 19. Limitaciones de lambdas
# - No pueden contener declaraciones (solo expresiones)
# - No soportan anotaciones de tipo
# - Una sola expresión
# - Menos legibles en casos complejos

# 20. Buenas prácticas
# - Usar para operaciones simples de una línea
# - Evitar código complejo
# - Preferir funciones normales cuando mejora legibilidad
# - Útiles como argumentos para otras funciones

# 21. Ejemplo avanzado: generador de funciones matemáticas
def generador_ecuacion(a, b, c):
    return lambda x: a * x**2 + b * x + c

ecuacion = generador_ecuacion(2, -3, 5)
print(ecuacion(2))  # 2*(4) + (-3)*2 + 5 = 8 -6 +5 = 7

# 22. Uso con argumentos keyword
kw_lambda = lambda **kwargs: sum(kwargs.values())
print(kw_lambda(a=1, b=2, c=3))  # 6

# 23. Lambdas y variables libres
factor = 3
multiplicador_externo = lambda x: x * factor
print(multiplicador_externo(5))  # 15

# 24. Lambdas en clases
class Calculadora:
    operaciones = {
        'add': lambda self, a, b: a + b,
        'sub': lambda self, a, b: a - b
    }
    
    def calcular(self, op, a, b):
        return self.operaciones[op](self, a, b)

calc = Calculadora()
print(calc.calcular('add', 5, 3))  # 8

# 25. Ordenamiento complejo con múltiples criterios
datos = [(2, 'Z'), (1, 'A'), (2, 'A'), (1, 'B')]
ordenado = sorted(datos, key=lambda x: (x[0], x[1]))
print(ordenado)  # [(1, 'A'), (1, 'B'), (2, 'A'), (2, 'Z')]

# 26. Uso con zip()
combinador = lambda *lists: list(zip(*lists))
print(combinador([1, 2], ['a', 'b']))  # [(1, 'a'), (2, 'b')]

# 27. Validación con lambda
validadores = [
    lambda x: isinstance(x, int),
    lambda x: x > 0,
    lambda x: x % 2 == 0
]

numero = 4
valido = all(validador(numero) for validador in validadores)
print(valido)  # True

# 28. Ejemplo de lambda recursiva (no recomendado)
factorial = (lambda f: lambda x: f(f, x))(lambda f, x: 1 if x == 0 else x * f(f, x-1))
print(factorial(5))  # 120

# === Consideraciones finales ===
# - Lambdas son poderosas para código conciso
# - Ideal para funciones pequeñas y temporales
# - No abusar: mantener el código legible
# - Combinar bien con funciones de orden superior
# - Útiles en programación funcional