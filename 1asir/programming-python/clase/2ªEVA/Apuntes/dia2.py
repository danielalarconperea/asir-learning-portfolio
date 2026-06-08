'''
Ejercicio 1: Clasificación de Edad y Estado Civil

Escribe un programa en Python que clasifique a las personas según su edad y estado civil. 
El programa debe realizar las siguientes tareas:

--Definir dos variables: age (edad) y civil_status (estado civil).
--Comprobar y mostrar los tipos de las variables age y civil_status.

Utilizar condicionales para clasificar la edad de la siguiente manera:

--Si la edad es menor que 13, imprimir "Es un niño/a".
--Si la edad está entre 13 y 18 (inclusive), imprimir "Es un/a adolescente".
--Si la edad está entre 18 y 60 (inclusive), imprimir "Es un/a adulto/a".
--Si la edad es mayor que 60, imprimir "Es una persona mayor".

Utilizar condicionales para clasificar el estado civil de la siguiente manera:

--Si el estado civil es "single", imprimir "Está soltero/a".
--Si el estado civil es "married", imprimir "Está casado/a".
--Si el estado civil es "divorced", imprimir "Está divorciado/a".
--Si el estado civil es "widowed", imprimir "Está viudo/a".
--En cualquier otro caso, imprimir "Estado civil desconocido".

Combinación de edad y estado civil:

--Si la edad es mayor o igual a 18 y el estado civil es "single", imprimir "Es un adulto soltero".
--Si la edad es mayor o igual a 18 y el estado civil es "married", imprimir "Es un adulto casado".
--En cualquier otro caso, imprimir "Otra combinación".
'''

def Ejercicio1():
    
    # Definir variables
    age = int(input('Dime tu edad: '))
    civil_status = input('Dime tu estado civil: ')

    # Comprobar el tipo de variable
    print(type(age))
    print(type(civil_status))

    # Condicionales para clasificar la edad
    if age < 13:
        print("Es un niño/a")
    elif 13 <= age < 18:
        print("Es un/a adolescente")
    elif 18 <= age < 60:
        print("Es un/a adulto/a")
    else:
        print("Es una persona mayor")

    # Condicionales para clasificar el estado civil
    if civil_status == "single":
        print("Está soltero/a")
    elif civil_status == "married":
        print("Está casado/a")
    elif civil_status == "divorced":
        print("Está divorciado/a")
    elif civil_status == "widowed":
        print("Está viudo/a")
    else:
        print("Estado civil desconocido")

    # Combinación de edad y estado civil
    if age >= 18 and civil_status == "single":
        print("Es un adulto soltero")
    elif age >= 18 and civil_status == "married":
        print("Es un adulto casado")
    else:
        print("Otra combinación")

Ejercicio1()
