# 6. Pide al usuario  números enteros hasta que el usuario ingrese el 0. Finalmente, mostrar la 
# suma de todos los números ingresados.
num=float
suma=0
while num != 0:
    num=float(input('Introduce números y para ver que suman escribe -0-: '))
    suma+=num
print(suma)