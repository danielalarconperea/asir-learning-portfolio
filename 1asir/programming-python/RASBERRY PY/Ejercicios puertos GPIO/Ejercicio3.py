# ejercicio3.py
import RPi.GPIO as GPIO # type: ignore

LED_PIN_MAYOR = 17 
LED_PIN_MENOR = 27
EDAD_LIMITE = 18


GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_MAYOR, GPIO.OUT)
GPIO.setup(LED_PIN_MENOR, GPIO.OUT)
GPIO.output(LED_PIN_MAYOR, False)
GPIO.output(LED_PIN_MENOR, False)



edad = int(input(f"Introduce tu edad (número entero): "))
print(f"Edad introducida: {edad}")

if edad >= EDAD_LIMITE:
    print(f"Mayor o igual a {EDAD_LIMITE}. Encendiendo LED en pin {LED_PIN_MAYOR}.")
    GPIO.output(LED_PIN_MAYOR, True)
    GPIO.output(LED_PIN_MENOR, False)
else:
    print(f"Menor de {EDAD_LIMITE}. Encendiendo LED en pin {LED_PIN_MENOR}.")
    GPIO.output(LED_PIN_MAYOR, False)
    GPIO.output(LED_PIN_MENOR, True)

input("El LED correspondiente está encendido. Presiona Enter para salir y limpiar...")

GPIO.cleanup()