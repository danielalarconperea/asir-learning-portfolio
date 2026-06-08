# Explicación Completa del Módulo datetime en Python

# El módulo datetime en Python proporciona clases para trabajar con fechas y horas.
# Es una herramienta fundamental para cualquier aplicación que necesite manipular información temporal.
# Fecha de creación de esta explicación: 16 de mayo de 2025

# ---------------------------------------------------------------------------
# 1. Importaciones Principales
# ---------------------------------------------------------------------------
import datetime  # Importa el módulo principal
# Importaciones específicas para conveniencia y legibilidad:
from datetime import date, time, datetime as dt, timedelta, timezone

print("------ 1. Importaciones Principales Completadas ------\n")

# ---------------------------------------------------------------------------
# 2. Objetos `date` (Fechas)
# ---------------------------------------------------------------------------
# Representan una fecha (año, mes, día) sin información de hora.

print("------ 2. Objetos `date` (Fechas) ------")
# Creación de un objeto date
fecha_actual = date.today()  # Obtiene la fecha actual del sistema
print(f"Fecha actual: {fecha_actual}")

fecha_especifica = date(2024, 12, 25)  # Año, Mes, Día
print(f"Fecha específica (Navidad 2024): {fecha_especifica}")

# Atributos de un objeto date
print(f"Año de fecha_especifica: {fecha_especifica.year}")
print(f"Mes de fecha_especifica: {fecha_especifica.month}")
print(f"Día de fecha_especifica: {fecha_especifica.day}")

# Métodos comunes de date
print(f"Día de la semana (Lunes=0, Domingo=6): {fecha_especifica.weekday()}")
print(f"Día de la semana ISO (Lunes=1, Domingo=7): {fecha_especifica.isoweekday()}")
print(f"Formato ISO (YYYY-MM-DD): {fecha_especifica.isoformat()}")
# isocalendar() devuelve una tupla de 3 elementos: (año ISO, número de semana ISO, día de la semana ISO)
print(f"Calendario ISO (año, semana, día_semana): {fecha_especifica.isocalendar()}")

# Formateo de fechas (strftime - string format time)
# Convierte un objeto date a una cadena de texto con un formato específico.
# %Y: Año con siglo (ej. 2024)
# %m: Mes como número (01-12)
# %d: Día del mes (01-31)
# %A: Nombre completo del día de la semana (ej. Miércoles)
# %B: Nombre completo del mes (ej. Diciembre)
# Para más directivas: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
print(f"Fecha formateada (DD/MM/YYYY): {fecha_especifica.strftime('%d/%m/%Y')}")
print(f"Fecha con nombres textuales: {fecha_especifica.strftime('%A, %d de %B de %Y')}")

# Crear un objeto date a partir de una cadena en formato ISO
fecha_desde_iso = date.fromisoformat("2025-01-30")
print(f"Fecha desde cadena ISO '2025-01-30': {fecha_desde_iso}")
print("\n")

# ---------------------------------------------------------------------------
# 3. Objetos `time` (Horas)
# ---------------------------------------------------------------------------
# Representan una hora (hora, minuto, segundo, microsegundo) sin información de fecha.
# También pueden incluir información de zona horaria (tzinfo).

print("------ 3. Objetos `time` (Horas) ------")
# Creación de un objeto time
hora_especifica = time(14, 30, 15, 500000)  # Hora, Minuto, Segundo, Microsegundo
print(f"Hora específica: {hora_especifica}")

hora_sin_micro = time(9, 15)  # Solo hora y minuto (segundos y microsegundos son 0 por defecto)
print(f"Hora sin microsegundos: {hora_sin_micro}")

# Atributos de un objeto time
print(f"Hora: {hora_especifica.hour}")
print(f"Minuto: {hora_especifica.minute}")
print(f"Segundo: {hora_especifica.second}")
print(f"Microsegundo: {hora_especifica.microsecond}")
print(f"Información de zona horaria (tzinfo): {hora_especifica.tzinfo}")  # Será None si no se especifica

# Creación de un objeto time con zona horaria (offset fijo)
offset_plus_2 = timezone(timedelta(hours=2))
hora_con_tz = time(10, 30, tzinfo=offset_plus_2)
print(f"Hora con zona horaria (+02:00): {hora_con_tz}")
print(f"tzinfo de hora_con_tz: {hora_con_tz.tzinfo}")
print(f"Offset UTC de hora_con_tz: {hora_con_tz.utcoffset()}") # Devuelve el timedelta del offset
print(f"Nombre de la zona horaria (si se provee): {hora_con_tz.tzname()}") # Nombre de la zona horaria

# Métodos comunes de time
# isoformat() tiene un argumento 'timespec' para controlar la precisión
print(f"Formato ISO (HH:MM:SS.ffffff): {hora_especifica.isoformat()}")
print(f"Formato ISO (HH:MM): {hora_especifica.isoformat(timespec='minutes')}")
print(f"Formato ISO con zona horaria: {hora_con_tz.isoformat()}")

# Formateo de horas (strftime)
# %H: Hora (formato 24 horas, 00-23)
# %M: Minuto (00-59)
# %S: Segundo (00-59)
# %p: AM/PM (usualmente con %I)
# %I: Hora (formato 12 horas, 01-12)
print(f"Hora formateada (24h): {hora_especifica.strftime('%H:%M:%S')}")
print(f"Hora formateada (12h con AM/PM): {time(14, 30).strftime('%I:%M %p')}")

# Crear un objeto time a partir de una cadena en formato ISO
hora_desde_iso = time.fromisoformat("16:45:30.123456+01:00")
print(f"Hora desde cadena ISO '16:45:30.123456+01:00': {hora_desde_iso}")
print(f"tzinfo de hora_desde_iso: {hora_desde_iso.tzinfo}")
print("\n")

# ---------------------------------------------------------------------------
# 4. Objetos `datetime` (Fecha y Hora Combinadas)
# ---------------------------------------------------------------------------
# Combinan la información de `date` y `time` en un solo objeto.
# Pueden ser "naive" (ingenuos, sin zona horaria) o "aware" (conscientes, con zona horaria).

print("------ 4. Objetos `datetime` (Fecha y Hora) ------")
# Creación de objetos datetime
# "Naive" (sin información de zona horaria)
ahora_naive = dt.now()  # Fecha y hora actual local (naive, depende de la configuración del sistema)
print(f"Ahora (naive, local): {ahora_naive}")

# dt.utcnow() devuelve un datetime naive representando la hora UTC.
# ¡PRECAUCIÓN! Es naive, lo que puede ser propenso a errores.
# Se recomienda usar dt.now(timezone.utc) para obtener un datetime "aware" en UTC.
utc_ahora_naive_legacy = dt.utcnow()
print(f"Ahora (naive, UTC con dt.utcnow()): {utc_ahora_naive_legacy} - ¡Evitar para UTC aware!")

fecha_hora_especifica_naive = dt(2025, 1, 1, 10, 30, 0, 12345)  # Año, Mes, Día, Hora, Min, Seg, Microseg
print(f"Fecha y hora específicas (naive): {fecha_hora_especifica_naive}")

# "Aware" (con información de zona horaria)
# Para UTC, usar timezone.utc
utc_ahora_aware = dt.now(timezone.utc)  # Fecha y hora actual UTC (aware) - RECOMENDADO para UTC
print(f"Ahora (aware, UTC con timezone.utc): {utc_ahora_aware}")

# Creando una zona horaria simple con offset fijo (ej. UTC-5)
# Para manejo complejo de zonas horarias (DST, etc.), usar librerías como `zoneinfo` (Python 3.9+) o `pytz`.
zona_horaria_menos_5 = timezone(timedelta(hours=-5), name="EST_Test")
fecha_hora_aware_menos_5 = dt.now(zona_horaria_menos_5)
print(f"Ahora (aware, EST_Test -05:00): {fecha_hora_aware_menos_5}")

fecha_hora_especifica_aware = dt(2025, 6, 10, 15, 0, 0, tzinfo=zona_horaria_menos_5)
print(f"Fecha y hora específicas (aware, EST_Test -05:00): {fecha_hora_especifica_aware}")

# Atributos de un objeto datetime (hereda de date y time)
print(f"Año: {utc_ahora_aware.year}, Mes: {utc_ahora_aware.month}, Día: {utc_ahora_aware.day}")
print(f"Hora: {utc_ahora_aware.hour}, Min: {utc_ahora_aware.minute}, Seg: {utc_ahora_aware.second}")
print(f"Microsegundo: {utc_ahora_aware.microsecond}")
print(f"tzinfo: {utc_ahora_aware.tzinfo}")
print(f"Offset UTC: {utc_ahora_aware.utcoffset()}") # Devuelve el timedelta del offset
print(f"Nombre de zona horaria: {utc_ahora_aware.tzname()}") # Nombre proporcionado a tzinfo o por tzinfo

# Métodos comunes de datetime
print(f"Objeto date(): {utc_ahora_aware.date()}") # Extrae la parte de la fecha
print(f"Objeto time(): {utc_ahora_aware.time()}") # Extrae la parte de la hora (sin tzinfo)
print(f"Objeto timetz(): {utc_ahora_aware.timetz()}") # Extrae la parte de la hora (CON tzinfo)
print(f"Día de la semana (Lunes=0): {utc_ahora_aware.weekday()}")
# isoformat() incluye separador 'T' por defecto. Puede incluir offset si es aware.
print(f"Formato ISO: {fecha_hora_especifica_naive.isoformat()}")
print(f"Formato ISO con zona horaria: {utc_ahora_aware.isoformat()}")

# Reemplazar partes de un datetime (replace) - devuelve un nuevo objeto
dt_modificado = utc_ahora_aware.replace(year=2026, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
print(f"Datetime modificado: {dt_modificado}")
# replace() puede usarse para cambiar tzinfo (ej. de naive a aware, o cambiar tz)
dt_naive_a_aware = fecha_hora_especifica_naive.replace(tzinfo=timezone.utc)
print(f"Datetime naive a aware (UTC): {dt_naive_a_aware}")

# Combinar un objeto date y un objeto time para formar un datetime
fecha_obj = date(2025, 7, 4)
hora_obj = time(17, 30, tzinfo=timezone(timedelta(hours=-7), name="PDT_Test"))
fecha_hora_combinada = dt.combine(fecha_obj, hora_obj) # tzinfo se toma del objeto time
print(f"Fecha y hora combinadas: {fecha_hora_combinada}, tz: {fecha_hora_combinada.tzinfo}")
fecha_hora_combinada_naive = dt.combine(fecha_obj, time(17,30)) # Si time es naive, datetime es naive
print(f"Fecha y hora combinadas (naive): {fecha_hora_combinada_naive}")


# Conversión entre zonas horarias (SOLO para objetos datetime "aware")
dt_origen_utc = dt.now(timezone.utc)
print(f"Datetime origen (UTC): {dt_origen_utc}")
# Crear una zona horaria para Tokyo (UTC+9)
tz_tokyo_simple = timezone(timedelta(hours=9), name="JST_Simple")
dt_convertido_tokyo = dt_origen_utc.astimezone(tz_tokyo_simple)
print(f"Datetime convertido a Tokyo (JST_Simple +09:00): {dt_convertido_tokyo}")

# Módulo zoneinfo (Python 3.9+) para manejo robusto de zonas horarias IANA (maneja DST)
try:
    from zoneinfo import ZoneInfo
    dt_madrid_actual = dt.now(ZoneInfo("Europe/Madrid"))
    print(f"Ahora en Madrid (con zoneinfo): {dt_madrid_actual.isoformat()} ({dt_madrid_actual.tzname()})")
    dt_los_angeles = dt_madrid_actual.astimezone(ZoneInfo("America/Los_Angeles"))
    print(f"Convertido a Los Angeles (con zoneinfo): {dt_los_angeles.isoformat()} ({dt_los_angeles.tzname()})")

    # Crear un datetime en una zona específica
    # Para horas ambiguas (cuando el reloj se atrasa por DST) o inexistentes (cuando se adelanta)
    # `fold` ayuda a desambiguar. fold=0 (defecto) es antes del cambio DST, fold=1 es después.
    # Ejemplo: En Madrid, el 27 de octubre de 2024 a las 02:30 AM ocurre dos veces.
    dt_ambiguo_madrid_antes = dt(2024, 10, 27, 2, 30, 0, tzinfo=ZoneInfo("Europe/Madrid"), fold=0)
    dt_ambiguo_madrid_despues = dt(2024, 10, 27, 2, 30, 0, tzinfo=ZoneInfo("Europe/Madrid"), fold=1)
    print(f"Hora ambigua en Madrid (antes DST): {dt_ambiguo_madrid_antes.isoformat()} -> UTC {dt_ambiguo_madrid_antes.astimezone(timezone.utc).time()}")
    print(f"Hora ambigua en Madrid (después DST): {dt_ambiguo_madrid_despues.isoformat()} -> UTC {dt_ambiguo_madrid_despues.astimezone(timezone.utc).time()}")

except ImportError:
    print("El módulo zoneinfo no está disponible (necesita Python 3.9+). Considere usar `pytz` para versiones anteriores.")

# Crear un datetime a partir de una cadena en formato ISO
dt_desde_iso = dt.fromisoformat("2025-02-15T14:30:59.123456+05:30")
print(f"Datetime desde cadena ISO '2025-02-15T14:30:59.123456+05:30': {dt_desde_iso}")
print(f"tzinfo: {dt_desde_iso.tzinfo}, offset: {dt_desde_iso.utcoffset()}")
print("\n")

# ---------------------------------------------------------------------------
# 5. Objetos `timedelta` (Diferencias o Duraciones de Tiempo)
# ---------------------------------------------------------------------------
# Representan una duración, la diferencia entre dos instantes de date, time, o datetime.

print("------ 5. Objetos `timedelta` (Diferencias de Tiempo) ------")
# Creación de un timedelta
delta1 = timedelta(days=10, hours=5, minutes=20, seconds=30, microseconds=100, weeks=2)
print(f"Timedelta 1: {delta1}")

# Atributos de timedelta (internamente solo almacena days, seconds, microseconds)
# Los demás argumentos del constructor se normalizan a estos tres.
print(f"Días en delta1: {delta1.days}")  # Solo la parte de días
print(f"Segundos en delta1: {delta1.seconds}")  # Solo la parte de segundos (0 <= s < 24*3600)
print(f"Microsegundos en delta1: {delta1.microseconds}")  # Solo la parte de microsegundos (0 <= us < 1000000)

# total_seconds() devuelve la duración total expresada en segundos.
print(f"Total de segundos en delta1: {delta1.total_seconds()}")

# Operaciones aritméticas con timedelta
fecha_hora_inicio = dt(2025, 1, 1, 12, 0, 0)
print(f"Fecha y hora de inicio: {fecha_hora_inicio}")

# Sumar un timedelta a un datetime
fecha_hora_futura = fecha_hora_inicio + delta1
print(f"Fecha futura (inicio + delta1): {fecha_hora_futura}")

# Restar un timedelta a un datetime
fecha_hora_pasada = fecha_hora_inicio - delta1
print(f"Fecha pasada (inicio - delta1): {fecha_hora_pasada}")

# Restar dos datetimes devuelve un timedelta
delta2 = fecha_hora_futura - fecha_hora_inicio
print(f"Diferencia calculada (delta2): {delta2}")
print(f"¿delta1 es igual a delta2? {delta1 == delta2}")

# Multiplicación y división de timedeltas por números (enteros o flotantes)
delta_doble = delta1 * 2
print(f"Delta doble (delta1 * 2): {delta_doble}")
delta_mitad = delta1 / 2
print(f"Delta mitad (delta1 / 2): {delta_mitad}")

# También se puede usar con objetos date (la parte de tiempo del timedelta se usa para calcular días)
fecha_simple_inicio = date(2025, 3, 1)
dias_a_sumar = timedelta(days=7, hours=48) # 48 horas son 2 días adicionales
fecha_simple_futura = fecha_simple_inicio + dias_a_sumar
print(f"Fecha simple futura (inicio + 7d 48h = 9d): {fecha_simple_futura}")

# La resta de dos objetos date también devuelve un timedelta
diferencia_fechas = date(2025, 1, 15) - date(2025, 1, 1)
print(f"Diferencia entre dos fechas: {diferencia_fechas}")
print("\n")

# ---------------------------------------------------------------------------
# 6. Formateo y Parseo (strftime y strptime)
# ---------------------------------------------------------------------------
# strftime: Convierte un objeto datetime/date/time a una cadena de texto con formato.
# strptime: Convierte una cadena de texto (parsea) a un objeto datetime.

print("------ 6. Formateo y Parseo (strftime y strptime) ------")
# strftime (string format time - ya visto en ejemplos anteriores)
ahora = dt.now()
cadena_formateada = ahora.strftime("Hoy es %A, %d de %B de %Y. Son las %I:%M:%S %p.") # Formato personalizado
print(f"strftime - Fecha y hora formateada: {cadena_formateada}")

# strptime (string parse time)
# Convierte una cadena a un objeto datetime según un formato específico.
cadena_fecha_hora = "15/07/2025 18:45:30"
formato_entrada = "%d/%m/%Y %H:%M:%S" # Debe coincidir EXACTAMENTE con la cadena
objeto_datetime_parseado = dt.strptime(cadena_fecha_hora, formato_entrada)
print(f"strptime - Objeto datetime desde cadena '{cadena_fecha_hora}': {objeto_datetime_parseado}")
print(f"Tipo del objeto parseado: {type(objeto_datetime_parseado)}")

# Si la cadena parseada no tiene información de zona horaria, el datetime resultante es naive.
# Para parsear cadenas con información de zona horaria:
# 1. Usar dt.fromisoformat() para cadenas en formato ISO 8601 (maneja offsets).
# 2. Usar strptime con la directiva %z para offsets UTC (ej. +0200).
# 3. Para nombres de zona (ej. "CEST"), strptime con %Z es dependiente de la plataforma y locale,
#    y a menudo no es fiable. Usar zoneinfo/pytz después de parsear la parte naive es más robusto.

cadena_con_offset_z = "2025-08-20 10:30:00-0400" # Offset -04:00
formato_con_z = "%Y-%m-%d %H:%M:%S%z"
dt_parseado_con_z = dt.strptime(cadena_con_offset_z, formato_con_z)
print(f"strptime con %z desde '{cadena_con_offset_z}': {dt_parseado_con_z}")
print(f"tzinfo del parseado: {dt_parseado_con_z.tzinfo}, offset: {dt_parseado_con_z.utcoffset()}")

# Lista de directivas de formato comunes para strftime y strptime:
# %Y: Año con siglo (2025)          %y: Año sin siglo (25)
# %m: Mes como número (01-12)       %B: Nombre completo del mes (Julio)    %b: Nombre abreviado mes (Jul)
# %d: Día del mes (01-31)           %A: Nombre completo día semana (Martes) %a: Nombre abrev. día (Mar)
# %H: Hora (24h, 00-23)             %I: Hora (12h, 01-12)
# %M: Minuto (00-59)                %S: Segundo (00-59)
# %f: Microsegundo (000000-999999)
# %p: AM/PM (en el locale actual)
# %z: Offset UTC en formato ±HHMM[SS[.ffffff]] (ej. +0100, -0400). Si es naive, string vacío.
# %Z: Nombre de la zona horaria (puede ser ambiguo, ej. EST, CEST). Si es naive, string vacío.
# %j: Día del año (001-366)
# %U: Número de semana del año (Domingo como primer día, 00-53)
# %W: Número de semana del año (Lunes como primer día, 00-53)
# %c: Representación local de fecha y hora (ej. 'Tue Aug 20 10:30:00 2025')
# %x: Representación local de fecha (ej. '08/20/25')
# %X: Representación local de hora (ej. '10:30:00')
# Para la lista completa: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes
print("\n")

# ---------------------------------------------------------------------------
# 7. Timestamps (Sellos de Tiempo POSIX)
# ---------------------------------------------------------------------------
# Un timestamp POSIX es el número de segundos transcurridos desde el "Epoch"
# (1 de enero de 1970, 00:00:00 UTC).

print("------ 7. Timestamps (Sellos de Tiempo POSIX) ------")
# Obtener el timestamp de un objeto datetime
ahora_local_naive = dt.now()  # Naive datetime (zona horaria local del sistema)
timestamp_naive = ahora_local_naive.timestamp()
print(f"Timestamp de ahora (naive, local '{ahora_local_naive}'): {timestamp_naive}")
# Para datetimes naive, .timestamp() usa la zona horaria local del sistema para la conversión a UTC.

ahora_utc_aware = dt.now(timezone.utc)  # Aware datetime en UTC
timestamp_aware_utc = ahora_utc_aware.timestamp()
print(f"Timestamp de ahora (aware, UTC '{ahora_utc_aware}'): {timestamp_aware_utc}")
# Para datetimes aware, .timestamp() calcula correctamente el timestamp UTC.

# Crear un objeto datetime a partir de un timestamp
ts_ejemplo = 1735689600.0  # Corresponde a 2025-01-01 00:00:00 UTC
# dt.fromtimestamp(ts) crea un datetime NAIVE en la zona horaria LOCAL del sistema.
dt_desde_ts_local = dt.fromtimestamp(ts_ejemplo)
print(f"Datetime desde timestamp {ts_ejemplo} (local, naive): {dt_desde_ts_local}")

# dt.fromtimestamp(ts, tz=timezone_obj) crea un datetime AWARE en la zona horaria especificada.
dt_desde_ts_utc_aware = dt.fromtimestamp(ts_ejemplo, tz=timezone.utc)
print(f"Datetime desde timestamp {ts_ejemplo} (UTC, aware): {dt_desde_ts_utc_aware}")

try:
    from zoneinfo import ZoneInfo
    tz_madrid = ZoneInfo("Europe/Madrid")
    dt_desde_ts_madrid_aware = dt.fromtimestamp(ts_ejemplo, tz=tz_madrid)
    print(f"Datetime desde timestamp {ts_ejemplo} (Madrid, aware): {dt_desde_ts_madrid_aware}")
except ImportError:
    pass # zoneinfo no disponible

# dt.utcfromtimestamp(ts) crea un datetime NAIVE que representa la hora UTC. ¡PRECAUCIÓN: es naive!
dt_desde_ts_utc_naive_legacy = dt.utcfromtimestamp(ts_ejemplo)
print(f"Datetime desde ts {ts_ejemplo} (UTC, naive con utcfromtimestamp()): {dt_desde_ts_utc_naive_legacy} - ¡Naive!")
print("\n")

# ---------------------------------------------------------------------------
# 8. Comparación de Objetos Datetime, Date y Time
# ---------------------------------------------------------------------------
# Los objetos date, time y datetime se pueden comparar usando operadores estándar (<, >, <=, >=, ==, !=).

print("------ 8. Comparación de Objetos Datetime, Date y Time ------")
dt1 = dt(2025, 1, 1, 10, 0, 0)
dt2 = dt(2025, 1, 1, 12, 0, 0)
dt3 = dt(2025, 1, 1, 10, 0, 0)

print(f"dt1: {dt1}, dt2: {dt2}, dt3: {dt3}")
print(f"dt1 < dt2: {dt1 < dt2}")    # True, dt1 es anterior a dt2
print(f"dt1 > dt2: {dt1 > dt2}")    # False
print(f"dt1 == dt3: {dt1 == dt3}")  # True, dt1 y dt3 representan el mismo instante
print(f"dt1 != dt2: {dt1 != dt2}")  # True

# Comparación entre datetimes naive y aware:
# En Python, comparar directamente un datetime naive con uno aware produce un TypeError.
# Se deben convertir ambos a un tipo común (ambos naive o ambos aware en la misma zona, usualmente UTC) antes de comparar.

dt_naive_local = dt(2025, 5, 15, 12, 0, 0) # Asumamos que es hora local, ej. Madrid (UTC+2 en verano)
dt_aware_utc = dt(2025, 5, 15, 10, 0, 0, tzinfo=timezone.utc) # 10:00 UTC

# print(dt_naive_local == dt_aware_utc) # Esto daría TypeError

# Para comparar correctamente, si sabemos que dt_naive_local es de Madrid (UTC+2 en ese momento hipotético):
# Opción 1: Convertir el aware a la zona local (si conocemos la zona del naive) y luego a naive.
# O, mejor, convertir el naive a aware.
# Si asumimos que dt_naive_local es UTC+2:
# dt_naive_local_como_aware = dt_naive_local.replace(tzinfo=timezone(timedelta(hours=2)))
# print(f"Comparando {dt_naive_local_como_aware} con {dt_aware_utc}: {dt_naive_local_como_aware == dt_aware_utc}") # True

# Es más seguro trabajar siempre con datetimes aware, preferiblemente convirtiéndolos a UTC para la comparación.
# Si dt_naive_local es la hora en Madrid (UTC+2), entonces 12:00 Madrid = 10:00 UTC.
# dt_naive_local_en_utc = dt_naive_local - timedelta(hours=2) # Conversión manual a UTC (si sabemos el offset)
# dt_naive_local_en_utc_aware = dt_naive_local_en_utc.replace(tzinfo=timezone.utc)
# print(f"Comparando {dt_naive_local_en_utc_aware} con {dt_aware_utc}: {dt_naive_local_en_utc_aware == dt_aware_utc}")

# La mejor práctica es hacer los datetimes "aware" lo antes posible y estandarizar a UTC para lógica interna y comparaciones.
try:
    from zoneinfo import ZoneInfo
    tz_madrid = ZoneInfo("Europe/Madrid")
    # Supongamos que dt_naive_local representa un tiempo en Madrid.
    # Lo hacemos "aware" localizándolo en Madrid.
    dt_local_aware_madrid = tz_madrid.localize(dt_naive_local) # ¡Ojo! Pytz usa .localize(), zoneinfo no lo tiene directamente.
                                                               # Para zoneinfo, es mejor crear con tzinfo desde el inicio:
    dt_local_aware_madrid = dt(dt_naive_local.year, dt_naive_local.month, dt_naive_local.day,
                               dt_naive_local.hour, dt_naive_local.minute, dt_naive_local.second,
                               tzinfo=tz_madrid)
    print(f"Comparando {dt_local_aware_madrid.astimezone(timezone.utc)} con {dt_aware_utc}: {dt_local_aware_madrid.astimezone(timezone.utc) == dt_aware_utc}") # True
except Exception as e:
    print(f"Error en comparación con zoneinfo: {e}. Esto suele requerir manejo cuidadoso de 'localize'.")


# Comparación de objetos date
d1 = date(2025, 1, 1)
d2 = date(2025, 1, 10)
print(f"Comparación de fechas: d1 ({d1}) < d2 ({d2}) es {d1 < d2}") # True

# Comparación de objetos time
t1 = time(10, 0, 0)
t2 = time(11, 0, 0)
t3 = time(10, 0, 0, tzinfo=timezone.utc)
t4 = time(11, 0, 0, tzinfo=timezone(timedelta(hours=1))) # 11:00+01:00 es 10:00 UTC

print(f"Comparación de horas (naive): t1 ({t1}) < t2 ({t2}) es {t1 < t2}") # True
# Comparar time naive con time aware también da TypeError.
# print(t1 == t3) # TypeError
# Si ambos son aware, se comparan sus equivalentes UTC si los offsets son diferentes.
print(f"Comparación de horas (aware): t3 ({t3}) == t4 ({t4}) es {t3 == t4}") # True, ambos son 10:00 UTC
print("\n")


# ---------------------------------------------------------------------------
# 9. Constantes Útiles del Módulo Datetime
# ---------------------------------------------------------------------------
print("------ 9. Constantes Útiles del Módulo Datetime ------")
print(f"Fecha mínima soportada (date.min): {date.min}")
print(f"Fecha máxima soportada (date.max): {date.max}")
print(f"Datetime mínimo soportado (dt.min): {dt.min}")  # Naive
print(f"Datetime máximo soportado (dt.max): {dt.max}")  # Naive
print(f"Time mínimo soportado (time.min): {time.min}")  # Naive
print(f"Time máximo soportado (time.max): {time.max}")  # Naive
# Nota: dt.min y dt.max no pueden tener tzinfo. Si se necesita un aware min/max, se crea:
# dt_min_aware_utc = dt.min.replace(tzinfo=timezone.utc)

print(f"Resolución de timedelta (timedelta.resolution): {timedelta.resolution}") # El menor timedelta > 0 (1 microsegundo)
print(f"Timedelta mínimo (timedelta.min): {timedelta.min}")
print(f"Timedelta máximo (timedelta.max): {timedelta.max}")

print(f"Epoch (referencia para timestamps, naive): {dt.fromtimestamp(0)}")
print(f"Epoch (referencia para timestamps, aware UTC): {dt.fromtimestamp(0, tz=timezone.utc)}")
print("\n")

# ---------------------------------------------------------------------------
# Resumen de Buenas Prácticas y Consideraciones sobre Zonas Horarias:
# ---------------------------------------------------------------------------
# 1. Claridad Naive vs. Aware: Siempre sea consciente si un objeto datetime es naive o aware.
#    - Naive: No tiene `tzinfo`. Se asume local o UTC según el contexto (peligroso).
#    - Aware: Tiene `tzinfo` no None. Representa un instante inequívoco.

# 2. UTC como Estándar Interno: Para aplicaciones robustas, especialmente con múltiples zonas horarias:
#    - Almacene todas las fechas y horas en UTC (aware).
#    - Realice todos los cálculos y lógica de negocio en UTC.

# 3. Conversión para Visualización: Convierta de UTC a la zona horaria local del usuario
#    SOLO en el punto de visualización (frontend, reportes).

# 4. Obtener Hora Actual:
#    - Para UTC actual "aware": `datetime.now(timezone.utc)`
#    - Para hora local actual "aware" (con zoneinfo/pytz): `datetime.now(ZoneInfo("Europe/Madrid"))`
#    - Evitar `datetime.utcnow()` (naive) y `datetime.now()` (naive local) si se necesita robustez.

# 5. Manejo de Zonas Horarias Complejas (DST):
#    - Python 3.9+: Usar el módulo `zoneinfo` (distribuido con Python, usa la base de datos IANA).
#      Ej: `from zoneinfo import ZoneInfo`, `tz = ZoneInfo("America/New_York")`.
#    - Python < 3.9: Usar la librería externa `pytz`.
#      Ej: `import pytz`, `tz = pytz.timezone("America/New_York")`.
#    - `timezone(timedelta(hours=X))` es solo para offsets fijos, no maneja DST.

# 6. Parseo de Cadenas:
#    - `datetime.fromisoformat()`: Ideal para cadenas en formato ISO 8601 (maneja offsets).
#    - `datetime.strptime()`: Para formatos personalizados. Cuidado con `%Z` (nombre de zona),
#      es mejor parsear como naive y luego localizar con `zoneinfo`/`pytz` si la zona es compleja.
#      `%z` (offset) es más fiable para parsear offsets numéricos.

# 7. Comparaciones:
#    - Asegúrese que ambos datetimes son del mismo tipo (ambos naive o ambos aware).
#    - Si son aware, es mejor convertirlos a una zona común (usualmente UTC) antes de comparar.
#    - Comparar naive con aware directamente resulta en `TypeError`.

# 8. `fold` para Tiempos Ambiguos/Inexistentes:
#    - Cuando un reloj se atrasa (fin de DST), una hora local puede ocurrir dos veces.
#      El atributo `fold` (0 o 1) en objetos `datetime` (Python 3.6+) y `time` ayuda a desambiguar.
#      `fold=0` es la primera ocurrencia, `fold=1` es la segunda.
#    - Al construir datetimes en zonas con DST, o al cruzar cambios DST, `fold` es relevante.
#      Librerías como `zoneinfo` lo manejan al localizar o convertir.

# ---------------------------------------------------------------------------

print("------ Fin de la explicación completa del módulo datetime ------")