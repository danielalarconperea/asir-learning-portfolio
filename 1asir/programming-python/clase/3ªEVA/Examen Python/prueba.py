# diccionario = {
#     'dani':12341234,
#     'pedro':23452345,
#     'mauricio':123432,
#     'pepe':123423,
#     'si':12
# }
# diccionario.pop('dani')
# for _ in diccionario:
#     print(diccionar)


tupla = (1, 2, 3, 4, 5)

lista_tupla = list(tupla)

lista_tupla.append(6)
lista_tupla.pop(4)
print(type(lista_tupla))
print()

tupla2 = tuple(lista_tupla)
print(tupla2)
print(type(tupla2))