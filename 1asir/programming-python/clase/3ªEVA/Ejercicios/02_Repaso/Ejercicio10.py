num1 = int(input('Introduce el primer número: '))
num2 = int(input('Introduce el segundo número: '))

if num1 < num2:
    inicio = num1
    fin = num2
else:
    inicio = num2
    fin = num1

print(f'Números comprendidos entre {inicio} y {fin}:')
for i in range(inicio + 1, fin):
    print(i, end=' ')