# Clase en vídeo: https://youtu.be/Kp4Mvapo5kc?t=16335

### Sets ###

# Definición------------Son mutables, lo que significa que puedes añadir y eliminar elementos después de haberlos creado. 

# Sin embargo, los elementos dentro de un set deben ser inmutables (por ejemplo, números, cadenas, tuplas)

# No permiten elementos duplicados. Si intentas añadir un duplicado, simplemente no se añadirá.

# No mantienen un orden específico de los elementos.

# Soportan operaciones matemáticas como unión, intersección, diferencia y diferencia simétrica

'''
Los sets tienen métodos específicos para manejar conjuntos:

add(x): Añade un ítem al set.

remove(x): Elimina un ítem del set. Lanza un error si el ítem no está presente.

discard(x): Elimina un ítem del set si está presente.

pop(): Elimina y devuelve un ítem arbitrario del set.

clear(): Elimina todos los ítems del set.

union(*others): Devuelve la unión de sets.

intersection(*others): Devuelve la intersección de sets.

difference(*others): Devuelve la diferencia de sets.

symmetric_difference(other): Devuelve la diferencia simétrica de sets.

update(*others): Actualiza el set con la unión de sets.

intersection_update(*others): Actualiza el set con la intersección de sets.

difference_update(*others): Actualiza el set con la diferencia de sets.

symmetric_difference_update(other): Actualiza el set con la diferencia simétrica de sets.

copy(): Devuelve una copia superficial del set.
'''

my_set = set()
my_other_set = {}

print(type(my_set))
print(type(my_other_set))  # Inicialmente es un diccionario

my_other_set = {"Brais", "Moure", 35}
print(type(my_other_set))

print(len(my_other_set))

# Inserción

my_other_set.add("MoureDev")

print(my_other_set)  # Un set no es una estructura ordenada

my_other_set.add("MoureDev")  # Un set no admite repetidos

print(my_other_set)

# Búsqueda

print("Moure" in my_other_set)
print("Mouri" in my_other_set)

# Eliminación

my_other_set.remove("Moure")
print(my_other_set)

my_other_set.clear()
print(len(my_other_set))

del my_other_set
# print(my_other_set) NameError: name 'my_other_set' is not defined

# Transformación

my_set = {"Brais", "Moure", 35}
my_list = list(my_set)
print(my_list)
print(my_list[0])

my_other_set = {"Kotlin", "Swift", "Python"}

# Otras operaciones

my_new_set = my_set.union(my_other_set)
print(my_new_set.union(my_new_set).union(my_set).union({"JavaScript", "C#"}))
print(my_new_set.difference(my_set))



'''
Ejercicio 1: Operaciones Básicas con Sets
Descripción: En este ejercicio, te familiarizarás con las operaciones básicas que puedes realizar con sets en Python, 
como la adición y eliminación de elementos, la búsqueda de elementos, y la conversión de sets a otras estructuras de datos.

Instrucciones:

1.Definir un set y añadir elementos:
--Define un set vacío llamado mi_set.
--Añade varios elementos de distintos tipos (cadenas, números) al set.

2.Eliminar elementos del set:
--Elimina un elemento específico del set usando remove().
--Elimina otro elemento usando discard().
--Vacía el set completamente usando clear().

3.Buscar elementos en el set:
--Comprueba si un elemento específico está en el set utilizando el operador in.
--Intenta buscar un elemento que no existe y maneja cualquier excepción que pueda surgir.

4.Convertir un set a una lista:
--Convierte el set a una lista y muestra el primer elemento de la lista.

5.Realizar operaciones de unión y diferencia:
--Define otro set llamado otro_set y realiza una operación de unión con mi_set.
--Calcula la diferencia entre mi_set y otro_set.
'''
def Ejercicio1():

    # 1. Definir un set y añadir elementos
    mi_set = set()  # Crear un set vacío
    mi_set.add(('Marcos', 'Aurelio', 33))  # Añadir una tupla al set
    mi_set.add(30)  # Añadir un número al set
    mi_set.add(51)  # Añadir otro número al set
    mi_set.add(('pepe', 'doge', 'solana', 'polkadot'))  # Añadir otra tupla al set
    print(mi_set) # Salida: {('Marcos', 'Aurelio', 33), 51, 30, ('pepe', 'doge', 'solana', 'polkadot')}

    # 2. Eliminar elementos del set
    mi_set.remove(('Marcos', 'Aurelio', 33))  # Eliminar la tupla del set, en caso de que no exista da error
    print(mi_set) # Salida: {51, 30, ('pepe', 'doge', 'solana', 'polkadot')}
    mi_set.discard(51)  # Eliminar el número 51 del set si existierá
    print(mi_set) # Salida: {30, ('pepe', 'doge', 'solana', 'polkadot')}
    mi_set.clear()  # Vaciar el set por completo
    print(mi_set) # Salida: set()

    # 3. Buscar elementos en el set
    mi_set = {('Marcos', 'Aurelio', 33), 30, 51, ('pepe', 'doge', 'solana', 'polkadot')}
    print('¿Está el 50 en mi set?', 50 in mi_set) # Comprobar si el número 50 está en el set.  Salida: ¿Está el 50 en mi set? False
    print('¿Está el 30 en mi set?', 30 in mi_set)  # Comprobar si el número 30 está en el set. Salida: ¿Está el 30 en mi set? True

    # 4. Convertir un set a una lista
    mi_set = list(mi_set)  # Convertir el set a una lista
    print(mi_set[0])  # Imprimir el primer elemento de la lista
    # Salida depende del orden de los elementos en el set, podría ser:
    # ('Marcos', 'Aurelio', 33) o 30 o 51 o ('pepe', 'doge', 'solana', 'polkadot')
    mi_set = set(mi_set)  # Volver a convertir la lista a un set

    # 5. Realizar operaciones de unión y diferencia
    otro_set = {'comida', ('pasta', 10, 'pizza', 30), 40, 51}
    union_set = mi_set.union(otro_set) # Realizar la unión de los dos sets
    print(mi_set) # Salida:    {('Marcos', 'Aurelio', 33), 30, 51, ('pepe', 'doge', 'solana', 'polkadot')} 
    print(otro_set) # Salida:  {'comida', ('pasta', 10, 'pizza', 30), 40, 51} 
    print(union_set) # Salida: {('Marcos', 'Aurelio', 33), 30, 51, ('pepe', 'doge', 'solana', 'polkadot'), 'comida', ('pasta', 10, 'pizza', 30), 40} 
    difference_set = mi_set.difference(otro_set) # Realizar la diferencia entre mi_set y otro_set --> mi_set - otro_set
    print(difference_set) # Salida: {('Marcos', 'Aurelio', 33), 30, ('pepe', 'doge', 'solana', 'polkadot')}

Ejercicio1()

'''
Ejercicio 2: Operaciones Avanzadas con Sets
Descripción: En este ejercicio, explorarás operaciones avanzadas con sets, incluyendo la intersección, 
diferencia simétrica, y la actualización de sets. También aprenderás a hacer copias de sets.

Instrucciones:

1.Operaciones de intersección y diferencia simétrica:
--Define dos sets y realiza una operación de intersección.
--Realiza una operación de diferencia simétrica entre los dos sets.

2.Actualizar un set con elementos de otro set:
--Define un tercer set y actualízalo con los elementos de uno de los sets iniciales utilizando update().
--Realiza una actualización con la intersección utilizando intersection_update().

3.Hacer copias de un set:
--Haz una copia de uno de los sets iniciales usando copy().
--Verifica que la copia es independiente del set original.
'''

def Ejercicio_2():
    
    # 1. Operaciones de intersección y diferencia simétrica
    set1 = {"Brais", "Moure", 35, "Python"}
    set2 = {"Kotlin", "Swift", "Python", 35}
    print('set1:', set1, '\nset2:', set2)
    interseccion_set = set1.intersection(set2) # Intersección: elementos comunes en ambos sets
    print(interseccion_set) # Salida: {'Python', 35}
    diferencia_simetrica_set = set1.symmetric_difference(set2) # Diferencia simétrica: elementos que están en set1 o en set2 pero no en ambos
    print(diferencia_simetrica_set) # Salida: {'Kotlin', 'Swift', 'Brais', 'Moure'}

    # 2. Actualizar un set con elementos de otro set
    set3 = {"Java", "C#", "JavaScript"} 
    set3.update(set1) # Añadimos los elementos de set1 a set3
    print(set3) # Salida: {'Java', 'Python', 'C#', 35, 'Brais', 'JavaScript', 'Moure'}
    set3.intersection_update(set2) # Actualizamos set3 con la intersección de set3 y set2
    print(set3) # Salida: {35, 'Python'}

    # 3. Hacer copias de un set
    copia_set1 = set1.copy() # Creamos una copia de set1
    print(copia_set1) # Salida: {'Brais', 'Moure', 35, 'Python'}
    set1.add("Nuevo Elemento") # Añadimos un nuevo elemento a set1
    print("Set1 original:", set1) # Salida:       Set1 original: {'Brais', 'Moure', 35, 'Python', 'Nuevo Elemento'}  (La salida saldria desordenada debido a que es un set y lo muestra desordenado)
    print("Copia de Set1:", copia_set1) # Salida: Copia de Set1: {'Brais', 'Moure', 35, 'Python'}

Ejercicio_2()