def ordenar_numeros(lista):
    par = []
    impar = []
    lista.sort()
    for i in lista:
        if i % 2 == 0:
            par.append(i)
        else:
            impar.append(i)
    return impar, par

numeros = [23, 345, 234, 1, 2, 34, 5, 2, 314, 23, 54]

lista_par, lista_impar= ordenar_numeros(numeros)

print('Pares:', lista_par)
print('Impares:', lista_impar)
