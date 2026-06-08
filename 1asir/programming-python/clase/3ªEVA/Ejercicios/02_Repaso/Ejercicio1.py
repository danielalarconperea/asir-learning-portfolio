def suma(lista):
        sum = 0
        for num in lista:
            sum += num
        return sum

numeros = [23, 345, 234, 1, 2, 34, 5, 2, 314, 23, 54]

def media(lista):
    return suma(lista)/len(lista)
print('La media de los números ingresados es de: ',media(numeros),'\n')

# O mejor

def media(lista):
    return sum(lista)/len(lista)
print('La media de los números ingresados es de: ',media(numeros),'\n')