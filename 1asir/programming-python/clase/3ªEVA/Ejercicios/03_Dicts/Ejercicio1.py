'''
Escribir un programa que guarde en un diccionario la lista de la compra con el precio de cada uno de los productos.
Pregunta al usuario por un producto y muestra por pantalla el precio de ese producto. Si el producto preguntado no 
está en el diccionario debe mostrar un mensaje informando de ello.
'''

dic_compra = {
    "melón": 5,
    "melocotón": 3,
    "mandarina": 2,
    "plátano": 1.5,
    "limón": 2.5,
    "pera": 3.2
}
producto = str
while True:
    producto = input('Salir[S]\nDime un producto\n>>> ')

    if producto in dic_compra:
        print(f'\nEl precio de {producto} es {dic_compra[producto]:O} euros.\n')
    elif producto == 'S' or producto == 's':
        print('Hasta pronto')
        break
    else:
        print('\nEl producto no se encuentra en la tienda.\n')
