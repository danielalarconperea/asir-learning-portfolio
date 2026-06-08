# -*- coding: utf-8 -*-

# ###############################################
# ##      APUNTES COMPLETOS SOBRE             ##
# ##      HIGHER-ORDER FUNCTIONS EN PYTHON    ##
# ###############################################

# ---------------------------------------------------------------------------
# 1. INTRODUCCIÓN A LAS HIGHER-ORDER FUNCTIONS (HOFs)
# ---------------------------------------------------------------------------

# Definición:
# Una Higher-Order Function (Función de Orden Superior) es una función que cumple
# al menos una de las siguientes condiciones:
#   a) Acepta una o más funciones como argumentos.
#   b) Devuelve una función como resultado.

# Concepto Clave: Funciones como Ciudadanos de Primera Clase (First-Class Citizens)
# En Python, las funciones son tratadas como objetos de primera clase. Esto significa que:
#   - Pueden ser asignadas a variables.
#   - Pueden ser pasadas como argumentos a otras funciones.
#   - Pueden ser devueltas como resultado de otras funciones.
#   - Pueden ser almacenadas en estructuras de datos (listas, diccionarios, etc.).
# Esta característica es fundamental para el concepto de HOFs.

print("--- 1. Introducción y Funciones como Ciudadanos de Primera Clase ---")

def saludar(nombre):
    """Función simple que saluda a alguien."""
    return f"Hola, {nombre}!"

# a) Asignar una función a una variable
saludo_variable = saludar
print(f"Tipo de saludo_variable: {type(saludo_variable)}")
print(f"Llamando a través de la variable: {saludo_variable('Mundo')}")

# d) Almacenar funciones en estructuras de datos
def sumar(a, b): return a + b
def restar(a, b): return a - b
def multiplicar(a, b): return a * b

operaciones = {
    'suma': sumar,
    'resta': restar,
    'multiplica': multiplicar
}

x, y = 10, 5
for nombre_op, funcion_op in operaciones.items():
    print(f"Resultado de {nombre_op}({x}, {y}): {funcion_op(x, y)}")

lista_operaciones = [sumar, restar]
print(f"Resultado de la primera op en lista: {lista_operaciones[0](3, 4)}") # Salida: 7

print("-" * 60)

# ---------------------------------------------------------------------------
# 2. HOFs: ACEPTANDO FUNCIONES COMO ARGUMENTOS
# ---------------------------------------------------------------------------

# Esta es una de las características principales de las HOFs. Permite crear
# funciones más genéricas y reutilizables, cuyo comportamiento específico
# puede ser definido por la función que se pasa como argumento.

print("--- 2. HOFs: Aceptando Funciones como Argumentos ---")

# Ejemplo: Una función genérica para aplicar una operación a dos números
def aplicar_operacion(func_operacion, a, b):
    """
    Aplica la función 'func_operacion' a los argumentos 'a' y 'b'.
    'aplicar_operacion' es una HOF porque acepta 'func_operacion' como argumento.
    """
    print(f"Aplicando '{func_operacion.__name__}' a {a} y {b}")
    return func_operacion(a, b)

# Usamos las funciones definidas anteriormente (sumar, restar, multiplicar)
resultado_suma = aplicar_operacion(sumar, 15, 10)
print(f"Resultado: {resultado_suma}")

resultado_resta = aplicar_operacion(restar, 15, 10)
print(f"Resultado: {resultado_resta}")

resultado_multiplicacion = aplicar_operacion(multiplicar, 15, 10)
print(f"Resultado: {resultado_multiplicacion}")

# También podemos usar funciones lambda (anónimas) directamente
resultado_division = aplicar_operacion(lambda x, y: x / y if y != 0 else "Error: División por cero", 15, 10)
print(f"Resultado división (lambda): {resultado_division}")

resultado_division_cero = aplicar_operacion(lambda x, y: x / y if y != 0 else "Error: División por cero", 15, 0)
print(f"Resultado división por cero (lambda): {resultado_division_cero}")

# --- Funciones Integradas (Built-in) que son HOFs ---

# Python incluye varias funciones integradas que son HOFs comunes.

# a) map(funcion, iterable)
#    Aplica 'funcion' a cada elemento de 'iterable' y devuelve un iterador
#    con los resultados.
print("\n-- Ejemplo con map() --")
numeros = [1, 2, 3, 4, 5]

def cuadrado(n):
    return n * n

cuadrados_map = map(cuadrado, numeros)
# map devuelve un iterador, lo convertimos a lista para ver los resultados
lista_cuadrados = list(cuadrados_map)
print(f"Cuadrados usando map con función nombrada: {lista_cuadrados}")

# Usando lambda con map
dobles_map = map(lambda x: x * 2, numeros)
lista_dobles = list(dobles_map)
print(f"Dobles usando map con lambda: {lista_dobles}")

# b) filter(funcion_predicado, iterable)
#    Filtra los elementos de 'iterable', devolviendo un iterador con aquellos
#    elementos para los cuales 'funcion_predicado' devuelve True.
print("\n-- Ejemplo con filter() --")
def es_par(n):
    return n % 2 == 0

pares_filter = filter(es_par, numeros)
# filter también devuelve un iterador
lista_pares = list(pares_filter)
print(f"Números pares usando filter con función nombrada: {lista_pares}")

# Usando lambda con filter
impares_filter = filter(lambda x: x % 2 != 0, numeros)
lista_impares = list(impares_filter)
print(f"Números impares usando filter con lambda: {lista_impares}")

# c) sorted(iterable, key=funcion, reverse=False)
#    Devuelve una nueva lista ordenada a partir de los elementos de 'iterable'.
#    El argumento 'key' acepta una función que se llama sobre cada elemento
#    antes de hacer las comparaciones. Esto la convierte en una HOF.
print("\n-- Ejemplo con sorted() y 'key' --")
palabras = ["manzana", "banana", "kiwi", "uva", "pera"]

# Ordenar por longitud de palabra
palabras_ordenadas_longitud = sorted(palabras, key=len)
print(f"Palabras ordenadas por longitud: {palabras_ordenadas_longitud}")

# Ordenar sin distinguir mayúsculas/minúsculas
palabras_mixtas = ["Manzana", "banana", "Kiwi", "uva", "Pera"]
palabras_ordenadas_ignorando_caso = sorted(palabras_mixtas, key=str.lower)
print(f"Palabras ordenadas ignorando caso: {palabras_ordenadas_ignorando_caso}")

# Ordenar una lista de diccionarios por una clave específica
personas = [
    {'nombre': 'Ana', 'edad': 30},
    {'nombre': 'Juan', 'edad': 25},
    {'nombre': 'Eva', 'edad': 35}
]
personas_ordenadas_edad = sorted(personas, key=lambda persona: persona['edad'])
print(f"Personas ordenadas por edad: {personas_ordenadas_edad}")

# d) functools.reduce(funcion, iterable[, initializador])
#    Aplica 'funcion' de forma acumulativa a los elementos de 'iterable',
#    de izquierda a derecha, para reducir el iterable a un único valor.
#    Nota: A partir de Python 3, reduce fue movido al módulo functools.
print("\n-- Ejemplo con functools.reduce() --")
import functools # Necesario importar

numeros_reduce = [1, 2, 3, 4, 5]

# Calcular la suma total
suma_total = functools.reduce(lambda acumulador, elemento: acumulador + elemento, numeros_reduce)
print(f"Suma total usando reduce: {suma_total}")

# Calcular el producto total
producto_total = functools.reduce(lambda acumulador, elemento: acumulador * elemento, numeros_reduce)
print(f"Producto total usando reduce: {producto_total}")

# Usando un valor inicializador
suma_con_inicial = functools.reduce(lambda acc, el: acc + el, numeros_reduce, 100) # Empieza con 100
print(f"Suma total usando reduce con inicializador 100: {suma_con_inicial}")

print("-" * 60)

# ---------------------------------------------------------------------------
# 3. HOFs: DEVOLVIENDO FUNCIONES COMO RESULTADO (CLOSURES)
# ---------------------------------------------------------------------------

# La segunda característica definitoria de las HOFs es su capacidad para devolver
# otras funciones. Estas funciones devueltas a menudo "recuerdan" el entorno
# en el que fueron creadas (el scope de la función exterior). Este fenómeno
# se conoce como "closure" (clausura).

print("--- 3. HOFs: Devolviendo Funciones (Closures) ---")

# Ejemplo: Una función fábrica que crea funciones de multiplicación
def crear_multiplicador(factor):
    """
    Esta es una HOF que devuelve una nueva función.
    La función devuelta multiplica su argumento por 'factor'.
    'factor' está "encerrado" (closed over) en la función interna.
    """
    def multiplicador(numero):
        """Esta función interna es la que se devuelve."""
        return numero * factor
    
    # La función 'multiplicador' "recuerda" el valor de 'factor'
    # incluso después de que 'crear_multiplicador' haya terminado de ejecutarse.
    return multiplicador

# Creamos funciones específicas usando la fábrica
duplicador = crear_multiplicador(2) # 'factor' es 2 para esta función
triplicador = crear_multiplicador(3) # 'factor' es 3 para esta función
decuplicador = crear_multiplicador(10) # 'factor' es 10 para esta función

# Usamos las funciones generadas
print(f"Duplicador(5): {duplicador(5)}")   # Salida: 10
print(f"Triplicador(5): {triplicador(5)}") # Salida: 15
print(f"Decuplicador(5): {decuplicador(5)}") # Salida: 50

# Inspeccionando el closure (avanzado)
# Podemos ver las variables capturadas en el closure de una función
print(f"Variables en el closure de 'duplicador': {duplicador.__closure__}")
if duplicador.__closure__:
    print(f"Valor de 'factor' en 'duplicador': {duplicador.__closure__[0].cell_contents}") # Debería ser 2

# Ejemplo: Contador con closure
def crear_contador(inicio=0):
    """Crea un contador que incrementa cada vez que se llama."""
    contador_actual = inicio
    def incrementar():
        nonlocal contador_actual # Necesario para modificar la variable del scope exterior
        contador_actual += 1
        return contador_actual
    return incrementar

contador1 = crear_contador()
print(f"Contador 1: {contador1()}") # Salida: 1
print(f"Contador 1: {contador1()}") # Salida: 2

contador2 = crear_contador(100)
print(f"Contador 2: {contador2()}") # Salida: 101
print(f"Contador 1: {contador1()}") # Salida: 3 (contador1 es independiente de contador2)
print(f"Contador 2: {contador2()}") # Salida: 102

print("-" * 60)

# ---------------------------------------------------------------------------
# 4. DECORADORES: UNA APLICACIÓN COMÚN DE HOFs
# ---------------------------------------------------------------------------

# Los decoradores en Python son una forma de "envolver" una función existente
# para añadirle funcionalidad extra (como logging, control de acceso,
# medición de tiempo, etc.) sin modificar su código fuente original.
# Son esencialmente "azúcar sintáctico" para aplicar HOFs.

# Un decorador es una HOF que:
#   1. Acepta una función como argumento.
#   2. Define una nueva función "wrapper" (envoltura) interna.
#   3. La función wrapper usualmente llama a la función original y añade lógica antes/después.
#   4. Devuelve la función wrapper.

print("--- 4. Decoradores ---")

# --- Ejemplo 1: Decorador simple para medir el tiempo de ejecución ---
import time
import functools # Importante para usar @functools.wraps

def medir_tiempo(func):
    """Decorador que mide y muestra el tiempo de ejecución de una función."""
    @functools.wraps(func) # Preserva metadatos de la función original (nombre, docstring, etc.)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs) # Llama a la función original
        fin = time.perf_counter()
        print(f"Función '{func.__name__}' tardó {fin - inicio:.6f} segundos en ejecutarse.")
        return resultado
    return wrapper

# Aplicando el decorador usando la sintaxis @
@medir_tiempo
def proceso_largo(n):
    """Simula un proceso que tarda un poco."""
    time.sleep(n)
    return f"Proceso completado después de {n} segundos."

print("\n-- Probando decorador 'medir_tiempo' --")
resultado_proceso = proceso_largo(0.5)
print(resultado_proceso)

# La sintaxis @medir_tiempo es equivalente a hacer esto después de definir la función:
# def proceso_largo(n):
#     # ... (definición original) ...
# proceso_largo = medir_tiempo(proceso_largo) # Aplicación manual del decorador


# --- Ejemplo 2: Decorador para logging ---
def log_llamada(func):
    """Decorador que registra cuándo se llama a una función y con qué argumentos."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={repr(v)}" for k, v in kwargs.items()]
        firma = ", ".join(args_repr + kwargs_repr)
        print(f"Llamando a {func.__name__}({firma})")
        resultado = func(*args, **kwargs)
        print(f"{func.__name__} devolvió: {repr(resultado)}")
        return resultado
    return wrapper

@log_llamada
def saludar_persona(nombre, saludo="Hola"):
    """Saluda a una persona."""
    return f"{saludo}, {nombre}!"

print("\n-- Probando decorador 'log_llamada' --")
saludar_persona("Ana")
saludar_persona("Carlos", saludo="Buenos días")


# --- Ejemplo 3: Decoradores con Argumentos ---
# Para crear un decorador que acepte argumentos, necesitamos una capa extra de función.
# La función exterior (fábrica de decoradores) acepta los argumentos del decorador.
# Esta función devuelve el decorador real (que acepta la función a decorar).
# El decorador real devuelve la función wrapper.

def repetir(veces):
    """Fábrica de decoradores que repite la ejecución de una función 'veces' veces."""
    def decorador_repetir(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            resultados = []
            for i in range(veces):
                print(f"Ejecución {i+1}/{veces} de {func.__name__}")
                resultado = func(*args, **kwargs)
                resultados.append(resultado)
            return resultados # O podría devolver solo el último, o None, etc.
        return wrapper
    return decorador_repetir

@repetir(veces=3)
def decir_hola():
    """Una función simple que imprime Hola."""
    print("¡Hola!")
    return "Dicho" # Devolvemos algo para ver la lista de resultados

print("\n-- Probando decorador 'repetir(veces=3)' --")
resultados_hola = decir_hola()
print(f"Resultados de decir_hola repetido: {resultados_hola}")


# --- Ejemplo 4: Apilamiento de Decoradores ---
# Se pueden aplicar múltiples decoradores a una sola función.
# Se aplican de abajo hacia arriba (el más cercano a la función se aplica primero).
# Se ejecutan de arriba hacia abajo (el wrapper del de más arriba envuelve al de más abajo).

@log_llamada    # Se ejecuta segundo (envuelve al wrapper de medir_tiempo)
@medir_tiempo   # Se aplica primero a 'calculo_complejo', se ejecuta primero (más cerca de la llamada original)
def calculo_complejo(a, b):
    """Simula un cálculo que toma tiempo."""
    time.sleep(0.3)
    return a ** b

print("\n-- Probando apilamiento de decoradores --")
resultado_calculo = calculo_complejo(2, 5)
print(f"Resultado final del cálculo complejo: {resultado_calculo}")
# Observa el orden de los prints de los decoradores en la consola.

print("-" * 60)

# ---------------------------------------------------------------------------
# 5. LAMBDA FUNCTIONS Y SU RELACIÓN CON HOFs
# ---------------------------------------------------------------------------

# Las funciones lambda (o funciones anónimas) son funciones pequeñas, de una sola
# expresión, que se definen en línea. No son HOFs por sí mismas, pero se usan
# MUY frecuentemente como argumentos para HOFs como map(), filter(), sorted(),
# y en decoradores o closures simples, debido a su sintaxis concisa.

print("--- 5. Funciones Lambda y HOFs ---")

numeros_lambda = [10, 3, 8, 9, 4, 6]

# Uso con map: Obtener el sucesor de cada número
sucesores = list(map(lambda x: x + 1, numeros_lambda))
print(f"Sucesores (map + lambda): {sucesores}")

# Uso con filter: Obtener números mayores que 5
mayores_que_5 = list(filter(lambda x: x > 5, numeros_lambda))
print(f"Mayores que 5 (filter + lambda): {mayores_que_5}")

# Uso con sorted: Ordenar por el último dígito
numeros_multi_digito = [12, 5, 27, 11, 38]
ordenados_ultimo_digito = sorted(numeros_multi_digito, key=lambda x: x % 10)
print(f"Ordenados por último dígito (sorted + lambda): {ordenados_ultimo_digito}")

# Uso con reduce (si es necesario, aunque a menudo hay alternativas más claras)
producto_pares = functools.reduce(
    lambda acc, x: acc * x if x % 2 == 0 else acc,
    numeros_lambda,
    1 # Inicializador es 1 para la multiplicación
)
print(f"Producto de los pares (reduce + lambda): {producto_pares}")

# Uso para crear una función simple devuelta por una HOF (similar a crear_multiplicador)
def crear_sumador(n):
    return lambda x: x + n

sumador_5 = crear_sumador(5)
print(f"Sumador 5 aplicado a 10: {sumador_5(10)}") # Salida: 15

print("-" * 60)

# ---------------------------------------------------------------------------
# 6. PARTIAL APPLICATION (APLICACIÓN PARCIAL) CON functools.partial
# ---------------------------------------------------------------------------

# La aplicación parcial es una técnica relacionada con las HOFs donde se toma
# una función y se "fijan" algunos de sus argumentos, produciendo una nueva
# función con una aridad (número de argumentos) menor. `functools.partial`
# es una HOF que facilita esto.

print("--- 6. Aplicación Parcial con functools.partial ---")

# Función original con varios argumentos
def potencia(base, exponente):
    """Calcula la base elevada al exponente."""
    return base ** exponente

# Crear una función especializada para calcular potencias de 2
potencia_de_dos = functools.partial(potencia, 2) # Fija el primer argumento (base) a 2
print(f"Potencia de dos (3): {potencia_de_dos(3)}") # Llama potencia(2, 3) -> 8
print(f"Potencia de dos (5): {potencia_de_dos(5)}") # Llama potencia(2, 5) -> 32

# Crear una función especializada para calcular cubos
cubo = functools.partial(potencia, exponente=3) # Fija el argumento 'exponente' a 3
print(f"Cubo de 4: {cubo(4)}") # Llama potencia(4, exponente=3) -> 64
print(f"Cubo de 5: {cubo(5)}") # Llama potencia(5, exponente=3) -> 125

# Puede ser útil para adaptar funciones a interfaces que esperan menos argumentos
# (como en callbacks o al usar map/filter si la función original tiene más args)
def procesar_dato(dato, factor, offset):
    return (dato * factor) + offset

# Supongamos que map solo puede pasar un argumento (el elemento de la lista)
# Queremos aplicar procesar_dato con factor=10 y offset=1 a una lista
datos = [1, 2, 3, 4]
procesador_fijo = functools.partial(procesar_dato, factor=10, offset=1)
# Ahora procesador_fijo solo espera el argumento 'dato'
datos_procesados = list(map(procesador_fijo, datos))
print(f"Datos procesados con partial: {datos_procesados}") # [11, 21, 31, 41]

# Comparación con lambda para el mismo caso:
datos_procesados_lambda = list(map(lambda d: procesar_dato(d, factor=10, offset=1), datos))
print(f"Datos procesados con lambda: {datos_procesados_lambda}") # Mismo resultado
# `partial` puede ser más legible si la función original es compleja o tiene muchos argumentos fijos.

print("-" * 60)

# ---------------------------------------------------------------------------
# 7. CONCLUSIONES Y VENTAJAS DE LAS HOFs
# ---------------------------------------------------------------------------

print("--- 7. Conclusiones ---")

# Las Higher-Order Functions son un pilar fundamental de la programación funcional
# y ofrecen varias ventajas en Python:

# - **Abstracción:** Permiten abstraer patrones de control (como iterar y aplicar,
#   filtrar, reducir, decorar) en funciones reutilizables.
# - **Reutilización de Código:** Se puede escribir código más genérico que opere
#   sobre diferentes comportamientos (definidos por las funciones pasadas como argumento).
# - **Composición:** Facilitan la combinación de funciones para crear comportamientos complejos
#   a partir de piezas más simples (ej: decoradores apilados, pipelines con map/filter).
# - **Expresividad:** A menudo permiten escribir código más conciso y declarativo,
#   especialmente cuando se combinan con lambdas (ej: `sorted(..., key=lambda...)`).
# - **Flexibilidad:** Patrones como los decoradores y las factorías de funciones (closures)
#   ofrecen mecanismos poderosos para extender o modificar comportamiento dinámicamente.

# Sin embargo, un uso excesivo o complejo (especialmente de closures anidados o
# lambdas muy complicadas) puede a veces reducir la legibilidad. Es importante
# encontrar un equilibrio.

print("\n¡Fin de los apuntes sobre Higher-Order Functions en Python!")
print("-" * 60)

# Puedes ejecutar este script para ver todos los ejemplos en acción.