# sudo apt install python3-pandas
# apt search alpha_vantage

# pip install alpha_vantage pandas

import pandas as pd # type: ignore
import time
from alpha_vantage.timeseries import TimeSeries # type: ignore
import RPi.GPIO as GPIO # type: ignore

LED_SUBIDA = 17 
LED_BAJADA = 27

GPIO.setmode(GPIO.BCM) 
GPIO.setup(LED_SUBIDA, GPIO.OUT) 
GPIO.setup(LED_BAJADA, GPIO.OUT)

# --- CONFIGURACIÓN ---
YOUR_API_KEY = "CLAVE_API"  
TICKER_SYMBOL = "AAPL" # Símbolo del activo Apple
INTERVAL = '1min'

# Función para apagar ambos LEDs
def apagar_leds():
    GPIO.output(LED_SUBIDA, False)
    GPIO.output(LED_BAJADA, False)

# --- FUNCIÓN PARA OBTENER LOS DATOS Y ANALIZAR ---
def get_stock_data_and_analyze(api_key, ticker, interval):
    ts = TimeSeries(key=api_key, output_format='pandas')

    data, meta_data = ts.get_intraday(symbol=ticker, interval=interval, outputsize='compact')
    
    if data.empty:
        print(f"No se pudieron obtener datos para {ticker}. Revisa el símbolo o tu conexión.")
        apagar_leds()
        return

    # Índice de tipo fecha y hora para facilitar el manejo
    data.index = pd.to_datetime(data.index)
    data = data.sort_index(ascending=True) # Asegurarse que los datos estén ordenados por tiempo

    print(f"\n--- Analizando datos para {ticker} ---")
    print(f"Última actualización de datos: {data.index[-1]}")
    print(f"Precio actual ({data.index[-1].strftime('%H:%M')}): ${float(data['4. close'].iloc[-1]):.2f}")

    if len(data) > 1: # Asegurarse de que hay al menos 2 puntos para comparar
        precio_actual = float(data['4. close'].iloc[-1])
        precio_anterior = float(data['4. close'].iloc[-2]) # Comparamos con el precio anterior inmediato

        print(f"Precio anterior ({data.index[-2].strftime('%H:%M')}): ${precio_anterior:.2f}")

        apagar_leds()

        if precio_actual > precio_anterior:
            print(f"¡El precio de {ticker} está SUBIENDO! (Ha subido de ${precio_anterior:.2f} a ${precio_actual:.2f})")
            GPIO.output(LED_SUBIDA, True) # Enciende el LED de subida
        elif precio_actual < precio_anterior:
            print(f"¡El precio de {ticker} está BAJANDO! (Ha bajado de ${precio_anterior:.2f} a ${precio_actual:.2f})")
            GPIO.output(LED_BAJADA, True) # Enciende el LED de bajada
        else:
            print(f"El precio de {ticker} se ha mantenido ESTABLE.")
            # Ambos LEDs permanecen apagados
    else:
        print("No hay suficientes datos para realizar una comparación significativa.")
        apagar_leds()

# --- EJECUCIÓN DEL CÓDIGO ---

apagar_leds()
get_stock_data_and_analyze(YOUR_API_KEY, TICKER_SYMBOL, INTERVAL)
time.sleep(10)
apagar_leds()
GPIO.cleanup()