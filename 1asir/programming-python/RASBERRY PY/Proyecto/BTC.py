import RPi.GPIO as GPIO # type: ignore
import requests # type: ignore
import time
import sys


L_VERDE = 17  
L_ROJO = 27
L_AMARILLO = 22
PIN_BOTON = 23

# API de CoinGecko
BITCOIN_API_URL_HISTORICAL = "https://api.coingecko.com/api/v3/coins/bitcoin/market_chart"
BITCOIN_API_URL_CURRENT = "https://api.coingecko.com/api/v3/simple/price"
PARAMS_CURRENT = {
    'ids': 'bitcoin',
    'vs_currencies': 'usd'
}
PARAMS_HISTORICAL = {
    'vs_currency': 'usd', # Debe coincidir con la moneda actual
    'days': '1',          # Pedimos datos del último día para tener granularidad horaria
    'interval': 'hourly'  # Nos da datos por hora
}

# Umbrales
UMBRAL_PORCENTAJE = 0.5  # 0.5%

# Intervalo de actualización (en segundos)
INTERVALO_ACTUALIZACION = 300  # 5 minutos

# --- Funciones ---

def configurar_gpio():
    """Configura los pines GPIO."""
    GPIO.setwarnings(False) # Desactivar advertencias si los pines ya están en uso
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(L_VERDE, GPIO.OUT)
    GPIO.setup(L_ROJO, GPIO.OUT)
    GPIO.setup(L_AMARILLO, GPIO.OUT)
    GPIO.setup(PIN_BOTON, GPIO.IN)
    GPIO.input(PIN_BOTON, GPIO.PUD_UP) # Botón conectado a GND, resistencia pull-up interna
    GPIO.output(L_VERDE, False)
    GPIO.output(L_ROJO, False)
    GPIO.output(L_AMARILLO, False)

def limpiar_gpio():
    """Limpia la configuración de GPIO al salir."""
    print("\nLimpiando GPIO...")
    GPIO.output(L_VERDE, False)
    GPIO.output(L_ROJO, False)
    GPIO.output(L_AMARILLO, False)
    GPIO.cleanup()
    print("Programa terminado.")

def obtener_precio_bitcoin_actual():
    """Obtiene el precio actual de Bitcoin desde CoinGecko."""
    try:
        response = requests.get(BITCOIN_API_URL_CURRENT, params=PARAMS_CURRENT, timeout=10)
        response.raise_for_status()  # Lanza un error para respuestas HTTP malas (4xx o 5xx)
        data = response.json()
        precio = data['bitcoin'][PARAMS_CURRENT['vs_currencies']]
        print(f"Precio actual de Bitcoin: ${precio:.2f} {PARAMS_CURRENT['vs_currencies'].upper()}")
        return float(precio)
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el precio actual: {e}")
        return None
    except (KeyError, ValueError) as e:
        print(f"Error al procesar los datos del precio actual: {e}")
        return None

def obtener_precio_bitcoin_hace_una_hora():
    """Obtiene el precio de Bitcoin de hace aproximadamente una hora desde CoinGecko."""
    try:
        response = requests.get(BITCOIN_API_URL_HISTORICAL, params=PARAMS_HISTORICAL, timeout=10)
        response.raise_for_status()
        data = response.json()
        # La API devuelve precios [timestamp, price]
        # El último punto es el precio al inicio de la hora actual.
        # El penúltimo es el precio al inicio de la hora anterior.
        if len(data['prices']) >= 2:
            # El penúltimo dato corresponde al precio de cierre de la hora anterior
            # o el inicio de la hora anterior, dependiendo de la granularidad.
            # Con 'interval=hourly' y 'days=1', el segundo al último punto es de hace ~1 hora.
            # CoinGecko devuelve timestamps en milisegundos.
            precio_hace_una_hora = data['prices'][-2][1] # Tomamos el penúltimo precio
            timestamp_hace_una_hora = data['prices'][-2][0] / 1000 # Convertir a segundos
            print(f"Precio de Bitcoin hace ~1 hora ({time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp_hace_una_hora))}): ${precio_hace_una_hora:.2f} {PARAMS_HISTORICAL['vs_currency'].upper()}")
            return float(precio_hace_una_hora)
        else:
            print("No hay suficientes datos históricos para obtener el precio de hace una hora.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el precio histórico: {e}")
        return None
    except (KeyError, ValueError, IndexError) as e:
        print(f"Error al procesar los datos del precio histórico: {e}")
        return None

def controlar_leds(precio_actual, precio_hace_una_hora):
    """Controla los LEDs según el cambio de precio."""
    if precio_actual is None or precio_hace_una_hora is None or precio_hace_una_hora == 0:
        # Si no tenemos datos o el precio anterior es cero, encendemos el amarillo por defecto
        print("Datos de precio insuficientes, LED amarillo encendido.")
        GPIO.output(L_VERDE, False)
        GPIO.output(L_ROJO, False)
        GPIO.output(L_AMARILLO, True)
        return

    cambio_porcentual = ((precio_actual - precio_hace_una_hora) / precio_hace_una_hora) * 100
    print(f"Cambio en la última hora: {cambio_porcentual:.2f}%")

    # Apagar todos los LEDs primero
    GPIO.output(L_VERDE, False)
    GPIO.output(L_ROJO, False)
    GPIO.output(L_AMARILLO, False)

    if cambio_porcentual > UMBRAL_PORCENTAJE:
        print("Bitcoin SUBIÓ. Encendiendo LED VERDE.")
        GPIO.output(L_VERDE, True)
    elif cambio_porcentual < -UMBRAL_PORCENTAJE:
        print("Bitcoin BAJÓ. Encendiendo LED ROJO.")
        GPIO.output(L_ROJO, True)
    else:
     print("Bitcoin ESTABLE. Encendiendo LED AMARILLO.")
     GPIO.output(L_AMARILLO, True)

def boton_presionado(channel):
    """Función callback que se ejecuta cuando se presiona el botón."""
    print("¡Botón presionado! Saliendo del programa...")
    global corriendo
    corriendo = False

# --- Programa Principal ---
corriendo = True

if __name__ == "__main__":
    try:
        configurar_gpio()
        print("Programa iniciado. Presiona el botón para detener.")
        print(f"Consultando precios cada {INTERVALO_ACTUALIZACION} segundos.")
        print(f"Umbral de cambio: +/- {UMBRAL_PORCENTAJE}%")
        print("---")

        # Añadir detección de evento para el botón
        GPIO.add_event_detect(PIN_BOTON, GPIO.FALLING, callback=boton_presionado, bouncetime=300)
        # GPIO.FALLING porque usamos pull_up_down=GPIO.PUD_UP (el pin está en HIGH y pasa a LOW al presionar)

        while corriendo:
            precio_actual = obtener_precio_bitcoin_actual()
            precio_anterior = obtener_precio_bitcoin_hace_una_hora()

            if precio_actual is not None and precio_anterior is not None:
                controlar_leds(precio_actual, precio_anterior)
            else:
                # En caso de error, encender LED amarillo como indicador
                GPIO.output(L_VERDE, False)
                GPIO.output(L_ROJO, False)
                GPIO.output(L_AMARILLO, True)
                print("Error al obtener precios, LED amarillo como indicador de fallo.")

            print("---")
            # Esperar antes de la próxima actualización o hasta que el botón sea presionado
            # Hacemos un bucle de espera más corto para que el botón responda más rápido
            for _ in range(INTERVALO_ACTUALIZACION):
                if not corriendo:
                    break
                time.sleep(1)

    except KeyboardInterrupt: # Permite salir con Ctrl+C
        print("\nInterrupción por teclado recibida.")
    finally:
        limpiar_gpio()
        sys.exit(0) # Salir del programa limpiamente