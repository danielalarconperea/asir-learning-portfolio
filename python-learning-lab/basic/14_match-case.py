#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
=================================================
 Apuntes Completos sobre match-case en Python
=================================================

Introducción:
-------------
La declaración `match-case` (Structural Pattern Matching) se introdujo en Python 3.10 (PEP 634, PEP 635, PEP 636).
Permite comparar un valor (el "sujeto") contra una serie de patrones ("cases").
Es similar a la declaración `switch` en otros lenguajes como C++ o Java, pero mucho más potente
porque permite hacer coincidir patrones complejos basados en la *estructura* de los datos,
no solo en valores literales.

Utilidad Principal:
-------------------
- Desempaquetar y procesar estructuras de datos complejas (listas, tuplas, diccionarios, objetos)
  de una manera legible y concisa.
- Reemplazar cadenas largas y complejas de `if/elif/else` cuando se verifica el tipo y la estructura
  de una variable.
- Procesar diferentes tipos de mensajes, eventos o comandos en una aplicación.

Sintaxis Básica:
----------------
match sujeto:
    case patron_1:
        # Bloque de código si el sujeto coincide con patron_1
        ...
    case patron_2:
        # Bloque de código si el sujeto coincide con patron_2
        ...
    case patron_N:
        # Bloque de código si el sujeto coincide con patron_N
        ...
    case _: # Patrón comodín (wildcard) - Opcional pero recomendado
        # Bloque de código si ninguno de los patrones anteriores coincide
        ...

- `sujeto`: La variable o valor que se quiere comparar.
- `case`: Introduce un patrón a comparar.
- `patron_X`: Define la estructura o valor que se busca. Python evalúa los `case` en orden
             y ejecuta el bloque de código del *primer* patrón que coincida.
- `_` (underscore): Es el patrón comodín (wildcard). Coincide con *cualquier* valor sin asignarlo
                   a una variable. Se usa típicamente como el último `case` para manejar
                   situaciones no contempladas explícitamente (similar al `else` en `if/elif/else`).

"""

# Importaciones para ejemplos más avanzados (clases)
from dataclasses import dataclass

# --- 1. Patrones Literales ---
# Coinciden con valores exactos: números, strings, booleanos, None.
print("--- 1. Patrones Literales ---")

def describir_valor(valor):
    """Describe un valor usando patrones literales."""
    match valor:
        case 42:
            print("El valor es el número entero 42.")
        case "hola":
            print("El valor es el string 'hola'.")
        case 3.14:
            print("El valor es el número flotante 3.14.")
        case True:
            print("El valor es el booleano True.")
        case None:
            print("El valor es None.")
        case _: # Comodín para cualquier otro valor
            print(f"El valor es {valor} (otro tipo/valor).")

describir_valor(42)
describir_valor("hola")
describir_valor(True)
describir_valor(None)
describir_valor(100)
describir_valor([1, 2])
print("-" * 20)


# --- 2. Patrones de Captura ---
# Un nombre de variable simple (ej: `x`) actúa como un patrón de captura.
# Coincide con cualquier valor y lo *asigna* a esa variable dentro del bloque `case`.
# ¡OJO! Un nombre de variable simple *siempre* coincide, a menos que sea un literal
# conocido como True, False o None.
print("--- 2. Patrones de Captura ---")

def procesar_entrada(entrada):
    """Demuestra la captura de variables."""
    match entrada:
        case None: # Esto es un patrón literal, no de captura
            print("Se recibió None.")
        case x: # Patrón de captura: coincide con cualquier cosa y la asigna a 'x'
            print(f"Se capturó el valor: {x} (tipo: {type(x).__name__})")
            # Podemos usar 'x' dentro de este bloque
            if isinstance(x, int) and x > 100:
                print("   (Es un entero mayor que 100)")

procesar_entrada(99)
procesar_entrada("un texto")
procesar_entrada([1, 2, 3])
procesar_entrada(None) # Coincide con el primer case literal
print("-" * 20)

# --- 3. El Patrón Comodín (_) ---
# Como se vio antes, `_` coincide con cualquier cosa, pero *no* la asigna a una variable.
# Se usa cuando no necesitas el valor coincidente, solo saber que algo coincidió.
# Es útil para ignorar partes de una estructura o como caso por defecto.
print("--- 3. El Patrón Comodín (_) ---")

def identificar_tipo_basico(dato):
    """Usa el comodín para tipos no específicos."""
    match dato:
        case int(): # Coincide si 'dato' es una instancia de int (ver patrones de clase más adelante)
            print("Es un entero.")
        case str(): # Coincide si 'dato' es una instancia de str
            print("Es una cadena de texto.")
        case _: # Comodín para cualquier otro tipo
            print(f"Es de otro tipo: {type(dato).__name__}")

identificar_tipo_basico(123)
identificar_tipo_basico("python")
identificar_tipo_basico([1, 2])
identificar_tipo_basico(3.14)
print("-" * 20)


# --- 4. Patrones OR (|) ---
# Permiten combinar varios patrones en un solo `case`. Si el sujeto coincide
# con *cualquiera* de los patrones unidos por `|`, el bloque se ejecuta.
# Todos los subpatrones deben asignar las *mismas* variables o ninguna.
print("--- 4. Patrones OR (|) ---")

def manejar_comando(comando):
    """Usa patrones OR para agrupar comandos similares."""
    match comando:
        case "start" | "iniciar":
            print("Iniciando proceso...")
        case "stop" | "parar" | "detener":
            print("Deteniendo proceso...")
        case "status" | "estado":
            print("Mostrando estado actual...")
        case code if isinstance(code, int) and 100 <= code < 200: # Combina OR implícito con guarda
             print(f"Código de información: {code}")
        case code if isinstance(code, int) and 400 <= code < 500:
             print(f"Código de error de cliente: {code}")
        case _:
            print(f"Comando desconocido: {comando}")

manejar_comando("start")
manejar_comando("parar")
manejar_comando("estado")
manejar_comando(101)
manejar_comando(404)
manejar_comando("otro")
print("-" * 20)


# --- 5. Patrones AS (as) ---
# Permiten asignar el valor que coincide con un patrón más complejo a una variable.
# Sintaxis: `patron as nombre_variable`
print("--- 5. Patrones AS (as) ---")

def procesar_punto_as(punto):
    """Usa 'as' para capturar la tupla completa además de sus componentes."""
    match punto:
        case (0, 0):
            print("El punto está en el origen.")
        # Captura las coordenadas en x e y, Y TAMBIÉN la tupla completa en 'p'
        case (x, y) as p:
            print(f"Punto en ({x}, {y}). La tupla completa es: {p}")
            # Podemos usar 'p' aquí
            print(f"   Distancia al origen (aprox): {(x**2 + y**2)**0.5:.2f}")
        case _:
            print("Formato de punto no reconocido.")

procesar_punto_as((0, 0))
procesar_punto_as((3, 4))
procesar_punto_as("no es un punto")
print("-" * 20)


# --- 6. Guardas (if condition) ---
# Permiten añadir una condición booleana a un patrón.
# El `case` solo coincide si el patrón coincide *y* la condición de la guarda es `True`.
# Sintaxis: `case patron if condicion:`
print("--- 6. Guardas (if condition) ---")

def filtrar_numeros(numero):
    """Usa guardas para añadir condiciones a los patrones."""
    match numero:
        # Captura 'num' si es un entero Y num es positivo
        case num if isinstance(num, int) and num > 0:
            print(f"{num} es un entero positivo.")
        # Captura 'num' si es un entero Y num es negativo
        case num if isinstance(num, int) and num < 0:
            print(f"{num} es un entero negativo.")
        case 0: # Patrón literal para cero
            print("El número es cero.")
        case flt if isinstance(flt, float):
            print(f"{flt} es un número flotante.")
        case _:
            print(f"{numero} no es un número reconocido o es cero.")

filtrar_numeros(10)
filtrar_numeros(-5)
filtrar_numeros(0)
filtrar_numeros(3.14)
filtrar_numeros("texto")
print("-" * 20)


# --- 7. Patrones de Secuencia ---
# Coinciden con listas o tuplas.
# Pueden tener longitud fija o variable usando `*`.
print("--- 7. Patrones de Secuencia ---")

def procesar_secuencia(seq):
    """Demuestra varios patrones de secuencia."""
    match seq:
        # Secuencia vacía (lista o tupla)
        case [] | ():
            print("Secuencia vacía.")
        # Secuencia con exactamente un elemento (capturado en 'item')
        case [item] | (item,): # Ojo a la coma para tupla de un elemento
            print(f"Secuencia con un elemento: {item}")
        # Lista con exactamente dos elementos (capturados en 'x', 'y')
        case [x, y]:
            print(f"Lista de dos elementos: {x}, {y}")
        # Tupla con exactamente tres elementos
        case (x, y, z):
            print(f"Tupla de tres elementos: {x}, {y}, {z}")
        # Lista que empieza con "CMD" y tiene al menos un argumento más
        # 'comando' captura "CMD", 'args' captura el resto como una lista
        case ["CMD", *args]:
            print(f"Comando 'CMD' con argumentos: {args}")
        # Tupla que termina con 0
        # 'inicio' captura todo excepto el último elemento como una lista
        case (*inicio, 0):
             print(f"Tupla que termina en 0. Elementos iniciales: {inicio}")
        # Lista con al menos dos elementos, captura el primero y el último
        # 'medio' captura los elementos intermedios como una lista
        case [primero, *medio, ultimo]:
             print(f"Lista con primero={primero}, ultimo={ultimo}. Medio: {medio}")
        # Secuencia de cualquier otro tipo (no coincide con los anteriores)
        case list() as l:
             print(f"Es una lista no reconocida: {l}")
        case tuple() as t:
             print(f"Es una tupla no reconocida: {t}")
        case _:
            print(f"No es una lista o tupla procesable: {seq}")

procesar_secuencia([])
procesar_secuencia(["Hola"])
procesar_secuencia((10,))
procesar_secuencia([1, 2])
procesar_secuencia((10, 20, 30))
procesar_secuencia(["CMD", "arg1", "arg2"])
procesar_secuencia(["CMD"]) # No coincide con ["CMD", *args] porque args sería []
procesar_secuencia(("a", "b", "c", 0))
procesar_secuencia([1, 2, 3, 4, 5])
procesar_secuencia({}) # No es secuencia
procesar_secuencia((1, 2, 3, 4)) # Tupla no reconocida
print("-" * 20)


# --- 8. Patrones de Mapeo (Diccionarios) ---
# Coinciden con diccionarios.
# Pueden verificar la presencia de claves específicas y capturar sus valores.
# Pueden usar `**rest` para capturar las claves y valores restantes.
print("--- 8. Patrones de Mapeo (Diccionarios) ---")

def procesar_diccionario(data):
    """Demuestra patrones de mapeo."""
    match data:
        # Diccionario vacío
        case {}:
            print("Diccionario vacío.")
        # Diccionario con exactamente la clave "nombre" (valor capturado en 'n')
        # y la clave "edad" (valor capturado en 'e')
        case {"nombre": n, "edad": e}:
            print(f"Persona: {n}, Edad: {e}")
        # Diccionario que contiene la clave "ciudad" con el valor literal "Madrid"
        # y captura el resto de claves/valores en el diccionario 'resto'
        case {"ciudad": "Madrid", **resto}:
            print(f"Vive en Madrid. Otros datos: {resto}")
        # Diccionario que DEBE tener la clave "status", cuyo valor se captura en 's'
        # y opcionalmente otras claves capturadas en 'detalle'
        case {"status": s, **detalle} if s == "error":
            print(f"Error detectado. Detalles: {detalle}")
        # Diccionario que contiene al menos la clave "id" (valor capturado)
        # No importa qué otras claves tenga (implícito por no usar **rest)
        case {"id": user_id}:
            print(f"Diccionario con ID de usuario: {user_id}")
        # Cualquier otro diccionario
        case dict() as d:
             print(f"Otro diccionario no reconocido: {d}")
        case _:
            print(f"No es un diccionario procesable: {data}")

procesar_diccionario({})
procesar_diccionario({"nombre": "Ana", "edad": 30})
procesar_diccionario({"ciudad": "Madrid", "profesion": "Ingeniera"})
procesar_diccionario({"status": "error", "codigo": 500, "mensaje": "Fallo interno"})
procesar_diccionario({"status": "ok"}) # No coincide con el caso de error
procesar_diccionario({"id": 12345, "extra": "dato"})
procesar_diccionario({"clave": "valor"}) # Otro diccionario
procesar_diccionario("no es diccionario")
print("-" * 20)


# --- 9. Patrones de Clase ---
# Coinciden con instancias de clases específicas.
# Pueden verificar los valores de atributos específicos.
# La sintaxis es `NombreClase(atributo1=patron1, atributo2=patron2, ...)`.
# También pueden usar atributos posicionales si la clase define `__match_args__`.
print("--- 9. Patrones de Clase ---")

# Definimos algunas clases para los ejemplos
@dataclass
class Punto:
    x: int
    y: int

@dataclass
class Circulo:
    centro: Punto
    radio: float

class Rectangulo:
    # Sin dataclass, definimos __init__ y __match_args__ (opcional)
    # __match_args__ define qué atributos se usan para coincidencia posicional
    __match_args__ = ("ancho", "alto", "color")

    def __init__(self, ancho, alto, color="azul"):
        self.ancho = ancho
        self.alto = alto
        self.color = color

    # Es buena idea definir __repr__ para una mejor visualización
    def __repr__(self):
        return f"Rectangulo(ancho={self.ancho}, alto={self.alto}, color='{self.color}')"

def procesar_figura(figura):
    """Demuestra patrones de clase."""
    match figura:
        # Coincide con cualquier instancia de Punto
        # Captura los atributos 'x' e 'y' usando el nombre del atributo
        case Punto(x=px, y=py):
            print(f"Es un Punto en ({px}, {py})")
        # Coincide con un Punto específico en el origen (usando literales)
        case Punto(x=0, y=0): # Este caso nunca se alcanzará por el anterior más general! Orden importa.
             print("Punto en el origen (nunca se alcanza aquí).") # Demuestra importancia del orden

        # Coincide con un Círculo, captura su radio 'r' y su centro en 'c'
        case Circulo(centro=c, radio=r):
            print(f"Es un Círculo con centro {c} y radio {r}")
            # Podemos anidar patrones:
            match c:
                case Punto(0, 0):
                    print("   (El círculo está centrado en el origen)")

        # Coincide con un Rectángulo usando atributos nombrados
        case Rectangulo(ancho=a, alto=alt, color="rojo"):
            print(f"Es un Rectángulo rojo de {a}x{alt}")

        # Coincide con un Rectángulo usando atributos posicionales (__match_args__)
        # Captura ancho en 'w', alto en 'h', y el color por defecto
        case Rectangulo(w, h): # Coincide con Rectangulo(ancho=w, alto=h)
            print(f"Es un Rectángulo (posición) de {w}x{h} (color por defecto o no especificado)")

        # Coincide con un Rectángulo y captura la instancia completa con 'as'
        case Rectangulo() as r: # Coincide con cualquier Rectángulo no capturado antes
            print(f"Otro rectángulo: {r}")

        # Coincide con cualquier instancia de Punto (si no coincidió antes)
        # Útil si el primer caso de Punto tuviera una guarda, por ejemplo.
        case Punto():
            print("Es alguna instancia de Punto.")

        case _:
            print(f"Figura desconocida: {figura}")

# Crear instancias
p1 = Punto(10, 20)
p_origen = Punto(0, 0) # Para demostrar el orden
circ1 = Circulo(centro=Punto(5, 5), radio=10.0)
circ_origen = Circulo(centro=Punto(0, 0), radio=5.0)
rect1 = Rectangulo(ancho=100, alto=50, color="rojo")
rect2 = Rectangulo(ancho=30, alto=30) # Usa color por defecto 'azul'

print("Procesando p1:")
procesar_figura(p1)
print("Procesando p_origen (demuestra orden):")
procesar_figura(p_origen) # Coincide con el primer caso Punto(x=px, y=py)
print("Procesando circ1:")
procesar_figura(circ1)
print("Procesando circ_origen:")
procesar_figura(circ_origen)
print("Procesando rect1:")
procesar_figura(rect1)
print("Procesando rect2:")
procesar_figura(rect2) # Coincidirá con Rectangulo(w, h)
print("Procesando otro objeto:")
procesar_figura("esto no es una figura")
print("-" * 20)

# --- 10. Patrones Anidados ---
# Se pueden combinar todos los tipos de patrones para estructuras complejas.
print("--- 10. Patrones Anidados ---")

def procesar_datos_complejos(datos):
    """Demuestra patrones anidados."""
    match datos:
        # Lista que contiene un diccionario con clave "usuario" y un Punto
        case [{"usuario": u, "coords": Punto(x, y)}, *resto]:
            print(f"Primer elemento: Usuario '{u}' en ({x}, {y}). Resto: {resto}")
        # Tupla donde el primer elemento es "ERROR" y el segundo un dict con "code"
        case ("ERROR", {"code": codigo, "msg": mensaje}):
            print(f"Error {codigo}: {mensaje}")
        # Diccionario con clave "items" que es una lista que empieza con 1
        case {"items": [1, *otros_items]}:
            print(f"Diccionario con items que empiezan con 1. Otros: {otros_items}")
        # Lista que contiene al menos un Círculo
        case [*_, Circulo(centro=Punto(cx, cy), radio=r), *_]:
             print(f"La lista contiene al menos un círculo con centro ({cx}, {cy}) y radio {r}")
             # Nota: Esto solo encuentra la *primera* coincidencia de Círculo en la lista
        case _:
            print(f"Estructura de datos no reconocida: {datos}")

datos1 = [{"usuario": "admin", "coords": Punto(10, -5)}, {"status": "pending"}]
datos2 = ("ERROR", {"code": 404, "msg": "No encontrado"})
datos3 = {"items": [1, 2, 3, 4]}
datos4 = [Punto(1,1), "texto", Circulo(Punto(0,0), 5), Rectangulo(10,10)]
datos5 = {"clave": "valor"}

procesar_datos_complejos(datos1)
procesar_datos_complejos(datos2)
procesar_datos_complejos(datos3)
procesar_datos_complejos(datos4)
procesar_datos_complejos(datos5)
print("-" * 20)

# --- 11. Consideraciones Importantes ---
print("--- 11. Consideraciones Importantes ---")

# 1. El orden de los `case` importa:
#    Python ejecuta el bloque del *primer* patrón que coincida.
#    Coloca los patrones más específicos *antes* que los más generales.
#    (Ver ejemplo en Patrones de Clase con Punto(0,0) después de Punto(x,y)).

# 2. Exhaustividad:
#    Asegúrate de manejar todos los casos posibles, o incluye un caso comodín `case _:`
#    para capturar cualquier cosa que no coincida con los patrones anteriores.
#    Si un valor no coincide con ningún patrón y no hay `case _`, no se ejecuta
#    ningún bloque del `match` (no se produce un error, simplemente no hace nada).

# 3. Legibilidad vs Complejidad:
#    `match-case` puede hacer el código más legible para estructuras complejas,
#    pero patrones excesivamente anidados o complejos pueden volverse difíciles de entender.
#    Busca un equilibrio. A veces, una combinación de `match` y `if/else` o funciones
#    auxiliares puede ser más clara.

# 4. Cuándo NO usar `match-case`:
#    - Para reemplazos simples de `if/elif/else` basados en igualdad o condiciones booleanas
#      simples, `if/elif/else` suele ser más directo y eficiente.
#      Ejemplo: `if x > 0: ... elif x < 0: ... else: ...` es perfectamente claro.
#    - Cuando solo necesitas verificar el tipo de una variable, `isinstance()` suele ser suficiente.
#      Ej: `if isinstance(obj, MiClase): ...`

# 5. Variables de captura y alcance:
#    Las variables capturadas en un `case` (ej: `case [x, y]:`) están disponibles
#    *dentro* del bloque de ese `case`.

# 6. Constantes vs Captura:
#    - `case MiConstante:` compara con el valor de `MiConstante`.
#    - `case miconstante:` (minúscula) captura el valor en la variable `miconstante`.
#    - Para usar variables como parte de un patrón de comparación, usa nombres cualificados
#      (ej: `math.pi`) o patrones de clase/atributos. O usa guardas.

import math
PI = math.pi

def comparar_con_constante(valor):
    mi_variable_local = 100
    match valor:
        case PI: # Correcto: compara con el valor de math.pi importado como PI
            print("El valor es PI.")
        # case mi_variable_local: # ¡INCORRECTO! Esto capturaría el valor en 'mi_variable_local'
        #                         # No lo compara con 100.
        case x if x == mi_variable_local: # Forma correcta de comparar con una variable local usando guarda
            print(f"El valor es igual a mi_variable_local ({mi_variable_local}).")
        case mi_variable_local: # Este caso ahora sí captura (si la guarda anterior falla)
             print(f"Capturado valor en mi_variable_local: {mi_variable_local}") # Sombrea la variable exterior
        case _:
             print("Otro valor.")

comparar_con_constante(math.pi)
comparar_con_constante(100)
comparar_con_constante(50) # Será capturado por el último 'case mi_variable_local'

print("-" * 20)

print("--- Fin de los apuntes sobre match-case ---")