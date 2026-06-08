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
agregar_contacto(agenda, "Brais", "123456789", "brais@mouredev.com", "Calle MoureDev\n")

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

agenda2={}

agenda2['comida'] = {
        "Teléfono": 4563456,
        "Correo": 'sdfasdf@sdhsdf.fd',
        "Dirección": 'muy lejos'
    }

agenda2['otra cosa'] = (
        4563456,
        "Correo",
        'muy lejos'
    )
print(agenda2)

print('print con get:', agenda2.get('otra cosa', 'clave no encontrada'))

print('print con get:', agenda2.get('dsfasdf', 'clave no encontrada'))

my_dict = {
    "Nombre": "Brais",
    "Apellido": "Moure",
    "Edad": 35,
    "Lenguajes": {"Python", "Swift", "Kotlin"},
    1: 1.77
}
print()

for i in range(len(my_dict["Nombre"])):
    print(my_dict["Nombre"][i])

for i in my_dict:
    print(f'{i} : {my_dict[i]}')


# my_dict.get('Nombre') && my_dict['Nombre']

# my_dict.pop('Nombre')
# print(my_dict)

print(my_dict['Nombre'])

print(my_dict.setdefault('Nombre', 'hola'))

print(my_dict.setdefault('saludo', 'hola'))

print(my_dict)

print(my_dict.items()[1])