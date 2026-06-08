-- EJERCICIOS PRÁCTICA 3 - BASE DE DATOS AEROPUERTO

-- 1. Obtenga los tipos de avión, el doble de su envergadura y el cuadrado de su longitud
-- para aquellos aviones con longitud menor que la media y que realizan vuelos con origen o
-- destino en una ciudad que comience por la letra 'M', ordenándolos de mayor a menor
-- envergadura. [cite: 3]

-- subselect
SELECT DISTINCT tipo, envergadura*2 AS doble_envergadura, longitud*longitud AS longitud_cuadrada
FROM aviones
WHERE longitud < (SELECT AVG(longitud) FROM aviones)
AND tipo IN (SELECT DISTINCT tipo_avion FROM vuelos WHERE origen LIKE 'M%' OR destino LIKE 'M%')
ORDER BY doble_envergadura DESC;

-- join
SELECT DISTINCT a.tipo, a.envergadura*2 AS doble_envergadura, a.longitud*a.longitud AS longitud_cuadrada
FROM aviones a
JOIN vuelos v ON a.tipo = v.tipo_avion
WHERE a.longitud < (SELECT AVG(longitud) FROM aviones)
AND (v.origen LIKE 'M%' OR v.destino LIKE 'M%')
ORDER BY doble_envergadura DESC;

-- EXISTS
SELECT DISTINCT tipo, envergadura*2 AS doble_envergadura, longitud*longitud AS longitud_cuadrada
FROM aviones a
WHERE a.longitud < (SELECT AVG(longitud) FROM aviones)
AND EXISTS (SELECT 1 FROM vuelos v WHERE a.tipo = v.tipo_avion AND (v.origen LIKE 'M%' OR v.destino LIKE 'M%'))
ORDER BY doble_envergadura DESC;


-- 2. Obtenga las tres primeras letras de los orígenes y destinos de los vuelos realizados por
-- aviones con longitud mayor que la media y envergadura menor que 2/3 la máxima
-- envergadura, ordenados alfabéticamente por destino. [cite: 10]

-- subselect
SELECT LEFT(origen, 3) AS origen_3, LEFT(destino, 3) AS destino_3
FROM vuelos
WHERE tipo_avion IN (
    SELECT tipo FROM aviones
    WHERE longitud > (SELECT AVG(longitud) FROM aviones)
    AND envergadura < (SELECT MAX(envergadura)*2/3 FROM aviones)
)
ORDER BY destino;

-- join
SELECT LEFT(v.origen, 3) AS origen_3, LEFT(v.destino, 3) AS destino_3
FROM vuelos v
JOIN aviones a ON v.tipo_avion = a.tipo
WHERE a.longitud > (SELECT AVG(longitud) FROM aviones)
AND a.envergadura < (SELECT MAX(envergadura)*2/3 FROM aviones)
ORDER BY v.destino;

-- EXISTS
SELECT LEFT(v.origen, 3) AS origen_3, LEFT(v.destino, 3) AS destino_3
FROM vuelos v
WHERE EXISTS (
    SELECT 1 FROM aviones a
    WHERE a.tipo = v.tipo_avion
    AND a.longitud > (SELECT AVG(longitud) FROM aviones)
    AND a.envergadura < (SELECT MAX(envergadura)*2/3 FROM aviones)
)
ORDER BY v.destino;


-- 3. Obtenga los dos primeros caracteres de los números de vuelo y el origen de los vuelos
-- a los que corresponden partes con número de parte entre 400 y 450 y que recorren
-- distancias mayores que la media, ordenándolos alfabéticamente por origen. [cite: 15]

-- subselect
SELECT DISTINCT LEFT(num_vuelo, 2) AS vuelo_2, origen
FROM vuelos
WHERE distancia > (SELECT AVG(distancia) FROM vuelos)
AND num_vuelo IN (
    SELECT num_vuelo
    FROM partes
    WHERE num_parte BETWEEN 400 AND 450
)
ORDER BY origen;

-- join
SELECT DISTINCT LEFT(v.num_vuelo, 2) AS vuelo_2, v.origen
FROM vuelos v
JOIN partes p ON v.num_vuelo = p.num_vuelo
WHERE v.distancia > (SELECT AVG(distancia) FROM vuelos)
AND p.num_parte BETWEEN 400 AND 450
ORDER BY v.origen;

-- EXISTS
SELECT DISTINCT LEFT(v.num_vuelo, 2) AS vuelo_2, v.origen
FROM vuelos v
WHERE v.distancia > (SELECT AVG(distancia) FROM vuelos)
AND EXISTS (
    SELECT 1 FROM partes p
    WHERE p.num_vuelo = v.num_vuelo
    AND p.num_parte BETWEEN 400 AND 450
)
ORDER BY v.origen;


-- 4. Obtenga los números de vuelo, las tres primeras letras del origen y las tres primeras
-- letras del destino para los vuelos realizados por aviones cuyo alcance sea mayor que la
-- media de todos y con longitud menor que 2/3 la máxima longitud, ordenándolos por
-- número de vuelo. [cite: 18]

-- subselect
SELECT num_vuelo, LEFT(origen, 3) AS origen_3, LEFT(destino, 3) AS destino_3
FROM vuelos
WHERE tipo_avion IN (
    SELECT tipo FROM aviones
    WHERE alcance > (SELECT AVG(alcance) FROM aviones)
    AND longitud < (SELECT MAX(longitud)*2/3 FROM aviones)
)
ORDER BY num_vuelo;

-- join
SELECT v.num_vuelo, LEFT(v.origen, 3) AS origen_3, LEFT(v.destino, 3) AS destino_3
FROM vuelos v
JOIN aviones a ON v.tipo_avion = a.tipo
WHERE a.alcance > (SELECT AVG(alcance) FROM aviones)
AND a.longitud < (SELECT MAX(longitud)*2/3 FROM aviones)
ORDER BY v.num_vuelo;

-- EXISTS
SELECT v.num_vuelo, LEFT(v.origen, 3) AS origen_3, LEFT(v.destino, 3) AS destino_3
FROM vuelos v
WHERE EXISTS (
    SELECT 1 FROM aviones a
    WHERE a.tipo = v.tipo_avion
    AND a.alcance > (SELECT AVG(alcance) FROM aviones)
    AND a.longitud < (SELECT MAX(longitud)*2/3 FROM aviones)
)
ORDER BY v.num_vuelo;


-- 5. Recupere todas las características de los aviones que nunca han pasado por Barcelona. [cite: 20]

-- subselect (NOT IN)
SELECT * FROM aviones
WHERE tipo NOT IN (
    SELECT DISTINCT tipo_avion FROM vuelos
    WHERE origen = 'BARCELONA' OR destino = 'BARCELONA'
)
ORDER BY tipo;

-- join (LEFT JOIN / IS NULL)
SELECT a.*
FROM aviones a
LEFT JOIN vuelos v ON a.tipo = v.tipo_avion AND (v.origen = 'BARCELONA' OR v.destino = 'BARCELONA')
WHERE v.num_vuelo IS NULL
ORDER BY a.tipo;

-- EXISTS (NOT EXISTS)
SELECT * FROM aviones a
WHERE NOT EXISTS (
    SELECT 1 FROM vuelos v
    WHERE a.tipo = v.tipo_avion
    AND (v.origen = 'BARCELONA' OR v.destino = 'BARCELONA')
)
ORDER BY tipo;


-- 6. Indique los tipos de avión, el doble de su longitud y su envergadura, para los aviones
-- con envergadura mayor que la media y que realicen vuelos desde o hacia Madrid,
-- ordenándolos de mayor a menor longitud. [cite: 24]

-- subselect
SELECT tipo, longitud*2 AS doble_longitud, envergadura
FROM aviones
WHERE envergadura > (SELECT AVG(envergadura) FROM aviones)
AND tipo IN (
    SELECT DISTINCT tipo_avion FROM vuelos
    WHERE origen = 'MADRID' OR destino = 'MADRID'
)
ORDER BY longitud DESC;

-- join
SELECT DISTINCT a.tipo, a.longitud*2 AS doble_longitud, a.envergadura
FROM aviones a
JOIN vuelos v ON a.tipo = v.tipo_avion
WHERE a.envergadura > (SELECT AVG(envergadura) FROM aviones)
AND (v.origen = 'MADRID' OR v.destino = 'MADRID')
ORDER BY a.longitud DESC;

-- EXISTS
SELECT tipo, longitud*2 AS doble_longitud, envergadura
FROM aviones a
WHERE a.envergadura > (SELECT AVG(envergadura) FROM aviones)
AND EXISTS (
    SELECT 1 FROM vuelos v
    WHERE a.tipo = v.tipo_avion
    AND (v.origen = 'MADRID' OR v.destino = 'MADRID')
)
ORDER BY longitud DESC;


-- 7. Obtenga, para cada destino, la mayor distancia recorrida hacia él, por vuelos realizados
-- por aviones con longitud mayor que la media, ordenados alfabéticamente. [cite: 28]
-- Nota: JOIN es la forma más natural aquí. Las otras son más complejas o menos directas.

-- join (Más natural)
SELECT v.destino, MAX(v.distancia) AS max_distancia
FROM vuelos v
JOIN aviones a ON v.tipo_avion = a.tipo
WHERE a.longitud > (SELECT AVG(longitud) FROM aviones)
GROUP BY v.destino
ORDER BY v.destino;

-- subselect (Anidada en WHERE)
SELECT destino, MAX(distancia) AS max_distancia
FROM vuelos
WHERE tipo_avion IN (SELECT tipo FROM aviones WHERE longitud > (SELECT AVG(longitud) FROM aviones))
GROUP BY destino
ORDER BY destino;

-- EXISTS (No es la forma más directa para agregación, se usaría en el WHERE)
SELECT v.destino, MAX(v.distancia) AS max_distancia
FROM vuelos v
WHERE EXISTS (
    SELECT 1 FROM aviones a
    WHERE a.tipo = v.tipo_avion AND a.longitud > (SELECT AVG(longitud) FROM aviones)
)
GROUP BY v.destino
ORDER BY v.destino;


-- 8. Obtenga, para cada origen, la menor distancia recorrida desde él por vuelos realizados
-- por aviones con menos butacas que la media, ordenados alfabéticamente. [cite: 31]
-- Nota: Similar al ejercicio 7, JOIN es más natural.

-- join (Más natural)
SELECT v.origen, MIN(v.distancia) AS min_distancia
FROM vuelos v
JOIN aviones a ON v.tipo_avion = a.tipo
WHERE a.butacas < (SELECT AVG(butacas) FROM aviones)
GROUP BY v.origen
ORDER BY v.origen;

-- subselect (Anidada en WHERE)
SELECT origen, MIN(distancia) AS min_distancia
FROM vuelos
WHERE tipo_avion IN (SELECT tipo FROM aviones WHERE butacas < (SELECT AVG(butacas) FROM aviones))
GROUP BY origen
ORDER BY origen;

-- EXISTS (No es la forma más directa para agregación, se usaría en el WHERE)
SELECT v.origen, MIN(v.distancia) AS min_distancia
FROM vuelos v
WHERE EXISTS (
    SELECT 1 FROM aviones a
    WHERE a.tipo = v.tipo_avion AND a.butacas < (SELECT AVG(butacas) FROM aviones)
)
GROUP BY v.origen
ORDER BY v.origen;


-- 9. Indique el total de plazas reservadas existentes para cada número de vuelo de Iberia. [cite: 33]
-- Nota: Requiere JOIN o subconsulta correlacionada/EXISTS si se quiere filtrar por compañía en `vuelos` o `flota`.
--       Asumiendo que 'IB' en `num_vuelo` indica Iberia.

-- Directo con WHERE (Asumiendo 'IB' prefijo)
SELECT num_vuelo, SUM(plazas) AS total_plazas
FROM reservas
WHERE num_vuelo LIKE 'IB%'
GROUP BY num_vuelo
ORDER BY num_vuelo;

-- join (Si se requiere confirmar compañía via `flota` o `vuelos` -> `companias`)
-- Asumiendo que necesitamos la tabla `vuelos` para confirmar la compañía (no directamente en `reservas`)
-- y que `vuelos` tiene una columna `compania` (que no tiene en el schema proporcionado).
-- O uniendo `reservas` -> `partes` -> `flota` -> `companias` (más complejo).
-- Si la lógica es sólo el prefijo 'IB', la primera consulta es suficiente.
-- Ejemplo hipotético con JOIN a `vuelos` (si tuviera `compania`)
/*
SELECT r.num_vuelo, SUM(r.plazas) AS total_plazas
FROM reservas r
JOIN vuelos v ON r.num_vuelo = v.num_vuelo
JOIN companias c ON v.compania = c.code -- Asumiendo columna compania en vuelos
WHERE c.code = 'IB' -- o c.nombre = 'Iberia'
GROUP BY r.num_vuelo
ORDER BY r.num_vuelo;
*/

-- 10. Indique a cuántos destinos diferentes se vuela desde cada uno de los orígenes,
-- mostrando la salida ordenada de mayor a menor número de destinos. [cite: 37]
-- Nota: Consulta simple de agregación.

SELECT origen, COUNT(DISTINCT destino) AS num_destinos_diferentes
FROM vuelos
GROUP BY origen
ORDER BY num_destinos_diferentes DESC, origen;


-- 11. Indique cuántos tipos de aviones diferentes salen de cada origen de la tabla vuelos,
-- mostrando la salida ordenada de mayor a menor número de aviones. [cite: 41]
-- Sólo nos interesan aquellos orígenes de los que salen más de tres tipos de aviones diferentes. [cite: 41]
-- Nota: Agregación con HAVING.

SELECT origen, COUNT(DISTINCT tipo_avion) AS num_tipos_avion_diferentes
FROM vuelos
GROUP BY origen
HAVING COUNT(DISTINCT tipo_avion) > 3
ORDER BY num_tipos_avion_diferentes DESC, origen;


-- 12. ¿Cuántas horas de salida diferentes hay para cada tramo (origen - destino) de la tabla
-- vuelos? [cite: 44]
-- Nota: Agregación simple.

SELECT origen, destino, COUNT(DISTINCT hora_salida) AS horas_salida_diferentes
FROM vuelos
GROUP BY origen, destino
ORDER BY origen, destino;


-- 13. Obtenga, para cada número de vuelo, el total de plazas reservadas de los vuelos que
-- recorren distancias mayores que la media de las distancias recorridas por vuelos de la misma
-- compañía. [cite: 50, 52]
-- Sólo nos interesan aquellos vuelos en los que el total de plazas reservadas es mayor que
-- la media de plazas reservadas para los vuelos de Iberia. [cite: 53]
-- Nota: Requiere subconsultas correlacionadas o CTEs. JOIN/EXISTS aplicables en condiciones.
--       Necesita la compañía del vuelo. Usaremos `flota` para obtenerla a través de `partes`.

-- Usando Subconsultas y JOINs
SELECT r.num_vuelo, SUM(r.plazas) AS total_plazas_reservadas
FROM reservas r
JOIN vuelos v ON r.num_vuelo = v.num_vuelo
JOIN ( -- Para obtener la compañía de cada vuelo (asumiendo un vuelo usa un avión -> una compañía)
    SELECT DISTINCT p.num_vuelo, f.compania
    FROM partes p
    JOIN flota f ON p.mat = f.matricula
) vf ON v.num_vuelo = vf.num_vuelo
WHERE v.distancia > (
    -- Media de distancia para la compañía de ESE vuelo
    SELECT AVG(v_comp.distancia)
    FROM vuelos v_comp
    JOIN (
        SELECT DISTINCT p_comp.num_vuelo, f_comp.compania
        FROM partes p_comp
        JOIN flota f_comp ON p_comp.mat = f_comp.matricula
    ) vf_comp ON v_comp.num_vuelo = vf_comp.num_vuelo
    WHERE vf_comp.compania = vf.compania
)
GROUP BY r.num_vuelo
HAVING SUM(r.plazas) > (
    -- Media de plazas reservadas para vuelos de Iberia ('IB')
    SELECT AVG(total_plazas_por_vuelo)
    FROM (
        SELECT SUM(plazas) AS total_plazas_por_vuelo
        FROM reservas
        WHERE num_vuelo LIKE 'IB%' -- Asumiendo prefijo 'IB' para Iberia
        GROUP BY num_vuelo
    ) AS plazas_iberia
)
ORDER BY r.num_vuelo;


-- 14. Obtenga la hora de salida más temprana para cada uno de los orígenes de los vuelos
-- realizados por aviones con un alcance menor que 2/3 de la media del alcance de los otros
-- aviones. [cite: 54]
-- Nota: La condición "media del alcance de los otros aviones" es ambigua. Interpretaremos como
-- "alcance menor que 2/3 de la media del alcance de TODOS los aviones".

-- subselect
SELECT origen, MIN(hora_salida) AS primera_hora_salida
FROM vuelos
WHERE tipo_avion IN (
    SELECT tipo FROM aviones
    WHERE alcance < (SELECT AVG(alcance) * 2/3 FROM aviones)
)
GROUP BY origen
ORDER BY origen;

-- join
SELECT v.origen, MIN(v.hora_salida) AS primera_hora_salida
FROM vuelos v
JOIN aviones a ON v.tipo_avion = a.tipo
WHERE a.alcance < (SELECT AVG(alcance) * 2/3 FROM aviones)
GROUP BY v.origen
ORDER BY v.origen;

-- EXISTS
SELECT v.origen, MIN(v.hora_salida) AS primera_hora_salida
FROM vuelos v
WHERE EXISTS (
    SELECT 1 FROM aviones a
    WHERE a.tipo = v.tipo_avion
    AND a.alcance < (SELECT AVG(alcance) * 2/3 FROM aviones)
)
GROUP BY v.origen
ORDER BY v.origen;


-- 15. Obtenga los números de parte de los partes que corresponden a vuelos que recorren
-- una distancia mayor que la media de la distancia de los otros vuelos. [cite: 56]
-- Nota: "media de la distancia de los otros vuelos" es ambiguo. Interpretaremos como
-- "distancia mayor que la media de TODOS los vuelos".

-- subselect
SELECT num_parte
FROM partes
WHERE num_vuelo IN (
    SELECT num_vuelo FROM vuelos
    WHERE distancia > (SELECT AVG(distancia) FROM vuelos)
)
ORDER BY num_parte;

-- join
SELECT p.num_parte
FROM partes p
JOIN vuelos v ON p.num_vuelo = v.num_vuelo
WHERE v.distancia > (SELECT AVG(distancia) FROM vuelos)
ORDER BY p.num_parte;

-- EXISTS
SELECT p.num_parte
FROM partes p
WHERE EXISTS (
    SELECT 1 FROM vuelos v
    WHERE v.num_vuelo = p.num_vuelo
    AND v.distancia > (SELECT AVG(distancia) FROM vuelos)
)
ORDER BY p.num_parte;


-- 16. Obtenga el número de butacas de aquellos aviones con más butacas que la media de
-- los otros aviones y envergadura menor que la media de las diferentes envergaduras de
-- los otros aviones. [cite: 59]
-- Nota: "media de los otros aviones" es ambiguo. Se interpretará como la media de TODOS los aviones.
--       "media de las diferentes envergaduras" -> AVG(DISTINCT envergadura).

SELECT butacas
FROM aviones a1
WHERE butacas > (SELECT AVG(butacas) FROM aviones)
AND envergadura < (SELECT AVG(DISTINCT envergadura) FROM aviones)
ORDER BY butacas;


-- 17. Obtenga la longitud de aquellos aviones con longitud menor que la media de los otros
-- aviones y capacidad mayor que la media de las diferentes capacidades de los otros aviones. [cite: 60, 62]
-- Nota: "capacidad" se interpreta como `butacas`. "media de los otros aviones" -> media de TODOS.

SELECT longitud
FROM aviones a1
WHERE longitud < (SELECT AVG(longitud) FROM aviones)
AND butacas > (SELECT AVG(DISTINCT butacas) FROM aviones)
ORDER BY longitud;


-- 18. Obtenga la longitud de los aviones que realizan vuelos que recorren distancias
-- mayores que la media de las distancias de los vuelos recorridos por la misma compaña. [cite: 63]
-- Nota: Necesita la compañía del vuelo. Usaremos `flota` y `partes`.

-- join y subconsulta correlacionada
SELECT DISTINCT a.longitud
FROM aviones a
JOIN vuelos v ON a.tipo = v.tipo_avion
JOIN ( -- Para obtener la compañía de cada vuelo
    SELECT DISTINCT p.num_vuelo, f.compania
    FROM partes p
    JOIN flota f ON p.mat = f.matricula
) vf ON v.num_vuelo = vf.num_vuelo
WHERE v.distancia > (
    -- Media de distancia para la compañía de ESE vuelo
    SELECT AVG(v_comp.distancia)
    FROM vuelos v_comp
    JOIN (
        SELECT DISTINCT p_comp.num_vuelo, f_comp.compania
        FROM partes p_comp
        JOIN flota f_comp ON p_comp.mat = f_comp.matricula
    ) vf_comp ON v_comp.num_vuelo = vf_comp.num_vuelo
    WHERE vf_comp.compania = vf.compania
)
ORDER BY a.longitud;

-- EXISTS (Más complejo de aplicar directamente por la media correlacionada)


-- 19. Saliendo en el primer vuelo Sevilla - Madrid, averigüe la hora de salida del primer
-- vuelo que se puede coger en Madrid con destino a Barcelona. [cite: 65]
-- Nota: Requiere encontrar la hora de llegada del primer Sevilla-Madrid y luego la primera salida MAD-BCN posterior.

SELECT MIN(v_mad_bcn.hora_salida) AS primera_salida_mad_bcn
FROM vuelos v_mad_bcn
WHERE v_mad_bcn.origen = 'MADRID'
AND v_mad_bcn.destino = 'BARCELONA'
AND v_mad_bcn.hora_salida > (
    -- Hora de llegada del primer vuelo Sevilla-Madrid
    SELECT MIN(v_svq_mad.hora_llegada)
    FROM vuelos v_svq_mad
    WHERE v_svq_mad.origen = 'SEVILLA'
    AND v_svq_mad.destino = 'MADRID'
    -- Asegurarse de que es el vuelo más temprano por hora de salida
    AND v_svq_mad.hora_salida = (SELECT MIN(hora_salida) FROM vuelos WHERE origen = 'SEVILLA' AND destino = 'MADRID')
);


-- 20. Obtenga el total de plazas reservadas para vuelos de Iberia cada día entre cada dos
-- ciudades, ordenados de mayor a menor número de plazas reservadas. [cite: 66]
-- Nota: Necesita JOIN con `vuelos` para obtener origen/destino. Asume 'IB' prefijo para Iberia.

SELECT r.fecha, v.origen, v.destino, SUM(r.plazas) AS total_plazas
FROM reservas r
JOIN vuelos v ON r.num_vuelo = v.num_vuelo
WHERE r.num_vuelo LIKE 'IB%' -- Asumiendo prefijo 'IB' para Iberia
GROUP BY r.fecha, v.origen, v.destino
ORDER BY total_plazas DESC;


-- 21. Obtenga los diferentes recorridos que se pueden realizar desde una ciudad hasta
-- Madrid y haciendo escala llegar a otra ciudad. [cite: 70]
-- Nota: Self-join en `vuelos`.

SELECT DISTINCT v1.origen AS origen_inicial, v1.destino AS escala, v2.destino AS destino_final
FROM vuelos v1
JOIN vuelos v2 ON v1.destino = v2.origen -- La escala es el origen del segundo vuelo
WHERE v1.destino = 'MADRID' -- La escala debe ser Madrid
AND v1.origen != v2.destino -- El origen inicial no puede ser el destino final
AND v1.origen != 'MADRID' -- No empezar en Madrid
AND v2.destino != 'MADRID' -- No terminar en Madrid
ORDER BY v1.origen, v2.destino;


-- 22. Obtenga, en una sola columna, los nombres de todas las ciudades que aparecen en la
-- tabla de vuelos, ordenados alfabéticamente. [cite: 84]
-- Nota: UNION para combinar origen y destino.

SELECT origen AS ciudad FROM vuelos
UNION
SELECT destino AS ciudad FROM vuelos
ORDER BY ciudad;


-- 23. Obtenga en una sola columna el nombre de todas las ciudades origen de un vuelo y el
-- de las que son destino de un vuelo. [cite: 86]
-- (Una misma ciudad puede aparecer como origen y como destino.) [cite: 87]
-- Nota: UNION ALL para incluir duplicados si una ciudad es origen y destino.

SELECT origen AS ciudad FROM vuelos
UNION ALL
SELECT destino AS ciudad FROM vuelos
ORDER BY ciudad;


-- 24. Obtenga en dos columnas, para cada ciudad que es origen, el número de vuelos que
-- salen de ella y luego para cada una que es destino, el número de vuelos que recibe. [cite: 90]
-- Nota: Se necesitan dos consultas separadas o una UNION ALL de agregaciones.

-- Como Origen
SELECT origen AS ciudad, COUNT(*) AS vuelos_salen
FROM vuelos
GROUP BY origen

UNION ALL

-- Como Destino
SELECT destino AS ciudad, COUNT(*) AS vuelos_llegan
FROM vuelos
GROUP BY destino

ORDER BY ciudad; -- Ordenar para ver juntos, aunque la cuenta sea de roles distintos


-- 25. Obtenga en tres columnas, para cada ciudad que aparece en la tabla vuelos, su
-- nombre ordenado alfabéticamente, el total de vuelos que parten de ella y el total de
-- vuelos que llegan a ella. [cite: 94]
-- Si no llega o no parte ningún vuelo, debe aparecer cero en la columna correspondiente. [cite: 95]
-- Nota: Necesita una lista completa de ciudades y luego LEFT JOIN con agregaciones.

WITH todas_ciudades AS (
    SELECT origen AS ciudad FROM vuelos
    UNION
    SELECT destino AS ciudad FROM vuelos
),
vuelos_salen AS (
    SELECT origen, COUNT(*) AS num_salen FROM vuelos GROUP BY origen
),
vuelos_llegan AS (
    SELECT destino, COUNT(*) AS num_llegan FROM vuelos GROUP BY destino
)
SELECT
    tc.ciudad,
    COALESCE(vs.num_salen, 0) AS total_vuelos_salen,
    COALESCE(vl.num_llegan, 0) AS total_vuelos_llegan
FROM todas_ciudades tc
LEFT JOIN vuelos_salen vs ON tc.ciudad = vs.origen
LEFT JOIN vuelos_llegan vl ON tc.ciudad = vl.destino
ORDER BY tc.ciudad;


-- 26. Obtenga en dos columnas, las diferentes fechas de llegada reflejadas en los partes de
-- vuelo con el menor combustible consumido en cada una de ellas y, a continuación, estas
-- mismas fechas con el mayor combustible consumido en cada una de ellas. [cite: 100]
-- Nota: UNION ALL de dos agregaciones.

-- Menor consumo por fecha
SELECT fecha, MIN(comb_consumido) AS consumo
FROM partes
GROUP BY fecha

UNION ALL

-- Mayor consumo por fecha
SELECT fecha, MAX(comb_consumido) AS consumo
FROM partes
GROUP BY fecha

ORDER BY fecha, consumo; -- Ordena para ver min y max juntos por fecha