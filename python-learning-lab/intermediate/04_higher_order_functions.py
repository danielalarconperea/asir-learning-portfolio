# Clase en vídeo: https://youtu.be/TbcEqkabAWU?t=10172

### Higher Order Functions ###

from functools import reduce


def sum_one(value):
    return value + 1


def sum_five(value):
    return value + 5


def sum_two_values_and_add_value(first_value, second_value, f_sum):
    return f_sum(first_value + second_value)


print(sum_two_values_and_add_value(5, 2, sum_one))
print(sum_two_values_and_add_value(5, 2, sum_five))

### Closures ###


def sum_ten(original_value):
    def add(value):
        return value + 10 + original_value
    return add


add_closure = sum_ten(1)
print(add_closure(5))
print((sum_ten(5))(1))

### Built-in Higher Order Functions ###

numbers = [2, 5, 10, 21, 3, 30]

# Map


def multiply_two(number):
    return number * 2


print(list(map(multiply_two, numbers)))
print(list(map(lambda number: number * 2, numbers)))

# Filter


def filter_greater_than_ten(number):
    if number > 10:
        return True
    return False


print(list(filter(filter_greater_than_ten, numbers)))
print(list(filter(lambda number: number > 10, numbers)))

# Reduce


def sum_two_values(first_value, second_value):
    return first_value + second_value


print(reduce(sum_two_values, numbers))



#-------------------------------------------------------------------------------------------------------------------------------



"""
====================
FUNCIONES DE ORDEN SUPERIOR EN PYTHON
====================
Las funciones de orden superior son aquellas que pueden:
1. Recibir otras funciones como argumentos
2. Retornar funciones como resultado
3. Ambas cosas
"""

# ====================
# 1. FUNCIONES COMO ARGUMENTOS
# ====================

def aplicar_funcion(func, valor):
    """
    Aplica una función a un valor dado.
    Esto es una función de orden superior porque recibe otra función como argumento.
    """
    return func(valor)

# Ejemplo de uso con diferentes funciones
def cuadrado(x):
    return x ** 2

def doble(x):
    return x * 2

print(aplicar_funcion(cuadrado, 5))  # 25
print(aplicar_funcion(doble, 5))     # 10

# ====================
# 2. FUNCIONES INCORPORADAS DE ORDEN SUPERIOR
# ====================

# --------------------
# a) map(función, iterable)
# --------------------
# Aplica una función a cada elemento de un iterable

numeros = [1, 2, 3, 4, 5]
cuadrados = list(map(lambda x: x**2, numeros))
print(cuadrados)  # [1, 4, 9, 16, 25]

# --------------------
# b) filter(función, iterable)
# --------------------
# Filtra elementos que cumplen una condición

pares = list(filter(lambda x: x % 2 == 0, numeros))
print(pares)  # [2, 4]

# --------------------
# c) reduce(función, iterable)
# --------------------
# (Requiere importar functools)
# Aplica acumulativamente una función a pares de elementos

from functools import reduce

sumatoria = reduce(lambda a, b: a + b, numeros, 0)
print(sumatoria)  # 15

# ====================
# 3. FUNCIONES LAMBDA
# ====================
# Funciones anónimas creadas con lambda

# Ejemplo de lambda con map
mayusculas = list(map(lambda s: s.upper(), ['hola', 'mundo']))
print(mayusculas)  # ['HOLA', 'MUNDO']

# ====================
# 4. RETORNAR FUNCIONES
# ====================

def crear_multiplicador(n):
    """Retorna una función que multiplica por n"""
    def multiplicador(x):
        return x * n
    return multiplicador

doblar = crear_multiplicador(2)
triplicar = crear_multiplicador(3)

print(doblar(5))   # 10
print(triplicar(5)) # 15

# ====================
# 5. CLOSURES
# ====================
# Funciones que recuerdan variables de ámbito superior

def contador():
    count = 0
    def incrementar():
        nonlocal count
        count += 1
        return count
    return incrementar

mi_contador = contador()
print(mi_contador())  # 1
print(mi_contador())  # 2

# ====================
# 6. DECORADORES
# ====================
# Funciones que modifican/complementan otras funciones

# --------------------
# Decorador básico
# --------------------
def mi_decorador(func):
    def wrapper():
        print("Antes de llamar a la función")
        func()
        print("Después de llamar a la función")
    return wrapper

@mi_decorador
def saludar():
    print("¡Hola!")

saludar()

# --------------------
# Decorador con argumentos
# --------------------
def decorador_con_argumentos(func):
    def wrapper(*args, **kwargs):
        print(f"Llamando a {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@decorador_con_argumentos
def suma(a, b):
    return a + b

print(suma(3, 4))  # 7

# --------------------
# Decorador con parámetros
# --------------------
def repetir(n_veces):
    def decorador(func):
        def wrapper(*args, **kwargs):
            for _ in range(n_veces):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorador

@repetir(3)
def saludar():
    print("Hola mundo!")

saludar()

# ====================
# 7. ORDEN SUPERIOR CON CLASES
# ====================
class ManipuladorFunciones:
    def __init__(self, func):
        self.func = func
    
    def aplicar(self, *args):
        return self.func(*args)

manipulador = ManipuladorFunciones(lambda x: x * 10)
print(manipulador.aplicar(5))  # 50

# ====================
# 8. EJEMPLOS AVANZADOS
# ====================

# --------------------
# Composición de funciones
# --------------------
def componer(f, g):
    """Retorna f(g(x))"""
    return lambda x: f(g(x))

def sumar_uno(x):
    return x + 1

def cuadrado(x):
    return x ** 2

composicion = componer(cuadrado, sumar_uno)
print(composicion(3))  # (3+1)^2 = 16

# --------------------
# Funciones de orden superior personalizadas
# --------------------
def procesador_pipeline(datos, *funciones):
    """Aplica múltiples funciones en pipeline"""
    resultado = datos
    for func in funciones:
        resultado = func(resultado)
    return resultado

datos = [1, 2, 3, 4, 5]
procesado = procesador_pipeline(
    datos,
    lambda x: filter(lambda n: n % 2 == 0, x),
    lambda x: map(lambda n: n * 10, x),
    list
)
print(procesado)  # [20, 40]

# ====================
# 9. USO CON ITERTOOLS
# ====================
import itertools

# Función accumulate como ejemplo de orden superior
sumas_acumuladas = list(itertools.accumulate(numeros, lambda a, b: a + b))
print(sumas_acumuladas)  # [1, 3, 6, 10, 15]

# ====================
# 10. CASOS PRÁCTICOS
# ====================

# --------------------
# Sistema de permisos
# --------------------
def requiere_login(func):
    def wrapper(usuario, *args, **kwargs):
        if usuario.autenticado:
            return func(usuario, *args, **kwargs)
        else:
            raise Exception("Acceso denegado")
    return wrapper

class Usuario:
    def __init__(self, autenticado):
        self.autenticado = autenticado

@requiere_login
def ver_perfil(usuario):
    print("Mostrando perfil...")

usuario_valido = Usuario(True)
ver_perfil(usuario_valido)

# --------------------
# Procesamiento de datos
# --------------------
datos_usuarios = [
    {'nombre': 'Alice', 'edad': 30},
    {'nombre': 'Bob', 'edad': 25},
    {'nombre': 'Charlie', 'edad': 35}
]

# Pipeline de procesamiento
resultado = (
    datos_usuarios
    .filter(lambda u: u['edad'] > 25)
    .map(lambda u: {**u, 'nombre': u['nombre'].upper()})
    .sorted(key=lambda u: u['edad'], reverse=True)
)

print(list(resultado))
# [{'nombre': 'CHARLIE', 'edad': 35}, {'nombre': 'ALICE', 'edad': 30}]

# ====================
# 11. FUNCIONES PARCIALES
# ====================
from functools import partial

def potencia(base, exponente):
    return base ** exponente

# Crear función parcial
cuadrado = partial(potencia, exponente=2)
cubo = partial(potencia, exponente=3)

print(cuadrado(5))  # 25
print(cubo(5))      # 125

# ====================
# 12. ORDENAMIENTO COMPLEJO
# ====================
personas = [
    ('Alice', 32),
    ('Bob', 25),
    ('Charlie', 19)
]

# Ordenar por edad usando lambda como key function
print(sorted(personas, key=lambda x: x[1])) 
# [('Charlie', 19), ('Bob', 25), ('Alice', 32)]

"""
Este código cubre:
- Funciones como argumentos y retornos
- Lambdas
- map, filter, reduce
- Decoradores (simples, con argumentos, con parámetros)
- Closures
- Clases con funciones de orden superior
- Composición de funciones
- Casos prácticos reales
- Funciones parciales
- Ordenamiento complejo
- Itertools
- Pipelines de procesamiento
"""