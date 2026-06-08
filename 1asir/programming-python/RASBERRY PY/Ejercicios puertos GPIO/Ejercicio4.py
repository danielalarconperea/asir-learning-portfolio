# Pedir al usuario una contraseña alfanumérica, si es igual a la almacenada, encender un LED, si no, encender el otro.

import RPi.GPIO as GPIO # type: ignore

LED_PIN_CORRECTO = 17
LED_PIN_INCORRECTO = 27
CONTRASEÑA_ALMACENADA = "RaspberryPi123"

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_CORRECTO, GPIO.OUT)
GPIO.setup(LED_PIN_INCORRECTO, GPIO.OUT)
GPIO.output(LED_PIN_CORRECTO, False)
GPIO.output(LED_PIN_INCORRECTO, False)

contraseña_usuario = input("Introduce la contraseña alfanumérica: ")

print("Verificando contraseña...")

if contraseña_usuario == CONTRASEÑA_ALMACENADA:
    print(f"Contraseña CORRECTA. Encendiendo LED en pin {LED_PIN_CORRECTO}.")
    GPIO.output(LED_PIN_CORRECTO, True)
    GPIO.output(LED_PIN_INCORRECTO, False)
else:
    print(f"Contraseña INCORRECTA. Encendiendo LED en pin {LED_PIN_INCORRECTO}.")
    GPIO.output(LED_PIN_CORRECTO, False)
    GPIO.output(LED_PIN_INCORRECTO, True)

input("El LED correspondiente está encendido. Presiona Enter para salir y limpiar...")

GPIO.cleanup()