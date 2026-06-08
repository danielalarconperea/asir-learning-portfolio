import requests # type: ignore
import time
from datetime import datetime, timedelta

def verificar_btc_cambio_historico():
    # Obtener el precio actual de Bitcoin
    url_actual = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    try:
        respuesta_actual = requests.get(url_actual).json()
        precio_actual = respuesta_actual['bitcoin']['usd']
        print(f"Precio actual de BTC: ${precio_actual:.2f}")
    except Exception as e:
        print(f"Error al obtener el precio actual: {e}")
        return

    # Obtener el timestamp de hace 1 hora (en segundos)
    hace_una_hora = datetime.now() - timedelta(hours=1)
    timestamp_hace_una_hora = int(hace_una_hora.timestamp())

    # La API de CoinGecko para el historial por rango (market_chart/range) espera segundos UNIX
    # y para el último día, la granularidad suele ser de 5 minutos, que es suficiente para nuestra "hora".
    # Necesitamos un rango, así que tomamos desde hace 65 minutos hasta hace 55 minutos para asegurar un punto de datos.
    timestamp_inicio = int((datetime.now() - timedelta(minutes=65)).timestamp())
    timestamp_fin = int((datetime.now() - timedelta(minutes=55)).timestamp())

    url_historico = f"https://api.coingecko.com/api/v3/coins/bitcoin/market_chart/range?vs_currency=usd&from={timestamp_inicio}&to={timestamp_fin}"

    try:
        respuesta_historico = requests.get(url_historico).json()
        precios_historicos = respuesta_historico.get('prices')

        if precios_historicos:
            # Tomamos el primer precio del rango como el precio de "hace una hora"
            # o el más cercano a esa hora si hay varios puntos de datos en ese rango
            precio_hace_una_hora = precios_historicos[0][1] # El segundo elemento es el precio
            print(f"Precio de BTC hace aproximadamente 1 hora: ${precio_hace_una_hora:.2f}")

            # Comparar los precios
            if precio_actual > precio_hace_una_hora:
                print("¡BTC ha **SUBIDO** en la última hora!")
            elif precio_actual < precio_hace_una_hora:
                print("BTC ha **BAJADO** en la última hora.")
            else:
                print("El precio de BTC no ha cambiado significativamente en la última hora.")
        else:
            print("No se pudieron obtener datos históricos para la última hora. La API podría tener una granularidad limitada para ese rango.")

    except Exception as e:
        print(f"Error al obtener el precio histórico: {e}")

# Ejecutar la función
verificar_btc_cambio_historico()