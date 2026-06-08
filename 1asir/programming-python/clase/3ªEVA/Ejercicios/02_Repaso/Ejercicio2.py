i = 0
lista = []
while i != 20:
    num=int(input('Dime un número: \n--- '))
    if num > 0 and num < 11:
        lista.append(num)
        i+=1
    else:
        print('Introduce un número valido')
print(lista)