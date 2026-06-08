'''
Crea una tupla de números. Pide al usuario un número y accede a la tupla e indica cuántas veces se encuentra en la misma.
'''

numeros_tupla = (1, 5, 2, 8, 5, 3, 4, 5, 9, 0, 5)
print('Tupla de números:', numeros_tupla)

buscar_numeros = int(input('Introduce un número para contar cuántas veces aparece en la tupla: '))
cantidad = numeros_tupla.count(buscar_numeros)

print(f'El número {buscar_numeros} aparece {cantidad} veces en la tupla.')