# Clase en vídeo: https://youtu.be/Kp4Mvapo5kc?t=14711

### Tuples ###

# Definición------------Son inmutables, lo que significa que no puedes cambiar sus elementos una vez creadas

'''
Las tuplas, al ser inmutables, tienen menos métodos:

count(x): Devuelve el número de veces que el ítem aparece en la tupla.

index(x[, start[, end]]): Devuelve el índice de la primera aparición del ítem.
'''

my_tuple = tuple()
my_other_tuple = ()

my_tuple = (35, 1.77, "Brais", "Moure", "Brais")
my_other_tuple = (35, 60, 30)

print(my_tuple)
print(type(my_tuple))

# Acceso a elementos y búsqueda

print(my_tuple[0])
print(my_tuple[-1])
# print(my_tuple[4]) IndexError
# print(my_tuple[-6]) IndexError

print(my_tuple.count("Brais"))#cuenta cuantas veces aparece este elemento en la tupla
print(my_tuple.index("Moure"))#Encuentra la primera posición (índice) del elemento en la tupla
print(my_tuple.index("Brais"))

# my_tuple[1] = 1.80 'tuple' object does not support item assignment

# Concatenación

my_sum_tuple = my_tuple + my_other_tuple
print(my_sum_tuple)

# Subtuplas

print(my_sum_tuple[3:6])

# Tupla mutable con conversión a lista

my_tuple = list(my_tuple)
print(type(my_tuple))

my_tuple[4] = "MoureDev"
my_tuple.insert(1, "Azul")
my_tuple = tuple(my_tuple)
print(my_tuple)
print(type(my_tuple))

# Eliminación

# del my_tuple[2] TypeError: 'tuple' object doesn't support item deletion

del my_tuple
# print(my_tuple) NameError: name 'my_tuple' is not defined




'''
### Ejercicio 1: Gestión de Datos Personales

**Descripción:**
Tienes que gestionar los datos personales de un individuo utilizando tuplas y listas. 
Necesitarás realizar operaciones como el acceso a elementos, búsqueda, concatenación de tuplas, extracción de subtuplas y 
la conversión de tuplas a listas para poder modificar sus elementos.

**Objetivos:**
1. Crear dos tuplas que contengan información personal.
2. Imprimir las tuplas y el tipo de dato que representan.
3. Acceder a elementos específicos de las tuplas e imprimirlos.
4. Contar cuántas veces aparece un elemento específico en una tupla.
5. Encontrar la posición de un elemento en una tupla.
6. Concatenar dos tuplas y mostrar el resultado.
7. Crear subtuplas a partir de la tupla concatenada.
8. Convertir una tupla a lista, modificar sus elementos, y volver a convertirla a tupla.
'''
def ejercicio_1():

    # 1. Definir las tuplas
    tupla1 = ('Daniel', 'Alarcon', 18, 'estudiante', 18)
    tupla2 = ('pepe', 'meme', 1, 'crypto')

    # 2. Imprimir las tuplas y su tipo
    print(tupla1) # ('Daniel', 'Alarcon', 18, 'estudiante', 18)
    print(tupla2) # ('pepe', 'meme', 1, 'crypto')
    print(type(tupla1)) # <class 'tuple'>
    print(type(tupla2)) # <class 'tuple'>

    # 3. Acceso a elementos y búsqueda
    print(tupla1[0])  # Daniel
    print(tupla2[1])  # meme
    print(tupla1[2])  # 18
    print(tupla2[-1]) # crypto

    # 4. Contar un elemento
    print(tupla1.count(18))       # 2
    print(tupla1.count('Daniel')) # 1

    # 5. Posición de un elemento
    print(tupla1.index("estudiante")) # 3
    print(tupla1.index(18))           # 2 (te devuelve "2", el primer '18' de la lista)

    # 6. Concatenación de tuplas
    sum_tuple = tupla1 + tupla2
    print(sum_tuple)  # ('Daniel', 'Alarcon', 18, 'estudiante', 18, 'pepe', 'meme', 1, 'crypto')

    # 7. Subtupla a través de una tupla concatenada
    subtupla1 = sum_tuple[3:6]
    subtupla2 = sum_tuple[0:3]
    print(subtupla1)  # ('estudiante', 18, 'pepe')
    print(subtupla2)  # ('Daniel', 'Alarcon', 18)

    # 8. Convertir a lista
    tupla2 = ('pepe', 'meme', 1, 'crypto')
    tupla2 = list(tupla2)
    print(type(tupla2))  # <class 'list'>
    tupla2[3] = "MoureDev"   # Sustituye el elemento en ese lugar
    tupla2.insert(1, "Azul") # Inserta el elemento "Azul" en la posición 1 (índice 1)
    tupla2.append(200)       # Añade el elemento 200 al final de la lista tupla2
    tupla2 = tuple(tupla2)
    print(tupla2)  # ('pepe', 'Azul', 'meme', 1, 'MoureDev', 200)
    print(type(tupla2))  # <class 'tuple'>

ejercicio_1()

'''
Ejercicio 2: Operaciones Avanzadas con Tuplas
Descripción: En este ejercicio, trabajarás con tuplas para realizar operaciones avanzadas. 
Aprenderás a usar operaciones como desempaquetado, manejo de tuplas anidadas, y técnicas de recorrido y manipulación de tuplas.

Instrucciones:

1.Desempaquetado de una tupla:
--Define una tupla llamada persona que contenga nombre, apellido, edad y profesión.
--Desempaqueta los elementos de la tupla en variables individuales y muéstralos en pantalla.

2.Trabajar con tuplas anidadas:
--Define una tupla anidada que contenga información sobre varias personas (nombre, edad, profesión).
--Recorre la tupla anidada e imprime la información de cada persona en formato de cadena.

3.Recorrer tuplas usando diferentes métodos:
--Define una tupla llamada colores con varios colores.
--Recorre la tupla utilizando un bucle for y muestra cada color.
--Recorre la tupla usando indexado y muestra cada color.
--Recorre la tupla utilizando enumerate y muestra cada color con su índice.

4.Comparación entre tuplas:
--Define dos tuplas tupla1 y tupla2 con algunos elementos.
--Compara si las tuplas son iguales y muestra el resultado.
--Compara si tupla1 es menor que tupla2 y muestra el resultado.

5.Comprobar si un elemento está en una tupla:
--Define una tupla llamada numeros con varios números.
--Comprueba si el número 30 está en la tupla y muestra el resultado.
--Comprueba si el número 100 está en la tupla y muestra el resultado.
'''
def ejercicio2():

    # 1. Desempaquetado de una tupla
    persona = ("Juan", "Perez", 30, "Ingeniero")
    nombre, apellido, edad, profesion = persona
    print("Nombre:", nombre)  # Nombre: Juan
    print("Apellido:", apellido)  # Apellido: Perez
    print("Edad:", edad)  # Edad: 30
    print("Profesión:", profesion)  # Profesión: Ingeniero

    # 2. Trabajar con tuplas anidadas
    tupla_anidada = (("Daniel", 28, "Doctor"), ("Laura", 32, "Abogada"), ("Pedro", 25, "Ingeniero"))
    for individuo in tupla_anidada:
        nombre, edad, profesion = individuo
        print(f"{nombre} tiene {edad} años y es {profesion}")
        # Daniel tiene 28 años y es Doctor
        # Laura tiene 32 años y es Abogada
        # Pedro tiene 25 años y es Ingeniero

    # 3. Recorrer tuplas usando diferentes métodos
    colores = ("rojo", "verde", "azul", "amarillo")
    print("Recorrido usando un bucle for:")
    for color in colores:
        print(color)
        # rojo
        # verde
        # azul
        # amarillo

    print("Recorrido usando indexado:")
    for i in range(len(colores)):
        print(colores[i])
        # rojo
        # verde
        # azul
        # amarillo

    print("Recorrido usando enumerate:")
    for index, color in enumerate(colores):
        print(f"Color en la posición {index}: {color}")
        # Color en la posición 0: rojo
        # Color en la posición 1: verde
        # Color en la posición 2: azul
        # Color en la posición 3: amarillo

    # 4. Comparación entre tuplas:
    tupla1 = (1, 2, 3)
    tupla2 = (1, 2, 4)
    print("¿Son las tuplas iguales?", tupla1 == tupla2)  # ¿Son las tuplas iguales? False
    print("¿Tupla1 es menor que tupla2?", tupla1 < tupla2)  # ¿Tupla1 es menor que tupla2? True

    # 5. Comprobar si un elemento está en una tupla:
    numeros = (10, 20, 30, 40, 50)
    print("¿30 está en la tupla?", 30 in numeros)  # ¿30 está en la tupla? True
    print("¿100 está en la tupla?", 100 in numeros)  # ¿100 está en la tupla? False

ejercicio2()