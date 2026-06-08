# Clase en vídeo: https://youtu.be/Kp4Mvapo5kc?t=21442

### Conditionals ###

# if

my_condition = False

print(type(my_condition))

if my_condition:  # Es lo mismo que if my_condition == True:
    print("Se ejecuta la condición del if")

my_condition = 5 * 5

if my_condition == 10:
    print("Se ejecuta la condición del segundo if")

# if, elif, else

if my_condition > 10 and my_condition < 20:
    print("Es mayor que 10 y menor que 20")
elif my_condition == 25:
    print("Es igual a 25")
else:
    print("Es menor o igual que 10 o mayor o igual que 20 o distinto de 25")

print("La ejecución continúa")

# Condicional con ispección de valor

my_string = ""

if not my_string:
    print("Mi cadena de texto es vacía")

if my_string == "Mi cadena de textoooooo":
    print("Estas cadenas de texto coinciden")





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

'''
Ejercicio 2: Sistema de Calificaciones y Bonificaciones

Escribe un programa en Python que calcule la calificación final de un estudiante y asigne una bonificación según su rendimiento. 
El programa debe realizar las siguientes tareas:

--Definir dos variables: score (puntaje) y extra_credit (bonificación extra).
--Comprobar y mostrar los tipos de las variables score y extra_credit.

Utilizar condicionales para determinar la calificación final del estudiante de la siguiente manera:

--Si el puntaje es mayor o igual a 90, la calificación final es "A".
--Si el puntaje está entre 80 y 90 (sin incluir 90), la calificación final es "B".
--Si el puntaje está entre 70 y 80 (sin incluir 80), la calificación final es "C".
--Si el puntaje está entre 60 y 70 (sin incluir 70), la calificación final es "D".
--Si el puntaje es menor que 60, la calificación final es "F".
--Imprimir la calificación final.

Utilizar condicionales para asignar una bonificación de la siguiente manera:

--Si el puntaje es mayor o igual a 85 y tiene bonificación extra, imprimir "El estudiante recibe una bonificación por mérito".
--Si el puntaje es menor que 60 y no tiene bonificación extra, imprimir "El estudiante necesita mejorar su desempeño".
--En cualquier otro caso, imprimir "El estudiante no recibe bonificación".

Combinación de calificación y bonificación:

--Si la calificación final es "A" y tiene bonificación extra, imprimir "Excelente desempeño con bonificación".
--Si la calificación final es "F" y no tiene bonificación extra, imprimir "Mal desempeño sin bonificación".
--En cualquier otro caso, imprimir "Rendimiento satisfactorio".
'''

def Ejercicio2():

    # Definir variables
    score = int(input('Dime tu puntuaje: '))
    extra_credit = bool(input('Dime si tienes bonificación exra True/False: '))

    # Comprobar el tipo de variable
    print(type(score))
    print(type(extra_credit))

    # Condicionales para determinar la calificación
    if score >= 90:
        final_grade = "A"
    elif 80 <= score < 90:
        final_grade = "B"
    elif 70 <= score < 80:
        final_grade = "C"
    elif 60 <= score < 70:
        final_grade = "D"
    else:
        final_grade = "F"

    print("La calificación final es:", final_grade)

    # Condicionales para asignar bonificación
    if score >= 85 and extra_credit:
        print("El estudiante recibe una bonificación por mérito")
    elif score < 60 and not extra_credit:
        print("El estudiante necesita mejorar su desempeño")
    else:
        print("El estudiante no recibe bonificación")

    # Combinación de calificación y bonificación
    if final_grade == "A" and extra_credit:
        print("Excelente desempeño con bonificación")
    elif final_grade == "F" and not extra_credit:
        print("Mal desempeño sin bonificación")
    else:
        print("Rendimiento satisfactorio")

Ejercicio2()