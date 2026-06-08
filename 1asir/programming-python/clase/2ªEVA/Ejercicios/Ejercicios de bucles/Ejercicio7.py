# 7. Mostrar un menú con tres opciones:  
#       1- Introducción 
#       2- Configuración 
#       3- Salir 
#   A continuación, el usuario debe poder seleccionar una opción (1, 2 ó 3).  Si escribe algo 
#   diferente a esos 3 números, informamos al usuario de que tiene que elegir una de esas 3 
#   opciones. El menú se debe volver a mostrar después de que se realice cada opción, 
#   permitiendo volver a elegir. Si elige las opciones 1 ó 2 se imprimirá un texto. Si elige la 
#   opción 3, se interrumpirá la impresión del menú y el programa finalizará.

while True:
    print('MENÚ')
    print('1- Introducción')
    print('2- Configuración')
    print('3- Salir')
    num=int(input('Escoge una opción del menú [1/2/3]: '))
    if num == 1 or num == 2:
        print('Un texto')
    elif num == 3:
        break
    else:
        print('introduce un número válido -->[1/2/3]')