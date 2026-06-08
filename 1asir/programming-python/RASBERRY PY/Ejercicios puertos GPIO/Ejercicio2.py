# Conectar dos LED y hacer una intermitencia entre ambos (Cuando uno está encendido, el otro está apagado), durante 10 segundos.

import RPi.GPIO as GPIO # type: ignore
import time

LED_PIN1 = 17 
LED_PIN2 = 27  

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN1, GPIO.OUT)
GPIO.setup(LED_PIN2, GPIO.OUT)
GPIO.output(LED_PIN1, False)
GPIO.output(LED_PIN2, False)


for i in range(10):
    GPIO.output(LED_PIN1, True)
    GPIO.output(LED_PIN2, False)
    time.sleep(0.5)

    GPIO.output(LED_PIN1, False)
    GPIO.output(LED_PIN2, True)
    time.sleep(0.5)

GPIO.cleanup()