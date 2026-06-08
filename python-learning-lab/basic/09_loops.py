# Clase en vídeo: https://youtu.be/Kp4Mvapo5kc?t=23822 

### Loops ###

# While

my_condition = 0

while my_condition < 10:
    print(my_condition)
    my_condition += 2
else:  # Es opcional
    print("Mi condición es mayor o igual que 10")

print("La ejecución continúa")

while my_condition < 20:
    my_condition += 1
    if my_condition == 15:
        print("Se detiene la ejecución")
        break
    print(my_condition)

print("La ejecución continúa")
my_condition=5
while my_condition < 20:
    my_condition += 1
    if my_condition == 8:
        print('numero 8')
    elif my_condition == 10:
        print('numero 10')
    elif my_condition == 15:
        print("La ejecución continúa")
        continue
    elif my_condition == 18:
        print('numero 18')
    print(my_condition)

print("La ejecución continúa")

# For

my_list = [35, 24, 62, 52, 30, 30, 17]

for element in my_list:
    print(element)

my_tuple = (35, 1.77, "Brais", "Moure", "Brais")

for element in my_tuple:
    print(element)

my_set = {"Brais", "Moure", 35}

for element in my_set:
    print(element)

my_dict = {"Nombre": "Brais", "Apellido": "Moure", "Edad": 35, 1: "Python"}

for element in my_dict:
    print(element)
    if element == "Edad":
        break
else:
    print("El bucle for para el diccionario ha finalizado")

print("La ejecución continúa")

for element in my_dict:
    print(element)
    if element == "Edad":
        continue
    print("Se ejecuta")
else:
    print("El bluce for para diccionario ha finalizado")

print('\n------------------------------\n')
'''
Ejercicio 1: Análisis de datos meteorológicos

Analizar datos de temperaturas registradas durante un mes, identificando días de calor y días de frío, 
calculando la temperatura media y encontrando la primera temperatura que supere un valor de referencia.

Instrucciones:

Lista de temperaturas: 
Considera una lista de temperaturas (en grados Celsius) que representa los datos meteorológicos registrados durante un mes.

Contar días de calor y días de frío: 
Usa bucles for y condicionales if-elif-else para contar los días en los que la temperatura fue igual o mayor a 25 grados (días de calor) 
y los días en los que la temperatura fue igual o menor a 18 grados (días de frío).

Calcular la temperatura media: 
Suma todas las temperaturas y divide el total entre el número de días para obtener la temperatura media.

Encontrar la primera temperatura mayor a un valor de referencia: 
Usa un bucle while para recorrer la lista de temperaturas y encontrar la primera que sea mayor a un valor de referencia dado. 
Si la encuentras, imprime el valor y el día correspondiente. 
Si no, indica que no se encontró ninguna temperatura mayor al valor de referencia.
'''


# Datos meteorológicos de temperaturas (en grados Celsius) registrados durante un mes
temperaturas = [23, 21, 19, 22, 24, 26, 28, 27, 25, 23, 22, 21, 19, 17, 16, 18, 20, 22, 24, 25, 23, 21, 20, 18, 17, 19, 21, 22, 23, 24]

# Analizar temperaturas
dias_calor = 0
dias_frio = 0
temp_total = 0

for temp in temperaturas:
    if temp >= 25:
        dias_calor += 1
    elif temp <= 18:
        dias_frio += 1
    temp_total += temp # sum(temperaturas) es lo mismo

temp_media = temp_total / len(temperaturas)

print(f"Días de calor: {dias_calor}")
print(f"Días de frío: {dias_frio}")
print(f"Temperatura media: {temp_media:.2f}°C")

# Usar bucle while para encontrar la primera temperatura mayor a un valor dado
valor_referencia = 26
indice = 0

while indice < len(temperaturas):
    if temperaturas[indice] > valor_referencia:
        print(f"La primera temperatura mayor a {valor_referencia}°C es {temperaturas[indice]}°C en el día {indice + 1}")
        break
    indice += 1
else:
    print(f"No se encontró ninguna temperatura mayor a {valor_referencia}°C")

print("Análisis completo")

print('\n------------------------------\n')
'''
Ejercicio 2: Sistema de inventario para una tienda

Gestionar el inventario de una tienda mediante la actualización de productos, simulación de ventas 
y determinación de productos que necesitan reabastecimiento.

Instrucciones:

Inventario inicial: 
Define un diccionario con el inventario inicial de productos, 
donde las claves son los nombres de los productos y los valores son las cantidades disponibles.

Mostrar inventario: 
Crea una función que recorra el diccionario e imprima el nombre de cada producto y su cantidad disponible.

Añadir nuevos productos: 
Crea una lista de tuplas que representen nuevos productos a añadir al inventario. 
Usa un bucle for para añadir estos productos al diccionario de inventario.

Simular ventas: 
Define una lista de tuplas que representen ventas de productos. 
Usa un bucle for para actualizar el inventario según las ventas, restando la cantidad vendida de la cantidad disponible en el inventario. 
Implementa condicionales if-else para manejar casos en los que el stock no sea suficiente o el producto no esté en el inventario.

Verificar reabastecimiento: 
Usa un bucle for y condicionales if para identificar productos cuya cantidad sea menor a 10 unidades 
y añádelos a una lista de productos que necesitan reabastecimiento. 
Si hay productos que necesitan reabastecimiento, imprímelos; si no, indica que no es necesario reabastecer ningún producto en este momento.
'''

# Inventario inicial de productos y sus cantidades
inventario = {
    "Manzanas": 50,
    "Naranjas": 30,
    "Peras": 20,
    "Plátanos": 10
}

# Función para mostrar el inventario
def mostrar_inventario(inventario):
    for producto, cantidad in inventario.items():
        print(f"{producto}: {cantidad} unidades")

# Añadir nuevos productos
nuevos_productos = [("Kiwis", 15), ("Mangos", 25), ("Uvas", 40)]

for producto, cantidad in nuevos_productos:
    inventario[producto] = cantidad

print("Inventario actualizado después de añadir nuevos productos:")
mostrar_inventario(inventario)

# Simular ventas y actualizaciones de inventario
ventas = [("Manzanas", 5), ("Plátanos", 2), ("Uvas", 10)]

for producto, cantidad_vendida in ventas:
    if producto in inventario:
        if inventario[producto] >= cantidad_vendida:
            inventario[producto] -= cantidad_vendida
            print(f"Venta realizada: {cantidad_vendida} unidades de {producto}")
        else:
            print(f"No hay suficiente stock de {producto} para vender {cantidad_vendida} unidades")
    else:
        print(f"Producto {producto} no encontrado en el inventario")

print("Inventario después de las ventas:")
mostrar_inventario(inventario)

# Verificar si algún producto necesita reabastecimiento (cantidad < 10)
reabastecer = []

for producto, cantidad in inventario.items():
    if cantidad < 10:
        reabastecer.append(producto)

if reabastecer:
    print("Productos que necesitan reabastecimiento:", reabastecer)
else:
    print("No es necesario reabastecer ningún producto en este momento")

print("Gestión de inventario completa")
