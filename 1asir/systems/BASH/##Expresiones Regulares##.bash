#!/bin/bash

# Apuntes Completos de Expresiones Regulares en Linux (Bash)
# Fecha: 2025-05-12
#
# Este script contiene explicaciones y ejemplos de expresiones regulares (regex)
# directamente ejecutables en un entorno Bash.
# Las explicaciones preceden a los ejemplos prácticos.

echo "################################################################################"
echo "#                                                                              #"
echo "#                EXPRESIONES REGULARES EN LINUX: GUÍA COMPLETA                 #"
#                                                                              #
echo "################################################################################"

echo -e "\n--- Introducción a las Expresiones Regulares (Regex) ---"
# ¿Qué son?
#   Son patrones que describen combinaciones de caracteres en cadenas de texto.
#   Se usan para buscar, validar, y manipular texto de forma potente y flexible.
#
# Comandos Comunes que Usan Regex en Linux:
#   grep: Busca patrones en archivos o entrada estándar.
#   sed: Editor de flujo para transformar texto.
#   awk: Lenguaje de procesamiento de patrones y texto.
#   less, more, find, y muchos otros también las soportan.
#
# Tipos Principales de Regex en Linux:
#   1. BRE (Basic Regular Expressions): Sintaxis más antigua y limitada. Algunos
#      metacaracteres necesitan ser escapados con '\' para tener su significado especial
#      (e.g., 'grep' por defecto).
#   2. ERE (Extended Regular Expressions): Sintaxis más moderna y con más metacaracteres
#      que no necesitan ser escapados (e.g., 'grep -E', 'egrep', 'sed -E').
#   3. PCRE (Perl Compatible Regular Expressions): La más potente, con características
#      avanzadas como lookarounds y cuantificadores no glotones (e.g., 'grep -P').

# ------------------------------------------------------------------------------
echo -e "\n\n################################################################################"
echo "#                            METACARACTERES BÁSICOS                            #"
echo "################################################################################"
# Estos son los bloques de construcción fundamentales.

echo -e "\n--- Símbolo: . (Punto) ---"
# Explicación: Coincide con CUALQUIER CARÁCTER INDIVIDUAL, excepto (generalmente) el carácter de nueva línea.
# Ejemplo: 'a.c' coincide con 'abc', 'axc', 'a1c'.
echo "Ejemplo con '.':"
echo -e "abc\naac\na1c\nabcde\nac" | grep 'a.c'
# Salida esperada:
# abc
# aac
# a1c

echo -e "\n--- Símbolo: * (Asterisco) ---"
# Explicación: Coincide con CERO O MÁS OCURRENCIAS del carácter, grupo o clase de caracteres que le precede inmediatamente.
# Ejemplo: 'col*' coincide con 'co', 'col', 'coll'. 'ab*c' coincide con 'ac' (cero 'b'), 'abc' (una 'b'), 'abbc' (múltiples 'b').
echo "Ejemplo con '*':"
echo -e "ac\nabc\nabbc\nabx\nc" | grep 'ab*c'
# Salida esperada:
# ac
# abc
# abbc

echo -e "\n--- Símbolo: ^ (Acento Circunflejo/Caret) ---"
# Uso 1: Inicio de línea
# Explicación: Ancla la coincidencia al INICIO DE LA LÍNEA.
# Ejemplo: '^Hola' coincide con líneas que EMPIEZAN con "Hola".
echo "Ejemplo con '^' (inicio de línea):"
echo -e "Hola mundo\nAdios Hola\nHola" | grep '^Hola'
# Salida esperada:
# Hola mundo
# Hola
#
# Uso 2: Negación en un conjunto (ver '[]' más abajo)
# Explicación: Dentro de corchetes '[^...]', NIEGA el conjunto de caracteres.

echo -e "\n--- Símbolo: $ (Dólar) ---"
# Explicación: Ancla la coincidencia al FINAL DE LA LÍNEA.
# Ejemplo: 'fin$' coincide con líneas que TERMINAN en "fin".
echo "Ejemplo con '$' (final de línea):"
echo -e "El fin\nfin del mundo\nfinal" | grep 'fin$'
# Salida esperada:
# El fin

echo -e "\n--- Símbolo: [] (Corchetes) ---"
# Explicación: Definen un CONJUNTO DE CARACTERES. Coincide con CUALQUIER CARÁCTER ÚNICO que esté listado dentro de los corchetes.
#              Se pueden usar rangos como 'a-z' (letras de 'a' a 'z') o '0-9' (dígitos de '0' a '9').
# Ejemplo: '[aeiou]' coincide con 'a', 'e', 'i', 'o', o 'u'. '[0-9]' coincide con cualquier dígito.
echo "Ejemplo con '[]':"
echo -e "gato\npeto\npato\npoto\nputo\npxto" | grep 'p[aeiou]to'
# Salida esperada:
# peto
# pato
# poto
# puto
echo "Ejemplo con rango '[0-9]':"
echo -e "color1\ncolor2\ncolorX" | grep 'color[0-9]'
# Salida esperada:
# color1
# color2

echo -e "\n--- Símbolo: [^...] (Corchetes con Caret) ---"
# Explicación: NIEGA el conjunto de caracteres. Coincide con CUALQUIER CARÁCTER ÚNICO que NO ESTÉ en el conjunto especificado después del caret.
# Ejemplo: '[^0-9]' coincide con cualquier carácter que NO sea un dígito.
echo "Ejemplo con '[^...]':"
echo -e "a1\nb2\ncX\nd4" | grep 'c[^0-9]'
# Salida esperada:
# cX

echo -e "\n--- Símbolo: \ (Barra Invertida) ---"
# Explicación: Es el CARÁCTER DE ESCAPE.
#   1. Anula el significado especial de un metacarácter, tratándolo como un carácter literal.
#      Ejemplo: '\.' coincide con un punto literal '.', no con "cualquier carácter".
echo "Ejemplo con '\' (escape de metacarácter):"
echo -e "final.\nfinal?\nfinal" | grep 'final\.'
# Salida esperada:
# final.
#   2. En BRE, da significado especial a caracteres que en ERE son metacaracteres por defecto (e.g., '\(', '\{').
#   3. Introduce secuencias de escape especiales (ver sección 'Escapes Especiales').

# ------------------------------------------------------------------------------
echo -e "\n\n################################################################################"
echo "#                                     ANCLAS                                     #"
echo "################################################################################"
# Las anclas no coinciden con caracteres, sino con posiciones en el texto.
# '^' (inicio de línea) y '$' (final de línea) ya fueron vistos.

echo -e "\n--- Ancla: \< (Menor que, escapado en BRE/GNU ERE) ---"
# Explicación: Coincide con el INICIO DE UNA PALABRA. Una palabra es una secuencia de caracteres alfanuméricos (y a veces '_').
# Ejemplo: '\<pan' coincide con 'pan' y 'panadero', pero no con 'empanada'.
echo "Ejemplo con '\<' (inicio de palabra):"
echo -e "el panadero\ncompania\npan y agua\n_pan" | grep '\<pan'
# Salida esperada:
# el panadero
# pan y agua

echo -e "\n--- Ancla: \> (Mayor que, escapado en BRE/GNU ERE) ---"
# Explicación: Coincide con el FINAL DE UNA PALABRA.
# Ejemplo: 'on\>' coincide con 'cancion' y 'camion', pero no con 'donde' o 'conejo'.
echo "Ejemplo con '\>' (final de palabra):"
echo -e "camion grande\ncancionero\naccionista\naccion" | grep 'on\>'
# Salida esperada:
# camion grande
# accion
echo "Ejemplo combinado '\<palabra\>':"
echo -e "el perro come\nperrocoma\nun gran perro" | grep '\<perro\>'
# Salida esperada:
# el perro come
# un gran perro

echo -e "\n--- Ancla: \b (Límite de palabra - ERE/PCRE) ---"
# Explicación: Coincide con un LÍMITE DE PALABRA (inicio o fin). Es más general y a menudo más portable en ERE/PCRE.
#              '\bpalabra\b' es similar a '\<palabra\>' en GNU.
#              Un límite de palabra es la posición entre un carácter de palabra (\w) y un carácter que no es de palabra (\W), o inicio/fin de string.
echo "Ejemplo con '\b' (límite de palabra - usando grep -E o -P):"
echo -e "catatonic\nthe cat sat\n_cat_\nconcat" | grep -E '\bcat\b'
# Salida esperada:
# the cat sat
# (Dependiendo de la implementación de \b y \w, _cat_ podría o no coincidir. PCRE es más consistente)
echo -e "catatonic\nthe cat sat\n_cat_\nconcat" | grep -P '\bcat\b' # PCRE es más preciso aquí
# Salida esperada con grep -P:
# the cat sat

# ------------------------------------------------------------------------------
echo -e "\n\n################################################################################"
echo "#                                  CUANTIFICADORES                                 #"
echo "################################################################################"
# Especifican cuántas veces debe aparecer el elemento anterior.
# '*' (cero o más) ya fue visto.

echo -e "\n--- Cuantificadores en BRE (necesitan escape) ---"
# \{n\} : Exactamente 'n' veces.
# \{n,\} : Al menos 'n' veces.
# \{n,m\} : Entre 'n' y 'm' veces, inclusive.

echo "Ejemplo con '\{n\}' (exactamente n veces):"
# 'o\{2\}' coincide con 'oo'.
echo -e "gol\ngool\ngooool" | grep 'o\{2\}'
# Salida esperada:
# gool

echo "Ejemplo con '\{n,\}' (al menos n veces):"
# 'o\{2,\}' coincide con 'oo', 'ooo', 'oooo', etc.
echo -e "gol\ngool\ngooool\ngoool" | grep 'go\{2,\}l'
# Salida esperada:
# gool
# gooool
# goool

echo "Ejemplo con '\{n,m\}' (entre n y m veces):"
# 'ba\{2,3\}l' coincide con 'baal' o 'baaal'.
echo -e "bal\nbaal\nbaaal\nbaaaal\nbaaaaal" | grep 'ba\{2,3\}l'
# Salida esperada:
# baal
# baaal

echo -e "\n--- Cuantificadores en ERE/PCRE (generalmente sin escape) ---"
# + (Más): Una o más ocurrencias.
# ? (Interrogación): Cero o una ocurrencia (opcional).
# {n} : Exactamente 'n' veces.
# {n,} : Al menos 'n' veces.
# {n,m} : Entre 'n' y 'm' veces.

echo "Ejemplo con '+' (una o más - ERE):"
# 'ab+c' coincide con 'abc', 'abbc', pero no 'ac'.
echo -e "ac\nabc\nabbc\nabx" | grep -E 'ab+c'
# Salida esperada:
# abc
# abbc

echo "Ejemplo con '?' (cero o una - ERE):"
# 'colou?r' coincide con 'color' y 'colour'.
echo -e "color\ncolour\ncolouur" | grep -E 'colou?r'
# Salida esperada:
# color
# colour

echo "Ejemplo con '{n,m}' (ERE):"
# 'ba{2,3}l' coincide con 'baal' o 'baaal'.
echo -e "bal\nbaal\nbaaal\nbaaaal\nbaaaaal" | grep -E 'ba{2,3}l'
# Salida esperada:
# baal
# baaal

echo -e "\n--- Cuantificadores No Glotones (Non-Greedy/Lazy) - PCRE ---"
# Explicación: Por defecto, los cuantificadores (*, +, {}) son "glotones" (greedy): intentan coincidir
#              con la MAYOR cantidad de texto posible. Añadiendo un '?' después del cuantificador
#              (e.g., *?, +?, ??, {n,m}?) los hace "no glotones", coincidiendo con la MENOR cantidad de texto.
#              Requiere 'grep -P'.
TEXTO_GLOTON="<a><b><c>"
echo "Ejemplo de cuantificador glotón (PCRE): '<.*>'"
echo "$TEXTO_GLOTON" | grep -P -o '<.*>'
# Salida esperada:
# <a><b><c>

echo "Ejemplo de cuantificador no glotón (PCRE): '<.*?>'"
echo "$TEXTO_GLOTON" | grep -P -o '<.*?>'
# Salida esperada:
# <a>
# <b>
# <c>

# ------------------------------------------------------------------------------
echo -e "\n\n################################################################################"
echo "#                         AGRUPACIÓN Y ALTERNANCIA (ERE/PCRE)                      #"
echo "################################################################################"

echo -e "\n--- Símbolo: () (Paréntesis) ---"
# Explicación:
#   1. Agrupación: Permiten tratar una secuencia de expresiones como una unidad,
#      para aplicarles cuantificadores o para delimitar en la alternancia.
#      Ejemplo (ERE): '(ab)+c' coincide con 'abc', 'ababc'.
echo "Ejemplo con '()' para agrupación (ERE):"
echo -e "abc\nababc\ncab\nabcabc" | grep -E '(ab)+c'
# Salida esperada:
# abc
# ababc
#   2. Captura (Backreferences): El texto coincidente dentro de los paréntesis se "captura"
#      y puede ser referenciado después (e.g., en 'sed' con '\1', '\2', o en PCRE).
echo "Ejemplo con '()' para captura y reemplazo (sed -E):"
echo "nombre apellido" | sed -E 's/([a-zA-Z]+) ([a-zA-Z]+)/\2, \1/'
# Salida esperada:
# apellido, nombre
# Explicación del sed:
#   s/PATRON/REEMPLAZO/ : Comando de sustitución.
#   ([a-zA-Z]+)          : Primer grupo de captura (\1), una o más letras.
#   ([a-zA-Z]+)          : Segundo grupo de captura (\2), una o más letras.
#   \2, \1               : Reemplazo: el contenido del segundo grupo, una coma, un espacio, y el contenido del primer grupo.

echo -e "\n--- Símbolo: | (Barra Vertical/Pipe) ---"
# Explicación: Actúa como un operador OR (o lógico). Coincide con la expresión a su izquierda O la expresión a su derecha.
# Ejemplo (ERE): 'gato|perro' coincide con 'gato' o 'perro'.
echo "Ejemplo con '|' (OR - ERE):"
echo -e "mi gato\ntu perro\nsu loro" | grep -E 'gato|perro'
# Salida esperada:
# mi gato
# tu perro

# ------------------------------------------------------------------------------
echo -e "\n\n################################################################################"
echo "#                          CLASES DE CARACTERES POSIX                          #"
echo "################################################################################"
# Explicación: Son nombres simbólicos para conjuntos de caracteres comunes, encerrados entre '[::]'
#              y a su vez dentro de los corchetes de conjunto '[]', por ejemplo, '[[:digit:]]'.
#              Son portables y se adaptan a la configuración regional (locale).
#
# Clases Comunes:
#   [[:alnum:]]  : Caracteres alfanuméricos ([A-Za-z0-9] en locale C).
#   [[:alpha:]]  : Caracteres alfabéticos ([A-Za-z] en locale C).
#   [[:blank:]]  : Espacio y tabulador.
#   [[:cntrl:]]  : Caracteres de control.
#   [[:digit:]]  : Dígitos ([0-9]).
#   [[:graph:]]  : Caracteres imprimibles, excluyendo el espacio.
#   [[:lower:]]  : Letras minúsculas ([a-z] en locale C).
#   [[:print:]]  : Caracteres imprimibles, incluyendo el espacio.
#   [[:punct:]]  : Caracteres de puntuación.
#   [[:space:]]  : Caracteres de espacio en blanco (espacio, tab, nueva línea, etc.).
#   [[:upper:]]  : Letras mayúsculas ([A-Z] en locale C).
#   [[:xdigit:]] : Dígitos hexadecimales ([0-9a-fA-F]).

echo "Ejemplo con clase POSIX [[:digit:]] (ERE):"
echo -e "Archivo1.txt\nDocumentoA.doc\nDatos_2023.csv\nReport" | grep -E '[[:digit:]]+'
# Salida esperada:
# Archivo1.txt
# Datos_2023.csv

echo "Ejemplo con clase POSIX [[:alpha:]] para extraer solo palabras (usando -o):"
echo "Hola123Mundo CRUEL456Fin." | grep -Eo '[[:alpha:]]+'
# Salida esperada (cada palabra en una nueva línea):
# Hola
# Mundo
# CRUEL
# Fin

# ------------------------------------------------------------------------------
echo -e "\n\n################################################################################"
echo "#                             ESCAPES ESPECIALES COMUNES                           #"
echo "################################################################################"
# Estos son atajos para clases de caracteres comunes, más frecuentes en ERE/PCRE.
# '\' (barra invertida) ya fue vista como escape genérico.

# \d : Dígito (PCRE, algunas ERE). Equivale a [0-9] o [[:digit:]].
# \D : No dígito (PCRE, algunas ERE). Equivale a [^0-9] o [^[:digit:]].
# \w : Carácter de palabra "word" (alfanumérico más '_') (PCRE, algunas ERE). Equivale a [a-zA-Z0-9_] o [[:alnum:]]_.
# \W : No carácter de palabra (PCRE, algunas ERE).
# \s : Carácter de espacio en blanco "space" (espacio, tab, nueva línea, etc.) (PCRE, algunas ERE). Equivale a [[:space:]].
# \S : No carácter de espacio en blanco (PCRE, algunas ERE).

echo "Ejemplo con '\d' (dígito - PCRE):"
echo "ID: 123 Fecha: 2023-01-15" | grep -P -o '\d+' # Extraer secuencias de dígitos
# Salida esperada:
# 123
# 2023
# 01
# 15

echo "Ejemplo con '\s' (espacio en blanco - PCRE):"
# Reemplazar múltiples espacios con uno solo usando sed y PCRE (si sed lo soporta, GNU sed sí con \s)
# Alternativamente, se puede usar [[:space:]] para mayor portabilidad con sed -E.
echo "Muchos    espacios   aquí" | sed -E 's/[[:space:]]+/ /g'
# Salida esperada:
# Muchos espacios aquí
echo "Muchos    espacios   aquí (PCRE con grep):"
echo "Muchos    espacios   aquí" | grep -P -o '\S+' # Extraer secuencias de no-espacios
# Salida esperada:
# Muchos
# espacios
# aquí

# \n : Nueva línea.
# \t : Tabulador.
# \r : Retorno de carro.
# Estos se usan más en cadenas de reemplazo o para construir texto con `echo -e`.
echo "Ejemplo con '\t' (tabulador) y '\n' (nueva línea) en echo:"
echo -e "Columna1\tColumna2\nFila2Val1\tFila2Val2"
# Salida esperada:
# Columna1        Columna2
# Fila2Val1       Fila2Val2

# ------------------------------------------------------------------------------
echo -e "\n\n################################################################################"
echo "#                 LOOKAROUNDS (ASERCIONES DE MIRADA ALREDEDOR) - PCRE              #"
echo "################################################################################"
# Explicación: Permiten verificar la existencia (o no existencia) de patrones ANTES o DESPUÉS
#              de la coincidencia actual, SIN INCLUIR esos patrones en la coincidencia final.
#              Son "zero-width assertions" (no consumen caracteres). Requieren 'grep -P'.

# (?=patron) : Positive Lookahead.
#   Asegura que "patron" SIGUE INMEDIATAMENTE a la posición actual.
echo "Ejemplo de Positive Lookahead (?=) (PCRE):"
echo -e "Isaac Newton\nIsaac Asimov\nAlbert Einstein" | grep -P -o 'Isaac(?= Asimov)'
# Salida esperada (coincide 'Isaac' solo si le sigue ' Asimov'):
# Isaac

# (?!patron) : Negative Lookahead.
#   Asegura que "patron" NO SIGUE INMEDIATAMENTE a la posición actual.
echo "Ejemplo de Negative Lookahead (?!) (PCRE):"
echo -e "Stark Tower\nNed Stark\nPeter Stark" | grep -P -o 'Stark(?! Tower)'
# Salida esperada (coincide 'Stark' solo si NO le sigue ' Tower'):
# Stark (de Ned Stark)
# Stark (de Peter Stark)

# (?<=patron) : Positive Lookbehind.
#   Asegura que "patron" PRECEDE INMEDIATAMENTE a la posición actual.
#   (El patrón en lookbehind a menudo debe ser de longitud fija en muchas implementaciones).
echo "Ejemplo de Positive Lookbehind (?<=) (PCRE):"
echo -e "Precio: $100\nDescuento: 20%" | grep -P -o '(?<=\$)\d+' # Extraer números precedidos por '$'
# Salida esperada:
# 100

# (?<!patron) : Negative Lookbehind.
#   Asegura que "patron" NO PRECEDE INMEDIATAMENTE a la posición actual.
echo "Ejemplo de Negative Lookbehind (?<!) (PCRE):"
echo -e "Area VIP\nSuper VIP Lounge\nCliente VIP" | grep -P -o '(?<!Super )VIP'
# Salida esperada (coincide 'VIP' solo si NO le precede 'Super '):
# VIP (de Area VIP)
# VIP (de Cliente VIP)

# ------------------------------------------------------------------------------
echo -e "\n\n################################################################################"
echo "#                             MODIFICADORES COMUNES (Flags)                        #"
echo "################################################################################"
# Explicación: Son opciones que se pasan a la herramienta de regex (como 'grep', 'sed'),
#              no parte de la sintaxis de la regex en sí. Afectan cómo se interpreta o se muestra el patrón.

# i : (ignore case) Realiza una búsqueda INSENSIBLE a mayúsculas y minúsculas.
#     Ejemplo: `grep -i 'patron'`
echo "Ejemplo de modificador -i (ignore case) con grep:"
echo -e "Hola\nhola\nHOLA MUNDO" | grep -i 'hola'
# Salida esperada:
# Hola
# hola
# HOLA MUNDO

# g : (global) En herramientas como `sed s/viejo/nuevo/g`, aplica el cambio a TODAS las ocurrencias
#     en la línea, no solo la primera.
echo "Ejemplo de modificador -g (global) con sed:"
echo "pan pan pan" | sed 's/pan/PAN/' # Sin -g, solo reemplaza la primera
# Salida esperada: PAN pan pan
echo "pan pan pan" | sed 's/pan/PAN/g' # Con -g, reemplaza todas
# Salida esperada: PAN PAN PAN

# o : (only matching) En `grep -o`, muestra SÓLO LA PARTE de la línea que coincide con el patrón,
#     no la línea entera. Cada coincidencia en una línea nueva.
echo "Ejemplo de modificador -o (only matching) con grep:"
echo "Números: 123 y 456." | grep -E -o '[0-9]+'
# Salida esperada:
# 123
# 456

# n : (line number) En `grep -n`, muestra el NÚMERO DE LÍNEA junto con la línea coincidente.
echo "Ejemplo de modificador -n (line number) con grep:"
echo -e "Primera línea.\nSegunda línea con patron.\nTercera línea." | grep -n 'patron'
# Salida esperada:
# 2:Segunda línea con patron.

# E : (extended) En `grep -E` o `sed -E`, interpreta el patrón como una Expresión Regular Extendida (ERE).
#     Ya se ha usado en múltiples ejemplos arriba.

# P : (Perl) En `grep -P`, interpreta el patrón como una Expresión Regular Compatible con Perl (PCRE).
#     Ya se ha usado en ejemplos de lookarounds y cuantificadores no glotones.

# ------------------------------------------------------------------------------
echo -e "\n\n################################################################################"
echo "#                                    CONCLUSIÓN                                    #"
echo "################################################################################"
echo "Las expresiones regulares son una herramienta extremadamente poderosa."
echo "La clave está en entender los bloques básicos y cómo combinarlos."
echo "Recuerda las diferencias entre BRE, ERE y PCRE y qué sintaxis soporta tu herramienta."
echo "Consulta los manuales ('man grep', 'man sed') para detalles específicos de la implementación."
echo "¡Practica construyendo tus propias expresiones!"

echo -e "\n--- Fin de los Apuntes ---"