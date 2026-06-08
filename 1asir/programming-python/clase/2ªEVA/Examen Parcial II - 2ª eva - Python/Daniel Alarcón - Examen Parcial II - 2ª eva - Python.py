nombre=input('Dime tu nombre: ')
print('')
print(f'¡Bienvenido {nombre}!. Éstas son las actividades que puedes realizar:')
while True:
    print('\n-----------------------------------------------------------')
    print('A. Cálculo del IMC (índice de masa corporal) - Escriba A')
    print('B. Suma de números - Escriba B')
    print('C. Números pares - Escriba C')
    print('D. Salir - Escriba D')
    print('-----------------------------------------------------------\n')

    eleccion=input('¿Qué actividad deseas hacer?: ')

    if eleccion.lower() == 'a':
        peso=float(input('Dime tu peso [Kg]: '))
        altura=float(input('Dime tu altura [m]: '))
        imc=peso/(altura**2)
        print(f'\nTu IMC es de {imc}')
        if imc < 18.5:
            print(f'Tu peso es inferior al normal')
        elif imc >= 18.5 and imc <= 24.9:
            print(f'Tu peso es normal')
        elif imc >= 25.0 and imc <= 29.9:
            print(f'Tu peso es superior al normal')
        elif imc >= 30.0:
            print(f'Tu tienes obesidad')

    elif eleccion.lower() == 'b':
        lista_num = []
        contador = 0
        while contador != 50:
            num = int(input('Dime un número para sumarlo: '))
            if contador + num > 50:
                print('La lista es mayor a 50 no lo añadas')
            else:
                lista_num.append(num)
                contador += num
        print(f'\nLa lista suma 50: {lista_num}')

    elif eleccion.lower() == 'c':
        num1 = int(input('Dime un número: '))
        num2 = int(input('Dime otro número: '))
        num_par=[]
        if num1 < num2:
            for _ in range(num2):
                if _ > num1 and _ % 2 == 0:
                    num_par.append(_)
            if num_par != []:
                print(f'Estos son los números pares que hay entre los dos número que me mencionaste:\n{num_par}')
            else:
                print('\nNo hay ningun numero par entre los dos números que me has dicho')
        elif num2 < num1:
            for _ in range(num1):
                if _ > num2 and _ % 2 == 0:
                    num_par.append(_)
            if num_par != []:
                print(f'Estos son los números pares que hay entre los dos número que me mencionaste:\n{num_par}')
            else:
                print('\nNo hay ningun numero par entre los dos números que me has dicho')
        else:
            print('\nNo hay ningun numero par entre los dos números que me has dicho')
    elif eleccion.lower() == 'd':
        print('\nMuchas gracias por haber usado este programa.\n')
        break
    else:
        print('\nEscribe una opción valida\n')