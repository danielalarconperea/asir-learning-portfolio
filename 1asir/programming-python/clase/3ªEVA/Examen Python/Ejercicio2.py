diccionario = {
    # nombre : telefono 
}
while True:
    print('\n'+'-'*20)
    print('1. Añadir/Modificar')
    print('2. Borrar')
    print('3. Listar')
    print('0. Salir')
    print('-'*20+'\n')
    opcion = int(input('Elige una opción:[1,2,3,0]\n--- '))
    print()
    if opcion == 1:
        nombre = input('Dime el nombre que desea añadir\n--- ')
        if nombre in diccionario.keys():
            print(f'\n{nombre} ya esta en la agenda\n\nEl número de teléfono correspondiente es: {diccionario[nombre]}\n')
            pregunta = input('Quieres modificar el número de teléfono?[S/N]\n--- ')
            if pregunta.lower() == 's':
                telefono = int(input('\nDime el nuevo teléfono\n--- '))
                diccionario[nombre]=telefono
            else:
                None
        else:
            telefono = int(input('\nDime el teléfono\n--- '))
            diccionario[nombre]=telefono

    elif opcion == 2:
        nombre = input('Dime el nombre que deseas borrar\n--- ')
        if nombre in diccionario.keys():
            diccionario.pop(nombre)
        else:
            print(f'\n{nombre} no se encuentra en la agenda')

    elif opcion == 3:
        print(diccionario)
    elif opcion == 0:
        break
    else:
        print('Elige una opción válida:[1,2,3,0]')