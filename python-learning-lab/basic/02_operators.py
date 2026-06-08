# Clase en vídeo: https://youtu.be/Kp4Mvapo5kc?t=5665

### Operadores Aritméticos ###

# Operaciones con enteros
print(3 + 4) #Suma de 3 y 4. Resultado: 7.
print(3 - 4) #Resta de 4 a 3. Resultado: -1.
print(3 * 4) #Multiplicación de 3 por 4. Resultado: 12.
print(3 / 4) #División de 3 entre 4. Resultado: 0.75.
print(10 % 3) #Operación módulo. Devuelve el resto de la división de 10 entre 3. Resultado: 1.
print(10 // 3) #División entera. Devuelve el cociente de la división de 10 entre 3, sin el resto. Resultado: 3.
print(2 ** 3) #Exponenciación. Eleva 2 a la potencia de 3. Resultado: 8.
print(2 ** 3 + 3 - 7 / 1 // 4) #8 + 3 - 1 = 10

# Operaciones con cadenas de texto
print("Hola " + "Python " + "¿Qué tal?")
print("Hola " + str(5))

# Operaciones mixtas
print("Hola " * 5)
print("Hola " * (2 ** 3))

my_float = 2.5 * 2
print("Hola " * int(my_float))

### Operadores Comparativos ###

# Operaciones con enteros
print(3 > 4)
print(3 < 4)
print(3 >= 4)
print(4 <= 4)
print(3 == 4)
print(3 != 4)

# Operaciones con cadenas de texto
print("Hola" > "Python")
print("Hola" < "Python")
print("aaaa" >= "abaa")  # Ordenación alfabética por ASCII
print(len("aaaa") >= len("abaa"))  # Cuenta caracteres
print("Hola" <= "Python")
print("Hola" == "Hola")
print("Hola" != "Python")

print("Hola" > "Python")
#Compara las cadenas de texto “Hola” y “Python” lexicográficamente (es decir, según el orden alfabético).
#Resultado: False porque “H” tiene un valor ASCII menor que “P”.
print("Hola" < "Python")
#Compara las cadenas de texto “Hola” y “Python” lexicográficamente.
#Resultado: True porque “H” tiene un valor ASCII menor que “P”.
print("aaaa" >= "abaa")
#Compara las cadenas de texto “aaaa” y “abaa” lexicográficamente.
#Resultado: False porque “a” tiene un valor ASCII menor que “b”.
print(len("aaaa") >= len("abaa"))
#Compara la longitud de las cadenas “aaaa” y “abaa”.
#Resultado: True porque ambas cadenas tienen una longitud de 4 caracteres.
print("Hola" <= "Python")
#Compara las cadenas de texto “Hola” y “Python” lexicográficamente.
#Resultado: True porque “H” tiene un valor ASCII menor que “P”.
print("Hola" == "Hola")
#Compara si las cadenas de texto “Hola” y “Hola” son iguales.
#Resultado: True porque ambas cadenas son idénticas.
print("Hola" != "Python")
#Compara si las cadenas de texto “Hola” y “Python” son diferentes.
#Resultado: True porque las cadenas no son iguales.

### Operadores Lógicos ###

# Basada en el Álgebra de Boole https://es.wikipedia.org/wiki/%C3%81lgebra_de_Boole
print(3 > 4 and "Hola" > "Python")
print(3 > 4 or "Hola" > "Python")
print(3 < 4 and "Hola" < "Python")
print(3 < 4 or "Hola" > "Python")
print(3 < 4 or ("Hola" > "Python" and 4 == 4))
print(not (3 > 4))
