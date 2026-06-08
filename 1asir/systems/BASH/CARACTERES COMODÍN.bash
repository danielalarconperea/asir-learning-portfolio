#!/bin/bash

# -----------------------------------------------------------------------------
# APUNTES SOBRE CARACTERES COMODÍN EN LINUX
# Este script se centra exclusivamente en la explicación y ejemplos
# del uso de caracteres comodín (wildcards) en la terminal de Linux.
# -----------------------------------------------------------------------------

# -------------------------
# CARACTERES COMODÍN (WILDCARDS)
# -------------------------

# Utilización:
# Mediante el uso de caracteres comodín podemos especificar nombres de archivo y directorios
# múltiples o con un formato en el nombre específico que nos ayude a distinguir entre unos y
# otros. Son interpretados por el shell (como Bash) antes de que el comando se ejecute.
# Estos comodines son muy útiles con comandos como ls, cp, mv, rm, find (en su opción -name), etc.

# Disponemos de tres caracteres especiales principales para este fin:

# 1. * (Asterisco)
# Representa a un número indeterminado de caracteres cualesquiera, incluyendo la ausencia
# de caracteres (es decir, puede representar desde 0 hasta 'n' caracteres).
# Ejemplo:
#   a* -> Coincide con 'a', 'alfa', 'archivo.txt', 'a123_beta', etc.
#   *.txt   -> Coincide con cualquier archivo que termine en '.txt'.
#   *datos* -> Coincide con cualquier nombre que contenga la palabra 'datos'.

# 2. ? (Interrogante)
# Representa un único carácter cualquiera. No incluye la posibilidad de 0 caracteres.
# Se pueden añadir tantos símbolos '?' como se quieran, indicando cada uno de ellos
# un carácter adicional.
# Ejemplo:
#   foto?.jpg -> Coincide con 'foto1.jpg', 'fotoA.jpg', pero no con 'foto.jpg' o 'foto10.jpg'.
#   ???.log   -> Coincide con archivos que tengan exactamente 3 caracteres antes de '.log', como 'abc.log' o '123.log'.

# 3. [ ] (Corchetes)
# Permite indicar un carácter de entre un grupo de caracteres incluidos en los corchetes.
# Se buscará la coincidencia con uno sólo de los caracteres listados dentro de los corchetes
# para esa posición en el nombre del archivo.
#
#   - Lista de caracteres: [abcde] -> Coincide si el carácter en esa posición es 'a', 'b', 'c', 'd', o 'e'.
#     Ejemplo: archivo[123].txt -> Coincide con 'archivo1.txt', 'archivo2.txt', o 'archivo3.txt'.
#
#   - Rangos: Se utiliza un guion '-' para especificar un rango de caracteres.
#     [0-9] -> Coincide con cualquier dígito del 0 al 9.
#     [a-z] -> Coincide con cualquier letra minúscula.
#     [A-Z] -> Coincide con cualquier letra mayúscula.
#     [a-fA-F0-9] -> Coincide con cualquier carácter hexadecimal.
#     Ejemplo: item[0-5] -> Coincide con 'item0', 'item1', ..., 'item5'.
#
#   - Negación: El símbolo '!' o '^' (dependiendo del shell o contexto, '!' es más común en Bash para globbing)
#     justo después del corchete de apertura indica negación. Buscará aquellos caracteres
#     que NO estén indicados entre corchetes.
#     [!0-9]   -> Coincide con cualquier carácter que NO sea un dígito.
#     [A-Z]*[!a-z] -> Comienza con mayúscula y NO termina con minúscula.
#     Ejemplo: dato[!aeiou] -> Coincide con 'datob', 'datoc', pero no con 'datoa'.
#
#   - Múltiples corchetes: Si se desea especificar más de un carácter variable de un conjunto específico
#     en la expresión, se debe incluir otro par de corchetes por cada uno de ellos.
#     Ejemplo: [A-C][1-3] -> Coincide con 'A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3'.

# Ejemplos Prácticos:
# Los siguientes ejemplos se realizan con el comando 'echo' para mostrar cómo el shell
# expande los comodines. Estos mismos patrones sirven para utilizarse con cualquiera
# de los comandos de gestión de archivos y directorios (ls, cp, mv, rm, etc.).

echo "--- Inicio de Ejemplos de Comodines ---"
# (Para que estos ejemplos funcionen como se espera, necesitarías tener archivos/directorios
#  que coincidan con los patrones en el directorio donde ejecutes 'echo')

# echo *
# Muestra todos los archivos y directorios no ocultos del directorio actual.
echo "Ejemplo con '*': (todos los archivos/directorios no ocultos)"
echo *

# echo ?
# Muestra los archivos/directorios cuyo nombre sea de una única letra.
echo "Ejemplo con '?': (nombres de una sola letra)"
echo ?

# echo ??*
# Muestra los archivos/directorios con nombre de dos letras o más.
# (Los dos '??' aseguran al menos dos caracteres, el '*' cubre el resto, si lo hay).
echo "Ejemplo con '??*': (nombres de dos o más letras)"
echo ??*

# echo .*
# Muestra todos los archivos y directorios ocultos del directorio actual (incluyendo '.' y '..').
echo "Ejemplo con '.*': (archivos/directorios ocultos)"
echo .*

# echo a*
# Muestra los archivos/directorios que empiezan por la letra 'a'.
echo "Ejemplo con 'a*': (empiezan con 'a')"
echo a*

# echo ??a*
# Muestra los archivos/directorios cuya tercera letra sea la 'a' (y tengan al menos 3 caracteres).
echo "Ejemplo con '??a*': (tercera letra es 'a')"
echo ??a*
# echo [0123456789]*
# Muestra los archivos/directorios cuyo nombre empiece por un número (del 0 al 9).
# También se puede escribir como [0-9]*
echo "Ejemplo con '[0123456789]*': (empiezan con un número)"
echo [0123456789]*
echo "Alternativa con rango: [0-9]*"
echo [0-9]*

# echo *[a-z]
# Muestra los archivos/directorios cuyo nombre acabe por una letra minúscula.
echo "Ejemplo con '*[a-z]': (terminan con una letra minúscula)"
echo *[a-z]

# echo f[123]
# Muestra los archivos/directorios cuyo nombre empiece por 'f' y después tenga exactamente un número: 1, 2 o 3.
# Coincidiría con 'f1', 'f2', 'f3'.
echo "Ejemplo con 'f[123]': (f seguida de 1, 2, o 3)"
echo f[123]

# echo [0-9][0-9]*
# Muestra los archivos/directorios cuyo nombre empiece por al menos dos números.
echo "Ejemplo con '[0-9][0-9]*': (empiezan con al menos dos números)"
echo [0-9][0-9]*

# echo [A-Z]*[a-z]
# Muestra los archivos/directorios que empiecen por una letra mayúscula, seguido de cero o más
# caracteres cualesquiera, y terminen por una letra minúscula.
echo "Ejemplo con '[A-Z]*[a-z]': (empiezan con mayúscula y terminan con minúscula)"
echo [A-Z]*[a-z]

# echo *[!0-9]
# Muestra los archivos/directorios que no terminen por un número.
echo "Ejemplo con '*[!0-9]': (no terminan en un número)"
echo *[!0-9]

# echo [!jkm]*
# Muestra los archivos/directorios que no empiecen con los caracteres 'j', 'k', o 'm'.
echo "Ejemplo con '[!jkm]*': (no empiezan con j, k, o m)"
echo [!jkm]*

echo "--- Fin de Ejemplos de Comodines ---"

# Nota final:
# Para probar estos ejemplos de 'echo', descomenta las líneas 'echo' y asegúrate
# de tener archivos y directorios en tu ubicación actual que puedan coincidir
# con los patrones. Por ejemplo, antes de `echo a*`, podrías crear archivos como
# `touch apple art anaconda`.
# Recuerda que el comportamiento de los comodines es una característica del shell.