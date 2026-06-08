# 3. Pide al usuario un primer número, después le pregunta por un segundo número y 
# comprueba si es mayor que el primero, si no lo es, sigue preguntando hasta que el usuario 
# introduce un número mayor que el primer número. El programa termina escribiendo los dos 
# números.

num1,num2=0,0
while num1 >= num2:
    num1=int(input('Dime un primer número: '))
    num2=int(input('Dime un segundo número: '))
    if num2 > num1:
        print('el segundo número es mayor')
        break