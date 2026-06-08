# -*- coding: utf-8 -*-

# ##############################################################################
# ##                                                                          ##
# ##                 APUNTES COMPLETOS SOBRE DICCIONARIOS EN PYTHON             ##
# ##                                                                          ##
# ##############################################################################

# Un diccionario en Python es una colección desordenada*, mutable y
# que contiene elementos en formato clave:valor.
# Las claves deben ser únicas y de tipo inmutable (como strings, números o tuplas
# que contengan solo elementos inmutables). Los valores pueden ser de cualquier tipo
# y pueden repetirse.

# (*) Nota sobre el orden: Desde Python 3.7+, los diccionarios recuerdan el orden
# de inserción de los elementos. En versiones anteriores (y como detalle de
# implementación en CPython 3.6), el orden no estaba garantizado.

print("====================== 1. CREACIÓN DE DICCIONARIOS ======================")
pop
# 1.1. Usando llaves {} (literal de diccionario)
mi_diccionario = {
    "nombre": "Alice",
    "edad": 30,
    "ciudad": "Nueva York",
    "habilidades": ["Python", "Data Science", "Web Dev"]
}
print(f"1.1. Diccionario creado con llaves: {mi_diccionario}")

# 1.2. Usando el constructor dict()
# 1.2.1. Con argumentos de palabra clave (las claves deben ser strings válidos como nombres de variables)
diccionario_vacio = {} # También dict()
otro_diccionario = dict(nombre="Bob", edad=25, ciudad="Londres")
print(f"1.2.1. Diccionario creado con dict() y kwargs: {otro_diccionario}")

# 1.2.2. Con un iterable de pares clave-valor (tuplas, listas, etc.)
lista_pares = [('a', 1), ('b', 2), ('c', 3)]
diccionario_desde_lista = dict(lista_pares)
print(f"1.2.2. Diccionario creado desde lista de tuplas: {diccionario_desde_lista}")

tupla_pares = (['x', 10], ['y', 20]) # Puede ser lista de listas también
diccionario_desde_tupla = dict(tupla_pares)
print(f"1.2.2. Diccionario creado desde tupla de listas: {diccionario_desde_tupla}")

# 1.2.3. Usando zip para combinar dos iterables (uno de claves, uno de valores)
claves = ["id", "producto", "precio"]
valores = [101, "Laptop", 1200.50]
diccionario_con_zip = dict(zip(claves, valores))
print(f"1.2.3. Diccionario creado con zip: {diccionario_con_zip}")

# 1.2.4. Creando una copia superficial de otro diccionario
copia_diccionario = dict(mi_diccionario)
print(f"1.2.4. Copia superficial creada con dict(): {copia_diccionario}")
print(f"       ¿Son el mismo objeto? {mi_diccionario is copia_diccionario}") # False

# 1.3. Diccionario vacío
dic_vacio_1 = {}
dic_vacio_2 = dict()
print(f"1.3. Diccionarios vacíos: {dic_vacio_1}, {dic_vacio_2}")
print(f"     Tipo: {type(dic_vacio_1)}")


print("\n====================== 2. ACCESO A ELEMENTOS ======================")

# Se accede a los valores usando sus claves correspondientes.

# 2.1. Usando corchetes []
# Si la clave existe, devuelve el valor.
# Si la clave NO existe, lanza un error `KeyError`.
print(f"2.1. Accediendo con ['nombre']: {mi_diccionario['nombre']}")
print(f"     Accediendo con ['edad']: {mi_diccionario['edad']}")

# Intentar acceder a una clave inexistente
try:
    valor = mi_diccionario['pais']
except KeyError as e:
    print(f"     Error al acceder a 'pais' con []: {e}")

# 2.2. Usando el método get()
# Si la clave existe, devuelve el valor.
# Si la clave NO existe, devuelve None (por defecto) o un valor especificado.
# ¡Este método NO lanza KeyError!
valor_ciudad = mi_diccionario.get('ciudad')
print(f"2.2. Accediendo con get('ciudad'): {valor_ciudad}")

valor_pais_none = mi_diccionario.get('pais') # No existe, devuelve None
print(f"     Accediendo con get('pais'): {valor_pais_none}")

valor_pais_default = mi_diccionario.get('pais', 'Desconocido') # No existe, devuelve 'Desconocido'
print(f"     Accediendo con get('pais', 'Desconocido'): {valor_pais_default}")


print("\n====================== 3. AÑADIR Y ACTUALIZAR ELEMENTOS ======================")

# Los diccionarios son mutables, podemos añadir nuevos pares clave-valor o modificar existentes.

# 3.1. Usando corchetes []
# Si la clave NO existe, añade el nuevo par clave-valor.
mi_diccionario['profesion'] = 'Ingeniera de Software' # Añade nueva clave
print(f"3.1. Diccionario tras añadir 'profesion': {mi_diccionario}")

# Si la clave SÍ existe, actualiza el valor asociado a esa clave.
mi_diccionario['ciudad'] = 'San Francisco' # Actualiza valor existente
print(f"     Diccionario tras actualizar 'ciudad': {mi_diccionario}")

# 3.2. Usando el método update()
# Permite añadir/actualizar múltiples elementos a la vez.
# Acepta otro diccionario o un iterable de pares clave-valor.
# Si las claves ya existen, se actualizan sus valores. Si no existen, se añaden.

# Actualizar con otro diccionario
nuevos_datos = {'edad': 31, 'email': 'alice@example.com', 'ciudad': 'Palo Alto'}
mi_diccionario.update(nuevos_datos)
print(f"3.2. Diccionario tras update() con otro diccionario: {mi_diccionario}")
# Nota: 'edad' y 'ciudad' se actualizaron, 'email' se añadió.

# Actualizar con un iterable de pares
mi_diccionario.update([('telefono', '555-1234'), ('edad', 32)])
print(f"     Diccionario tras update() con iterable de pares: {mi_diccionario}")
# Nota: 'telefono' se añadió, 'edad' se actualizó de nuevo.


print("\n====================== 4. ELIMINAR ELEMENTOS ======================")

# 4.1. Usando la palabra clave `del`
# Elimina el par clave-valor especificado por la clave.
# Lanza `KeyError` si la clave no existe.
del mi_diccionario['telefono']
print(f"4.1. Diccionario tras `del mi_diccionario['telefono']`: {mi_diccionario}")

# Intentar eliminar una clave inexistente
try:
    del mi_diccionario['pais']
except KeyError as e:
    print(f"     Error al intentar `del` una clave inexistente ('pais'): {e}")

# 4.2. Usando el método pop()
# Elimina el par clave-valor especificado por la clave y DEVUELVE el valor eliminado.
# Lanza `KeyError` si la clave no existe y no se proporciona un valor por defecto.
valor_email = mi_diccionario.pop('email')
print(f"4.2. Diccionario tras pop('email'): {mi_diccionario}")
print(f"     Valor devuelto por pop('email'): {valor_email}")

# pop() con valor por defecto si la clave no existe
valor_inexistente = mi_diccionario.pop('pais', 'No encontrado')
print(f"     Resultado de pop('pais', 'No encontrado'): {valor_inexistente}")
print(f"     Diccionario no cambia si la clave no existe y se da default: {mi_diccionario}")

# pop() sin valor por defecto para clave inexistente (lanza KeyError)
try:
    mi_diccionario.pop('direccion')
except KeyError as e:
    print(f"     Error al intentar pop('direccion') sin default: {e}")

# 4.3. Usando el método popitem()
# Elimina y devuelve el ÚLTIMO par clave-valor insertado (comportamiento LIFO desde Python 3.7+).
# En versiones anteriores a 3.7, eliminaba un par arbitrario.
# Lanza `KeyError` si el diccionario está vacío.
ultimo_item = mi_diccionario.popitem()
print(f"4.3. Diccionario tras popitem(): {mi_diccionario}")
print(f"     Par clave-valor devuelto por popitem(): {ultimo_item}")

# popitem() en diccionario vacío
dic_vacio_pop = {}
try:
    dic_vacio_pop.popitem()
except KeyError as e:
    print(f"     Error al intentar popitem() en diccionario vacío: {e}")


# 4.4. Usando el método clear()
# Elimina TODOS los elementos del diccionario, dejándolo vacío.
mi_diccionario_a_limpiar = {'a': 1, 'b': 2}
print(f"4.4. Diccionario antes de clear(): {mi_diccionario_a_limpiar}")
mi_diccionario_a_limpiar.clear()
print(f"     Diccionario después de clear(): {mi_diccionario_a_limpiar}")


print("\n====================== 5. COMPROBAR EXISTENCIA (CLAVES Y VALORES) ======================")

# 5.1. Comprobar si una clave existe usando `in` y `not in`
# Es la forma más eficiente y común.
if 'nombre' in mi_diccionario:
    print(f"5.1. La clave 'nombre' ESTÁ en el diccionario.")

if 'email' not in mi_diccionario:
    print(f"     La clave 'email' NO ESTÁ en el diccionario.")

# 5.2. Comprobar si un valor existe
# Para esto, necesitamos acceder a los valores del diccionario.
# `in` sobre el diccionario directamente solo comprueba claves.
valor_a_buscar = 32
if valor_a_buscar in mi_diccionario.values():
    print(f"5.2. El valor '{valor_a_buscar}' ESTÁ en los valores del diccionario.")
else:
    print(f"5.2. El valor '{valor_a_buscar}' NO ESTÁ en los valores del diccionario.")

valor_a_buscar_2 = "Python"
# Para valores dentro de listas u otras estructuras anidadas:
encontrado = False
for v in mi_diccionario.values():
    if isinstance(v, list) and valor_a_buscar_2 in v:
        encontrado = True
        break
if encontrado:
     print(f"     El valor '{valor_a_buscar_2}' ESTÁ dentro de una lista en los valores.")
else:
     print(f"     El valor '{valor_a_buscar_2}' NO ESTÁ dentro de una lista en los valores.")


print("\n====================== 6. OBTENER VISTAS (KEYS, VALUES, ITEMS) ======================")

# Los métodos keys(), values() e items() devuelven objetos "vista" (view objects).
# Las vistas son dinámicas: reflejan cualquier cambio posterior en el diccionario.
# Son iterables.

diccionario_vistas = {'a': 1, 'b': 2, 'c': 3}
print(f"6. Diccionario para demostración de vistas: {diccionario_vistas}")

# 6.1. keys(): Vista de las claves
vista_claves = diccionario_vistas.keys()
print(f"6.1. Vista de claves (keys()): {vista_claves}")
print(f"     Tipo de la vista de claves: {type(vista_claves)}")
# Podemos convertirla a lista si necesitamos una copia estática
lista_claves = list(vista_claves)
print(f"     Vista de claves convertida a lista: {lista_claves}")

# 6.2. values(): Vista de los valores
vista_valores = diccionario_vistas.values()
print(f"6.2. Vista de valores (values()): {vista_valores}")
print(f"     Tipo de la vista de valores: {type(vista_valores)}")
lista_valores = list(vista_valores)
print(f"     Vista de valores convertida a lista: {lista_valores}")

# 6.3. items(): Vista de los pares clave-valor (como tuplas)
vista_items = diccionario_vistas.items()
print(f"6.3. Vista de items (items()): {vista_items}")
print(f"     Tipo de la vista de items: {type(vista_items)}")
lista_items = list(vista_items)
print(f"     Vista de items convertida a lista: {lista_items}")

# 6.4. Demostración de la naturaleza dinámica de las vistas
print(f"6.4. Vista de items ANTES de modificar el diccionario: {vista_items}")
diccionario_vistas['d'] = 4 # Añadimos un elemento al diccionario original
print(f"     Diccionario modificado: {diccionario_vistas}")
print(f"     Vista de items DESPUÉS de modificar el diccionario: {vista_items}") # ¡La vista se actualiza!
# Lo mismo ocurre con keys() y values()


print("\n====================== 7. ITERAR SOBRE DICCIONARIOS ======================")

# Hay varias formas de recorrer los elementos de un diccionario.

# 7.1. Iterar sobre las claves (forma predeterminada)
print("7.1. Iterando sobre las claves (predeterminado):")
for clave in mi_diccionario:
    print(f"     Clave: {clave}, Valor: {mi_diccionario[clave]}") # Accedemos al valor con la clave

# 7.2. Iterar explícitamente sobre las claves usando keys()
print("7.2. Iterando sobre las claves usando keys():")
for clave in mi_diccionario.keys():
    print(f"     Clave: {clave}")

# 7.3. Iterar sobre los valores usando values()
print("7.3. Iterando sobre los valores usando values():")
for valor in mi_diccionario.values():
    print(f"     Valor: {valor}")

# 7.4. Iterar sobre los pares clave-valor usando items() (la forma más común y pitónica)
print("7.4. Iterando sobre los items (pares clave-valor):")
for clave, valor in mi_diccionario.items(): # Desempaquetado de tuplas
    print(f"     Clave: {clave}, Valor: {valor}")


print("\n====================== 8. LONGITUD DE UN DICCIONARIO ======================")

# La función len() devuelve el número de pares clave-valor en el diccionario.
num_elementos = len(mi_diccionario)
print(f"8. El diccionario 'mi_diccionario' tiene {num_elementos} elementos.")
print(f"   len(diccionario_vacio): {len(diccionario_vacio)}")


print("\n====================== 9. COPIAR DICCIONARIOS ======================")

# Es importante distinguir entre copia superficial (shallow) y profunda (deep).

dic_original = {
    'id': 1,
    'datos': [10, 20],
    'info': {'estado': 'activo'}
}
print(f"9. Diccionario original: {dic_original}")

# 9.1. Copia Superficial (Shallow Copy)
# Crea un nuevo objeto diccionario, pero los valores que son objetos mutables
# (como listas o otros diccionarios) son referencias a los objetos originales.
# Métodos: copy() o dict()

copia_superficial_1 = dic_original.copy()
copia_superficial_2 = dict(dic_original)

print(f"9.1. Copia superficial 1 (con copy()): {copia_superficial_1}")
print(f"     Copia superficial 2 (con dict()): {copia_superficial_2}")
print(f"     ¿Original y copia1 son el mismo objeto? {dic_original is copia_superficial_1}") # False
print(f"     ¿Los 'datos' (lista) son el mismo objeto? {dic_original['datos'] is copia_superficial_1['datos']}") # True
print(f"     ¿La 'info' (dict) son el mismo objeto? {dic_original['info'] is copia_superficial_1['info']}") # True

# Modificar un elemento mutable DENTRO de la copia superficial afecta al original
copia_superficial_1['datos'].append(30)
copia_superficial_1['info']['estado'] = 'inactivo'
print(f"     Copia superficial 1 modificada: {copia_superficial_1}")
print(f"     ¡Diccionario original afectado!: {dic_original}")

# Modificar un elemento inmutable o añadir/quitar claves en la copia NO afecta al original
copia_superficial_1['id'] = 2
copia_superficial_1['nuevo'] = 'valor'
print(f"     Copia superficial 1 con más cambios: {copia_superficial_1}")
print(f"     Diccionario original (id no cambia, nuevo no aparece): {dic_original}")

# Restauramos el original para la copia profunda
dic_original = {
    'id': 1,
    'datos': [10, 20],
    'info': {'estado': 'activo'}
}

# 9.2. Copia Profunda (Deep Copy)
# Crea un nuevo objeto diccionario Y recursivamente copia todos los objetos
# contenidos en él, incluyendo los objetos mutables anidados.
# Se necesita el módulo `copy`.

import copy

copia_profunda = copy.deepcopy(dic_original)

print(f"9.2. Copia profunda (con copy.deepcopy()): {copia_profunda}")
print(f"     ¿Original y copia profunda son el mismo objeto? {dic_original is copia_profunda}") # False
print(f"     ¿Los 'datos' (lista) son el mismo objeto? {dic_original['datos'] is copia_profunda['datos']}") # False
print(f"     ¿La 'info' (dict) son el mismo objeto? {dic_original['info'] is copia_profunda['info']}") # False

# Modificar elementos mutables DENTRO de la copia profunda NO afecta al original
copia_profunda['datos'].append(40)
copia_profunda['info']['estado'] = 'pendiente'
copia_profunda['id'] = 3

print(f"     Copia profunda modificada: {copia_profunda}")
print(f"     ¡Diccionario original NO afectado!: {dic_original}")


print("\n====================== 10. COMBINAR O FUSIONAR DICCIONARIOS ======================")

dict1 = {'a': 1, 'b': 2}
dict2 = {'b': 3, 'c': 4, 'd': 5}
print(f"10. Diccionario 1: {dict1}")
print(f"    Diccionario 2: {dict2}")

# 10.1. Usando update()
# Modifica el diccionario original (dict1 en este caso).
# Si hay claves repetidas, prevalecen los valores del diccionario que se pasa como argumento (dict2).
dict1_copia_update = dict1.copy() # Hacemos copia para no modificar el original para los siguientes ejemplos
dict1_copia_update.update(dict2)
print(f"10.1. Resultado de dict1.update(dict2): {dict1_copia_update}")

# 10.2. Usando el operador de unión `|` (Python 3.9+)
# Crea un NUEVO diccionario sin modificar los originales.
# Si hay claves repetidas, prevalecen los valores del diccionario de la derecha.
try:
    dict_unido = dict1 | dict2
    print(f"10.2. Resultado de dict1 | dict2 (Python 3.9+): {dict_unido}")
    print(f"     dict1 original no modificado: {dict1}")
    print(f"     dict2 original no modificado: {dict2}")
except TypeError:
    print("10.2. El operador | requiere Python 3.9 o superior.")


# 10.3. Usando el operador de actualización `|=` (Python 3.9+)
# Modifica el diccionario de la izquierda (como update()).
# Si hay claves repetidas, prevalecen los valores del diccionario de la derecha.
dict1_copia_opeq = dict1.copy()
try:
    dict1_copia_opeq |= dict2
    print(f"10.3. Resultado de dict1 |= dict2 (Python 3.9+): {dict1_copia_opeq}")
except TypeError:
     print("10.3. El operador |= requiere Python 3.9 o superior.")

# 10.4. Usando desempaquetado `**` (Python 3.5+)
# Crea un NUEVO diccionario.
# Si hay claves repetidas, prevalece el valor del último diccionario desempaquetado.
dict_desempaquetado = {**dict1, **dict2}
print(f"10.4. Resultado usando desempaquetado {{**dict1, **dict2}}: {dict_desempaquetado}")

dict_desempaquetado_orden_inverso = {**dict2, **dict1} # 'b' tendrá el valor de dict1
print(f"     Resultado con orden inverso {{**dict2, **dict1}}: {dict_desempaquetado_orden_inverso}")


print("\n====================== 11. DICCIONARIOS POR COMPRENSIÓN ======================")

# Forma concisa de crear diccionarios a partir de iterables.
# Sintaxis: {clave_expresion: valor_expresion for elemento in iterable [if condicion]}

# 11.1. Crear un diccionario con números y sus cuadrados
cuadrados = {x: x*x for x in range(6)}
print(f"11.1. Diccionario de cuadrados: {cuadrados}")

# 11.2. Crear un diccionario a partir de dos listas usando zip
nombres = ['Alice', 'Bob', 'Charlie']
edades = [30, 25, 35]
diccionario_nombres_edades = {nombre: edad for nombre, edad in zip(nombres, edades)}
print(f"11.2. Diccionario creado desde dos listas con zip: {diccionario_nombres_edades}")

# 11.3. Crear un diccionario con condición (solo números pares)
cuadrados_pares = {x: x*x for x in range(10) if x % 2 == 0}
print(f"11.3. Diccionario de cuadrados de números pares: {cuadrados_pares}")

# 11.4. Crear un diccionario invirtiendo claves y valores de otro
# ¡Cuidado! Solo funciona si los valores son únicos y de tipo inmutable (hashable).
original = {'a': 1, 'b': 2, 'c': 3}
invertido = {valor: clave for clave, valor in original.items()}
print(f"11.4. Diccionario original: {original}")
print(f"     Diccionario invertido: {invertido}")

original_con_duplicados = {'a': 1, 'b': 2, 'c': 1} # Valor '1' duplicado
invertido_con_perdida = {valor: clave for clave, valor in original_con_duplicados.items()}
print(f"     Original con valores duplicados: {original_con_duplicados}")
print(f"     Invertido (se pierde una clave porque el valor 1 se sobrescribe): {invertido_con_perdida}")

# 11.5. Crear un diccionario a partir de una cadena
texto = "hola mundo"
conteo_letras = {letra: texto.count(letra) for letra in set(texto) if letra.isalpha()}
print(f"11.5. Conteo de letras en '{texto}': {conteo_letras}")


print("\n====================== 12. DICCIONARIOS ANIDADOS ======================")

# Un diccionario puede contener otros diccionarios como valores.

# 12.1. Crear un diccionario anidado
usuarios = {
    'user1': {
        'nombre': 'Alice',
        'edad': 30,
        'email': 'alice@example.com'
    },
    'user2': {
        'nombre': 'Bob',
        'edad': 25,
        'email': 'bob@example.com',
        'direccion': {
            'calle': '123 Main St',
            'ciudad': 'Anytown'
        }
    }
}
print(f"12.1. Diccionario anidado 'usuarios': {usuarios}")

# 12.2. Acceder a elementos en diccionarios anidados
nombre_user1 = usuarios['user1']['nombre']
print(f"12.2. Nombre de user1: {nombre_user1}")

email_user2 = usuarios.get('user2', {}).get('email', 'No disponible')
print(f"     Email de user2 (usando get anidado seguro): {email_user2}")

ciudad_user2 = usuarios['user2']['direccion']['ciudad']
print(f"     Ciudad de user2: {ciudad_user2}")

# Acceso seguro por si alguna clave intermedia no existe
calle_user_inexistente = usuarios.get('user3', {}).get('direccion', {}).get('calle', 'No encontrada')
print(f"     Calle de user3 (inexistente): {calle_user_inexistente}")

# 12.3. Modificar elementos en diccionarios anidados
usuarios['user1']['edad'] = 31
usuarios['user2']['direccion']['ciudad'] = 'New City'
print(f"12.3. Diccionario 'usuarios' modificado: {usuarios}")

# Añadir nueva información anidada
usuarios['user1']['telefono'] = '555-9876'
usuarios['user2']['direccion']['cp'] = '12345'
print(f"     Diccionario 'usuarios' con más datos añadidos: {usuarios}")


print("\n====================== 13. OTROS MÉTODOS ÚTILES ======================")

# 13.1. setdefault(key[, default])
# Si 'key' está en el diccionario, devuelve su valor.
# Si 'key' no está, inserta 'key' con el valor 'default' (o None si no se especifica)
# y DEVUELVE el valor 'default'. Es útil para inicializar claves si no existen.

config = {'host': 'localhost'}
print(f"13.1. Diccionario 'config' inicial: {config}")

# La clave 'host' existe, devuelve su valor
host = config.setdefault('host', 'default.com')
print(f"     setdefault('host', 'default.com'): {host}")
print(f"     'config' no cambia: {config}")

# La clave 'port' no existe, la añade con el valor 8080 y devuelve 8080
port = config.setdefault('port', 8080)
print(f"     setdefault('port', 8080): {port}")
print(f"     'config' ahora tiene 'port': {config}")

# La clave 'user' no existe, no se da default, se añade con None y devuelve None
user = config.setdefault('user')
print(f"     setdefault('user'): {user}")
print(f"     'config' ahora tiene 'user': {config}")

# Comparación con get(): get() nunca modifica el diccionario.
db_name = config.get('database', 'mydb') # Devuelve 'mydb' pero no lo añade
print(f"     get('database', 'mydb'): {db_name}")
print(f"     'config' sigue sin 'database': {config}")


# 13.2. fromkeys(iterable[, value])
# Crea un NUEVO diccionario con claves tomadas del 'iterable' y
# todas con el mismo 'value' especificado.
# Si 'value' no se especifica, el valor por defecto es None.
# Es un método de clase, se llama desde `dict`.

claves_nuevas = ['nombre', 'edad', 'ciudad']
diccionario_desde_claves = dict.fromkeys(claves_nuevas)
print(f"13.2. dict.fromkeys({claves_nuevas}): {diccionario_desde_claves}")

diccionario_con_valor = dict.fromkeys(claves_nuevas, 'Desconocido')
print(f"     dict.fromkeys({claves_nuevas}, 'Desconocido'): {diccionario_con_valor}")

# El iterable puede ser cualquier cosa, como un string
diccionario_letras = dict.fromkeys('abc', 0)
print(f"     dict.fromkeys('abc', 0): {diccionario_letras}")


print("\n====================== 14. RESTRICCIONES DE LAS CLAVES ======================")

# Las claves de un diccionario DEBEN ser de tipo inmutable.
# Tipos inmutables comunes: int, float, bool, str, tuple (si contiene solo inmutables).
# Tipos mutables (NO válidos como claves): list, dict, set.

diccionario_claves_variadas = {
    1: "Entero",
    3.14: "Flotante",
    True: "Booleano",
    "texto": "String",
    ('a', 1): "Tupla de inmutables"
}
print(f"14. Diccionario con claves inmutables válidas: {diccionario_claves_variadas}")

# Intentar usar una lista como clave (mutable) -> TypeError
try:
    diccionario_error = {[1, 2]: "Lista"}
except TypeError as e:
    print(f"     Error al usar una lista como clave: {e}")

# Intentar usar un diccionario como clave (mutable) -> TypeError
try:
    diccionario_error_2 = {{'a': 1}: "Diccionario"}
except TypeError as e:
    print(f"     Error al usar un diccionario como clave: {e}")

# Una tupla que contiene un mutable TAMPOCO es válida como clave
try:
    tupla_con_lista = ('a', [1, 2])
    diccionario_error_3 = {tupla_con_lista: "Tupla con mutable"}
except TypeError as e:
    print(f"     Error al usar una tupla con un mutable dentro como clave: {e}")


print("\n====================== 15. CONSIDERACIONES DE RENDIMIENTO ======================")

# Los diccionarios en Python están implementados usando tablas hash.
# Esto hace que las operaciones promedio de búsqueda, inserción y eliminación
# de elementos (por clave) sean muy rápidas: O(1) en promedio.
# En el peor de los casos (colisiones de hash muy frecuentes), pueden degradarse a O(n),
# pero esto es raro en la práctica con buenos algoritmos de hash.
# Iterar sobre un diccionario (claves, valores o items) es O(n), donde n es el número de elementos.
# Comprobar la existencia de una clave (`key in dict`) es O(1) en promedio.
# Comprobar la existencia de un valor (`value in dict.values()`) es O(n) porque requiere buscar en todos los valores.

print("15. Operaciones básicas (acceso, inserción, borrado por clave) son O(1) en promedio.")
print("    La iteración y búsqueda de valores son O(n).")


print("\n====================== 16. ORDEN DE LOS DICCIONARIOS ======================")

# Como se mencionó al principio:
# - Python 3.7+: Los diccionarios garantizan el orden de inserción. `popitem()` quita el último insertado.
# - Python 3.6: El orden de inserción era un detalle de implementación en CPython, pero no se debía confiar en él.
# - Python < 3.6: Los diccionarios eran fundamentalmente desordenados.

# Si necesitas un diccionario ordenado y trabajas con versiones < 3.7,
# puedes usar `collections.OrderedDict`. Ofrece funcionalidades similares
# pero garantiza el orden explícitamente en todas las versiones.

from collections import OrderedDict

d_ordenado = OrderedDict()
d_ordenado['primero'] = 1
d_ordenado['segundo'] = 2
d_ordenado['tercero'] = 3
print(f"16. collections.OrderedDict: {d_ordenado}")
# popitem(last=True) por defecto (LIFO), popitem(last=False) para FIFO (primero insertado)
print(f"    popitem() en OrderedDict: {d_ordenado.popitem()}")
print(f"    OrderedDict después de popitem(): {d_ordenado}")

# En Python 3.7+ los diccionarios normales se comportan de forma similar respecto al orden.
d_normal_ordenado = {}
d_normal_ordenado['primero'] = 1
d_normal_ordenado['segundo'] = 2
d_normal_ordenado['tercero'] = 3
print(f"    Diccionario normal en Python 3.7+: {d_normal_ordenado}")
print(f"    popitem() en diccionario normal: {d_normal_ordenado.popitem()}")
print(f"    Diccionario normal después de popitem(): {d_normal_ordenado}")


print("\n====================== FIN DE LOS APUNTES ======================")
# Los diccionarios son una estructura de datos extremadamente útil y versátil
# en Python, fundamental para muchas tareas de programación.