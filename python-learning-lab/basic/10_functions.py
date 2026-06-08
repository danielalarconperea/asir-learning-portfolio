# Clase en vídeo: https://youtu.be/Kp4Mvapo5kc?t=26619

### Functions ###

# Definición

def my_function():
    print("Esto es una función")


my_function()
my_function()
my_function()

# Función con parámetros de entrada/argumentos


def sum_two_values(first_value, second_value):
    print(first_value + second_value)


sum_two_values(5, 7)
sum_two_values(54754, 71231)
sum_two_values("5", "7")
sum_two_values(1.4, 5.2)

# Función con parámetros de entrada/argumentos y retorno


def sum_two_values_with_return(first_value, second_value):
    my_sum = first_value + second_value
    return my_sum


my_result = sum_two_values(1.4, 5.2)
print(my_result)

my_result = sum_two_values_with_return(10, 5)
print(my_result)

# Función con parámetros de entrada/argumentos por clave


def print_name(name, surname):
    print(f"{name} {surname}")


print_name(surname="Moure", name="Brais")

# Función con parámetros de entrada/argumentos por defecto


def print_name_with_default(name, surname, alias="Sin alias"):
    print(f"{name} {surname} {alias}")


print_name_with_default("Brais", "Moure")
print_name_with_default("Brais", "Moure", "MoureDev")

# Función con parámetros de entrada/argumentos arbitrarios


def print_upper_texts(*texts):
    print(type(texts))
    for text in texts:
        print(text.upper())


print_upper_texts("Hola", "Python", "MoureDev")
print_upper_texts("Hola")


'''javascript:
var palabra, contador;
palabra=prompt('introduce una palabra:')
contador=0
for(i=0; i<palabra.length; i++){
    contador++;
}
document.write(palabra+' tiene '+contador+' letras.<br>')
'''

def contador(palabra):
    variable=0
    for i in range(len(palabra)):
        variable+=1
    print(variable)
        

contador('hola')

def contador(palabra):
    for i in range(len(palabra)):
        print(palabra[i])

contador('hola')

#  X  X  X  X
#  X        X
#  X        X
#  X  X  X  X

def cuadrado(lado):
    if lado > 1:
        print(' X '*lado+'\n'+(' X '+('   '*(lado-2))+' X\n')*(lado-2)+' X '*lado)
    else:
        print(' X '*lado+'\n'+(' X '+('   '*(lado-2))+' X\n')*(lado-2))
# for i in range(1):
#     l = int(input('Dime el lado del cuadrado: '))
#     cuadrado(l)
cuadrado(4)

#    X 
#   X X
#  X X X
# X X X X

def triangulo(altura):
    for i in range(altura+1):
        print(' '*(altura-i)+' X'*i+('   '*(altura-2)))
# for i in range(1):
#     l = int(input('Dime la altura del triangualo: '))
#     triangulo(l)
triangulo(4)

#     X 
#   X   X
# X       X
#   X   X
#     X 

def rombo(altura):
    print('\n')
    for i in range(altura):
        if i < 1:
            print('  '*(altura//2-i)+'  X '+('    '*(i-1)))
        elif i < altura//2:
            print('  '*(altura//2-i)+'  X '+('    '*(i-1)+'  X '))
        elif i == altura//2 and altura%2 == 0:
            print('  '*(altura//2-i+1)+'  X '+('    '*(i-2)+'  X '))
        elif i == altura//2 and altura%2 != 0:
            print('  '*(altura//2-i)+'  X '+('    '*(i-1)+'  X '))
        elif i > altura//2 and i != altura-1 and altura%2 == 0:
            print('  '*(i+1-altura//2)+'  X '+('    '*(altura-i-2)+'  X '))
        elif i > altura//2 and i != altura-1 and altura%2 != 0:
            print('  '*(i-altura//2)+'  X '+('    '*(altura-i-2)+'  X '))
        else:
            print('  '*(altura//2)+'  X '+('    '*(i-1)))
# for i in range(1):
#     l = int(input('Dime la altura del rombo: '))
#     rombo(l)
rombo(7)

#       X 
#     X   X
#   X       X
# X           X
#  X         X
#   X       X
#    X X X X

def pentagono(altura):
    print('\n')
    for i in range(altura):
        if i < 1:
            print('  '*(altura//2-i)+'  X ')
        elif i < altura//2:
            print('  '*(altura//2-i)+'  X '+('    '*(i-1)+'  X'))
        elif i == altura//2 and altura%2 == 0:
            print('  '*(altura//2-i)+'  X '+('    '*(i-1)+'  X'))
        elif i == altura//2 and altura%2 != 0:
            print('  '*(altura//2-i)+'  X '+('    '*(i-1)+'  X'))
        elif i > altura//2 and i != altura-1 and altura%2 == 0:
            print(' '*(i-altura//2)+'  X'+('  '*(altura-i)+' '*(altura-1)+'X'))
        elif i > altura//2 and i != altura-1 and altura%2 != 0:
            print(' '*(i-altura//2)+'  X'+('  '*(altura-i)+' '*(altura-4)+'X'))
        elif i > altura//2 and i != altura and altura%2 == 0:
            print(' '*(i-altura//2+1)+' X'*(altura//2+2)+('    '*(i-1)))
        else:
            print(' '*(i-altura//2+1)+' X'*(altura//2+1)+('    '*(i-1)))
# for i in range(1):
#     l = int(input('Dime la altura del rombo: '))
#     rombo(l)
pentagono(7)


def hoola():
    while 1 > 0:
        print(1)
        if 0 > 1:
            print('no')
        elif 1 == 1: 
            print('antes')
        if 2 > 1:
            print('Salida')
            continue
        if 1 == 1: 
            print('no salió')
    if 1 == 1:
        print('debajo')

valor = hoola()
print(valor)
