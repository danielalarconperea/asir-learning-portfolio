lista=[]
while True:
    palabra=input('dime la palabra que quieras añadir, si no quieres añadir más escribe [FIN]: ')
    if palabra == 'FIN' or palabra == 'fin':
        break
    else:
        lista.append(palabra)

print(lista)
veces_en_la_lista=lista.count(input('Dime la palabra que deseas contar cuantas veces aparece en la lista: '))
print('Tu palabra aparece:',veces_en_la_lista,'veces en la lista')
