# Realizar un programa para que parpadee un led durante 40 veces, dejando entre encendido y apagado 1 segundo.

import RPi.GPIO as GPIO # type: ignore ; Importar la librería RPi.GPIO para controlar los pines GPIO de la Raspberry Pi
import time

# Configuración de la numeración de pines
GPIO.setmode(GPIO.BCM) # Usar la numeración BCM de los pines GPIO 
# Configuración del pin del LED
led_pin = 18 # Número del pin GPIO donde está conectado el LED
GPIO.setup(led_pin, GPIO.OUT) # Configuración del pin como salida
# Parpadeo del LED
for i in range(40):
    GPIO.output(led_pin, GPIO.HIGH)  # Encender el LED
    time.sleep(1)                    # Esperar 1 segundo
    GPIO.output(led_pin, GPIO.LOW)   # Apagar el LED
    time.sleep(1)                    # Esperar 1 segundo
# Limpieza de la configuración de GPIO
GPIO.cleanup() # Restablecer la configuración de GPIO a su estado inicial
# Fin del programa
# El programa enciende y apaga un LED conectado al pin 18 de la Raspberry Pi 40 veces, con un intervalo de 1 segundo entre cada cambio de estado.