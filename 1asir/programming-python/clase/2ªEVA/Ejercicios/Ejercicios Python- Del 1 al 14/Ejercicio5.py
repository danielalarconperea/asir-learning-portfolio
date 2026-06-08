num1 = int(input('Dime un número: '))
num2 = int(input('Dime otro número: '))

if num2 > num1:
    print(f'El número {num2} es mayor que el {num1}')
elif num2 == num1:
    print('Los dos números son iguales')
elif num2 < num1: 
    print(f'El número {num2} es menor que el {num1}')
else:
    print('Introduce un valor valido para -los números-')