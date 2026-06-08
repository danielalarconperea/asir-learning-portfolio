# -*- coding: utf-8 -*-
"""
PYTHON 3.0: FUNCIONES DE ORDEN SUPERIOR (HOF)
--------------------------------------------
Una HOF es una función que acepta otras funciones como argumentos 
o devuelve una función como resultado. 
En Python, las funciones son "objetos de primera clase".
"""

import functools
import time

# ==============================================================================
# NIVEL 1: FUNCIONES COMO OBJETOS
# ==============================================================================

def greet(): return "¡Hola!"
def scream(): return "¡¡HOLA!!"

# 1.1. Asignación y Colecciones
# Podemos guardar lógica en estructuras de datos
actions = [greet, scream]
for action in actions:
    print(f"Ejecutando: {action()}")

# ==============================================================================
# NIVEL 2: FUNCIONES COMO ARGUMENTOS (EL "CALLBACK")
# ==============================================================================

# 2.1. HOF Personalizada
def process_data(func, value):
    """Aplica 'func' al 'value'."""
    return func(value)

print(f"Procesado: {process_data(str.upper, 'python')}")

# 2.2. HOF Built-ins Clásicas
nums = [1, 5, 8, 12]
# MAP: Transforma cada elemento
sq_nums = list(map(lambda x: x**2, nums))
# FILTER: Filtra según una condición (bool)
big_nums = list(filter(lambda x: x > 10, sq_nums))
print(f"Pipeline: {nums} -> {sq_nums} -> {big_nums}")

# ==============================================================================
# NIVEL 3: CLOSURES (FUNCIONES QUE GENERAN FUNCIONES)
# ==============================================================================

# 3.1. El Concepto de Fábrica
def build_tagger(tag):
    """Crea una función que envuelve texto en etiquetas HTML."""
    def tag_text(text):
        return f"<{tag}>{text}</{tag}>"
    return tag_text

h1 = build_tagger("h1")
p = build_tagger("p")
print(h1("Título Pro"))
print(p("Este es un párrafo generado por un closure."))

# 3.2. Modificando Scope Externo (nonlocal)
def create_counter():
    count = 0
    def increment():
        nonlocal count # Permite modificar la variable de la función padre
        count += 1
        return count
    return increment

ticker = create_counter()
print(f"Click: {ticker()}, Click: {ticker()}")

# ==============================================================================
# NIVEL 4: DECORADORES (EL NIVEL MAESTRO)
# ==============================================================================
# Un decorador es una HOF que "envuelve" a otra para añadirle funcionalidad.

def debug_logger(func):
    """Registra la ejecución de cualquier función."""
    @functools.wraps(func) # Mantiene el nombre y docstring original
    def wrapper(*args, **kwargs):
        print(f"[LOG] Ejecutando {func.__name__} con {args}")
        result = func(*args, **kwargs)
        print(f"[LOG] Resultado: {result}")
        return result
    return wrapper

@debug_logger
def add_bonus(salary, bonus):
    return salary + bonus

add_bonus(2000, 500)

# ==============================================================================
# NIVEL 5: HERRAMIENTAS DE FUNCTOOLS
# ==============================================================================

# 5.1. Aplicación Parcial (partial)
# 'Fija' argumentos de una función para crear una nueva más simple.
def power(base, exp): return base ** exp
square = functools.partial(power, exp=2)
cube = functools.partial(power, exp=3)

print(f"Cuadrado de 9: {square(9)}")

# 5.2. Reducción (reduce)
# De muchas a una. Ejemplo: Producto de todos los elementos.
product = functools.reduce(lambda x, y: x * y, [1, 2, 3, 4])
print(f"Producto total: {product}")

# ==============================================================================
# TIPS PRO PARA APRENDER MÁS
# ==============================================================================
# 1. Composición: Las HOFs permiten crear "pipelines" de datos (map -> filter -> reduce).
# 2. Currificación (Currying): Técnica avanzada de closures (investigar).
# 3. Decoradores con argumentos: Requieren una capa extra de envoltura (fábrica de decoradores).
