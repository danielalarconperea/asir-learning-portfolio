print('hola')
numero = 4
nombre = 'Daniel'
a, b, c = 1, 'pepe', 2.3
'''asdf
ased'''
# asdgqawsdrfg
print(3 + 4) #Suma de 3 y 4. Resultado: 7.
print(3 - 4) #Resta de 4 a 3. Resultado: -1.
print(3 * 4) #Multiplicación de 3 por 4. Resultado: 12.
print(3 / 4) #División de 3 entre 4. Resultado: 0.75.
print(10 % 3) #Operación módulo. Devuelve el resto de la división de 10 entre 3. Resultado: 1.
print(10 // 3) #División entera. Devuelve el cociente de la división de 10 entre 3, sin el resto. Resultado: 3.
print(2 ** 3) #Exponenciación. Eleva 2 a la potencia de 3. Resultado: 8.
print(2 ** 3 + 3 - 7 / 1 // 4) #8 + 3 - 1 = 10

# División

# Python

nombre_slice = nombre[1:3]
print(nombre_slice) # yt -- toma una subcadena desde el índice 1 hasta el índice 2 (el índice final no se incluye)

nombre_slice = nombre[1:]
print(nombre_slice) # ython

nombre_slice = nombre[-2]
print(nombre_slice) # o -- toma el segundo carácter desde el final de la cadena

nombre_slice = nombre[0:6:2]
print(nombre_slice) # pto -- toma una subcadena desde el índice 0 hasta el índice 5 (el índice final no se incluye) saltando cada 2 caracteres


nombre, apellido, edad=input('dime tu nombre:'), input('dime tu apellido:'), int(input('dime tu edad:'))

print(f'Buenos días {nombre} como fue tu cumple nº{edad} con tu familia {apellido}')
print('Buenos días '+nombre+' como fue tu cumple nº'+str(edad)+' con tu familia '+apellido)