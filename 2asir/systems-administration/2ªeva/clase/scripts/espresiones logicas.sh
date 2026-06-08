#!/bin/bash

### --- Sección 1: Comparaciones Numéricas (Enteros) ---

# Se utilizan operadores específicos para comparar números enteros dentro de corchetes simples [ ].
# -eq: Equal (igual) | -ne: Not Equal (distinto) | -gt: Greater Than (mayor)
# -ge: Greater or Equal (mayor o igual) | -lt: Less Than (menor) | -le: Less or Equal (menor o igual)
n1=10
n2=20
[ $n1 -lt $n2 ] && echo "10 es menor que 20"
# -> 10 es menor que 20

# Uso de comparaciones en estructuras if tradicionales.
if [ $n1 -ne $n2 ]; then echo "Son diferentes"; fi
# -> Son diferentes

### --- Sección 2: Comparaciones de Cadenas de Texto (Strings) ---

# Para strings usamos operadores visuales. Es vital usar comillas para evitar errores si la variable está vacía.
# = o ==: Igualdad | !=: Desigualdad | -z: String vacío | -n: String no vacío
str1="Hola"
str2="Mundo"
[ "$str1" != "$str2" ] && echo "Las cadenas son distintas"
# -> Las cadenas son distintas

# Comprobar si una variable no ha sido definida o está vacía (-z).
[ -z "$var_inexistente" ] && echo "La variable está vacía"
# -> La variable está vacía

### --- Sección 3: Evaluación de Archivos y Directorios ---

# Bash permite verificar el estado del sistema de archivos de forma nativa.
# -e: Existe | -f: Es un archivo regular | -d: Es un directorio | -r: Tiene permiso de lectura
# -w: Tiene permiso de escritura | -x: Es ejecutable | -s: No está vacío
touch nota.txt
[ -f "nota.txt" ] && echo "El archivo existe"
# -> El archivo existe

# Verificación de permisos de ejecución (útil para automatización).
[ -x "script.sh" ] || echo "No es ejecutable"
# -> No es ejecutable (si no se han dado permisos con chmod)

### --- Sección 4: Operadores Lógicos Combinados (AND, OR, NOT) ---

# Dentro de [ ], se usa -a (AND) y -o (OR). El operador ! invierte el resultado (NOT).
edad=25
[ $edad -gt 18 -a $edad -lt 30 ] && echo "Rango de edad válido"
# -> Rango de edad válido

# El uso de && y || fuera de los corchetes sirve como cortocircuito lógico.
[ "A" == "A" ] || echo "Esto no se ejecutará"
# -> (No hay salida)

### --- Sección 5: Expresiones Avanzadas con Doble Corchete [[ ]] ---

# [[ ]] es una mejora de Bash sobre [ ]. No requiere comillas en variables y permite Regex.
# El operador =~ permite comparar contra expresiones regulares.
email="usuario@dominio.com"
[[ $email =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$ ]] && echo "Email válido"
# -> Email válido

# Uso de Wildcards (comodines) con el operador ==.
nombre="script_backup_2023.sh"
[[ $nombre == script_* ]] && echo "Es un script de backup"
# -> Es un script de backup

### --- Sección 6: Evaluación Aritmética con (( )) ---

# Para comparaciones matemáticas puras, se pueden usar símbolos matemáticos tradicionales.
# > , < , >= , <= , == , !=
valor=50
(( valor + 10 > 55 )) && echo "El cálculo es correcto"
# -> El cálculo es correcto

### --- Sección 7: Diagnóstico y Código de Salida ($?) ---

# Cada expresión lógica devuelve un código de salida: 0 (True/Éxito) o 1 (False/Error).
# Podemos usar $? para verificar el resultado de la última evaluación.
[ 5 -eq 10 ]
echo $?
# -> 1

test "proceso" == "proceso"
echo $?
# -> 0