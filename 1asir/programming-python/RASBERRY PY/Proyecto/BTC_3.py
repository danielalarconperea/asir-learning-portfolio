import RPi.GPIO as GPIO # type: ignore
import requests # type: ignore
import time

# --- Configuración de Pines GPIO ---
# Cambia estos números a los pines GPIO reales que estés utilizando
LED_VERDE_PIN = 17  # Ejemplo: GPIO 17
LED_ROJO_PIN = 27   # Ejemplo: GPIO 27
BOTON_PIN = 22      # Ejemplo: GPIO 22

# --- Variables Globales ---
precio_anterior_bitcoin = None
programa_corriendo = True

# --- Configuración de GPIO ---
GPIO.setmode(GPIO.BCM)  # Usamos el modo BCM para referirnos a los pines por su número GPIO
GPIO.setup(LED_VERDE_PIN, GPIO.OUT)
GPIO.setup(LED_ROJO_PIN, GPIO.OUT)
GPIO.setup(BOTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) # PUD_UP significa que el pin está HIGH por defecto, y LOW cuando se pulsa el botón

# --- Función para apagar todos los LEDs ---
def apagar_leds():
    GPIO.output(LED_VERDE_PIN, GPIO.LOW)
    GPIO.output(LED_ROJO_PIN, GPIO.LOW)

# --- Función para obtener el precio de Bitcoin usando CoinDesk API ---
def obtener_precio_bitcoin():
    global precio_anterior_bitcoin
    try:
        # API de CoinDesk para el precio actual de Bitcoin en USD
        url = "https://api.coindesk.com/v1/bpi/currentprice.json"
        response = requests.get(url)
        data = response.json()

        # Accedemos al precio en USD. Puedes cambiar 'USD' por 'EUR' si prefieres el precio en Euros.
        precio_actual = data['bpi']['USD']['rate_float'] 
        print(f"Precio actual de Bitcoin (CoinDesk): ${precio_actual:.2f}") # Formatear a 2 decimales

        if precio_anterior_bitcoin is not None:
            if precio_actual > precio_anterior_bitcoin:
                print("Bitcoin ha SUBIDO. Encendiendo LED Verde.")
                apagar_leds()
                GPIO.output(LED_VERDE_PIN, GPIO.HIGH)
            elif precio_actual < precio_anterior_bitcoin:
                print("Bitcoin ha BAJADO. Encendiendo LED Rojo.")
                apagar_leds()
                GPIO.output(LED_ROJO_PIN, GPIO.HIGH)
            else:
                print("Bitcoin se mantiene sin cambios.")
                apagar_leds()

        precio_anterior_bitcoin = precio_actual
        return True # Indica que se obtuvo el precio correctamente

    except Exception as e:
        print(f"Error al obtener el precio de Bitcoin (CoinDesk): {e}")
        apagar_leds() # Apaga los LEDs en caso de error
        return False # Indica que hubo un error

# --- Función de callback para el botón ---
def boton_pulsado(channel):
    global programa_corriendo
    print("\n¡Botón pulsado! Deteniendo el programa...")
    programa_corriendo = False

# --- Añadir el evento de detección de botón ---
GPIO.add_event_detect(BOTON_PIN, GPIO.FALLING, callback=boton_pulsado, bouncetime=200)

# --- Bucle principal ---
print("Iniciando monitor de Bitcoin. Pulsa el botón para salir.")
apagar_leds() # Asegurarse de que los LEDs estén apagados al inicio

try:
    while programa_corriendo:
        obtener_precio_bitcoin()
        time.sleep(60)  # Esperar 60 segundos (1 minuto) antes de la siguiente comprobación

except KeyboardInterrupt:
    print("\nPrograma detenido manualmente por KeyboardInterrupt.")

finally:
    apagar_leds()
    GPIO.cleanup() # Libera todos los recursos GPIO
    print("GPIO limpiado. Programa finalizado.")