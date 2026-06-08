# -*- coding: utf-8 -*-
"""
PYTHON 3.0: DICCIONARIOS (ESTRUCTURAS CLAVE-VALOR)
-------------------------------------------------
Un diccionario es una colección mutable, optimizada para búsquedas rápidas.
Funciona mediante una "llave" única que apunta a un "valor".
"""

# ==============================================================================
# NIVEL 1: CIMENTANDO LAS BASES (CREACIÓN Y ACCESO)
# ==============================================================================

# 1.1. Creación clásica vs Constructor
# La forma más rápida es {}, pero dict() permite conversiones.
student = {
    "name": "Alex",
    "age": 22,
    "courses": ["Python", "DB"]
}

# Creación desde pares (útil para datos que vienen de fuentes externas)
pairs = [("id", 101), ("status", "active")]
meta_data = dict(pairs)

# 1.2. Acceso Seguro
# Evita el KeyError usando .get()
print(f"Nombre: {student['name']}") # Acceso directo (falla si no existe)
print(f"Email: {student.get('email', 'No registrado')}") # Acceso seguro con valor por defecto

# ==============================================================================
# NIVEL 2: GESTIÓN DINÁMICA DE DATOS
# ==============================================================================

# 2.1. Inserción y Actualización
student["age"] = 23             # Actualiza si existe
student["is_active"] = True     # Crea si no existe

# 2.2. Eliminación Inteligente
# 'del' es directo, 'pop' devuelve el valor eliminado (útil para procesar)
last_course = student["courses"].pop() # Elimina el último de la lista interna
deleted_age = student.pop("age")      # Elimina 'age' y lo guarda en la variable

# 2.3. Fusión Moderna (Python 3.9+)
# El operador '|' crea un nuevo dict, '|=' actualiza el original (in-place)
extra_info = {"city": "Madrid", "is_active": False}
merged_student = student | extra_info # 'extra_info' prevalece en caso de conflicto
print(f"Fusión 3.9+: {merged_student}")

# ==============================================================================
# NIVEL 3: RECORRIENDO EL DICCIONARIO (VISTAS)
# ==============================================================================
# .items() es la forma más "Pythonic" de iterar.

inventory = {"apples": 50, "bananas": 100, "oranges": 30}

print("\n--- Listado de Inventario ---")
for product, quantity in inventory.items():
    status = "Suficiente" if quantity > 40 else "Poco stock"
    print(f"-> {product.capitalize()}: {quantity} ({status})")

# ==============================================================================
# NIVEL 4: AVANZADO Y OPTIMIZACIÓN
# ==============================================================================

# 4.1. Dict Comprehension
# Crear diccionarios al vuelo de forma elegante.
# Ejemplo: Filtrar productos con stock y aplicar descuento.
discounted_stock = {k: v * 0.9 for k, v in inventory.items() if v > 40}
print(f"\nStock con descuento: {discounted_stock}")

# 4.2. Diccionarios Anidados (Estructuras Complejas)
# Ideal para representar datos tipo JSON.
db = {
    "user_1": {"name": "Sara", "role": "admin"},
    "user_2": {"name": "Luz", "role": "editor"}
}
# Acceso "encadenado"
print(f"Rol de Sara: {db['user_1']['role']}")

# 4.3. El método .setdefault()
# Inserta una clave con valor solo si NO existe. Muy útil para inicializar.
counts = {}
for letter in "abracadabra":
    counts[letter] = counts.get(letter, 0) + 1 # Opción A
    # counts.setdefault(letter, 0) # Opción B: alternativa elegante
print(f"Conteo: {counts}")

# ==============================================================================
# TIPS PRO PARA APRENDER MÁS
# ==============================================================================
# 1. Búsqueda O(1): Buscar una clave es instantáneo sin importar el tamaño.
# 2. Inmutabilidad: Las claves DEBEN ser inmutables (strings, ints, tuplas).
# 3. Orden: Desde Python 3.7, mantienen el orden de inserción.

# ¿Quieres saber más? Investiga 'collections.defaultdict' para obviar el KeyError.
