colores = ('rojo', 'azul', 'amarillo', 'verde', 'morado', 'naranja','marrón')
posicion = ''

while True:
    posicion = input('Dime un número\n--- ')
    if posicion.lower() == 's':
        break
    else:
        posicionnum=int(posicion)-1
        if posicionnum > len(colores)-1:
            print(f'\nERROR: El contenido de la tupla es menor de {posicion}\n')
        else:
            print(f'\nEl color en la posición {posicionnum+1} es el {colores[posicionnum]}\n')
    print('-'*20+'\n')