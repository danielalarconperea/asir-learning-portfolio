# 5. Pide al usuario una cadena de caracteres (frase), y los introduce en una lista sin repetir 
# ninguno de ellos.

lista=[]
frase=str(input('Dime una frase en la cual voy a coger los caracteres sin repetirlos: '))
for i in frase:
    if lista.count(i) != 1:
        lista.append(i)
print(lista)