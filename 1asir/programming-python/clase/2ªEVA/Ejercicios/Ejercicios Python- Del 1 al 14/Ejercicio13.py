lista_modulos=['Fundamentos de hardware','Implantación de Sistemas operativos','Gestión de base de datos','IPE','Fundamentos de programación','Admnistración de redes']
lista_notas=[]
for i in lista_modulos:
    nota = input('Dime la nota que has sacado en ' + i + ': ')
    lista_notas.append(nota)

for i in range(len(lista_modulos)):
    print(f'En {lista_modulos[i]} has sacado {lista_notas[i]}')