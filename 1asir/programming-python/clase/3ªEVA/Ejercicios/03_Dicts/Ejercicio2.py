'''
Crea un diccionario vacío y vete llenándolo con Nombre, Edad, Sexo y Teléfono que se le pida al usuario. 
Cada vez que se añada un nuevo dato debe imprimirse el contenido del diccionario.
'''

diccionario = {}
tupla=('Nombre', 'Edad', 'Sexo', 'Teléfono')
for i in tupla:
    elemento = str(input(f'\nIntroduce tu {i}\n>>> '))
    diccionario[i] = elemento
    print(diccionario)
    
print(f'\nNombre : {diccionario['Nombre']}')
print(f'Edad : {diccionario['Edad']}')
print(f'Sexo : {diccionario['Sexo']}')
print(f'Teléfono : {diccionario['Teléfono']}\n')