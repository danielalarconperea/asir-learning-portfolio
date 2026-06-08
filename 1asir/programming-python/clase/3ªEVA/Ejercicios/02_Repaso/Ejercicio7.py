lista = []
for i in range(10):
    num = int(input('Dime un número:\n--- '))
    lista.append(num)

min_numero = min(lista)
print(f'El número más pequeño es: {min_numero}')

numero_veces = lista.count(min_numero)

lista2 = []
for num in lista:
    if num != min_numero:
        lista2.append(num)

print(f'El número más pequeño apareció {numero_veces} veces.')
print(f'La lista después de eliminar el número más pequeño es: {lista2}')