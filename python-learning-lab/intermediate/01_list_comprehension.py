# Clase en vídeo: https://youtu.be/TbcEqkabAWU?t=3239

### List Comprehension ###

my_original_list = [0, 1, 2, 3, 4, 5, 6, 7]
print(my_original_list)

my_range = range(8)
print(list(my_range))

# Definición

my_list = [i + 1 for i in range(8)]
print(my_list)

my_list = [i * 2 for i in range(8)]
print(my_list)

my_list = [i * i for i in range(8)]
print(my_list)


def sum_five(number):
    return number + 5


my_list = [sum_five(i) for i in range(8)]
print(my_list)













### Ejemplo completo del uso de .split() en Python

# 1. Dividir una cadena por espacios (por defecto)
texto1 = "Hola mundo Python"
resultado1 = texto1.split()
print("1. Dividir por espacios:", resultado1) # --- ['Hola', 'mundo', 'Python']

# 2. Dividir una cadena por un carácter específico (coma)
texto2 = "manzana,pera,uva,banana"
resultado2 = texto2.split(',')
print("2. Dividir por coma:", resultado2) # --- ['manzana', 'pera', 'uva', 'banana']

# 3. Limitar el número de divisiones con maxsplit
texto3 = "uno dos tres cuatro cinco"
resultado3 = texto3.split(' ', maxsplit=2)
print("3. Limitar divisiones (maxsplit=2):", resultado3) # --- ['uno', 'dos', 'tres cuatro cinco']

# 4. Dividir una cadena por saltos de línea
texto4 = "Línea 1\nLínea 2\nLínea 3"
resultado4 = texto4.split('\n')
print("4. Dividir por saltos de línea:", resultado4) # --- ['Línea 1', 'Línea 2', 'Línea 3']

# 5. Dividir una cadena vacía
texto5 = ""
resultado5 = texto5.split(',')
print("5. Dividir cadena vacía:", resultado5) # --- ['']

# 6. Dividir una cadena sin espacios ni separadores
texto6 = "HolaMundo"
resultado6 = texto6.split(',')
print("6. Dividir cadena sin separador:", resultado6) # --- ['HolaMundo']

# 7. Eliminar espacios en blanco adicionales
texto7 = "   Hola    mundo   Python   "
resultado7 = texto7.split()
print("7. Eliminar espacios adicionales:", resultado7) # --- ['Hola', 'mundo', 'Python']

# 8. Dividir y eliminar cadenas vacías
texto8 = "manzana,,pera,,,uva"
resultado8 = texto8.split(',')
print("8. Dividir y cadenas vacías:", resultado8) # --- ['manzana', '', 'pera', '', '', 'uva']

# Filtrar cadenas vacías
resultado8_filtrado = [item for item in resultado8 if item]
print("8. Filtrar cadenas vacías:", resultado8_filtrado) # --- ['manzana', 'pera', 'uva']

# 9. Dividir un diccionario (solo claves)
diccionario = {'a': 1, 'b': 2, 'c': 3}
texto9 = " ".join(diccionario)  # Convertimos las claves en una cadena
resultado9 = texto9.split()
print("9. Dividir claves de un diccionario:", resultado9) # --- ['a', 'b', 'c']

# 10. Dividir un rango (convertido a cadena)
rango = range(1, 6)
texto10 = " ".join(map(str, rango))  # Convertimos el rango en una cadena
resultado10 = texto10.split()
print("10. Dividir un rango:", resultado10) # --- ['1', '2', '3', '4', '5']