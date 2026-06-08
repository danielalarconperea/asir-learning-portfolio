import random
import RPi.GPIO as GPIO # type: ignore
GPIO.setmode(GPIO.BCM)
L1 = 17
L2 = 27
Boton = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(L1, GPIO.OUT)
GPIO.setup(L2, GPIO.OUT)
GPIO.output(L1, False)
GPIO.output(L2, False)

colores = ["rojo","negro"]
numeros = range(0,37)

numero_usuario = int(input("Elige un numero: "))
color_usuario = input("Elige un color: ")

if numero_usuario not in numeros or color_usuario.lower() not in colores:
    print("ERROR, DATOS NO VALIDOS")
    quit()

color_ganador = random.choice(colores)
numero_ganador = random.choice(numeros)

print(f"Ha tocado... el {numero_ganador} {color_ganador}")

if numero_ganador == numero_usuario and color_ganador == color_usuario:
    print("HAS GANADO")
elif numero_ganador == numero_usuario:
    print("Has acertado el numero")
elif color_ganador == color_usuario:
    print("Has acertado el color")
else:
    print("Has Perdido!")

input("El LED correspondiente está encendido. Presiona Enter para salir y limpiar...")

GPIO.cleanup()