'''
Escribir una función que meta por parámetro dos tuplas que representan dos fichas de dominó. 
La función devolverá "True" si encajan y "False" si no encajan.
Por ejemplo, se le puede pasar por parámetro: (3,4) y (5,4) y devolvería "True" ya que se podría juntar la ficha (3,4) con la (5,4) mediante el 4. 
Sin embargo, las fichas: (2,4) con (1,3) devolvería "False".
'''

def encajan_domino(ficha1, ficha2):
  return ficha1[0] == ficha2[0] or ficha1[0] == ficha2[1] or ficha1[1] == ficha2[0] or ficha1[1] == ficha2[1]

domino1 = (3, 4)
domino2 = (5, 4)
domino3 = (2, 4)
domino4 = (1, 3)
domino5 = (6, 6)
domino6 = (1, 6)

print(f"\n¿Encajan {domino1} y {domino2}? {encajan_domino(domino1, domino2)}") 
print(f"¿Encajan {domino3} y {domino4}? {encajan_domino(domino3, domino4)}")
print(f"¿Encajan {domino1} y {domino4}? {encajan_domino(domino1, domino4)}")
print(f"¿Encajan {domino5} y {domino6}? {encajan_domino(domino5, domino6)}\n")
