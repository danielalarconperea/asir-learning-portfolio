import requests # type: ignore
import time

# --- Variables Globales ---
precio_anterior_bitcoin = None

# --- Función para obtener el precio de Bitcoin usando CoinDesk API ---
def obtener_precio_bitcoin():
    global precio_anterior_bitcoin
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        response = requests.get(url)
        data = response.json()

        precio_actual = data['bitcoin']['usd']
        print(f"Precio actual de Bitcoin: ${precio_actual:.2f}")

        if precio_anterior_bitcoin is not None:
            if precio_actual > precio_anterior_bitcoin:
                print("¡Bitcoin ha SUBIDO!")
            elif precio_actual < precio_anterior_bitcoin:
                print("¡Bitcoin ha BAJADO!")
            else:
                print("Bitcoin se mantiene sin cambios.")

        precio_anterior_bitcoin = precio_actual
        return True

    except Exception as e:
        print(f"Error al obtener el precio de Bitcoin: {e}")
        return False

# --- Bucle principal ---
print("Iniciando monitor de Bitcoin. Usa Ctrl+C para salir.")

try:
    while True:
        obtener_precio_bitcoin()
        time.sleep(60) # Esperar 60 segundos (1 minuto)

except KeyboardInterrupt:
    print("\nPrograma detenido manualmente.")

finally:
    print("Programa finalizado.")