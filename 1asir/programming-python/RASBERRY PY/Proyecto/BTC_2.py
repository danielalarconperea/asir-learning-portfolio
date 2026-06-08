import RPi.GPIO as GPIO # type: ignore
import requests # type: ignore
import time
import sys
from datetime import date

# --- Constantes de Pines GPIO ---
L_VERDE = 17
L_ROJO = 27
PIN_BOTON = 23

# --- Configuración API Coinlore ---
BITCOIN_API_URL_COINLORE = f"https://api.coinlore.net/api/ticker/?id=90"

# --- Temporización ---
INTERVALO_ACTUALIZACION = 300  # 300s = 5min

# --- Variables Globales ---
corriendo = True
precio_inicio_dia_almacenado = None
fecha_del_precio_inicio = None # Para rastrear para qué día es el precio_inicio_dia_almacenado

# --- Funciones ---

def configurar_gpio():
    """Configura los pines GPIO."""
    GPIO.setwarnings(False) # Desactivar advertencias
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(L_VERDE, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(L_ROJO, GPIO.OUT, initial=GPIO.LOW)
    # Configurar el pin del botón con resistencia pull-up interna
    GPIO.setup(PIN_BOTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def limpiar_gpio():
    """Limpia la configuración de GPIO al salir."""
    print("\nLimpiando GPIO...")
    if 'GPIO' in sys.modules and GPIO.getmode() is not None: # Solo limpiar si GPIO fue inicializado
        GPIO.output(L_VERDE, False)
        GPIO.output(L_ROJO, False)
        GPIO.cleanup()
    print("Programa terminado.")

def obtener_precio_bitcoin_actual_coinlore():
    """Obtiene el precio actual de Bitcoin desde Coinlore."""
    try:
        response = requests.get(BITCOIN_API_URL_COINLORE, timeout=10)
        response.raise_for_status()  # Lanza un error para respuestas HTTP malas
        data = response.json()
        if data and isinstance(data, list) and len(data) > 0:
            precio_str = data[0].get('price_usd')
            if precio_str is None:
                print("Error: Campo 'price_usd' no encontrado en la respuesta de Coinlore.")
                return None
            precio = float(precio_str)
            return precio
        else:
            print("Error: Respuesta inesperada o vacía de Coinlore.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener el precio actual de Coinlore: {e}")
        return None
    except (KeyError, ValueError, IndexError) as e:
        print(f"Error al procesar los datos del precio actual de Coinlore: {e}")
        return None
    except Exception as e: # Captura cualquier otra excepción no prevista
        print(f"Error inesperado en obtener_precio_bitcoin_actual_coinlore: {e}")
        return None

def controlar_leds_estado_diario(precio_actual, precio_referencia_inicio_dia, fecha_referencia):
    """Controla los LEDs según si el precio sube o baja respecto al inicio del día."""
    if precio_actual is None or precio_referencia_inicio_dia is None:
        # Este caso se maneja principalmente en el bucle principal,
        # pero es una salvaguarda aquí.
        print("Datos de precio insuficientes para controlar LEDs. Apagando LEDs.")
        GPIO.output(L_VERDE, False)
        GPIO.output(L_ROJO, False)
        return

    # Imprimir información sobre los precios para depuración y seguimiento
    cambio_abs = precio_actual - precio_referencia_inicio_dia
    cambio_porc = (cambio_abs / precio_referencia_inicio_dia) * 100 if precio_referencia_inicio_dia != 0 else 0
    print(f"Precio inicio día ({fecha_referencia}): ${precio_referencia_inicio_dia:.2f} USD")
    print(f"Precio actual ({time.strftime('%H:%M:%S')}): ${precio_actual:.2f} USD. Cambio diario: {cambio_porc:.2f}% (${cambio_abs:+.2f})")

    # Lógica binaria para los LEDs: solo verde o rojo
    if precio_actual > precio_referencia_inicio_dia:
        print("Bitcoin SUBIENDO hoy. Encendiendo LED VERDE.")
        GPIO.output(L_VERDE, True)
        GPIO.output(L_ROJO, False)
    elif precio_actual < precio_referencia_inicio_dia:
        print("Bitcoin BAJANDO hoy. Encendiendo LED ROJO.")
        GPIO.output(L_VERDE, False)
        GPIO.output(L_ROJO, True)
    else: # precio_actual == precio_referencia_inicio_dia
        print("Bitcoin ESTABLE hoy (igual al precio de inicio). Considerando como 'no subiendo', LED ROJO.")
        GPIO.output(L_VERDE, False)
        GPIO.output(L_ROJO, True) # LED rojo si es igual

def boton_presionado(channel):
    """Función callback que se ejecuta cuando se presiona el botón."""
    print("¡Botón presionado! Saliendo del programa...")
    global corriendo
    corriendo = False

# --- Programa Principal ---
if __name__ == "__main__":
    try:
        configurar_gpio()
        print("Programa iniciado. Presiona el botón para detener.")
        print(f"Consultando precios cada {INTERVALO_ACTUALIZACION} segundos ({INTERVALO_ACTUALIZACION/60:.1f} minutos).")
        print("LED VERDE si el precio de Bitcoin sube respecto al inicio del día.")
        print("LED ROJO si el precio de Bitcoin baja o es igual al precio de inicio del día.")
        print(f"API utilizada: Coinlore (ID Bitcoin: 90)")
        print("---")

        GPIO.add_event_detect(PIN_BOTON, GPIO.FALLING, callback=boton_presionado, bouncetime=300)

        while corriendo:
            hoy = date.today() # Obtener la fecha actual al inicio de cada ciclo
            precio_ahora = obtener_precio_bitcoin_actual_coinlore() # Obtener el precio actual UNA VEZ por ciclo

            if precio_ahora is None:
                # Si no se pudo obtener el precio, apagar ambos LEDs
                print(f"({time.strftime('%H:%M:%S')}) Error al obtener el precio actual. Apagando LEDs.")
                GPIO.output(L_VERDE, False)
                GPIO.output(L_ROJO, False)
            else:
                # Si es un nuevo día o la primera vez que se ejecuta el script,
                # se establece el precio_ahora como el precio de inicio del día.
                if fecha_del_precio_inicio is None or fecha_del_precio_inicio != hoy:
                    print(f"Nuevo día ({hoy}) o primera ejecución del script.")
                    precio_inicio_dia_almacenado = precio_ahora
                    fecha_del_precio_inicio = hoy
                    print(f"Precio de inicio para {hoy} establecido en: ${precio_inicio_dia_almacenado:.2f} USD (a las {time.strftime('%H:%M:%S')})")
                    # Llamar a controlar_leds para establecer el estado inicial de los LEDs
                    # (será rojo si el precio es igual al de inicio, como es el caso aquí)
                    controlar_leds_estado_diario(precio_ahora, precio_inicio_dia_almacenado, fecha_del_precio_inicio)
                else:
                    # Si ya tenemos un precio de inicio para hoy, comparamos el precio_ahora con él.
                    controlar_leds_estado_diario(precio_ahora, precio_inicio_dia_almacenado, fecha_del_precio_inicio)
            
            print("---")
            
            # Espera optimizada para respuesta del botón
            for _ in range(INTERVALO_ACTUALIZACION):
                if not corriendo:
                    break
                time.sleep(1) # Esperar 1 segundo y comprobar
            
            if not corriendo: # Salir del bucle while principal si el botón fue presionado
                break

    except KeyboardInterrupt: # Permite salir con Ctrl+C
        print("\nInterrupción por teclado recibida.")
    finally:
        limpiar_gpio()
        sys.exit(0) # Salir del programa limpiamente