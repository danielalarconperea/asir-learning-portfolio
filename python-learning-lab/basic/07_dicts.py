# Clase en vídeo: https://youtu.be/Kp4Mvapo5kc

### Dictionaries ###

# Definición------Son mutables, lo que significa que puedes añadir, eliminar y modificar pares clave-valor después de haberlos creado.

# No permiten claves duplicadas. Si añades una clave que ya existe, su valor será actualizado.

# Dicts: Accedes a los valores usando las claves.
# valor = mi_dict["nombre"]

# Mantienen el orden de inserción de las claves

'''
keys(): Devuelve una vista de las claves del diccionario.

values(): Devuelve una vista de los valores del diccionario.

items(): Devuelve una vista de los pares clave-valor del diccionario.

get(key, default): Devuelve el valor de la clave si está en el diccionario; si no, devuelve el valor por defecto.

update([other]): Actualiza el diccionario con los pares clave-valor de otro diccionario u otro iterable.

pop(key, default): Elimina la clave y devuelve su valor. Si la clave no está en el diccionario, devuelve el valor por defecto.

popitem(): Elimina y devuelve un par clave-valor arbitrario del diccionario.

setdefault(key, default): Devuelve el valor de la clave si está en el diccionario; si no, inserta la clave con el valor por defecto y devuelve el valor por defecto.

clear(): Elimina todos los ítems del diccionario.

copy(): Devuelve una copia superficial del diccionario.
'''

# Crear diccionarios
my_dict = dict()
my_other_dict = {}

print(type(my_dict)) # <class 'dict'>
print(type(my_other_dict)) # <class 'dict'>

my_other_dict = {"Nombre": "Brais", "Apellido": "Moure", "Edad": 35, 1: "Python"}

my_dict = {
    "Nombre": "Brais",
    "Apellido": "Moure",
    "Edad": 35,
    "Lenguajes": {"Python", "Swift", "Kotlin"},
    1: 1.77
}

print(my_other_dict) # {'Nombre': 'Brais', 'Apellido': 'Moure', 'Edad': 35, 1: 'Python'}
print(my_dict) # {'Nombre': 'Brais', 'Apellido': 'Moure', 'Edad': 35, 'Lenguajes': {'Kotlin', 'Swift', 'Python'}, 1: 1.77}

print(len(my_other_dict)) # 4
print(len(my_dict)) # 5

# Búsqueda
print(my_dict[1]) # 1.77
print(my_dict["Nombre"]) # Brais

print("Moure" in my_dict) # False
print("Apellido" in my_dict) # True

# Inserción
my_dict["Calle"] = "Calle MoureDev"
print(my_dict) # {'Nombre': 'Brais', 'Apellido': 'Moure', 'Edad': 35, 'Lenguajes': {'Kotlin', 'Swift', 'Python'}, 1: 1.77, 'Calle': 'Calle MoureDev'}

# Actualización
my_dict["Nombre"] = "Pedro"
print(my_dict["Nombre"]) # Pedro

# Eliminación
del my_dict["Calle"]
print(my_dict) # {'Nombre': 'Pedro', 'Apellido': 'Moure', 'Edad': 35, 'Lenguajes': {'Kotlin', 'Swift', 'Python'}, 1: 1.77}

# Otras operaciones
print(my_dict.items()) # dict_items([('Nombre', 'Pedro'), ('Apellido', 'Moure'), ('Edad', 35), ('Lenguajes', {'Kotlin', 'Swift', 'Python'}), (1, 1.77)])
print(my_dict.keys()) # dict_keys(['Nombre', 'Apellido', 'Edad', 'Lenguajes', 1])
print(my_dict.values()) # dict_values(['Pedro', 'Moure', 35, {'Kotlin', 'Swift', 'Python'}, 1.77])

my_list = ["Nombre", 1, "Piso"]

my_new_dict = dict.fromkeys(my_list)
print(my_new_dict) # {'Nombre': None, 1: None, 'Piso': None}
my_new_dict = dict.fromkeys(("Nombre", 1, "Piso"))
print(my_new_dict) # {'Nombre': None, 1: None, 'Piso': None}
my_new_dict = dict.fromkeys(my_dict)
print(my_new_dict) # {'Nombre': None, 'Apellido': None, 'Edad': None, 'Lenguajes': None, 1: None}
my_new_dict = dict.fromkeys(my_dict, "MoureDev")
print(my_new_dict) # {'Nombre': 'MoureDev', 'Apellido': 'MoureDev', 'Edad': 'MoureDev', 'Lenguajes': 'MoureDev', 1: 'MoureDev'}

my_values = my_new_dict.values()
print(type(my_values)) # <class 'dict_values'>

print(my_new_dict.values()) # dict_values(['MoureDev', 'MoureDev', 'MoureDev', 'MoureDev', 'MoureDev'])
print(list(dict.fromkeys(list(my_new_dict.values())).keys())) # ['MoureDev']
print(tuple(my_new_dict)) # ('Nombre', 'Apellido', 'Edad', 'Lenguajes', 1)
print(set(my_new_dict)) # {'Nombre', 'Edad', 'Apellido', 1, 'Lenguajes'}

'''
Ejercicio 1: Agenda de Contactos
Descripción: Crear una agenda de contactos donde se puedan realizar las siguientes operaciones:

1.Añadir un nuevo contacto.
2.Eliminar un contacto existente.
3.Buscar un contacto por nombre.
4.Mostrar todos los contactos.
5.Actualizar la información de un contacto.

Requisitos:

Utilizar un diccionario para almacenar los contactos, 
donde la clave sea el nombre del contacto y 
el valor sea otro diccionario con la información del contacto 
(teléfono, correo electrónico, dirección).

Implementar las funciones de añadir, eliminar, buscar, mostrar y actualizar contactos.

Utilizar las funciones keys(), values(), items(), get(), update(), 
pop(), popitem(), setdefault(), clear() y copy() en algún punto del ejercicio.
'''
# Funciones para la agenda de contactos

# Definición de la función agregar_contacto
def agregar_contacto(agenda, nombre, telefono, correo, direccion):
    
    # Añade una nueva entrada al diccionario 'agenda'.
    # La clave es el nombre del contacto.
    # El valor es otro diccionario que contiene el teléfono, correo y dirección del contacto.
    agenda[nombre] = {
        "Teléfono": telefono,
        "Correo": correo,
        "Dirección": direccion
    }

# Ejemplo de uso de la función
# Creamos un diccionario vacío llamado 'agenda'
agenda = {}

# Llamamos a la función agregar_contacto para añadir un nuevo contacto a la agenda
agregar_contacto(agenda, "Brais", "123456789", "brais@mouredev.com", "Calle MoureDev")

# Imprimimos la agenda para verificar que el contacto ha sido añadido correctamente
print(agenda)

# Salida esperada en la terminal:
# {'Brais': {'Teléfono': '123456789', 'Correo': 'brais@mouredev.com', 'Dirección': 'Calle MoureDev'}}

# Agregamos otro contacto a la agenda
agregar_contacto(agenda, "Pedro", "987654321", "pedro@example.com", "Calle Ejemplo")

# Imprimimos la agenda nuevamente para verificar que el nuevo contacto ha sido añadido
print(agenda)

# Salida esperada en la terminal:
# {
#   'Brais': {'Teléfono': '123456789', 'Correo': 'brais@mouredev.com', 'Dirección': 'Calle MoureDev'},
#   'Pedro': {'Teléfono': '987654321', 'Correo': 'pedro@example.com', 'Dirección': 'Calle Ejemplo'}
# }

# Definición de la función eliminar_contacto
def eliminar_contacto(agenda, nombre):
    
    # Elimina la entrada del diccionario 'agenda' correspondiente al 'nombre' dado.
    # Si el nombre no existe en la agenda, no hace nada.
    agenda.pop(nombre, None)

    # Ejemplo de uso de la función
    # Creamos un diccionario con algunos contactos
    agenda = {
        "Brais": {"Teléfono": "123456789", "Correo": "brais@mouredev.com", "Dirección": "Calle MoureDev"},
        "Pedro": {"Teléfono": "987654321", "Correo": "pedro@example.com", "Dirección": "Calle Ejemplo"}
    }

    # Imprimimos la agenda antes de eliminar un contacto
    print("Agenda antes de eliminar un contacto:", agenda)

    # Salida esperada en la terminal:
    # Agenda antes de eliminar un contacto: {
    #     'Brais': {'Teléfono': '123456789', 'Correo': 'brais@mouredev.com', 'Dirección': 'Calle MoureDev'},
    #     'Pedro': {'Teléfono': '987654321', 'Correo': 'pedro@example.com', 'Dirección': 'Calle Ejemplo'}
    # }

    # Llamamos a la función eliminar_contacto para eliminar a "Pedro" de la agenda
eliminar_contacto(agenda, "Pedro")

    # Imprimimos la agenda después de eliminar un contacto
print("Agenda después de eliminar un contacto:", agenda)

    # Salida esperada en la terminal:
    # Agenda después de eliminar un contacto: {
    #     'Brais': {'Teléfono': '123456789', 'Correo': 'brais@mouredev.com', 'Dirección': 'Calle MoureDev'}
    # }

    # Intentamos eliminar un contacto que no existe, "Carlos"
eliminar_contacto(agenda, "Carlos")

    # Imprimimos la agenda después de intentar eliminar un contacto que no existe
print("Agenda después de intentar eliminar un contacto que no existe:", agenda)

    # Salida esperada en la terminal:
    # Agenda después de intentar eliminar un contacto que no existe: {
    #     'Brais': {'Teléfono': '123456789', 'Correo': 'brais@mouredev.com', 'Dirección': 'Calle MoureDev'}
    # }

# Definición de la función buscar_contacto
def buscar_contacto(agenda, nombre):

    # Utiliza el método get del diccionario para buscar el contacto.
    # Si el contacto no se encuentra, devuelve "Contacto no encontrado".
    return agenda.get(nombre, "Contacto no encontrado")

# Ejemplo de uso de la función
# Creamos un diccionario con algunos contactos
agenda = {
    "Brais": {"Teléfono": "123456789", "Correo": "brais@mouredev.com", "Dirección": "Calle MoureDev"},
    "Pedro": {"Teléfono": "987654321", "Correo": "pedro@example.com", "Dirección": "Calle Ejemplo"}
}

# Buscamos el contacto "Brais"
resultado_brais = buscar_contacto(agenda, "Brais")
print("Resultado de buscar 'Brais':", resultado_brais)

# Salida esperada en la terminal:
# Resultado de buscar 'Brais': {'Teléfono': '123456789', 'Correo': 'brais@mouredev.com', 'Dirección': 'Calle MoureDev'}

# Buscamos el contacto "Carlos", que no existe en la agenda
resultado_carlos = buscar_contacto(agenda, "Carlos")
print("Resultado de buscar 'Carlos':", resultado_carlos)

# Salida esperada en la terminal:
# Resultado de buscar 'Carlos': Contacto no encontrado

# Definición de la función mostrar_contactos
def mostrar_contactos(agenda):
    
    # Itera a través de todos los elementos (pares clave-valor) en el diccionario 'agenda'.
    for nombre, info in agenda.items():
        # Imprime el nombre del contacto.
        print(f"Nombre: {nombre}")
        
        # Itera a través de todos los elementos (pares clave-valor) en el diccionario 'info' del contacto.
        for clave, valor in info.items():
            # Imprime la clave y el valor del contacto.
            print(f"  {clave}: {valor}")

    # Ejemplo de uso de la función
    # Creamos un diccionario con algunos contactos
    agenda = {
        "Brais": {"Teléfono": "123456789", "Correo": "brais@mouredev.com", "Dirección": "Calle MoureDev"},
        "Pedro": {"Teléfono": "987654321", "Correo": "pedro@example.com", "Dirección": "Calle Ejemplo"}
    }

    # Llamamos a la función mostrar_contactos para mostrar todos los contactos en la agenda
    print("Agenda de Contactos")
mostrar_contactos(agenda)

    # Salida esperada en la terminal:
    # Agenda de Contactos
    # Nombre: Brais
    #   Teléfono: 123456789
    #   Correo: brais@mouredev.com
    #   Dirección: Calle MoureDev
    # Nombre: Pedro
    #   Teléfono: 987654321
    #   Correo: pedro@example.com
    #   Dirección: Calle Ejemplo

# Definición de la función actualizar_contacto
def actualizar_contacto(agenda, nombre, telefono=None, correo=None, direccion=None):
    
    # Comprueba si el contacto existe en la agenda.
    if nombre in agenda:
        # Si se proporciona un nuevo número de teléfono, actualiza el teléfono del contacto.
        if telefono:
            agenda[nombre]["Teléfono"] = telefono
        # Si se proporciona un nuevo correo electrónico, actualiza el correo del contacto.
        if correo:
            agenda[nombre]["Correo"] = correo
        # Si se proporciona una nueva dirección, actualiza la dirección del contacto.
        if direccion:
            agenda[nombre]["Dirección"] = direccion
    else:
        # Si el nombre no está en la agenda, imprime un mensaje indicando que el contacto no se encontró.
        print("Contacto no encontrado")

    # Ejemplo de uso de la función
    # Creamos un diccionario con algunos contactos
    agenda = {
        "Brais": {"Teléfono": "123456789", "Correo": "brais@mouredev.com", "Dirección": "Calle MoureDev"},
        "Pedro": {"Teléfono": "987654321", "Correo": "pedro@example.com", "Dirección": "Calle Ejemplo"}
    }

    # Imprimimos la agenda antes de actualizar un contacto
    print("Agenda antes de actualizar un contacto:", agenda)

    # Salida esperada en la terminal:
    # Agenda antes de actualizar un contacto: {
    #     'Brais': {'Teléfono': '123456789', 'Correo': 'brais@mouredev.com', 'Dirección': 'Calle MoureDev'},
    #     'Pedro': {'Teléfono': '987654321', 'Correo': 'pedro@example.com', 'Dirección': 'Calle Ejemplo'}
    # }

    # Llamamos a la función actualizar_contacto para actualizar la información de "Brais"
actualizar_contacto(agenda, "Brais", telefono="1122334455", correo="nuevo_correo@mouredev.com")

    # Imprimimos la agenda después de actualizar el contacto
print("Agenda después de actualizar un contacto:", agenda)

    # Salida esperada en la terminal:
    # Agenda después de actualizar un contacto: {
    #     'Brais': {'Teléfono': '1122334455', 'Correo': 'nuevo_correo@mouredev.com', 'Dirección': 'Calle MoureDev'},
    #     'Pedro': {'Teléfono': '987654321', 'Correo': 'pedro@example.com', 'Dirección': 'Calle Ejemplo'}
    # }

    # Intentamos actualizar un contacto que no existe, "Carlos"
actualizar_contacto(agenda, "Carlos", telefono="0000000000")

    # Salida esperada en la terminal:
    # Contacto no encontrado


# Ejemplo de uso de la agenda de contactos
print("\nAgenda de Contactos")
agenda = {}
agregar_contacto(agenda, "Brais", "123456789", "brais@mouredev.com", "Calle MoureDev")
agregar_contacto(agenda, "Pedro", "987654321", "pedro@example.com", "Calle Ejemplo")

# Mostramos todos los contactos
mostrar_contactos(agenda)
# Salida esperada:
# Nombre: Brais
#   Teléfono: 123456789
#   Correo: brais@mouredev.com
#   Dirección: Calle MoureDev
# Nombre: Pedro
#   Teléfono: 987654321
#   Correo: pedro@example.com
#   Dirección: Calle Ejemplo

# Actualizamos el correo de Brais
actualizar_contacto(agenda, "Brais", correo="nuevo_correo@mouredev.com")

# Eliminamos a Pedro
eliminar_contacto(agenda, "Pedro")

# Mostramos los contactos después de la actualización y eliminación
mostrar_contactos(agenda)

# Salida esperada:
# Nombre: Brais
#   Teléfono: 123456789
#   Correo: nuevo_correo@mouredev.com
#   Dirección: Calle MoureDev

'''
Ejercicio 2: Sistema de Inventario
Descripción: Crear un sistema de inventario para una tienda donde se puedan realizar las siguientes operaciones:

1.Añadir un nuevo producto.
2.Eliminar un producto existente.
3.Buscar un producto por nombre.
4.Mostrar todos los productos.
5.Actualizar la cantidad de un producto.

Requisitos:
Utilizar un diccionario para almacenar los productos, donde la clave sea el nombre del producto 
y el valor sea otro diccionario con la información del producto (precio, cantidad, categoría).

Implementar las funciones de añadir, eliminar, buscar, mostrar y actualizar productos.

Utilizar las funciones keys(), values(), items(), get(), update(), 
pop(), popitem(), setdefault(), clear() y copy() en algún punto del ejercicio.
'''

# Funciones para el sistema de inventario

def agregar_producto(inventario, nombre, precio, cantidad, categoria):
    """Añade un nuevo producto al inventario"""
    inventario[nombre] = {
        "Precio": precio,
        "Cantidad": cantidad,
        "Categoría": categoria
    }

def eliminar_producto(inventario, nombre):
    """Elimina un producto del inventario"""
    inventario.pop(nombre, None)

# Definición de la función buscar_producto
def buscar_producto(inventario, nombre):
    
    # Utiliza el método get del diccionario para buscar el producto.
    # Si el producto no se encuentra, devuelve "Producto no encontrado".
    return inventario.get(nombre, "Producto no encontrado")

# Ejemplo de uso de la función
# Creamos un diccionario con algunos productos
inventario = {
    "Manzanas": {"Precio": 1.5, "Cantidad": 50, "Categoría": "Frutas"},
    "Pan": {"Precio": 0.8, "Cantidad": 30, "Categoría": "Panadería"}
}

# Buscamos el producto "Manzanas"
resultado_manzanas = buscar_producto(inventario, "Manzanas")
print("Resultado de buscar 'Manzanas':", resultado_manzanas)

# Salida esperada en la terminal:
# Resultado de buscar 'Manzanas': {'Precio': 1.5, 'Cantidad': 50, 'Categoría': 'Frutas'}

# Buscamos el producto "Leche", que no existe en el inventario
resultado_leche = buscar_producto(inventario, "Leche")
print("Resultado de buscar 'Leche':", resultado_leche)

# Salida esperada en la terminal:
# Resultado de buscar 'Leche': Producto no encontrado

# Definición de la función mostrar_productos


def mostrar_productos(inventario):
    
    # Itera a través de todos los elementos (pares clave-valor) en el diccionario 'inventario'.
    for nombre, info in inventario.items():
        # Imprime el nombre del producto.
        print(f"Producto: {nombre}")
        
        # Itera a través de todos los elementos (pares clave-valor) en el diccionario 'info' del producto.
        for clave, valor in info.items():
            # Imprime la clave y el valor del producto.
            print(f"  {clave}: {valor}")

# Ejemplo de uso de la función
# Creamos un diccionario con algunos productos
inventario = {
    "Manzanas": {"Precio": 1.5, "Cantidad": 50, "Categoría": "Frutas"},
    "Pan": {"Precio": 0.8, "Cantidad": 30, "Categoría": "Panadería"}
}

# Llamamos a la función mostrar_productos para mostrar todos los productos en el inventario
print("Inventario de Productos")
mostrar_productos(inventario)

# Salida esperada en la terminal:
# Inventario de Productos
# Producto: Manzanas
#   Precio: 1.5
#   Cantidad: 50
#   Categoría: Frutas
# Producto: Pan
#   Precio: 0.8
#   Cantidad: 30
#   Categoría: Panadería


def actualizar_cantidad(inventario, nombre, cantidad):
    """Actualiza la cantidad de un producto existente"""
    if nombre in inventario:
        inventario[nombre]["Cantidad"] = cantidad
    else:
        print("Producto no encontrado")

# Ejemplo de uso del sistema de inventario
print("\nSistema de Inventario")# Definición de la función actualizar_cantidad
def actualizar_cantidad(inventario, nombre, cantidad):
   
    # Comprueba si el producto existe en el inventario.
    if nombre in inventario:
        # Si el producto existe, actualiza su cantidad con el nuevo valor.
        inventario[nombre]["Cantidad"] = cantidad
    else:
        # Si el producto no existe, imprime un mensaje indicando que no se encontró el producto.
        print("Producto no encontrado")

# Ejemplo de uso de la función
# Creamos un diccionario con algunos productos
inventario = {
    "Manzanas": {"Precio": 1.5, "Cantidad": 50, "Categoría": "Frutas"},
    "Pan": {"Precio": 0.8, "Cantidad": 30, "Categoría": "Panadería"}
}

# Imprimimos el inventario antes de actualizar la cantidad de un producto
print("Inventario antes de actualizar la cantidad de un producto:", inventario)

# Salida esperada en la terminal:
# Inventario antes de actualizar la cantidad de un producto: {
#     'Manzanas': {'Precio': 1.5, 'Cantidad': 50, 'Categoría': 'Frutas'},
#     'Pan': {'Precio': 0.8, 'Cantidad': 30, 'Categoría': 'Panadería'}
# }

# Llamamos a la función actualizar_cantidad para actualizar la cantidad de "Manzanas"
actualizar_cantidad(inventario, "Manzanas", 60)

# Imprimimos el inventario después de actualizar la cantidad del producto
print("Inventario después de actualizar la cantidad de un producto:", inventario)

# Salida esperada en la terminal:
# Inventario después de actualizar la cantidad de un producto: {
#     'Manzanas': {'Precio': 1.5, 'Cantidad': 60, 'Categoría': 'Frutas'},
#     'Pan': {'Precio': 0.8, 'Cantidad': 30, 'Categoría': 'Panadería'}
# }

# Intentamos actualizar la cantidad de un producto que no existe, "Leche"
actualizar_cantidad(inventario, "Leche", 20)

# Salida esperada en la terminal:
# Producto no encontrado




inventario = {}
agregar_producto(inventario, "Manzanas", 1.5, 50, "Frutas")
agregar_producto(inventario, "Pan", 0.8, 30, "Panadería")

# Mostramos todos los productos del inventario
mostrar_productos(inventario)

# Salida esperada:
# Producto: Manzanas
#   Precio: 1.5
#   Cantidad: 50
#   Categoría: Frutas
# Producto: Pan
#   Precio: 0.8
#   Cantidad: 30
#   Categoría: Panadería

# Actualizamos la cantidad de manzanas
actualizar_cantidad(inventario, "Manzanas", 60)

# Eliminamos el pan del inventario
eliminar_producto(inventario, "Pan")

# Mostramos los productos después de la actualización y eliminación
mostrar_productos(inventario)

# Salida esperada:
# Producto: Manzanas
#   Precio: 1.5
#   Cantidad: 60
#   Categoría: Frutas
