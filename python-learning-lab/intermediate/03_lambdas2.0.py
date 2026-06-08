# -*- coding: utf-8 -*-

# ##############################################
# ##      APUNTES COMPLETOS SOBRE LAMBDAS     ##
# ##            EN PYTHON (EXPLICADO)         ##
# ##############################################

# ==============================================================================
# 1. INTRODUCCIÓN: ¿QUÉ SON LAS FUNCIONES LAMBDA?
# ==============================================================================

# - Las funciones lambda son funciones ANÓNIMAS, es decir, funciones sin un nombre
#   definido formalmente con la palabra clave `def`.
# - Se crean usando la palabra clave `lambda`.
# - Son funciones pequeñas, generalmente de UNA SOLA LÍNEA.
# - Su principal propósito es definir funciones rápidas y cortas, especialmente
#   cuando necesitas pasar una función como argumento a otra función (funciones
#   de orden superior como `map`, `filter`, `sorted`, etc.).
# - No son un reemplazo completo para las funciones normales (`def`), ya que tienen
#   limitaciones importantes (principalmente, solo pueden contener una expresión).

print("--- 1. Introducción ---")
print("Las lambdas son funciones anónimas de una sola expresión.")
print("-" * 20)

# ==============================================================================
# 2. SINTAXIS BÁSICA
# ==============================================================================

# La sintaxis general de una función lambda es:
#
# lambda argumentos: expresion
#
# - `lambda`: Palabra clave que indica la creación de una función anónima.
# - `argumentos`: Una lista opcional de argumentos de entrada (parámetros)
#                 separados por comas (igual que en `def`). Puede tener cero,
#                 uno o más argumentos.
# - `:`: Separa los argumentos de la expresión.
# - `expresion`: Una *única* expresión Python válida que se evalúa cuando se
#                llama a la función lambda. El resultado de esta expresión
#                es lo que la función devuelve *implícitamente* (no se usa `return`).

print("--- 2. Sintaxis ---")
print("Sintaxis: lambda argumentos: expresion")
# Ejemplo conceptual (no se ejecuta directamente así)
# lambda x: x * 2
# lambda x, y: x + y
# lambda: "Hola Mundo" # Sin argumentos
print("-" * 20)

# ==============================================================================
# 3. EJEMPLOS BÁSICOS DE CREACIÓN Y USO
# ==============================================================================

print("--- 3. Ejemplos Básicos ---")

# 3.1. Lambda sin argumentos
# --------------------------
# Devuelve un valor constante o realiza una acción simple sin entrada.
saludo = lambda: "¡Hola desde lambda!"
print(f"Lambda sin argumentos: {saludo()}")

# 3.2. Lambda con un argumento
# ----------------------------
# Toma un argumento y realiza una operación con él.
def cuadradox(x):
    return x* x

cuadrado = lambda x: x * x
print(f"Lambda con un argumento (cuadrado de 5): {cuadrado(5)}")

incrementar = lambda num: num + 1
print(f"Lambda con un argumento (incrementar 10): {incrementar(10)}")

# 3.3. Lambda con múltiples argumentos
# -----------------------------------
# Toma varios argumentos y los combina o procesa.
suma = lambda x, y: x + y
print(f"Lambda con dos argumentos (suma 3 + 4): {suma(3, 4)}")

producto = lambda a, b, c: a * b * c
print(f"Lambda con tres argumentos (producto 2*3*4): {producto(2, 3, 4)}")

# 3.4. Lambda con argumentos por defecto
# --------------------------------------
# Funciona igual que en las funciones `def`.
potencia = lambda base, exponente=2: base ** exponente
print(f"Lambda con argumento por defecto (5^2): {potencia(5)}")
print(f"Lambda con argumento por defecto (5^3, especificando): {potencia(5, 3)}")

# 3.5. Lambda con *args (argumentos posicionales variables)
# --------------------------------------------------------
# Para aceptar un número variable de argumentos posicionales.
suma_variable = lambda *args: sum(args)
print(f"Lambda con *args (suma 1, 2, 3): {suma_variable(1, 2, 3)}")
print(f"Lambda con *args (suma 10, 20, 30, 40): {suma_variable(10, 20, 30, 40)}")

# 3.6. Lambda con **kwargs (argumentos de palabra clave variables)
# --------------------------------------------------------------
# Para aceptar un número variable de argumentos de palabra clave.
mostrar_kwargs = lambda **kwargs: kwargs # Devuelve un diccionario con los kwargs
print(f"Lambda con **kwargs (nombre='Ana', edad=25): {mostrar_kwargs(nombre='Ana', edad=25)}")

# 3.7. Lambda combinando tipos de argumentos
# -----------------------------------------
# El orden debe ser: argumentos posicionales, *args, **kwargs.
# Argumentos por defecto van después de los posicionales sin defecto.
combinada = lambda x, y=10, *args, **kwargs: (x, y, args, kwargs)
print(f"Lambda combinada (1, 20, 30, 40, z=50): {combinada(1, 20, 30, 40, z=50)}")
# Output: (1, 20, (30, 40), {'z': 50}) -> x=1, y=20 (override default), args=(30, 40), kwargs={'z': 50}

print("-" * 20)

# ==============================================================================
# 4. COMPARACIÓN CON FUNCIONES DEFINIDAS CON `def`
# ==============================================================================

print("--- 4. Comparación con `def` ---")

# Una función `def` equivalente a `suma = lambda x, y: x + y` sería:
def suma_def(x, y):
  """Esta función suma dos números (definida con def)."""
  return x + y

# El resultado es el mismo
print(f"Resultado suma con lambda (5, 6): {suma(5, 6)}")
print(f"Resultado suma con def (5, 6):    {suma_def(5, 6)}")

# Diferencias Clave:
# ------------------
# 1. Nombre: `def` asigna un nombre a la función. `lambda` crea un objeto función
#    anónimo. Aunque puedes asignar una lambda a una variable (como `suma = ...`),
#    su `__name__` interno sigue siendo '<lambda>', lo que puede afectar a
#    tracebacks y debugging.
print(f"Nombre de la función def: {suma_def.__name__}")    # Output: suma_def
print(f"Nombre de la función lambda: {suma.__name__}") # Output: <lambda>

# 2. Cuerpo de la función: `def` puede contener múltiples sentencias (asignaciones,
#    bucles `for`/`while`, condicionales `if`/`elif`/`else`, `try`/`except`, etc.).
#    `lambda` SOLO puede contener UNA ÚNICA EXPRESIÓN. No puede contener sentencias.
#    (Aunque la expresión puede llamar a otra función que sí contenga sentencias).

# 3. `return` explícito: `def` requiere una sentencia `return` explícita para
#    devolver un valor (si no, devuelve `None`). `lambda` devuelve implícitamente
#    el resultado de su expresión.

# 4. Docstrings: Las funciones `def` pueden (y deben) tener docstrings (`"""Doc..."""`)
#    para documentación, accesibles a través de `__doc__`. Las lambdas no pueden
#    tener docstrings.
print(f"Docstring de suma_def: {suma_def.__doc__}")
# print(f"Docstring de suma (lambda): {suma.__doc__}") # AttributeError o None

# 5. Complejidad: `lambda` está diseñada para funciones muy simples. Si la lógica
#    es mínimamente compleja o requiere más de una línea, SIEMPRE es mejor usar `def`
#    por claridad y mantenibilidad.

# ¿Cuándo asignar una lambda a una variable?
# Generalmente se desaconseja si la función tiene un propósito claro o se reutiliza,
# ya que `def` es más explícito y mejor para debugging. Sin embargo, a veces se usa
# para funciones muy triviales y locales. La principal fortaleza de lambda es su
# uso *in situ* como argumento de otras funciones.

print("-" * 20)

# ==============================================================================
# 5. CASOS DE USO PRINCIPALES (FUNCIONES DE ORDEN SUPERIOR)
# ==============================================================================

print("--- 5. Casos de Uso (Funciones de Orden Superior) ---")

# El uso más común e idiomático de las lambdas es pasarlas como argumento
# a funciones que esperan otra función (funciones de orden superior).

numeros = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
palabras = ["python", "lambda", "map", "filter", "sorted"]

# 5.1. `map(funcion, iterable)`
# -----------------------------
# Aplica la `funcion` a cada elemento del `iterable` y devuelve un iterador
# con los resultados. Lambda es perfecta para definir la `funcion` rápidamente.

# Ejemplo: Obtener el cuadrado de cada número
cuadrados = list(map(lambda x: x * x, numeros))
print(f"map() para cuadrados: {cuadrados}")

# Ejemplo: Convertir números a cadenas
numeros_str = list(map(lambda x: f"Num-{x}", numeros))
print(f"map() para convertir a string: {numeros_str}")

# Ejemplo: Obtener la longitud de cada palabra
longitudes = list(map(lambda s: len(s), palabras))
print(f"map() para longitudes de palabras: {longitudes}")

# 5.2. `filter(funcion, iterable)`
# --------------------------------
# Filtra los elementos del `iterable`, manteniendo solo aquellos para los que
# la `funcion` devuelve `True`. Lambda es ideal para definir la condición de filtrado.

# Ejemplo: Obtener solo los números pares
pares = list(filter(lambda x: x % 2 == 0, numeros))
print(f"filter() para números pares: {pares}")

# Ejemplo: Obtener números mayores que 5
mayores_5 = list(filter(lambda x: x > 5, numeros))
print(f"filter() para números > 5: {mayores_5}")

# Ejemplo: Obtener palabras con más de 5 letras
largas = list(filter(lambda s: len(s) > 5, palabras))
print(f"filter() para palabras largas: {largas}")

# 5.3. `sorted(iterable, key=funcion, reverse=False)`
# --------------------------------------------------
# Ordena los elementos del `iterable`. Lambda se usa comúnmente para el
# argumento `key`, que especifica una función que extrae una "clave de
# comparación" de cada elemento.

# Ejemplo: Ordenar números por su valor (comportamiento por defecto, lambda no necesaria)
# sorted(numeros)

# Ejemplo: Ordenar palabras por longitud
palabras_ordenadas_long = sorted(palabras, key=lambda s: len(s))
print(f"sorted() por longitud de palabra: {palabras_ordenadas_long}")

# Ejemplo: Ordenar palabras por la última letra
palabras_ordenadas_ult = sorted(palabras, key=lambda s: s[-1])
print(f"sorted() por última letra: {palabras_ordenadas_ult}")

# Ejemplo: Ordenar una lista de tuplas por el segundo elemento
puntos = [(1, 5), (3, 2), (8, 10), (4, 7)]
puntos_ordenados = sorted(puntos, key=lambda p: p[1])
print(f"sorted() tuplas por 2º elemento: {puntos_ordenados}")

# Ejemplo: Ordenar una lista de diccionarios por un valor
personas = [{'nombre': 'Ana', 'edad': 30}, {'nombre': 'Juan', 'edad': 25}, {'nombre': 'Eva', 'edad': 35}]
personas_ordenadas_edad = sorted(personas, key=lambda p: p['edad'])
print(f"sorted() diccionarios por edad: {personas_ordenadas_edad}")

# 5.4. `functools.reduce(funcion, iterable[, initial])` (Menos común hoy en día)
# ----------------------------------------------------------------------------
# Aplica la `funcion` (que debe tomar dos argumentos) de forma acumulativa a los
# elementos del `iterable`. Lambda puede definir esta función acumuladora.
# Nota: A menudo, `sum()`, `min()`, `max()` o bucles/comprensiones son más legibles.
from functools import reduce

# Ejemplo: Calcular el producto de todos los números
producto_total = reduce(lambda x, y: x * y, numeros)
print(f"reduce() para producto total: {producto_total}")

# Ejemplo: Encontrar el número más grande (aunque max() es mejor)
maximo_reduce = reduce(lambda x, y: x if x > y else y, numeros)
print(f"reduce() para encontrar el máximo: {maximo_reduce}")

print("-" * 20)

# ==============================================================================
# 6. OTROS USOS Y CARACTERÍSTICAS
# ==============================================================================

print("--- 6. Otros Usos y Características ---")

# 6.1. Lambdas y Closures (Cierres Léxicos)
# -----------------------------------------
# Una lambda, como cualquier función interna en Python, puede "capturar"
# variables del ámbito (scope) donde fue definida. Esto se llama closure.

def crear_multiplicador(n):
  """Esta función devuelve una lambda que multiplica por n."""
  return lambda x: x * n # La lambda "recuerda" el valor de n

duplicar = crear_multiplicador(2) # n=2 queda capturado
triplicar = crear_multiplicador(3) # n=3 queda capturado

print(f"Closure - duplicar(10): {duplicar(10)}")   # Output: 20
print(f"Closure - triplicar(10): {triplicar(10)}") # Output: 30
# Cada lambda tiene su propia copia (referencia) de 'n' del momento en que se creó.

# 6.2. Uso de expresiones condicionales (operador ternario)
# --------------------------------------------------------
# Como lambda solo admite una expresión, la forma de hacer condicionales es
# usar la expresión ternaria: `valor_si_true if condicion else valor_si_false`.

maximo = lambda a, b: a if a > b else b
print(f"Lambda con condicional (max(15, 8)): {maximo(15, 8)}") # Output: 15

par_o_impar = lambda num: "Par" if num % 2 == 0 else "Impar"
print(f"Lambda con condicional (7 es Par/Impar): {par_o_impar(7)}") # Output: Impar

# 6.3. Lambdas en estructuras de datos
# ------------------------------------
# Puedes almacenar lambdas en listas, diccionarios, etc.

operaciones = {
    'sumar': lambda x, y: x + y,
    'restar': lambda x, y: x - y,
    'multiplicar': lambda x, y: x * y
}
op = 'multiplicar'
num1, num2 = 7, 6
print(f"Ejecutando desde diccionario: {op}({num1}, {num2}) = {operaciones[op](num1, num2)}") # Output: 42

# Lista de funciones para aplicar en secuencia
transformaciones = [
    lambda x: x + 5,    # Añadir 5
    lambda x: x * 2,    # Multiplicar por 2
    lambda x: x - 3     # Restar 3
]
valor_inicial = 10
valor_transformado = valor_inicial
for func in transformaciones:
    valor_transformado = func(valor_transformado)
print(f"Aplicando lista de lambdas a {valor_inicial}: {valor_transformado}") # Output: 27 (10+5=15, 15*2=30, 30-3=27)

# 6.4. Uso inmediato (IIFE - Immediately Invoked Function Expression)
# -------------------------------------------------------------------
# Puedes definir y llamar una lambda en la misma línea. Menos común en Python
# que en otros lenguajes como JavaScript, pero posible.

resultado_directo = (lambda x, y: x * y)(6, 7)
print(f"Lambda de uso inmediato (6 * 7): {resultado_directo}") # Output: 42

print("-" * 20)

# ==============================================================================
# 7. ¡CUIDADO! EL PROBLEMA DEL "LATE BINDING" EN BUCLES
# ==============================================================================

print("--- 7. Cuidado: Late Binding en Bucles ---")

# Un error común ocurre al definir lambdas dentro de un bucle que dependen de
# la variable del bucle. Las lambdas NO capturan el valor de la variable en
# cada iteración, sino que capturan la *variable misma*. Evalúan la variable
# cuando son *llamadas*, momento en el cual el bucle ya ha terminado y la
# variable tiene su valor final.

funciones_erroneas = []
for i in range(5):
    # Todas estas lambdas referencian la misma variable 'i'
    funciones_erroneas.append(lambda: i)

print("Intentando llamar lambdas creadas en bucle (resultado incorrecto):")
# Cuando se llaman, 'i' ya vale 4 (el último valor del range(5))
for f in funciones_erroneas:
    print(f()) # Imprime 4, 4, 4, 4, 4 ¡Incorrecto!

# --- Solución 1: Usar argumentos por defecto ---
# Los argumentos por defecto se evalúan en el momento de la *definición* de
# la lambda, capturando así el valor actual de la variable del bucle.

funciones_correctas_v1 = []
for i in range(5):
    # El valor actual de 'i' se asigna a 'valor' cuando se crea la lambda
    funciones_correctas_v1.append(lambda valor=i: valor)

print("\nLlamando lambdas con argumento por defecto (resultado correcto):")
for f in funciones_correctas_v1:
    print(f()) # Imprime 0, 1, 2, 3, 4 ¡Correcto!

# --- Solución 2: Usar una función generadora (closure) ---
# Similar al ejemplo de `crear_multiplicador`, creamos una función externa
# que genere la lambda, creando un nuevo scope y capturando el valor.

def crear_printer(valor_capturado):
    # Esta función crea y devuelve una lambda que usa el valor_capturado
    return lambda: valor_capturado

funciones_correctas_v2 = []
for i in range(5):
    funciones_correctas_v2.append(crear_printer(i)) # Llama a la fábrica en cada iteración

print("\nLlamando lambdas creadas con función generadora (resultado correcto):")
for f in funciones_correctas_v2:
    print(f()) # Imprime 0, 1, 2, 3, 4 ¡Correcto!

# --- Solución 3: Usar `functools.partial` (más avanzado) ---
# `partial` puede "fijar" argumentos a una función.
from functools import partial

funciones_correctas_v3 = []
# Definimos una lambda genérica que acepta un argumento
base_lambda = lambda val: val
for i in range(5):
    # Creamos una nueva función (parcial) donde 'val' está fijado al valor actual de 'i'
    f = partial(base_lambda, i)
    funciones_correctas_v3.append(f)

print("\nLlamando lambdas creadas con functools.partial (resultado correcto):")
for f in funciones_correctas_v3:
    print(f()) # Imprime 0, 1, 2, 3, 4 ¡Correcto!


print("-" * 20)

# ==============================================================================
# 8. LIMITACIONES DE LAS LAMBDAS
# ==============================================================================

print("--- 8. Limitaciones ---")

# 1.  **Solo una expresión:** Es la limitación más importante. No puedes tener
#     múltiples líneas de código, ni sentencias como `if/elif/else` completas
#     (solo la expresión ternaria), ni bucles `for`/`while`, ni `try/except`,
#     ni `pass`, `assert`, `yield`, o `return` explícito. Tampoco puedes hacer
#     asignaciones directas (`=`) dentro de la lambda (excepto en Python 3.8+
#     con el operador morsa `:=`, pero su uso en lambdas debe ser cuidadoso
#     y puede afectar la legibilidad).
#     *Ejemplo Inválido:* `lambda x: if x > 0: print(x) else: print("No")` -> SyntaxError
#     *Ejemplo Válido (llamando print):* `lambda x: print(x)` (la expresión es la llamada a print)
#     *Ejemplo Válido (operador morsa, Python 3.8+):* `lambda x: (y := x * 2) + y`

# 2.  **Anónimas:** Como se mencionó, su nombre es `<lambda>`, lo que puede hacer
#     el debugging (seguimiento de errores) más difícil. Los mensajes de error
#     pueden ser menos informativos.

# 3.  **Sin Docstrings:** No puedes incluir documentación formal (`__doc__`).

# 4.  **Legibilidad:** Si la única expresión se vuelve muy compleja, la lambda
#     puede ser difícil de leer y entender. En esos casos, una función `def`
#     normal es casi siempre preferible. La regla general es: si dudas, usa `def`.

print("Limitaciones principales: solo una expresión, anónimas, sin docstrings.")
print("-" * 20)

# ==============================================================================
# 9. CONCLUSIÓN: ¿CUÁNDO USAR LAMBDAS?
# ==============================================================================

print("--- 9. Conclusión ---")

# Las funciones lambda son una herramienta útil y concisa en Python, pero
# no son una solución universal. Úsalas principalmente cuando necesites:
#
# - Una función simple y corta que se pasará como argumento a otra función
#   (especialmente `map`, `filter`, `sorted`, y callbacks en GUIs o eventos).
# - Definir rápidamente una función "clave" para operaciones como la ordenación.
# - Crear closures simples (como en el ejemplo del multiplicador).
# - La lógica es trivial y cabe cómodamente en una sola expresión legible.
#
# Evita las lambdas (y usa `def` en su lugar) cuando:
#
# - La lógica requiere múltiples pasos, sentencias o es compleja.
# - La función necesita un nombre descriptivo para claridad o reutilización.
# - Necesitas documentación (docstrings).
# - La depuración puede ser complicada (una `def` facilita el seguimiento).

print("Usar lambdas para funciones simples como argumentos de otras funciones.")
print("Usar `def` para lógica compleja, reutilización y claridad.")
print("-" * 20)

# Fin de los apuntes sobre lambdas.