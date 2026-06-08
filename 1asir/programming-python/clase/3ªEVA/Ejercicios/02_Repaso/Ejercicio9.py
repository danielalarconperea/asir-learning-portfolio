def Quiniela(num1, num2):
    if num1 > num2:
        return '1'
    elif num1 == num2:
        return 'X'
    else:
        return '2'

num1 = int(input('Introduce el primer número: '))
num2 = int(input('Introduce el segundo número: '))

resultado = Quiniela(num1, num2)
print(f'El resultado de la Quiniela es: {resultado}')