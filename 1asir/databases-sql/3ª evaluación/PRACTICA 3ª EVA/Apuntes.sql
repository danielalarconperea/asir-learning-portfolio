-- APUNTES SQL PARA PRÁCTICA 3 - DESDE CERO

-- -----------------------------------------------------------------------------
-- CONCEPTOS BÁSICOS: SELECT, FROM, WHERE
-- -----------------------------------------------------------------------------

-- La sentencia fundamental en SQL para consultar datos es SELECT.
-- Indica qué columnas (campos) quieres ver.
-- FROM indica de qué tabla(s) quieres obtener los datos.
-- WHERE filtra las filas (registros) que cumplen una condición.

-- Ejemplo Básico: Ver todos los datos de la tabla 'aviones'.
SELECT * -- El asterisco (*) significa "todas las columnas"
FROM aviones;

-- Ejemplo: Ver solo el tipo y la longitud de los aviones.
SELECT tipo, longitud
FROM aviones;

-- Ejemplo: Ver los aviones cuya longitud sea mayor que 50 metros.
SELECT tipo, longitud, envergadura
FROM aviones
WHERE longitud > 50; -- Condición de filtrado

-- Operadores comunes en WHERE:
-- =  : Igual a
-- >  : Mayor que
-- <  : Menor que
-- >= : Mayor o igual que
-- <= : Menor o igual que
-- != o <> : Distinto de
-- LIKE : Para buscar patrones en texto (ver más abajo)
-- BETWEEN : Para comprobar si un valor está en un rango (ej: BETWEEN 10 AND 20)
-- IN : Para comprobar si un valor está en una lista (ej: IN ('MAD', 'BCN', 'SVQ'))
-- IS NULL : Para comprobar si un valor es nulo (no tiene valor)
-- IS NOT NULL : Para comprobar si un valor NO es nulo

-- Combinar condiciones con AND (se deben cumplir ambas) y OR (se debe cumplir al menos una):
-- Ejemplo: Aviones con longitud > 50 Y envergadura > 40
SELECT tipo, longitud, envergadura
FROM aviones
WHERE longitud > 50 AND envergadura > 40;

-- Ejemplo: Vuelos con origen en Madrid O destino en Madrid
SELECT num_vuelo, origen, destino
FROM vuelos
WHERE origen = 'MADRID' OR destino = 'MADRID'; -- [cite: 1] (Ej. 6 requiere esta lógica)

-- Uso de LIKE para patrones:
-- '%' representa cualquier secuencia de cero o más caracteres.
-- '_' representa un único carácter cualquiera.
-- Ejemplo: Ciudades que empiezan por 'M' [cite: 3] (Ej. 1 requiere esta lógica)
SELECT localidad
FROM aeropuertos -- O desde la tabla vuelos, columna origen/destino
WHERE localidad LIKE 'M%';

-- Ejemplo: Tipos de avión que contienen un '7'
SELECT tipo
FROM aviones
WHERE tipo LIKE '%7%';

-- -----------------------------------------------------------------------------
-- FUNCIONES ÚTILES Y ALIAS
-- -----------------------------------------------------------------------------

-- Alias de Columnas: Para dar nombres más descriptivos a las columnas resultantes,
-- especialmente si son calculadas. Se usa la palabra clave AS.
SELECT
    tipo,
    envergadura * 2 AS doble_envergadura, -- [cite: 3] (Ej. 1)
    longitud * longitud AS longitud_cuadrada -- [cite: 3] (Ej. 1)
FROM aviones;

-- Alias de Tablas: Útil en JOINs (ver más adelante) para acortar los nombres.
SELECT a.tipo, v.num_vuelo
FROM aviones a, vuelos v -- 'a' es alias de aviones, 'v' de vuelos
WHERE a.tipo = v.tipo_avion; -- Necesitamos prefijar columnas con el alias si hay ambigüedad

-- DISTINCT: Para eliminar filas duplicadas en el resultado.
SELECT DISTINCT origen -- Muestra cada origen una sola vez
FROM vuelos;

-- Funciones de Cadena:
-- LEFT(cadena, n): Devuelve los primeros 'n' caracteres de la 'cadena'. [cite: 10] (Ej. 2, 3, 4)
SELECT LEFT(origen, 3) AS primeras_3_letras_origen
FROM vuelos;

-- Funciones Matemáticas:
-- +, -, *, / : Operaciones aritméticas básicas.
SELECT longitud, longitud / 2 AS mitad_longitud
FROM aviones;

-- -----------------------------------------------------------------------------
-- ORDENACIÓN DE RESULTADOS: ORDER BY
-- -----------------------------------------------------------------------------

-- ORDER BY ordena las filas del resultado según una o más columnas.
-- ASC: Orden ascendente (por defecto).
-- DESC: Orden descendente.

-- Ejemplo: Aviones ordenados por longitud, de menor a mayor.
SELECT tipo, longitud
FROM aviones
ORDER BY longitud ASC; -- ASC es opcional

-- Ejemplo: Vuelos ordenados por destino alfabéticamente. [cite: 10] (Ej. 2)
SELECT num_vuelo, origen, destino
FROM vuelos
ORDER BY destino;

-- Ejemplo: Aviones ordenados por doble envergadura, de mayor a menor. [cite: 3] (Ej. 1)
-- Se puede ordenar por el alias o por la posición de la columna (¡cuidado si cambia el SELECT!).
SELECT tipo, envergadura * 2 AS doble_envergadura
FROM aviones
ORDER BY doble_envergadura DESC;
-- Alternativa por posición (menos recomendable): ORDER BY 2 DESC;

-- -----------------------------------------------------------------------------
-- FUNCIONES DE AGREGACIÓN: AVG, COUNT, MAX, MIN, SUM
-- -----------------------------------------------------------------------------

-- Estas funciones realizan cálculos sobre un conjunto de filas y devuelven un único valor.
-- AVG(columna): Calcula la media de los valores de la columna.
-- COUNT(columna): Cuenta el número de filas no nulas en la columna.
-- COUNT(*): Cuenta el número total de filas.
-- COUNT(DISTINCT columna): Cuenta el número de valores distintos no nulos.
-- MAX(columna): Devuelve el valor máximo de la columna.
-- MIN(columna): Devuelve el valor mínimo de la columna.
-- SUM(columna): Suma los valores de la columna.

-- Ejemplo: Longitud media de todos los aviones. [cite: 3] (Usado en Ej. 1, 2, 4, 7, 8, etc.)
SELECT AVG(longitud) AS longitud_media FROM aviones;

-- Ejemplo: Máxima envergadura. [cite: 10] (Usado en Ej. 2, 6)
SELECT MAX(envergadura) AS max_envergadura FROM aviones;

-- Ejemplo: Número total de vuelos.
SELECT COUNT(*) AS total_vuelos FROM vuelos;

-- Ejemplo: Número de orígenes distintos. [cite: 37] (Ej. 10)
SELECT COUNT(DISTINCT origen) AS num_origenes_distintos FROM vuelos;

-- Ejemplo: Suma total de plazas reservadas para un vuelo específico. [cite: 34] (Ej. 9, 20)
SELECT SUM(plazas) AS total_plazas_IB0103
FROM reservas
WHERE num_vuelo = 'IB0103';

-- -----------------------------------------------------------------------------
-- AGRUPACIÓN DE DATOS: GROUP BY
-- -----------------------------------------------------------------------------

-- GROUP BY se usa junto con funciones de agregación para agrupar filas que tienen
-- el mismo valor en una o más columnas y aplicar la función a cada grupo.
-- Las columnas en el SELECT deben ser o bien funciones de agregación o bien
-- columnas incluidas en el GROUP BY.

-- Ejemplo: Distancia máxima recorrida hacia cada destino. [cite: 28] (Ej. 7)
SELECT destino, MAX(distancia) AS max_distancia_destino
FROM vuelos
GROUP BY destino -- Agrupa por cada valor único de 'destino'
ORDER BY destino;

-- Ejemplo: Distancia mínima desde cada origen. [cite: 32] (Ej. 8)
SELECT origen, MIN(distancia) AS min_distancia_origen
FROM vuelos
GROUP BY origen
ORDER BY origen;

-- Ejemplo: Total de plazas reservadas por número de vuelo. [cite: 34] (Ej. 9)
SELECT num_vuelo, SUM(plazas) AS total_plazas
FROM reservas
GROUP BY num_vuelo
ORDER BY num_vuelo;

-- Ejemplo: Número de destinos distintos desde cada origen. [cite: 37] (Ej. 10)
SELECT origen, COUNT(DISTINCT destino) AS num_destinos
FROM vuelos
GROUP BY origen
ORDER BY num_destinos DESC;

-- -----------------------------------------------------------------------------
-- FILTRADO DE GRUPOS: HAVING
-- -----------------------------------------------------------------------------

-- HAVING se usa para filtrar grupos DESPUÉS de que se hayan formado con GROUP BY.
-- WHERE filtra filas ANTES de la agrupación.
-- HAVING filtra grupos BASADO en el resultado de las funciones de agregación.

-- Ejemplo: Orígenes desde los que salen más de 3 tipos de aviones distintos. [cite: 41] (Ej. 11)
SELECT origen, COUNT(DISTINCT tipo_avion) AS num_tipos_avion
FROM vuelos
GROUP BY origen
HAVING COUNT(DISTINCT tipo_avion) > 3 -- Filtra los grupos cuyo conteo sea > 3
ORDER BY num_tipos_avion DESC;

-- Ejemplo: Vuelos con más de 100 plazas reservadas en total. [cite: 53] (Lógica similar a Ej. 13)
SELECT num_vuelo, SUM(plazas) AS total_plazas
FROM reservas
GROUP BY num_vuelo
HAVING SUM(plazas) > 100;

-- -----------------------------------------------------------------------------
-- CONSULTAS MULTITABLA: OBTENER DATOS RELACIONADOS
-- -----------------------------------------------------------------------------

-- Muy a menudo, la información que necesitas está repartida en varias tablas
-- relacionadas (por ejemplo, 'vuelos' tiene 'tipo_avion', pero los detalles
-- de ese avión están en la tabla 'aviones'). Hay varias formas de combinar datos.

-- MÉTODO 1: SUBCONSULTAS (Consultas Anidadas)
-- Una subconsulta es una consulta SELECT dentro de otra consulta SQL.
-- Puede aparecer en la cláusula WHERE, SELECT, FROM o HAVING.

-- Subconsulta en WHERE con Operadores de Comparación (=, >, <, etc.):
-- La subconsulta debe devolver un ÚNICO valor (escalar).
-- Ejemplo: Aviones con longitud menor que la media. [cite: 3] (Ej. 1)
SELECT tipo, longitud
FROM aviones
WHERE longitud < (SELECT AVG(longitud) FROM aviones); -- Subconsulta escalar

-- Subconsulta en WHERE con IN / NOT IN:
-- La subconsulta devuelve una LISTA de valores. La condición principal comprueba
-- si el valor de la columna está (o no está) en esa lista.
-- Ejemplo: Tipos de avión que realizan vuelos desde/hacia Madrid. [cite: 3] (Ej. 1, 6)
SELECT tipo, descripcion
FROM aviones
WHERE tipo IN (SELECT DISTINCT tipo_avion FROM vuelos WHERE origen = 'MADRID' OR destino = 'MADRID');

-- Ejemplo: Aviones que NUNCA han pasado por Barcelona. [cite: 20] (Ej. 5)
SELECT *
FROM aviones
WHERE tipo NOT IN (SELECT DISTINCT tipo_avion FROM vuelos WHERE origen = 'BARCELONA' OR destino = 'BARCELONA');

-- Subconsultas Correlacionadas:
-- La subconsulta interna hace referencia a una columna de la tabla externa.
-- La subconsulta se ejecuta UNA VEZ POR CADA FILA de la consulta externa.
-- Suelen ser menos eficientes que los JOINs pero son potentes.
-- Se usan mucho con EXISTS (ver más abajo).
-- Ejemplo: Vuelos con distancia mayor que la media de SU compañía (requiere info de compañía). [cite: 64] (Ej. 18)
-- (Este ejemplo es complejo porque necesita obtener la compañía primero, ver solución Ej. 18)
-- SELECT v1.*
-- FROM vuelos v1
-- WHERE v1.distancia > (SELECT AVG(v2.distancia) FROM vuelos v2 WHERE v2.compania = v1.compania); -- ¡OJO! v1.compania referenciada dentro


-- MÉTODO 2: JOIN (Combinación de Tablas)
-- Permite combinar filas de dos o más tablas basándose en una columna relacionada entre ellas.

-- Sintaxis Antigua (implícita con coma y condición en WHERE):
-- Funciona como un INNER JOIN por defecto. Menos legible y propenso a errores si olvidas la condición.
-- Ejemplo: Obtener tipo de avión y número de vuelo.
SELECT a.tipo, v.num_vuelo
FROM aviones a, vuelos v -- Lista de tablas separadas por comas
WHERE a.tipo = v.tipo_avion; -- Condición de unión en el WHERE

-- Sintaxis Moderna (explícita con JOIN): ¡Recomendada!
-- INNER JOIN: Devuelve solo las filas donde hay coincidencias en AMBAS tablas según la condición ON.
--             Es el tipo de JOIN más común.
-- Ejemplo: Obtener tipo de avión y número de vuelo.
SELECT a.tipo, v.num_vuelo
FROM aviones a
INNER JOIN vuelos v ON a.tipo = v.tipo_avion; -- Condición de unión explícita con ON

-- Ejemplo: Vuelos con aviones de longitud > media y envergadura < 2/3 max. [cite: 10] (Ej. 2)
SELECT LEFT(v.origen, 3), LEFT(v.destino, 3)
FROM vuelos v
INNER JOIN aviones a ON v.tipo_avion = a.tipo -- Une vuelos y aviones
WHERE a.longitud > (SELECT AVG(longitud) FROM aviones) -- Condición sobre tabla aviones
AND a.envergadura < (SELECT MAX(envergadura)*2/3 FROM aviones); -- Otra condición sobre aviones

-- LEFT JOIN (o LEFT OUTER JOIN): Devuelve TODAS las filas de la tabla IZQUIERDA (la primera mencionada)
--         y las filas coincidentes de la tabla DERECHA. Si no hay coincidencia en la derecha,
--         las columnas de la derecha tendrán valor NULL.
-- Útil para encontrar filas en una tabla que NO tienen correspondencia en otra.
-- Ejemplo: Aviones que NUNCA han volado (no están en 'vuelos').
SELECT a.*
FROM aviones a
LEFT JOIN vuelos v ON a.tipo = v.tipo_avion
WHERE v.num_vuelo IS NULL; -- Si v.num_vuelo es NULL, no hubo coincidencia en vuelos

-- Ejemplo: Aviones que nunca han pasado por Barcelona (usando LEFT JOIN). [cite: 20] (Ej. 5 - Alternativa)
SELECT a.*
FROM aviones a
LEFT JOIN vuelos v ON a.tipo = v.tipo_avion AND (v.origen = 'BARCELONA' OR v.destino = 'BARCELONA') -- Condición de filtro en el ON
WHERE v.num_vuelo IS NULL; -- Busca los aviones que no tuvieron match con vuelos a/desde BCN

-- RIGHT JOIN (o RIGHT OUTER JOIN): Similar a LEFT JOIN, pero devuelve todas las filas de la tabla DERECHA.
-- FULL OUTER JOIN: Devuelve todas las filas de AMBAS tablas. Si no hay match, rellena con NULL. (No todos los SGBD lo soportan igual).

-- JOIN de Múltiples Tablas: Se pueden encadenar JOINs.
-- Ejemplo: Obtener número de parte, origen del vuelo y descripción del avión.
SELECT p.num_parte, v.origen, a.descripcion
FROM partes p
INNER JOIN vuelos v ON p.num_vuelo = v.num_vuelo -- Une partes y vuelos
INNER JOIN aviones a ON v.tipo_avion = a.tipo;   -- Une el resultado anterior con aviones


-- MÉTODO 3: EXISTS / NOT EXISTS
-- Se usa en la cláusula WHERE para comprobar si una subconsulta devuelve ALGUNA fila.
-- EXISTS es VERDADERO si la subconsulta devuelve al menos una fila.
-- NOT EXISTS es VERDADERO si la subconsulta NO devuelve ninguna fila.
-- Generalmente se usa con subconsultas correlacionadas. Suele ser más eficiente que IN
-- cuando la subconsulta devuelve muchas filas, porque se detiene en cuanto encuentra la primera.

-- Ejemplo: Aviones que SÍ han realizado algún vuelo (existen en la tabla vuelos).
SELECT tipo, descripcion
FROM aviones a
WHERE EXISTS (SELECT 1 FROM vuelos v WHERE v.tipo_avion = a.tipo); -- Comprueba si existe un vuelo para este avión 'a'

-- Ejemplo: Aviones que realizan vuelos desde/hacia Madrid. [cite: 6] (Ej. 1, 6 - Alternativa EXISTS)
SELECT tipo, longitud*longitud AS longitud_cuadrada
FROM aviones a
WHERE EXISTS (SELECT 1 FROM vuelos v WHERE v.tipo_avion = a.tipo AND (v.origen = 'MADRID' OR v.destino = 'MADRID'));

-- Ejemplo: Aviones que NUNCA han pasado por Barcelona. [cite: 20] (Ej. 5 - Alternativa NOT EXISTS)
SELECT *
FROM aviones a
WHERE NOT EXISTS (SELECT 1 FROM vuelos v WHERE v.tipo_avion = a.tipo AND (v.origen = 'BARCELONA' OR v.destino = 'BARCELONA'));


-- -----------------------------------------------------------------------------
-- OPERADORES DE CONJUNTO: UNION / UNION ALL
-- -----------------------------------------------------------------------------

-- Combinan los resultados de dos o más consultas SELECT en un único conjunto de resultados.
-- Las consultas deben tener el MISMO NÚMERO de columnas y tipos de datos COMPATIBLES.

-- UNION: Combina los resultados y ELIMINA las filas duplicadas.
-- Ejemplo: Lista única de todas las ciudades (origen o destino). [cite: 84] (Ej. 22)
SELECT origen AS ciudad FROM vuelos
UNION
SELECT destino AS ciudad FROM vuelos
ORDER BY ciudad;

-- UNION ALL: Combina los resultados e INCLUYE TODAS las filas, incluso duplicadas. Más rápido que UNION.
-- Ejemplo: Lista de todas las ciudades origen Y todas las ciudades destino (pueden repetirse). [cite: 87] (Ej. 23)
SELECT origen AS ciudad FROM vuelos
UNION ALL
SELECT destino AS ciudad FROM vuelos
ORDER BY ciudad;

-- Ejemplo: Fechas con menor y mayor consumo. [cite: 101] (Ej. 26)
SELECT fecha, MIN(comb_consumido) AS consumo FROM partes GROUP BY fecha
UNION ALL
SELECT fecha, MAX(comb_consumido) AS consumo FROM partes GROUP BY fecha
ORDER BY fecha, consumo;

-- -----------------------------------------------------------------------------
-- OTROS CONCEPTOS
-- -----------------------------------------------------------------------------

-- COALESCE(valor1, valor2, ...): Devuelve el primer valor NO NULO de la lista.
-- Útil para sustituir NULLs por un valor por defecto (ej: 0). [cite: 95] (Usado en Ej. 25)
-- SELECT COALESCE(SUM(plazas), 0) ... -- Si la suma es NULL (no hay reservas), devuelve 0.

-- WITH (Common Table Expressions - CTEs): Permite definir consultas temporales
-- con nombre que puedes usar dentro de una consulta mayor. Ayuda a organizar
-- consultas complejas. [cite: 95] (Usado en Ej. 25)
-- WITH ciudades_origen AS (
--    SELECT origen, COUNT(*) AS num_salen FROM vuelos GROUP BY origen
-- ),
-- ciudades_destino AS (
--    SELECT destino, COUNT(*) AS num_llegan FROM vuelos GROUP BY destino
-- )
-- SELECT ... FROM ciudades_origen co JOIN ciudades_destino cd ON ...

-- -----------------------------------------------------------------------------
-- CÓMO ABORDAR LOS EJERCICIOS DE LA PRÁCTICA 3
-- -----------------------------------------------------------------------------

-- 1. Lee atentamente el enunciado: ¿Qué te piden exactamente? ¿Qué tablas contienen esa información? ¿Cómo están relacionadas?
-- 2. Identifica las condiciones de filtrado: ¿Hay condiciones sobre columnas simples (WHERE)? ¿Sobre agregaciones (HAVING)?
-- 3. Identifica si necesitas datos de una o varias tablas:
--    - Si es una tabla: SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY.
--    - Si son varias tablas: Piensa cómo combinarlas.
-- 4. Piensa en las 3 formas (cuando sea aplicable):
--    - Subconsulta: ¿Puedes obtener una lista de IDs/valores en una tabla para filtrar la otra (WHERE IN/NOT IN)? ¿Necesitas un valor agregado de otra tabla para comparar (WHERE < (SELECT AVG...))?
--    - JOIN: ¿Puedes unir las tablas directamente por sus claves relacionadas (ON tabla1.clave = tabla2.clave)? Esta suele ser la forma más eficiente y clara para combinar datos. Usa INNER JOIN para coincidencias, LEFT JOIN si necesitas todos los de una tabla aunque no haya match en la otra.
--    - EXISTS/NOT EXISTS: ¿Te basta con saber SI EXISTE (o no) alguna fila relacionada en otra tabla que cumpla una condición? Útil con subconsultas correlacionadas.
-- 5. Escribe la consulta paso a paso: Empieza con un SELECT simple, añade el FROM, luego el JOIN o la subconsulta, después el WHERE/HAVING y finalmente el ORDER BY.
-- 6. Prueba y depura: Ejecuta la consulta y comprueba si los resultados son los esperados. Si no, revisa las condiciones, los JOINs, etc.

-- ¡Recuerda usar alias para tablas (a, v, p...) y columnas (AS nombre_claro) para hacer tus consultas más legibles!