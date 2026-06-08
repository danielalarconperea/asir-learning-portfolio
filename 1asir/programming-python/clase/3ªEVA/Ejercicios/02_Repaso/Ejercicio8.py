def eliminar_negativos(lista):
    for num in lista:
        if num >= 0:
            return num

lista = []
for i in range(5):
    num = int(input(f'Dime el valor {i+1}:\n--- '))
    lista.append(num)

lista_sin_negativos = eliminar_negativos(lista)

print(f'La lista sin valores negativos es: {lista_sin_negativos}')