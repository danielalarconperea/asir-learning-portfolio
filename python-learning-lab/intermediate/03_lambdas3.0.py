# -*- coding: utf-8 -*-
"""
PYTHON 3.0: FUNCIONES LAMBDA (ANÓNIMAS)
--------------------------------------
Las lambdas son funciones de una sola línea sin nombre. 
Son ideales para operaciones rápidas que se pasan como argumentos.
"""

# ==============================================================================
# NIVEL 1: SINTAXIS Y LO BÁSICO
# ==============================================================================
# Estructura: lambda argumentos: expresión (el retorno es implícito)

# 1.1. Lambda básica vs Función normal
def square_def(x): return x * x
square_lambda = lambda x: x * x

print(f"Cuadrado (def): {square_def(5)}")
print(f"Cuadrado (lambda): {square_lambda(5)}")

# 1.2. Múltiples argumentos y valores por defecto
multiply = lambda x, y: x * y
power = lambda base, exp=2: base ** exp

print(f"Multiplicación: {multiply(10, 5)}")
print(f"Potencia (default): {power(4)}") # 16

# ==============================================================================
# NIVEL 2: EL "CORE" DE LAS LAMBDAS (PROGRAMACIÓN FUNCIONAL)
# ==============================================================================
# Las lambdas brillan cuando se pasan a funciones de orden superior.

numbers = [1, 2, 3, 4, 5, 6]
users = [
    {"name": "Berto", "level": 15},
    {"name": "Ana", "level": 42},
    {"name": "Zoe", "level": 10}
]

# 2.1. Transformar (map) y Filtrar (filter)
# El map() aplica la lógica, list() convierte el iterador resultante.
doubled = list(map(lambda n: n * 2, numbers))
evens = list(filter(lambda n: n % 2 == 0, numbers))

# 2.2. Ordenación Avanzada (sorted)
# Usamos 'key' para decir por qué atributo queremos ordenar.
by_level = sorted(users, key=lambda user: user["level"])
print(f"Usuarios por nivel: {by_level}")

# ==============================================================================
# NIVEL 3: LÓGICA Y CIERRES (CLOSURES)
# ==============================================================================

# 3.1. Lógica Condicional (Operador Ternario)
# Sintaxis: [valor_si_true] if [condición] else [valor_si_false]
check_status = lambda score: "Pass" if score >= 5 else "Fail"
print(f"Resultado examen (4.5): {check_status(4.5)}")

# 3.2. Closures: Funciones que crean funciones
def multiplier_fatory(n):
    return lambda x: x * n # La lambda "recuerda" el valor de n

triple = multiplier_fatory(3)
print(f"Triplicar 10: {triple(10)}")

# ==============================================================================
# NIVEL 4: LA TRAMPA DEL "LATE BINDING"
# ==============================================================================
# ¡CUIDADO! Las lambdas en bucles capturan la variable, no su valor actual.

funcs = [lambda: i for i in range(3)]
print(f"Error común: {[f() for f in funcs]}") # Imprime [2, 2, 2]

# Solución: Capturar el valor como un argumento por defecto
correct_funcs = [lambda val=i: val for i in range(3)]
print(f"Solución correcta: {[f() for f in correct_funcs]}") # [0, 1, 2]

# ==============================================================================
# BEST PRACTICES (PEP 8)
# ==============================================================================
# 1. NO asignes lambdas a variables (como: saludo = lambda: "hola"). 
#    Usa 'def' para eso. Las lambdas son para ser ANÓNIMAS (in-line).
# 2. Legibilidad: Si la lambda es difícil de leer, conviértela en una función 'def'.
# 3. No abuses de ellas: Muchas veces una List Comprehension es más clara que un map/lambda.
