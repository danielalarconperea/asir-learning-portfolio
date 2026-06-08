num1 = int(input('Dime un número: '))
num2 = int(input('Dime otro número: '))

if num1 > num2 and num1%num2==0:
    print('El mayor es multiplo del menor')  
elif num2 > num1 and num2%num1==0:
    print('El mayor es multiplo del menor')
else:
    print('El mayor no es multiplo del menor')