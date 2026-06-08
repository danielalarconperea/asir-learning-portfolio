# pip install alpha_vantage pandas

import pandas as pd # type: ignore
import time
from alpha_vantage.timeseries import TimeSeries # type: ignore

# --- CONFIGURACIÓN ---
YOUR_API_KEY = "CLAVE_API"
TICKER_SYMBOL = "AAPL"  # Símbolo del activo Apple
INTERVAL = '1min'       

# --- FUNCIÓN PARA OBTENER LOS DATOS Y ANALIZAR ---
def get_stock_data_and_analyze(api_key, ticker, interval):
    ts = TimeSeries(key=api_key, output_format='pandas')

    data, meta_data = ts.get_intraday(symbol=ticker, interval=interval, outputsize='compact')
    # 'compact' para un intervalo pequeño.

    if data.empty:
        print(f"No se pudieron obtener datos para {ticker}. Revisa el símbolo o tu conexión.")
        return

    # Índice de tipo fecha y hora para facilitar el manejo
    data.index = pd.to_datetime(data.index)
    data = data.sort_index(ascending=True) # Asegurarse que los datos estén ordenados por tiempo

    print(f"\n--- Analizando datos para {ticker} ---")
    print(f"Última actualización de datos: {data.index[-1]}")
    print(f"Precio actual ({data.index[-1].strftime('%H:%M')}): ${float(data['4. close'].iloc[-1]):.2f}")

    # Aquí tomamos el primer dato dentro de la última hora.
    one_hour_ago = data.index[-1] - pd.Timedelta(hours=1)
    data_last_hour = data[data.index >= one_hour_ago]

    if len(data_last_hour) > 1:
        precio_actual = float(data_last_hour['4. close'].iloc[-1])
        precio_hace_una_hora = float(data_last_hour['4. close'].iloc[0]) # El primer dato en la última hora

        print(f"Precio hace una hora (aprox. {data_last_hour.index[0].strftime('%H:%M')}): ${precio_hace_una_hora:.2f}")

        if precio_actual > precio_hace_una_hora:
            print(f"¡El precio de {ticker} está SUBIENDO! (Ha subido de ${precio_hace_una_hora:.2f} a ${precio_actual:.2f})")
        elif precio_actual < precio_hace_una_hora:
            print(f"¡El precio de {ticker} está BAJANDO! (Ha bajado de ${precio_hace_una_hora:.2f} a ${precio_actual:.2f})")
        else:
            print(f"El precio de {ticker} se ha mantenido ESTABLE en la última hora.")
    else:
        print("No hay suficientes datos en la última hora para realizar una comparación significativa.")

# --- EJECUCIÓN DEL CÓDIGO ---
while True:
    get_stock_data_and_analyze(YOUR_API_KEY, TICKER_SYMBOL, INTERVAL)
    print("\nEsperando 60 segundos para la próxima actualización...") # Para no exceder el límite de 5 llamadas por minuto
    time.sleep(60)