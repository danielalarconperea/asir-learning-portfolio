# Apuntes Completos del Módulo `time` en Python

# El módulo `time` proporciona varias funciones relacionadas con el tiempo.

import time

# ------------------------------------------------------------------------------
# 1. Obtener el tiempo actual
# ------------------------------------------------------------------------------

# time.time(): Devuelve el tiempo actual en segundos desde la "Epoch".
# La Epoch es un punto de referencia en el tiempo; para sistemas Unix,
# es el 1 de enero de 1970, 00:00:00 (UTC).
# Devuelve un número de punto flotante (float).

segundos_desde_epoch = time.time()
print(f"1. Segundos desde la Epoch (time.time()): {segundos_desde_epoch}")

# ------------------------------------------------------------------------------
# 2. Estructuras de tiempo (struct_time)
# ------------------------------------------------------------------------------

# Varias funciones en el módulo `time` trabajan con objetos `time.struct_time`.
# Un objeto `struct_time` es una tupla con nombre que representa un instante
# de tiempo con los siguientes atributos (y sus índices en la tupla):
#
# tm_year  : Año (ej. 2024)
# tm_mon   : Mes (1-12)
# tm_mday  : Día del mes (1-31)
# tm_hour  : Hora (0-23)
# tm_min   : Minuto (0-59)
# tm_sec   : Segundo (0-61,      60 o 61 para segundos intercalares)
# tm_wday  : Día de la semana (0-6, Lunes es 0)
# tm_yday  : Día del año (1-366)
# tm_isdst : Indicador de horario de verano (0, 1, o -1 si es desconocido)

# time.gmtime([secs]): Convierte segundos desde la Epoch a un objeto `struct_time`
# en UTC (Tiempo Universal Coordinado). Si no se proporcionan `secs` o es `None`,
# se usa `time.time()`.

struct_time_utc = time.gmtime() # Usando el tiempo actual
print(f"\n2.1. Objeto struct_time en UTC (time.gmtime()): {struct_time_utc}")
print(f"    Año UTC: {struct_time_utc.tm_year}")
print(f"    Mes UTC: {struct_time_utc.tm_mon}")
print(f"    Día UTC: {struct_time_utc.tm_mday}")

struct_time_utc_especifico = time.gmtime(0) # Corresponde a la Epoch
print(f"2.2. struct_time en UTC para la Epoch (time.gmtime(0)): {struct_time_utc_especifico}")

# time.localtime([secs]): Similar a `gmtime()`, pero convierte a la hora local
# según la configuración del sistema.

struct_time_local = time.localtime() # Usando el tiempo actual
print(f"\n2.3. Objeto struct_time en hora local (time.localtime()): {struct_time_local}")
print(f"    Año Local: {struct_time_local.tm_year}")
print(f"    Mes Local: {struct_time_local.tm_mon}")
print(f"    Día Local: {struct_time_local.tm_mday}")
print(f"    Hora Local: {struct_time_local.tm_hour}")
print(f"    Horario de verano (tm_isdst): {struct_time_local.tm_isdst}") # 1 si está activo, 0 si no, -1 desconocido

# ------------------------------------------------------------------------------
# 3. Convertir struct_time a segundos desde la Epoch
# ------------------------------------------------------------------------------

# time.mktime(t): Es la función inversa de `localtime()`.
# Toma un objeto `struct_time` (o una tupla de 9 elementos) en hora local
# y devuelve los segundos desde la Epoch como un número de punto flotante.
# Los campos `tm_wday` y `tm_yday` no son necesarios y son calculados por la función.
# Si el valor `tm_isdst` es -1, `mktime` intentará adivinar si el horario de verano
# estaba en vigor para la fecha dada.

segundos_calculados = time.mktime(struct_time_local)
print(f"\n3. Segundos desde la Epoch calculados desde struct_time local (time.mktime()): {segundos_calculados}")

# Ejemplo creando una tupla para mktime:
# (año, mes, día, hora, min, seg, dia_semana, dia_año, is_dst)
tupla_tiempo = (2023, 12, 25, 10, 30, 0, 0, 359, -1) # Navidad 2023 a las 10:30
segundos_navidad_2023 = time.mktime(tupla_tiempo)
print(f"   Segundos para Navidad 2023 10:30: {segundos_navidad_2023}")
print(f"   Verificación (localtime de esos segundos): {time.localtime(segundos_navidad_2023)}")


# ------------------------------------------------------------------------------
# 4. Formatear tiempo como cadenas de texto
# ------------------------------------------------------------------------------

# time.asctime([t]): Convierte un objeto `struct_time` (o una tupla de 9 elementos)
# a una cadena de texto con un formato estándar, ej: 'Tue May 13 08:30:00 2025'.
# Si no se proporciona `t` o es `None`, se usa `time.localtime()`.

cadena_asctime_local = time.asctime() # Hora local actual
print(f"\n4.1. Cadena de tiempo local (time.asctime()): {cadena_asctime_local}")

cadena_asctime_utc = time.asctime(time.gmtime()) # Hora UTC actual
print(f"4.2. Cadena de tiempo UTC (time.asctime(time.gmtime())): {cadena_asctime_utc}")

cadena_asctime_especifico = time.asctime(struct_time_local)
print(f"4.3. Cadena para struct_time_local (time.asctime(struct_time_local)): {cadena_asctime_especifico}")

# time.ctime([secs]): Convierte un tiempo expresado en segundos desde la Epoch
# a una cadena de texto. Es equivalente a `asctime(localtime(secs))`.
# Si no se proporcionan `secs` o es `None`, se usa `time.time()`.

cadena_ctime_actual = time.ctime() # Hora local actual
print(f"\n4.4. Cadena de tiempo desde segundos (time.ctime()): {cadena_ctime_actual}")

cadena_ctime_epoch = time.ctime(0) # Tiempo en la Epoch (hora local)
print(f"4.5. Cadena de tiempo para la Epoch (time.ctime(0)): {cadena_ctime_epoch}")

# time.strftime(format, t): Convierte un objeto `struct_time` (o una tupla de 9 elementos)
# a una cadena de texto, según una directiva de formato especificada.
# Si no se proporciona `t`, se usa `time.localtime()`.

# Directivas de formato comunes:
# %Y - Año con siglo (ej. 2024)
# %y - Año sin siglo (ej. 24)
# %m - Mes como número decimal (01-12)
# %B - Nombre completo del mes (ej. May)
# %b - Nombre abreviado del mes (ej. May)
# %d - Día del mes como número decimal (01-31)
# %A - Nombre completo del día de la semana (ej. Tuesday)
# %a - Nombre abreviado del día de la semana (ej. Tue)
# %H - Hora (reloj de 24 horas) como decimal (00-23)
# %I - Hora (reloj de 12 horas) como decimal (01-12)
# %M - Minuto como número decimal (00-59)
# %S - Segundo como número decimal (00-61)
# %p - Equivalente local de AM o PM.
# %Z - Nombre de la zona horaria (o nada si no hay zona horaria).
# %j - Día del año como número decimal (001-366).
# %U - Número de semana del año (Domingo como primer día) (00-53).
# %W - Número de semana del año (Lunes como primer día) (00-53).
# %c - Representación de fecha y hora apropiada para la configuración regional.
# %x - Representación de fecha apropiada para la configuración regional.
# %X - Representación de hora apropiada para la configuración regional.

formato_personalizado = "%Y-%m-%d %H:%M:%S %Z (%A)"
cadena_formateada = time.strftime(formato_personalizado, struct_time_local)
print(f"\n4.6. Cadena formateada (time.strftime()): {cadena_formateada}")

cadena_formateada_actual = time.strftime("%Y-%m-%d %I:%M:%S %p") # Hora local actual
print(f"4.7. Cadena formateada (actual): {cadena_formateada_actual}")

cadena_fecha_iso = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()) # Formato ISO 8601 UTC
print(f"4.8. Cadena formato ISO 8601 UTC: {cadena_fecha_iso}Z")


# ------------------------------------------------------------------------------
# 5. Analizar cadenas de texto a tiempo (Parsing)
# ------------------------------------------------------------------------------

# time.strptime(string, format): Analiza una cadena que representa un tiempo
# según un formato y devuelve un objeto `struct_time`.
# Es la inversa de `strftime()`.

cadena_a_parsear = "2023-07-15 14:30:00"
formato_parseo = "%Y-%m-%d %H:%M:%S"
struct_time_parseado = time.strptime(cadena_a_parsear, formato_parseo)
print(f"\n5.1. struct_time parseado (time.strptime()): {struct_time_parseado}")
print(f"    Año parseado: {struct_time_parseado.tm_year}")
print(f"    Hora parseada: {struct_time_parseado.tm_hour}")

# Si la cadena no coincide con el formato, se lanzará un ValueError.

# ------------------------------------------------------------------------------
# 6. Pausar la ejecución
# ------------------------------------------------------------------------------

# time.sleep(secs): Suspende la ejecución del hilo actual durante el número
# de segundos especificado. El argumento puede ser un número de punto flotante
# para indicar un tiempo de suspensión más preciso.

print("\n6.1. Inicio de la pausa (time.sleep())")
time.sleep(1.5) # Pausa de 1.5 segundos
print("6.2. Fin de la pausa de 1.5 segundos")

# ------------------------------------------------------------------------------
# 7. Medición de rendimiento y tiempo de CPU
# ------------------------------------------------------------------------------

# time.perf_counter(): Devuelve el valor (en segundos fraccionarios) de un
# contador de rendimiento, es decir, un reloj con la mayor resolución disponible
# para medir una duración corta. Incluye el tiempo transcurrido durante el `sleep`.
# Es un reloj monotónico (no puede ir hacia atrás).
# El punto de referencia cero del valor devuelto no está definido, por lo que solo
# la diferencia entre los resultados de llamadas consecutivas es válida.

inicio_perf = time.perf_counter()
# Realizar alguna operación costosa aquí
for _ in range(1000000):
    pass
fin_perf = time.perf_counter()
duracion_perf = fin_perf - inicio_perf
print(f"\n7.1. Duración medida con perf_counter(): {duracion_perf:.6f} segundos")

# time.process_time(): Devuelve el valor (en segundos fraccionarios) de la suma
# del tiempo de CPU del sistema y del usuario del proceso actual.
# No incluye el tiempo transcurrido durante `sleep`.
# Es útil para medir el tiempo de CPU consumido por un bloque de código.
# El punto de referencia cero no está definido.

inicio_proc = time.process_time()
# Realizar alguna operación costosa aquí
for _ in range(1000000):
    pass
fin_proc = time.process_time()
duracion_proc = fin_proc - inicio_proc
print(f"7.2. Tiempo de CPU del proceso (process_time()): {duracion_proc:.6f} segundos")

# time.monotonic(): Devuelve el valor (en segundos fraccionarios) de un reloj
# monotónico. Un reloj monotónico no puede ir hacia atrás. No se ve afectado
# por las actualizaciones del reloj del sistema.
# El punto de referencia cero del valor devuelto no está definido.

inicio_mono = time.monotonic()
time.sleep(0.5)
fin_mono = time.monotonic()
duracion_mono = fin_mono - inicio_mono
print(f"7.3. Duración medida con monotonic(): {duracion_mono:.6f} segundos")


# ------------------------------------------------------------------------------
# 8. Información de la zona horaria
# ------------------------------------------------------------------------------

# time.tzname: Una tupla de dos cadenas: la primera es el nombre de la zona horaria
# local no DST (Horario Estándar), y la segunda es el nombre de la zona horaria
# local DST (Horario de Verano). Si no se define ninguna zona horaria DST, la
# segunda cadena no debería usarse.

print(f"\n8.1. Nombres de las zonas horarias (time.tzname): {time.tzname}")

# time.timezone: El desplazamiento de la zona horaria local no DST (Horario Estándar),
# en segundos al oeste de UTC. (Negativo para la mayoría de las zonas de Europa Occidental,
# positivo para EEUU). Esto es `(-time.altzone)` si `time.daylight` es cero.

print(f"8.2. Desplazamiento de la zona horaria estándar (time.timezone): {time.timezone} segundos al oeste de UTC")

# time.altzone: El desplazamiento de la zona horaria local DST (Horario de Verano),
# en segundos al oeste de UTC, si está definida. Este valor es negativo si la
# zona horaria local DST está al este de UTC (como en Europa Occidental, incluyendo el Reino Unido).
# Solo usar si `time.daylight` es distinto de cero.

# (Nota: El valor de altzone puede ser confuso. Es el offset en segundos al OESTE de UTC.
#  Para CET (UTC+1) sin DST, timezone es -3600. Para CEST (UTC+2) con DST, altzone es -7200)
if time.daylight != 0:
    print(f"8.3. Desplazamiento de la zona horaria de verano (time.altzone): {time.altzone} segundos al oeste de UTC")
else:
    print("8.3. Horario de verano (DST) no aplicable para la zona horaria actual en este momento, o no definido.")

# time.daylight: Distinto de cero si se define una zona horaria DST.

print(f"8.4. ¿Horario de verano (DST) definido? (time.daylight): {'Sí' if time.daylight != 0 else 'No'}")


# ------------------------------------------------------------------------------
# 9. Otras funciones (menos comunes o específicas)
# ------------------------------------------------------------------------------

# time.thread_time(): Devuelve el tiempo de CPU específico del hilo actual
# (suma de tiempo de sistema + usuario). Similar a process_time() pero para el hilo.
# Solo disponible en algunos sistemas (ej. Linux, Windows a partir de Python 3.7).
try:
    tiempo_hilo_inicio = time.thread_time()
    # alguna operación
    for _ in range(1000): pass
    tiempo_hilo_fin = time.thread_time()
    print(f"\n9.1. Tiempo de CPU del hilo (thread_time()): {(tiempo_hilo_fin - tiempo_hilo_inicio):.6f} segundos")
except AttributeError:
    print("\n9.1. time.thread_time() no está disponible en este sistema.")


# time.get_clock_info(name): Devuelve información sobre el reloj especificado como un objeto.
# Nombres de reloj comunes: 'monotonic', 'perf_counter', 'process_time', 'time', 'thread_time'.
# Atributos del objeto devuelto:
#   adjustable: True si el reloj puede ser cambiado (ej. por el administrador del sistema).
#   implementation: El nombre de la función C subyacente utilizada para obtener el valor del reloj.
#   monotonic: True si el reloj es monotónico.
#   resolution: La resolución del reloj en segundos fraccionarios (ej. 1e-09 para nanosegundos).

print("\n9.2. Información de los relojes (time.get_clock_info()):")
for clock_name in ['time', 'monotonic', 'perf_counter', 'process_time']:
    try:
        info = time.get_clock_info(clock_name)
        print(f"  Reloj: {clock_name}")
        print(f"    Ajustable: {info.adjustable}")
        print(f"    Implementación: {info.implementation}")
        print(f"    Monotónico: {info.monotonic}")
        print(f"    Resolución: {info.resolution:.0e} segundos") # Notación científica para resolución
    except Exception as e:
        print(f"  No se pudo obtener información para el reloj {clock_name}: {e}")

try:
    info_thread = time.get_clock_info('thread_time')
    print(f"  Reloj: thread_time")
    print(f"    Ajustable: {info_thread.adjustable}")
    print(f"    Implementación: {info_thread.implementation}")
    print(f"    Monotónico: {info_thread.monotonic}")
    print(f"    Resolución: {info_thread.resolution:.0e} segundos")
except AttributeError:
     print("  Reloj: thread_time no disponible para get_clock_info en este sistema.")
except Exception as e:
    print(f"  No se pudo obtener información para el reloj thread_time: {e}")


print("\n--- Fin de los apuntes del módulo time ---")

# NOTA FINAL:
# Para funcionalidades de tiempo más avanzadas, especialmente aquellas que involucran
# aritmética de fechas, manejo de zonas horarias complejas y parsing más robusto,
# considera usar el módulo `datetime` de la librería estándar de Python, o librerías
# de terceros como `pytz` (para zonas horarias) o `dateutil`.
# El módulo `time` es más de bajo nivel y está más orientado a las funciones de tiempo
# proporcionadas por el sistema operativo subyacente.