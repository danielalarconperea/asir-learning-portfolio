# -*- coding: utf-8 -*-

# ==================================================================
# Demostración de Funciones Built-in de Python para Introspección
# ==================================================================
# Este script muestra ejemplos de uso de varias funciones incorporadas
# útiles para examinar y manipular objetos en Python.

import datetime # Necesario para ejemplos con repr y str

# --- Clases de ejemplo para issubclass, hasattr, etc. ---
class Vehiculo:
    """Clase base simple."""
    tipo_motor = "Combustión" # Atributo de clase
    def __init__(self, marca):
        self.marca = marca # Atributo de instancia

    def arrancar(self):
        print(f"El vehículo {self.marca} ha arrancado.")

class Coche(Vehiculo):
    """Clase que hereda de Vehiculo."""
    def __init__(self, marca, modelo):
        super().__init__(marca)
        self.modelo = modelo # Atributo de instancia específico de Coche

    def tocar_bocina(self):
        print(f"El coche {self.marca} {self.modelo} toca la bocina: ¡Beep Beep!")

# --- Instancias y variables para las demostraciones ---
mi_coche = Coche("Seat", "Ibiza")
mi_vehiculo = Vehiculo("Genérico")
numero_entero = 42
numero_flotante = 3.14
texto = "Python es genial"
lista_datos = [1, "dos", 3.0]
tupla_datos = (True, False)
diccionario_datos = {'a': 1, 'b': 2}
booleano = True

def mi_funcion_ejemplo():
    """Una función simple para demostrar callable."""
    print("¡La función ha sido llamada!")

print("--- 1. isinstance(objeto, clase_o_tupla) ---")
# Comprueba si un objeto es instancia de una clase o subclase.
print(f"¿mi_coche es instancia de Coche? {isinstance(mi_coche, Coche)}") # True
print(f"¿mi_coche es instancia de Vehiculo? {isinstance(mi_coche, Vehiculo)}") # True (por herencia)
print(f"¿mi_vehiculo es instancia de Coche? {isinstance(mi_vehiculo, Coche)}") # False
print(f"¿numero_entero es int o float? {isinstance(numero_entero, (int, float))}") # True
print(f"¿texto es int o float? {isinstance(texto, (int, float))}") # False
print("-" * 30)

print("--- 2. issubclass(clase, clase_o_tupla) ---")
# Comprueba si una clase es subclase de otra.
print(f"¿Coche es subclase de Vehiculo? {issubclass(Coche, Vehiculo)}") # True
print(f"¿Vehiculo es subclase de Coche? {issubclass(Vehiculo, Coche)}") # False
print(f"¿Coche es subclase de Vehiculo o de object? {issubclass(Coche, (Vehiculo, object))}") # True (object es la base de todo)
print(f"¿int es subclase de float? {issubclass(int, float)}") # False
print("-" * 30)

print("--- 3. type(objeto) ---")
# Devuelve el tipo exacto del objeto. No considera la herencia como isinstance.
print(f"Tipo de mi_coche: {type(mi_coche)}") # <class '__main__.Coche'> (o similar)
print(f"Tipo de texto: {type(texto)}") # <class 'str'>
# Comparación directa de tipos:
print(f"¿El tipo de mi_coche es exactamente Coche? {type(mi_coche) == Coche}") # True
print(f"¿El tipo de mi_coche es exactamente Vehiculo? {type(mi_coche) == Vehiculo}") # False (es Coche, no Vehiculo directamente)
print("-" * 30)

print("--- 4. id(objeto) ---")
# Devuelve el identificador único (dirección de memoria en CPython) del objeto.
id_coche1 = id(mi_coche)
mi_otro_coche = mi_coche # mi_otro_coche apunta al MISMO objeto
id_coche2 = id(mi_otro_coche)
coche_nuevo = Coche("Seat", "Ibiza") # Objeto diferente, aunque con igual contenido
id_coche3 = id(coche_nuevo)
print(f"ID de mi_coche: {id_coche1}")
print(f"ID de mi_otro_coche (misma referencia): {id_coche2}")
print(f"ID de coche_nuevo (nuevo objeto): {id_coche3}")
print(f"¿id_coche1 == id_coche2? {id_coche1 == id_coche2}") # True
print(f"¿id_coche1 == id_coche3? {id_coche1 == id_coche3}") # False
print("-" * 30)

print("--- 5. callable(objeto) ---")
# Comprueba si un objeto se puede "llamar" (como una función o método).
print(f"¿mi_funcion_ejemplo es callable? {callable(mi_funcion_ejemplo)}") # True
print(f"¿El método mi_coche.tocar_bocina es callable? {callable(mi_coche.tocar_bocina)}") # True
print(f"¿La clase Coche es callable (para crear instancias)? {callable(Coche)}") # True
print(f"¿El número entero es callable? {callable(numero_entero)}") # False
print(f"¿La lista es callable? {callable(lista_datos)}") # False
print("-" * 30)

print("--- 6. hasattr(objeto, nombre_atributo) ---")
# Comprueba si un objeto tiene un atributo con ese nombre (string).
print(f"¿mi_coche tiene el atributo 'modelo'? {hasattr(mi_coche, 'modelo')}") # True (atributo de instancia)
print(f"¿mi_coche tiene el atributo 'marca'? {hasattr(mi_coche, 'marca')}") # True (atributo de instancia heredado)
print(f"¿mi_coche tiene el método 'tocar_bocina'? {hasattr(mi_coche, 'tocar_bocina')}") # True
print(f"¿mi_coche tiene el atributo 'tipo_motor'? {hasattr(mi_coche, 'tipo_motor')}") # True (atributo de clase heredado)
print(f"¿mi_coche tiene el atributo 'color'? {hasattr(mi_coche, 'color')}") # False
print("-" * 30)

print("--- 7. getattr(objeto, nombre_atributo[, valor_por_defecto]) ---")
# Obtiene el valor de un atributo por su nombre (string).
marca_coche = getattr(mi_coche, 'marca')
print(f"Marca obtenida con getattr: {marca_coche}") # Seat
metodo_bocina = getattr(mi_coche, 'tocar_bocina')
print("Llamando al método obtenido con getattr:")
metodo_bocina() # Ejecuta el método: El coche Seat Ibiza toca la bocina: ¡Beep Beep!
# Obtener un atributo inexistente con valor por defecto:
color_coche = getattr(mi_coche, 'color', 'Rojo por defecto')
print(f"Color obtenido con getattr (con default): {color_coche}") # Rojo por defecto
# Obtener un atributo inexistente SIN valor por defecto (causaría AttributeError):
# potencia = getattr(mi_coche, 'potencia') # Descomentar para ver el error
print("-" * 30)

print("--- 8. setattr(objeto, nombre_atributo, valor) ---")
# Establece el valor de un atributo usando su nombre (string). Crea el atributo si no existe.
print(f"Marca ANTES de setattr: {mi_coche.marca}")
setattr(mi_coche, 'marca', 'Volkswagen') # Cambia la marca
print(f"Marca DESPUÉS de setattr: {mi_coche.marca}") # Volkswagen
# Crear un nuevo atributo
print(f"¿Tiene 'color' ANTES de setattr? {hasattr(mi_coche, 'color')}") # False
setattr(mi_coche, 'color', 'Azul')
print(f"¿Tiene 'color' DESPUÉS de setattr? {hasattr(mi_coche, 'color')}") # True
print(f"Valor del nuevo atributo 'color': {mi_coche.color}") # Azul
print("-" * 30)

print("--- 9. delattr(objeto, nombre_atributo) ---")
# Elimina un atributo de un objeto usando su nombre (string).
print(f"¿Tiene 'modelo' ANTES de delattr? {hasattr(mi_coche, 'modelo')}") # True
delattr(mi_coche, 'modelo')
print(f"¿Tiene 'modelo' DESPUÉS de delattr? {hasattr(mi_coche, 'modelo')}") # False
# Intentar acceder al atributo eliminado causaría AttributeError:
# print(mi_coche.modelo) # Descomentar para ver el error
# Intentar eliminar un atributo inexistente causaría AttributeError:
# delattr(mi_coche, 'ruedas') # Descomentar para ver el error
print("-" * 30)

print("--- 10. repr(objeto) ---")
# Devuelve la representación "oficial" del objeto (para desarrolladores).
fecha_hora_actual = datetime.datetime.now()
print(f"repr de un entero: {repr(numero_entero)}") # 42
print(f"repr de un string: {repr(texto)}") # 'Python es genial' (con comillas)
print(f"repr de una lista: {repr(lista_datos)}") # [1, 'dos', 3.0]
print(f"repr de un objeto datetime: {repr(fecha_hora_actual)}") # E.g., datetime.datetime(2025, 4, 28, 10, 22, 0, 123456)
print("-" * 30)

print("--- 11. str(objeto) ---")
# Devuelve la representación "informal" del objeto (para usuarios). Usada por print().
print(f"str de un entero: {str(numero_entero)}") # 42
print(f"str de un string: {str(texto)}") # Python es genial (sin comillas extra)
print(f"str de una lista: {str(lista_datos)}") # [1, 'dos', 3.0]
print(f"str de un objeto datetime: {str(fecha_hora_actual)}") # E.g., 2025-04-28 10:22:00.123456
print("-" * 30)

print("--- 12. dir([objeto]) ---")
# Sin objeto: lista nombres en el scope local. Con objeto: lista sus atributos/métodos.
print("dir() del scope actual (parcial):")
# print(dir()) # Muestra muchas cosas, puede ser largo
print("dir() de un string (parcial):")
print(dir(texto)[-5:]) # Muestra los últimos 5 atributos/métodos de un string
print("dir() de mi_coche (parcial):")
print([a for a in dir(mi_coche) if not a.startswith('__')]) # Muestra atributos/métodos no especiales
print("-" * 30)

print("--- 13. vars([objeto]) ---")
# Sin objeto: diccionario del scope local. Con objeto: su diccionario __dict__ (atributos modificables).
print("vars() de la instancia mi_coche:")
# Nota: 'modelo' fue eliminado con delattr, 'color' fue añadido con setattr
# 'marca' fue modificada con setattr
# 'tipo_motor' es de clase, no suele aparecer en vars() de la instancia
print(vars(mi_coche)) # E.g., {'marca': 'Volkswagen', 'color': 'Azul'}
print("\nvars() del scope local actual (parcial):")
# print(vars()) # Muestra las variables locales como diccionario
print("-" * 30)

print("=== Fin de la demostración ===")

