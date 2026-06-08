lista=[]
while True:
    palabra=input('dime la palabra que quieras añadir, si no quieres añadir más escribe [FIN]: ')
    if palabra == 'FIN' or palabra == 'fin':
        break
    else:
        lista.append(palabra)

print(lista)
lista.remove(input('Dime la palabra que deseas eliminar de la lista: '))
print('Tu lista después de borrar la palabra:'),print(lista)