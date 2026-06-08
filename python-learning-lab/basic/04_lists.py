# Clase en vídeo: https://youtu.be/Kp4Mvapo5kc?t=10872

### Lists ###

# Definición----------Son mutables, lo que significa que puedes modificar sus elementos después de haberlas creado (añadir, eliminar o cambiar elementos)

'''
Las listas tienen una amplia variedad de métodos debido a su mutabilidad:

append(x): Añade un ítem al final de la lista.

extend(iterable): Extiende la lista añadiendo todos los ítems de un iterable.

insert(i, x): Inserta un ítem en una posición específica.

remove(x): Elimina la primera aparición del ítem.

pop([i]): Elimina y devuelve el ítem en la posición dada.

clear(): Elimina todos los ítems de la lista.

index(x[, start[, end]]): Devuelve el índice de la primera aparición del ítem.

count(x): Devuelve el número de veces que el ítem aparece en la lista.

sort(key=None, reverse=False): Ordena los ítems de la lista.

reverse(): Invierte los ítems de la lista.

copy(): Devuelve una copia superficial de la lista.
'''

my_list = list()
my_other_list = []

print(len(my_list))  # --- 0

my_list = [35, 24, 62, 52, 30, 30, 17]

print(my_list)  # --- [35, 24, 62, 52, 30, 30, 17]
print(len(my_list))  # --- 7

my_other_list = [35, 1.77, "Brais", "Moure"]

print(type(my_list))  # --- <class 'list'>
print(type(my_other_list))  # --- <class 'list'>

# Acceso a elementos y búsqueda

print(my_other_list[0])  # --- 35
print(my_other_list[1])  # --- 1.77
print(my_other_list[-1])  # --- Moure
print(my_other_list[-4])  # --- 35
print(my_list.count(30))  # --- 2
# print(my_other_list[4]) IndexError: list index out of range
# print(my_other_list[-5]) IndexError: list index out of range

print(my_other_list.index("Brais"))  # --- 2

age, height, name, surname = my_other_list
print(name)  # --- Brais

name, height, age, surname = my_other_list[2], my_other_list[1], my_other_list[0], my_other_list[3]
print(age)  # --- 35

# Concatenación

print(my_list + my_other_list)  # --- [35, 24, 62, 52, 30, 30, 17, 35, 1.77, 'Brais', 'Moure']
#print(my_list - my_other_list)  # TypeError: unsupported operand type(s) for -: 'list' and 'list'


# Usamos el método extend() para añadir todos los ítems de la tupla a lista1
lista1 = ['a', 'b', 'c']
tupla = ('d', 'e', 'f')
lista1.extend(tupla)
print(lista1) # --- ['a', 'b', 'c', 'd', 'e', 'f']

# Usamos el método extend() para añadir todos los ítems de la str a lista
lista = [1, 2, 3]
cadena = "abc"
lista.extend(cadena)
print(lista)  # --- [1, 2, 3, 'a', 'b', 'c']


# Creación, inserción, actualización y eliminación

my_other_list.append("MoureDev")
print(my_other_list)  # --- [35, 1.77, 'Brais', 'Moure', 'MoureDev']

my_other_list.insert(1, "Rojo")
print(my_other_list)  # --- [35, 'Rojo', 1.77, 'Brais', 'Moure', 'MoureDev']

my_other_list[1] = "Azul"
print(my_other_list)  # --- [35, 'Azul', 1.77, 'Brais', 'Moure', 'MoureDev']

my_other_list.remove("Azul")
print(my_other_list)  # --- [35, 1.77, 'Brais', 'Moure', 'MoureDev']

my_list.remove(30)
print(my_list)  # --- [35, 24, 62, 52, 30, 17]

print(my_list.pop())  # --- 17
print(my_list)  # --- [35, 24, 62, 52, 30]

my_pop_element = my_list.pop(2)
print(my_pop_element)  # --- 62
print(my_list)  # --- [35, 24, 52, 30]

del my_list[2]
print(my_list)  # --- [35, 24, 30]

# Operaciones con listas

my_new_list = my_list.copy()

my_list.clear()
print(my_list)  # --- []
print(my_new_list)  # --- [35, 24, 30]

my_new_list.reverse()
print(my_new_list)  # --- [30, 24, 35]

my_new_list.sort()
print(my_new_list)  # --- [24, 30, 35]

# Sublistas

print(my_new_list[1:3])  # --- [30, 35]

# Cambio de tipo

my_list = "Hola Python"
print(my_list)  # --- Hola Python
print(type(my_list))  # --- <class 'str'>

# --------------------------------------------------------------------------------------------------------
'''
Ejercicio 1: Gestor de Tareas
Objetivo: Crear un programa que gestione una lista de tareas pendientes. 
El usuario puede añadir, eliminar y ver las tareas.

Crear una lista vacía para almacenar las tareas.

Implementar un menú para que el usuario pueda elegir entre diferentes opciones: 
añadir tarea, eliminar tarea, mostrar todas las tareas y salir.

Utilizar métodos de listas como append, remove, pop, y index.
'''

def gestor_de_tareas():
    tareas = []

    while True:

        print("\n------------------------------")
        print("Gestor de Tareas")
        print("1. Añadir tarea")
        print("2. Eliminar tarea")
        print("3. Mostrar todas las tareas")
        print("4. Salir")
        print("------------------------------")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            tarea = input("Introduce la tarea: ")
            tareas.append(tarea) # Añade la tarea al final de la lista
            print("Tarea añadida.")

        elif opcion == '2':
            try:
                tarea = input("Introduce la tarea a eliminar: ")
                tareas.remove(tarea)
                print("Tarea eliminada.")
            except ValueError:
                print("La tarea no se encontró en la lista.")

        elif opcion == '3':
            print("\nLista de Tareas:")
            for i, tarea in enumerate(tareas, 1):
                print(f"{i}. {tarea}")
            #for i in range(len(tareas)):
                #print(f"{i + 1}. {tareas[i]}")

        elif opcion == '4':
            print("Saliendo del gestor de tareas...")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")

# gestor_de_tareas()

'''
Ejercicio 2: Análisis de Datos de Ventas
Objetivo: Crear un programa que analice datos de ventas de una tienda. 
El programa debe permitir añadir ventas, calcular el total de ventas, y mostrar la venta más alta y más baja.

Crear una lista vacía para almacenar las ventas.

Implementar un menú para que el usuario pueda elegir entre diferentes opciones: 
añadir venta, mostrar total de ventas, mostrar la venta más alta, mostrar la venta más baja y salir.

Utilizar métodos de listas como append, sum, max, y min.
'''

def analisis_ventas():
    ventas = []

    while True:

        print("\n------------------------------------")
        print("Datos de ventas")
        print("1. Añadir venta")
        print("2. mostrar lista de ventas")
        print("3. mostrar la venta más alta")
        print("4. mostrar la venta más baja")
        print("4. mostrar la suma total de ventas")
        print("5. Salir")
        print("------------------------------------")

        opcion = input("Elige una opción: ")

        if opcion == '1':
            try:
                venta = float(input("Introduce el monto de la venta: "))
                ventas.append(venta)
                print("Venta añadida.")
            except ValueError:
                print("Monto no válido. Inténtalo de nuevo.")

        elif opcion == '2':
            print('\nlista de ventas:')
            for i in range(len(ventas)):
                print(f'{i+1}. {ventas[i]}')

        elif opcion == '3':
            if ventas:
                venta_mas_alta = max(ventas)
                print(f"La venta más alta es: {venta_mas_alta}")
            else:
                print("No hay ventas registradas.")

        elif opcion == '4':
            if ventas:
                venta_mas_baja = min(ventas)
                print(f"La venta más baja es: {venta_mas_baja}")
            else:
                print("No hay ventas registradas.")

        elif opcion == '5':
            total_ventas = sum(ventas)
            print(f"El total de ventas es: {total_ventas}")

        elif opcion == '6':
            print("Saliendo del análisis de ventas...")
            break

        else:
            print("Opción no válida. Inténtalo de nuevo.")

# analisis_ventas()
