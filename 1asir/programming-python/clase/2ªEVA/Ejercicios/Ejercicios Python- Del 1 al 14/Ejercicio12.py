# lista=[1,2,3,6,12]

lista=[]
rango=int(input('Dime cuantos número quieres añadir en la lista: '))
while rango != 0:
    rango-=1
    num=int(input('dime el número que quieras añadir: '))
    lista.append(num)

suma_acumulada = []
suma=0
for i in lista:
    suma+=i
    suma_acumulada.append(suma)

print("Lista original:", lista)
print("Suma acumulada:", suma_acumulada)