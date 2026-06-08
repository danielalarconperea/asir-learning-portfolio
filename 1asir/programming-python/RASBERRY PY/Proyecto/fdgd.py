import requests # type: ignore
import time

def verificar_btc_cambio():
    # Obtener el precio actual de Bitcoin
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    respuesta_actual = requests.get(url).json()
    precio_actual = respuesta_actual['bitcoin']['usd']
    print(f"Precio actual de BTC: ${precio_actual:.2f}")

    # Esperar 1 hora (3600 segundos)
    print("Esperando 1 hora para comparar el precio...")
    time.sleep(3600)

    # Obtener el precio de Bitcoin después de 1 hora
    respuesta_despues = requests.get(url).json()
    precio_despues = respuesta_despues['bitcoin']['usd']
    print(f"Precio de BTC después de 1 hora: ${precio_despues:.2f}")

    # Comparar los precios
    if precio_despues > precio_actual:
        print("¡BTC ha SUBIDO en la última hora!")
    elif precio_despues < precio_actual:
        print("BTC ha BAJADO en la última hora.")
    else:
        print("El precio de BTC no ha cambiado en la última hora.")

# Ejecutar la función
verificar_btc_cambio()