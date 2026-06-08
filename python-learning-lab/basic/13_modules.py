# Clase en vídeo: https://youtu.be/Kp4Mvapo5kc?t=34583
'''
sys: Proporciona acceso a algunas variables utilizadas o mantenidas por el intérprete y a funciones que interactúan fuertemente con el intérprete.

os: Proporciona una forma de usar funcionalidades dependientes del sistema operativo.

math: Ofrece acceso a las funciones matemáticas definidas por el estándar C.

datetime: Suministra clases para manipular fechas y horas.

random: Implementa generadores de números pseudoaleatorios para varias distribuciones.

json: Permite trabajar con datos JSON.

re: Ofrece soporte para expresiones regulares.

http: Maneja solicitudes y respuestas HTTP.
'''
### Modules ###

import math

print(math.pi)
print(math.pow(2, 8))

from math import pi as PI_VALUE

print(PI_VALUE)

from my_module import sumValue, printValue

my_module.sumValue(5, 3, 1)
my_module.printValue("Hola Python!")

import my_module

sumValue(5, 3, 1)
printValue("Hola python")



