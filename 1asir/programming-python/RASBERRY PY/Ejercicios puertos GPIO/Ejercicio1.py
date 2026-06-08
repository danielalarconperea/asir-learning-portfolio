# Realizar un programa para que parpadee un led durante 40 veces, dejando entre encendido y apagado 1 segundo.

import RPi.GPIO as GPIO # type: ignore
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)
for i in range(40):
    GPIO.output(18, True) 
    time.sleep(1)                   
    GPIO.output(18, False)  
    time.sleep(1)                   
GPIO.cleanup()