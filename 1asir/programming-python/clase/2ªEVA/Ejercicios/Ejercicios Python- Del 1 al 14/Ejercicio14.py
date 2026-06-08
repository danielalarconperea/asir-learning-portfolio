lista_modulos=['Fundamentos de hardware','Implantación de Sistemas operativos','Gestión de base de datos','IPE','Fundamentos de programación','Admnistración de redes']
lista_notas=[]
for i in lista_modulos:
    nota = int(input('Dime la nota que has sacado en ' + i + ': '))
    lista_notas.append(nota)

print('Asignaturas suspendidas:')
for i in range(len(lista_modulos)):
    if lista_notas[i] < 5:
        print(f'En {lista_modulos[i]} has sacado {lista_notas[i]}')