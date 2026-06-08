notas = []
diccionario = {}
i=0

numero_alumnos = int(input('Dime el número de alumnos que hay\n--- '))
while i < numero_alumnos:
    print('\n'+'-'*20+'\n')
    nombre = input('Dime el nombre del alumno\n--- ')
    if nombre in diccionario.keys():
        print(f'\nERROR: El alumno {nombre} ya existe')
    else:
        i+=1
        while True:
            nota = float(input('\nDime una nota\n--- '))
            if nota >= 0:
                notas.append(nota)
            else:
                diccionario[nombre]=tuple(notas)
                notas.clear()
                break
print()
print(diccionario)
print()



