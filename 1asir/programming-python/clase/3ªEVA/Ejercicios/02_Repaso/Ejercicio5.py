lista = []
for i in range(4):
    num=int(input('Dime un número\n--- '))
    lista.append(num)
for num in lista:
    if num < 5:
        print(num, end=' ')

def suma(lista):
    sum = 0
    for num in lista:
        sum += num
    return sum


print('\n'*2,'La media de los números que me has pasado es:',suma(lista)/4,'\n')