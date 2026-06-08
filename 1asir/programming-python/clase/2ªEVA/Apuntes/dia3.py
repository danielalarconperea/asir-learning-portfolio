# lista=[1,'coche',2,5,2]
# lista.append('hola') # [1,'coche',2,5,2,'hola']
# lista.index('coche')
# lista.count(2)
# if 'coche' in lista:
#     print('hola')
# lista.insert(3,'si') # [1,'coche',2,'si',5,2,'hola']
# lista_str = [str(elemento) for elemento in lista]
# print(lista.sort())
# print(sorted(lista))

lista = [1, 'coche', 2, 5, 2]
lista.append('hola')  # [1, 'coche', 2, 5, 2, 'hola']
print("Índice de 'coche':", lista.index('coche'))  # Devuelve el índice de 'coche'
print("Conteo de 2:", lista.count(2))  # Cuenta cuántas veces aparece el número 2

if 'coche' in lista:
    print('hola')  # Imprime 'hola' si 'coche' está en la lista

lista.insert(3, 'si')  # [1, 'coche', 2, 'si', 5, 2, 'hola']
print("Lista después de insertar 'si':", lista)

# Convertir todos los elementos a str
lista_str = [str(elemento) for elemento in lista]
print("Lista convertida a str:", lista_str)

# Ordenar la lista convertida a str
lista_str.sort()
print("Lista ordenada (sort):", lista_str)

# Usar sorted() para obtener una nueva lista ordenada
lista_ordenada = sorted(lista_str)
print("Lista ordenada (sorted):", lista_ordenada)

# REVERSE para dar la vuelta a la lista
print(lista_ordenada.reverse)
