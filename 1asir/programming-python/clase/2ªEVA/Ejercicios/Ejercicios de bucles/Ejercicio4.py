# 4. Pide al usuario un primer número, después le pregunta por un segundo número  y 
# comprueba si la suma es igual o mayor que 15, si no lo es, sigue preguntando hasta que el 
# usuario introduzca un número que sume 15 o más con el primero. 

num1,num2=0,0
while num2 + num1 < 15:
    num1=int(input('Dime un primer número: '))
    num2=int(input('Dime un segundo número: '))
    if num2 + num1 >= 15:
        print('Suman más o igual a 15')
        break