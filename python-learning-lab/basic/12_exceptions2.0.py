# -*- coding: utf-8 -*-

"""
=======================================
 APUNTES COMPLETOS SOBRE EXCEPCIONES EN PYTHON
=======================================

Las excepciones son errores detectados durante la ejecución del programa.
Cuando ocurre un error, Python crea un objeto de excepción. Si este objeto no es
manejado (capturado), el programa termina y muestra un "traceback" (rastreo)
indicando dónde ocurrió el error.

Manejar excepciones permite que el programa continúe ejecutándose o termine
de forma controlada, incluso si ocurren errores.
"""

# ----------------------------------------
# 1. ¿QUÉ ES UNA EXCEPCIÓN?
# ----------------------------------------
print("--- 1. ¿Qué es una Excepción? ---")
# Es un evento que ocurre durante la ejecución que interrumpe el flujo normal.
# Ejemplo: Intentar dividir por cero.
# Si no se maneja, el programa se detiene.
# print(10 / 0)  # Esto lanzaría una ZeroDivisionError y detendría el script si no se maneja.
print("Una excepción es un error en tiempo de ejecución.\n")

# ----------------------------------------
# 2. EL BLOQUE try...except BÁSICO
# ----------------------------------------
print("--- 2. Bloque try...except Básico ---")
# El código que *podría* lanzar una excepción se coloca dentro del bloque 'try'.
# El código que maneja la excepción se coloca dentro del bloque 'except'.

try:
    # Intentamos realizar una operación propensa a errores
    numerador = 10
    denominador = 0
    print(f"Intentando calcular {numerador}/{denominador}...")
    resultado = numerador / denominador
    print(f"El resultado es {resultado}") # Esta línea no se ejecutará si hay error
except ZeroDivisionError:
    # Este bloque se ejecuta SÓLO si ocurre una ZeroDivisionError en el bloque try
    print("¡Error! No se puede dividir por cero.")

print("El programa continúa después del try...except.\n")

# ----------------------------------------
# 3. CAPTURANDO EXCEPCIONES ESPECÍFICAS
# ----------------------------------------
print("--- 3. Capturando Excepciones Específicas ---")
# Es una buena práctica capturar tipos de excepciones específicos en lugar de
# todas las excepciones posibles, para saber qué tipo de error ocurrió.

try:
    numero_str = "hola"
    print(f"Intentando convertir '{numero_str}' a entero...")
    numero_int = int(numero_str)
    print(f"El número es: {numero_int}")
except ValueError:
    # Este bloque sólo captura errores de tipo ValueError
    print("¡Error! La cadena no representa un número entero válido.")
except ZeroDivisionError:
     # Podríamos tener otros except para otros tipos de error
     print("¡Error! División por cero.") # Este no se ejecutará en este caso

print("Manejo específico de ValueError completado.\n")

# ----------------------------------------
# 4. CAPTURANDO MÚLTIPLES EXCEPCIONES
# ----------------------------------------
print("--- 4. Capturando Múltiples Excepciones ---")

# 4.1. Múltiples excepciones en un solo bloque 'except' (usando una tupla)
print("--- 4.1. Múltiples excepciones en una tupla ---")
try:
    valor = input("Introduce un número o una letra para buscar en una lista/diccionario: ")
    lista = [1, 2, 3]
    diccionario = {'a': 1, 'b': 2}

    if valor.isdigit():
        indice = int(valor)
        print(f"Accediendo a lista[{indice}]...")
        elemento = lista[indice] # Puede lanzar IndexError
        print(f"Elemento de la lista: {elemento}")
    else:
        print(f"Accediendo a diccionario['{valor}']...")
        elemento = diccionario[valor] # Puede lanzar KeyError
        print(f"Elemento del diccionario: {elemento}")

except (IndexError, KeyError):
    # Este bloque se ejecuta si ocurre IndexError O KeyError
    print("¡Error! El índice o la clave no existe.")
except ValueError:
    # Si el input no es convertible a int cuando se espera
     print("¡Error! Entrada inválida para índice.")

print("Manejo de múltiples excepciones (tupla) completado.\n")


# 4.2. Múltiples bloques 'except' para diferentes excepciones
print("--- 4.2. Múltiples bloques except ---")
try:
    operacion = input("¿Qué operación? (dividir / acceder_lista): ")
    if operacion == "dividir":
        num = int(input("Introduce numerador: "))
        den = int(input("Introduce denominador: "))
        print(f"Calculando {num}/{den}...")
        res = num / den # Puede lanzar ZeroDivisionError o ValueError si la entrada no es int
        print(f"Resultado: {res}")
    elif operacion == "acceder_lista":
        idx = int(input("Introduce índice: "))
        mi_lista = ['a', 'b']
        print(f"Accediendo a mi_lista[{idx}]...")
        val = mi_lista[idx] # Puede lanzar IndexError o ValueError si la entrada no es int
        print(f"Valor: {val}")
    else:
        print("Operación no reconocida")

except ValueError:
    print("¡Error de Valor! Asegúrate de introducir números enteros cuando se requiera.")
except ZeroDivisionError:
    print("¡Error de División por Cero! El denominador no puede ser cero.")
except IndexError:
    print("¡Error de Índice! El índice está fuera de los límites de la lista.")
except Exception as e:
    # Captura cualquier otra excepción no manejada específicamente antes
    print(f"Ocurrió un error inesperado: {type(e).__name__}")

print("Manejo con múltiples bloques except completado.\n")


# ----------------------------------------
# 5. OBTENER EL OBJETO DE EXCEPCIÓN
# ----------------------------------------
print("--- 5. Obtener el Objeto de Excepción ---")
# Puedes obtener el objeto de la excepción usando 'as nombre_variable'.
# Esto es útil para obtener más detalles sobre el error.

try:
    numero = int("texto no numérico")
except ValueError as e:
    # 'e' ahora contiene el objeto de la excepción ValueError
    print(f"Ocurrió un ValueError.")
    print(f"Tipo de excepción: {type(e)}")
    print(f"Argumentos de la excepción: {e.args}") # Detalles del error
    print(f"Representación textual de la excepción: {e}")

print("Obtención del objeto de excepción completada.\n")

# ----------------------------------------
# 6. EL BLOQUE else
# ----------------------------------------
print("--- 6. El Bloque else ---")
# El bloque 'else' es opcional y se ejecuta SÓLO si el bloque 'try'
# se completa SIN lanzar ninguna excepción.

try:
    numerador = 10
    denominador = 2 # Cambiado a un valor válido
    print(f"Intentando calcular {numerador}/{denominador}...")
    resultado = numerador / denominador
except ZeroDivisionError:
    print("¡Error! No se puede dividir por cero.")
else:
    # Este bloque se ejecuta porque no hubo excepción en el try
    print("La división se realizó correctamente.")
    print(f"El resultado es: {resultado}")

print("Ejecución con bloque else completada.\n")

# ----------------------------------------
# 7. EL BLOQUE finally
# ----------------------------------------
print("--- 7. El Bloque finally ---")
# El bloque 'finally' es opcional y se ejecuta SIEMPRE, independientemente
# de si ocurrió una excepción o no en el bloque 'try', o si se ejecutó
# 'except' o 'else'.
# Es útil para tareas de limpieza (cerrar archivos, liberar recursos, etc.).

print("--- 7.1. Caso SIN excepción ---")
try:
    print("Bloque try: Abriendo un recurso (simulado)...")
    resultado = 5 / 1 # Operación válida
    print(f"Bloque try: Operación exitosa, resultado={resultado}")
except ZeroDivisionError:
    print("Bloque except: Manejando división por cero (no ocurrirá aquí).")
else:
    print("Bloque else: Se ejecuta porque no hubo excepción.")
finally:
    # Este bloque SIEMPRE se ejecuta
    print("Bloque finally: Cerrando el recurso (simulado). Esto siempre se ejecuta.")

print("\n--- 7.2. Caso CON excepción ---")
try:
    print("Bloque try: Abriendo un recurso (simulado)...")
    resultado = 5 / 0 # Operación inválida
    print(f"Bloque try: Operación exitosa (no se llegará aquí).") # No se ejecuta
except ZeroDivisionError:
    print("Bloque except: Manejando división por cero.")
else:
    print("Bloque else: No se ejecuta porque hubo excepción.") # No se ejecuta
finally:
    # Este bloque SIEMPRE se ejecuta
    print("Bloque finally: Cerrando el recurso (simulado). Esto siempre se ejecuta.")

print("Ejecución con bloque finally completada.\n")


# ----------------------------------------
# 8. ESTRUCTURA COMPLETA: try...except...else...finally
# ----------------------------------------
print("--- 8. Estructura Completa: try...except...else...finally ---")

def dividir_numeros(a, b):
    """Intenta dividir a / b y muestra el flujo completo."""
    print(f"\nIntentando dividir {a} entre {b}")
    try:
        print("Dentro del try: Calculando...")
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
             raise TypeError("Ambos operandos deben ser numéricos.") # Lanzamos manualmente TypeError
        if b == 0:
            raise ZeroDivisionError("El denominador no puede ser cero.") # Lanzamos manualmente ZeroDivisionError
        
        resultado = a / b
        print("Dentro del try: Cálculo finalizado.") # Solo si no hay error antes
    
    except ZeroDivisionError as zde:
        print(f"Dentro de except (ZeroDivisionError): {zde}")
    
    except TypeError as te:
        print(f"Dentro de except (TypeError): {te}")
    
    except Exception as e: # Captura genérica para otros posibles errores
        print(f"Dentro de except (Genérico): Ocurrió un error inesperado: {e}")
    
    else:
        # Se ejecuta si NO hubo excepciones en el try
        print(f"Dentro de else: La división fue exitosa. Resultado = {resultado}")
    
    finally:
        # Se ejecuta SIEMPRE
        print("Dentro de finally: Limpieza final, esta parte siempre se ejecuta.")

# Prueba 1: División exitosa
dividir_numeros(10, 2)

# Prueba 2: División por cero
dividir_numeros(10, 0)

# Prueba 3: Tipo de dato incorrecto
dividir_numeros(10, "texto")

print("Estructura completa demostrada.\n")

# ----------------------------------------
# 9. LANZAR EXCEPCIONES MANUALMENTE (raise)
# ----------------------------------------
print("--- 9. Lanzar Excepciones Manualmente (raise) ---")
# Podemos lanzar excepciones intencionalmente usando la palabra clave 'raise'.
# Esto es útil para indicar condiciones de error específicas en nuestro código.

def validar_edad(edad):
    """Valida si la edad es positiva. Lanza ValueError si no."""
    if not isinstance(edad, int):
        raise TypeError("La edad debe ser un número entero.")
    if edad < 0:
        # Lanzamos una excepción ValueError con un mensaje descriptivo
        raise ValueError("La edad no puede ser negativa.")
    elif edad < 18:
        print("Es menor de edad.")
    else:
        print("Es mayor de edad.")

try:
    validar_edad(25)  # Válido
    validar_edad(-5)  # Inválido, lanzará ValueError
except ValueError as e:
    print(f"Error de validación (ValueError): {e}")
except TypeError as e:
     print(f"Error de tipo (TypeError): {e}")

try:
    validar_edad("treinta") # Inválido, lanzará TypeError
except ValueError as e:
    print(f"Error de validación (ValueError): {e}")
except TypeError as e:
     print(f"Error de tipo (TypeError): {e}")


# Re-lanzar una excepción capturada
print("\n--- Re-lanzar excepciones ---")
try:
    print("Intentando operación que puede fallar...")
    # Simula un error
    raise ConnectionError("Fallo al conectar con el servidor")
except ConnectionError as ce:
    print(f"Error de conexión capturado: {ce}. Intentando manejar localmente...")
    # Imagina que hacemos algo aquí, pero decidimos que el error debe propagarse
    print("No se pudo manejar localmente. Re-lanzando la excepción...")
    raise # Re-lanza la misma excepción que se capturó ('ce' en este caso)
except Exception as e:
     # Esta parte no se alcanzará si ConnectionError se re-lanza y no hay un try/except superior
     print(f"Captura de excepción superior: {e}") 

print("Esta línea no se imprimirá si la excepción se re-lanza y no se captura más arriba.\n")


# ----------------------------------------
# 10. CREAR EXCEPCIONES PERSONALIZADAS
# ----------------------------------------
print("--- 10. Crear Excepciones Personalizadas ---")
# Podemos definir nuestras propias clases de excepción heredando de la clase base
# 'Exception' o de alguna de sus subclases más específicas.

# Definimos nuestra propia clase de excepción
class MiErrorPersonalizado(Exception):
    """Una excepción personalizada para un caso específico."""
    def __init__(self, mensaje, codigo_error=None):
        super().__init__(mensaje) # Llama al constructor de la clase base (Exception)
        self.codigo_error = codigo_error

    def __str__(self):
        # Podemos personalizar cómo se muestra el error
        if self.codigo_error:
            return f'[Código {self.codigo_error}] {super().__str__()}'
        return super().__str__()

# Función que puede lanzar nuestra excepción personalizada
def procesar_dato_especial(dato):
    if not isinstance(dato, str):
         raise TypeError("El dato debe ser una cadena.")
    if dato == "prohibido":
        # Lanzamos nuestra excepción personalizada
        raise MiErrorPersonalizado("El dato 'prohibido' no está permitido.", codigo_error=101)
    elif dato == "muy_largo" * 10: # Simula otro error personalizado
        raise MiErrorPersonalizado("El dato es demasiado largo.")
    else:
        print(f"Procesando dato: '{dato}'")

# Manejando nuestra excepción personalizada
try:
    procesar_dato_especial("válido")
    procesar_dato_especial("prohibido") # Esto lanzará MiErrorPersonalizado
except MiErrorPersonalizado as mep:
    print(f"Error personalizado capturado: {mep}")
    # Podemos acceder a atributos específicos si los definimos
    if mep.codigo_error:
        print(f"Código de error asociado: {mep.codigo_error}")
except TypeError as te:
     print(f"Error de tipo capturado: {te}")

try:
    procesar_dato_especial(123) # Esto lanzará TypeError
except MiErrorPersonalizado as mep:
    print(f"Error personalizado capturado: {mep}")
except TypeError as te:
     print(f"Error de tipo capturado: {te}")
     
print("Uso de excepciones personalizadas demostrado.\n")


# ----------------------------------------
# 11. JERARQUÍA DE EXCEPCIONES INCORPORADAS (Built-in)
# ----------------------------------------
print("--- 11. Jerarquía de Excepciones Incorporadas ---")
# Python tiene una jerarquía de excepciones. 'Exception' es la base para la mayoría
# de los errores comunes. Capturar una clase base también captura sus subclases.
# Ejemplos comunes:
# - Exception
#   - ArithmeticError
#     - ZeroDivisionError
#     - OverflowError
#   - LookupError
#     - IndexError (listas, tuplas)
#     - KeyError (diccionarios)
#   - ValueError (tipo correcto, valor inapropiado)
#   - TypeError (operación con tipo inapropiado)
#   - OSError
#     - FileNotFoundError
#   - NameError (variable no definida)
#   - AttributeError (atributo o método no existente)
# ... y muchas más.

try:
    # Provocaremos un IndexError
    lista = [1, 2]
    print(lista[5])
except LookupError as le:
    # Capturamos LookupError, que es la clase base de IndexError y KeyError
    print(f"Error de búsqueda capturado (LookupError o subclase): {type(le).__name__} - {le}")
except Exception as e:
    # Si no fuera un LookupError, se capturaría aquí
    print(f"Otra excepción capturada: {type(e).__name__} - {e}")

print("Jerarquía de excepciones demostrada.\n")

# ----------------------------------------
# 12. EXCEPTION CHAINING (ENCADENAMIENTO DE EXCEPCIONES)
# ----------------------------------------
print("--- 12. Exception Chaining ---")
# A veces, al manejar una excepción, queremos lanzar una nueva excepción
# pero manteniendo la información sobre la excepción original (la causa).

# 12.1 Encadenamiento Implícito (Python 3 lo hace automáticamente a veces)
print("--- 12.1 Encadenamiento Implícito ---")
try:
    # Error original
    resultado = int("no_es_numero")
except ValueError as ve:
    print(f"Capturado ValueError: {ve}")
    # Ocurre otro error mientras se maneja el primero (implícito)
    # Por ejemplo, intentamos usar una variable que no existe dentro del except
    # print(variable_inexistente) # Esto causaría un NameError "during handling of the above exception"
    # O lanzamos una nueva excepción dentro del 'except'
    try:
        raise TypeError("Nuevo error de tipo ocurrido durante el manejo")
    except TypeError as te:
        print(f"Capturado TypeError anidado: {te}")
        # El traceback mostraría que este TypeError ocurrió mientras se manejaba el ValueError
        # Se puede acceder a la causa con __context__
        print(f"Contexto (causa implícita): {type(te.__context__).__name__} - {te.__context__}")


# 12.2 Encadenamiento Explícito (con 'raise from')
print("\n--- 12.2 Encadenamiento Explícito (raise from) ---")
def funcion_capa_inferior():
    """Simula una operación que puede fallar."""
    print("Ejecutando función de capa inferior...")
    # Simula un error de bajo nivel
    raise ConnectionError("Fallo de conexión en capa inferior")

def funcion_capa_superior():
    """Llama a la función inferior y maneja su error lanzando uno nuevo."""
    print("Ejecutando función de capa superior...")
    try:
        funcion_capa_inferior()
    except ConnectionError as ce:
        print(f"Capa superior capturó: {type(ce).__name__}")
        # Lanzamos una excepción de más alto nivel, pero indicamos la causa original
        raise MiErrorPersonalizado("Error al procesar la solicitud debido a un problema de conexión") from ce

try:
    funcion_capa_superior()
except MiErrorPersonalizado as mep:
    print(f"Excepción final capturada: {type(mep).__name__} - {mep}")
    # La excepción original está disponible en el atributo __cause__
    if mep.__cause__:
        causa_original = mep.__cause__
        print(f"Causa original (raise from): {type(causa_original).__name__} - {causa_original}")

print("Encadenamiento de excepciones demostrado.\n")


# ----------------------------------------
# 13. BUENAS PRÁCTICAS Y CONSIDERACIONES
# ----------------------------------------
print("--- 13. Buenas Prácticas ---")
# 1.  **Sé específico:** Captura las excepciones más específicas que esperas.
#     Evita `except Exception:` o `except:` sin más, a menos que tengas una
#     buena razón (como registrar el error y re-lanzarlo).
#
# 2.  **No silencies errores:** Evita bloques `except` vacíos (`pass`) o que
#     simplemente impriman un mensaje sin hacer nada más útil. Si no puedes
#     manejar el error, déjalo propagar o regístralo adecuadamente.
#
# 3.  **Usa `finally` para limpieza:** Garantiza que los recursos (archivos,
#     conexiones de red, bloqueos) se liberen siempre. A menudo, es mejor usar
#     gestores de contexto (`with`) para esto.
#
# 4.  **Usa `else` para código "exitoso":** El código que debe ejecutarse solo
#     si el `try` tuvo éxito (y que podría lanzar sus propias excepciones no
#     relacionadas con el `try` inicial) es un buen candidato para el bloque `else`.
#
# 5.  **Crea excepciones personalizadas:** Para errores específicos de tu
#     aplicación o dominio, crea tus propias excepciones. Mejora la claridad.
#
# 6.  **Mensajes de error claros:** Cuando lances (`raise`) excepciones, incluye
#     mensajes descriptivos que ayuden a diagnosticar el problema.
#
# 7.  **Considera el encadenamiento:** Usa `raise from` cuando manejes una
#     excepción y lances otra como consecuencia directa, para preservar el contexto.

print("Buenas prácticas resumidas.\n")
print("=======================================")
print(" FIN DE LOS APUNTES SOBRE EXCEPCIONES ")
print("=======================================")


# Ejemplo final usando 'with' (gestor de contexto), que maneja la limpieza automáticamente
# y es preferible a try/finally para recursos como archivos.
print("\n--- Ejemplo con 'with' para archivos (manejo implícito de cierre) ---")
nombre_archivo = "archivo_inexistente_para_prueba.txt"
try:
    # 'with' asegura que f.close() se llame, incluso si hay errores dentro del bloque.
    with open(nombre_archivo, 'r') as f:
        contenido = f.read()
        print("Contenido del archivo:")
        print(contenido)
# FileNotFoundError es una subclase de OSError
except FileNotFoundError:
    print(f"¡Error! El archivo '{nombre_archivo}' no fue encontrado.")
except OSError as oe:
    print(f"Error de sistema operativo al intentar leer el archivo: {oe}")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
finally:
    # Aunque 'with' cierra el archivo, 'finally' todavía se ejecuta.
    print("Bloque finally después del 'with' (se ejecuta igualmente).")