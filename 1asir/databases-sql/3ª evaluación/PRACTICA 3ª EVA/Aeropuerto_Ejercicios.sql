Sentencias Complejas con varias tablas 

1. Obtenga los tipos de avión, el doble de su envergadura y el cuadrado de su longitud 
para aquellos aviones con longitud menor que la media y que realizan vuelos con origen o 
destino en una ciudad que comience por la letra 'M', ordenándolos de mayor a menor 
envergadura. 
 
-- subselect 
SELECT DISTINCT tipo, envergadura*2,longitud*longitud 
FROM aviones 
WHERE longitud<(SELECT AVG(longitud) FROM aviones) 
AND tipo IN (SELECT DISTINCT tipo_avion FROM vuelos WHERE origen LIKE "M%"  
OR destino LIKE "M%") 
ORDER BY 2 desc; 

-- join
SELECT DISTINCT a.tipo, a.envergadura*2,a.longitud*a.longitud 
FROM aviones a, vuelos v 
WHERE a.tipo=v.tipo_avion 
AND a.longitud<(SELECT AVG(longitud) FROM aviones) 
AND a.tipo IN (SELECT DISTINCT tipo_avion FROM vuelos 
WHERE origen LIKE "M%" 
OR destino LIKE "M%") 
ORDER BY 2 desc; 

-- EXISTS
SELECT DISTINCT a.tipo, a.envergadura*2,a.longitud*a.longitud 
FROM aviones a, vuelos v 
WHERE a.longitud<(SELECT AVG(longitud) FROM aviones) 
AND EXISTS (SELECT * FROM vuelos v WHERE a.tipo=v.tipo_avion AND( v.origen 
LIKE "M%" OR v.destino LIKE "M%")) 
ORDER BY 2 desc; 
 
+------+-----------------+------------+ 
| tipo | (envergadura*2) | Longitud^2 | 
+------+-----------------+------------+ 
| M87  |           65.80 |  1576.0900 | 
| M80  |           65.72 |  2032.2064 | 
| D9S  |           56.84 |  1321.3225 | 
| CS5  |           51.62 |   457.9600 | 
+------+-----------------+------------+ 
4 rows IN set (0.00 sec) 
 

2. Obtenga las tres primeras letras de los orígenes y destinos de los vuelos realizados por 
aviones con longitud mayor que la media y envergadura menor que 2/3 la máxima 
envergadura, ordenados alfabéticamente por destino. 

-- subselect 
SELECT LEFT(Origen, 3), LEFT(Destino, 3)
FROM vuelos
WHERE tipo_avion IN (
    SELECT tipo FROM aviones 
    WHERE longitud > (SELECT AVG(longitud) FROM aviones)
    AND envergadura < (SELECT MAX(envergadura)*2/3 FROM aviones)
    )
ORDER BY destino;

-- join
SELECT LEFT(v.Origen, 3), LEFT(v.Destino, 3)
FROM vuelos v
INNER JOIN aviones a ON a.tipo = v.tipo_avion
WHERE a.longitud > (SELECT AVG(longitud) FROM aviones)
AND a.envergadura < (SELECT MAX(envergadura)*2/3 FROM aviones)
ORDER BY v.destino;

-- EXISTS
SELECT LEFT(v.Origen, 3), LEFT(v.Destino, 3)
FROM vuelos v
WHERE EXISTS (
    SELECT 1 FROM aviones a
    WHERE a.tipo = v.tipo_avion 
    AND a.longitud > (SELECT AVG(longitud) FROM aviones)
    AND a.envergadura < (SELECT MAX(envergadura)*2/3 FROM aviones)
    )
ORDER BY v.destino;

+----------------+-----------------+ 
| left(origen,3) | left(destino,3) | 
+----------------+-----------------+ 
| BIL            | AMS             | 
| BIL            | AMS             | 
| MAD            | BAR             | 
| MAD            | BAR             | 
| MAD            | BAR             | 
| BIL            | BAR             | 
| BAR            | BIL             | 
| MAD            | BUE             | 
| MAD            | CAS             | 
| LIS            | GRA             | 
| MAD            | LIS             | 
| PAR            | MAD             | 
| ROM            | MAD             | 
| BAR            | MAD             | 
| SAN            | MAD             | 
| BAR            | MAD             | 
| SEV            | MAD             | 
| BAR            | MAD             | 
| BAR            | MAD             | 
| SAN            | MAD             | 
| BIL            | MAD             | 
| BIL            | MAD             | 
| BIL            | MAD             | 
| BAR            | MAL             | 
| BAR            | MAL             | 
| MAD            | PAR             | 
| MAD            | ROM             | 
| BAR            | SAN             | 
| MAD            | SAN             | 
| BAR            | SEV             | 
+----------------+-----------------+ 
30 rows IN set (0.00 sec) 


3. Obtenga los dos primeros caracteres de los números de vuelo y el origen de los vuelos 
a los que corresponden partes con número de parte entre 400 y 450 y que recorren 
distancias mayores que la media, ordenándolos alfabéticamente por origen. 

-- subselect
SELECT DISTINCT LEFT(num_vuelo, 2), origen
FROM vuelos
WHERE distancia > (SELECT AVG(distancia) FROM vuelos)
AND num_vuelo IN (
    SELECT num_vuelo 
    FROM partes
    WHERE num_parte BETWEEN 400 AND 450
    )
ORDER BY origen;

-- join
SELECT DISTINCT LEFT(v.num_vuelo, 2), v.origen
FROM vuelos v INNER JOIN partes p on v.num_vuelo = p.num_vuelo
WHERE v.distancia > (SELECT AVG(distancia) FROM vuelos)
AND p.num_parte BETWEEN 400 AND 450
ORDER BY origen;

-- EXISTS
SELECT DISTINCT LEFT(num_vuelo, 2), origen
FROM vuelos v
WHERE EXISTS (
    SELECT 1 FROM partes p
    WHERE v.num_vuelo = p.num_vuelo
    AND v.distancia > (SELECT AVG(distancia) FROM vuelos)
    AND p.num_parte BETWEEN 400 AND 450
    )
ORDER BY origen;

+-------------------+-----------+ 
| left(num_vuelo,2) | origen    | 
+-------------------+-----------+ 
| IB                | ALICANTE  | 
| AO                | ALMERIA   | 
| IB                | ALMERIA   | 
| AO                | AMSTERDAM | 
| IB                | AMSTERDAM | 
| IB                | BARCELONA | 
| IB                | BILBAO    | 
+-------------------+-----------+ 
7 rows IN set (0.01 sec) 


4. Obtenga los números de vuelo, las tres primeras letras del origen y las tres primeras 
letras del destino para los vuelos realizados por aviones cuyo alcance sea mayor que la 
media de todos y con longitud menor que 2/3 la máxima longitud, ordenándolos por 
número de vuelo.

-- subselect 
SELECT num_vuelo, left(origen,3), left(destino,3) FROM vuelos
WHERE tipo_avion IN (
    SELECT tipo FROM aviones
    WHERE alcance > (SELECT AVG(alcance) FROM aviones)
    AND longitud < (SELECT MAX(longitud)*2/3 FROM aviones)
    )
ORDER BY num_vuelo;

-- join
SELECT v.num_vuelo, left(v.origen,3), left(v.destino,3) FROM vuelos v
INNER JOIN aviones a ON a.tipo = v.tipo_avion
WHERE a.alcance > (SELECT AVG(alcance) FROM aviones)
AND a.longitud < (SELECT MAX(longitud)*2/3 FROM aviones)
ORDER BY v.num_vuelo;

-- EXISTS
SELECT num_vuelo, left(origen,3), left(destino,3) FROM vuelos v
WHERE EXISTS(
    SELECT 1 FROM aviones a
    WHERE a.tipo = v.tipo_avion
    AND a.alcance > (SELECT AVG(alcance) FROM aviones)
    AND a.longitud < (SELECT MAX(longitud)*2/3 FROM aviones)
    )
ORDER BY v.num_vuelo;

+-----------+----------------+-----------------+ 
| num_vuelo | left(origen,3) | left(destino,3) | 
+-----------+----------------+-----------------+ 
| AR1386    | BUE            | BOG             | 
+-----------+----------------+-----------------+ 
1 row IN set (0.00 sec) 
 
 
 
5. Recupere todas las características de los aviones que nunca han pasado por Barcelona. 

-- subselect
SELECT * FROM aviones
WHERE tipo NOT IN (SELECT DISTINCT tipo_avion FROM vuelos
                   WHERE origen = 'BARCELONA' OR destino = 'BARCELONA')
                   order by tipo;

-- join
SELECT DISTINCT a.* FROM aviones a
LEFT JOIN vuelos v on a.tipo = v.tipo_avion
WHERE NOT (v.origen = 'BARCELONA' OR v.destino = 'BARCELONA');

-- EXISTS
SELECT * FROM aviones a
WHERE NOT EXISTS (
    SELECT 1 FROM vuelos v
    WHERE a.tipo = v.tipo_avion
    AND (v.origen = 'BARCELONA' OR v.destino = 'BARCELONA')
);


+------+ 
| tipo | 
+------+ 
| 310  | 
| 340  | 
| 737  | 
| 73S  | 
| 74M  | 
| 74S  | 
| AB2  | 
| AB3  | 
| ATR  | 
| CS5  | 
| D10  | 
| DC9  | 
| M88  | 
+------+ 
13 rows IN set (0.01 sec) 
 
6. Indique los tipos de avión, el doble de su longitud y su envergadura, para los aviones 
con envergadura mayor que la media y que realicen vuelos desde o hacia Madrid, 
ordenándolos de mayor a menor longitud. 

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


+------+------------+-------------+ 
| tipo | 2*longitud | envergadura | 
+------+------------+-------------+ 
| 747  |     141.02 |       59.64 | 
| 32S  |     127.40 |       60.30 | 
| D10  |     110.70 |       50.39 | 
| AB3  |     107.14 |       44.84 | 
+------+------------+-------------+ 
4 rows IN set (0.00 sec) 
 
 
 
7. Obtenga, para cada destino, la mayor distancia recorrida hacia él, por vuelos realizados 
por aviones con longitud mayor que la media, ordenados alfabéticamente. 

-- join
SELECT v.destino, MAX(v.distancia) AS max_distancia
FROM vuelos v
JOIN aviones a ON v.tipo_avion = a.tipo
WHERE a.longitud > (SELECT AVG(longitud) FROM aviones)
GROUP BY v.destino
ORDER BY v.destino;

-- subselect
SELECT destino, MAX(distancia) AS max_distancia
FROM vuelos
WHERE tipo_avion IN (SELECT tipo FROM aviones WHERE longitud > (SELECT AVG(longitud) FROM aviones))
GROUP BY destino
ORDER BY destino;

-- EXISTS
SELECT v.destino, MAX(v.distancia) AS max_distancia
FROM vuelos v
WHERE EXISTS (
    SELECT 1 FROM aviones a
    WHERE a.tipo = v.tipo_avion AND a.longitud > (SELECT AVG(longitud) FROM aviones)
)
GROUP BY v.destino
ORDER BY v.destino;



+------------------------+----------------+ 
| destino                | max(distancia) | 
+------------------------+----------------+ 
| ALICANTE               |           2700 | 
| ALMERIA                |           2700 | 
| AMSTERDAM              |           3000 | 
| BARCELONA              |            840 | 
| BERLIN                 |           2670 | 
| BILBAO                 |            600 | 
| BUENOS AIRES           |           NULL | 
| CANCUN                 |           NULL | 
| CARACAS                |           3240 | 
| CASABLANCA             |            240 | 
| GRAN CANARIA           |           2640 | 
| LA HABANA              |           2130 | 
| LISBOA                 |             60 | 
| LONDRES                |           2700 | 
| MADRID                 |           2010 | 
| MALAGA                 |            750 | 
| PARIS                  |            900 | 
| ROMA                   |           1320 | 
| SANTIAGO DE COMPOSTELA |            900 | 
| SEVILLA                |            750 | 
+------------------------+----------------+ 
20 rows IN set (0.01 sec) 
 
 
 
8. Obtenga, para cada origen, la menor distancia recorrida desde él por vuelos realizados 
por aviones con menos butacas que la media, ordenados alfabéticamente. 

-- join
SELECT v.origen, MIN(v.distancia) AS min_distancia
FROM vuelos v
JOIN aviones a ON v.tipo_avion = a.tipo
WHERE a.butacas < (SELECT AVG(butacas) FROM aviones)
GROUP BY v.origen
ORDER BY v.origen;

-- subselect
SELECT origen, MIN(distancia) AS min_distancia
FROM vuelos
WHERE tipo_avion IN (SELECT tipo FROM aviones WHERE butacas < (SELECT AVG(butacas) FROM aviones))
GROUP BY origen
ORDER BY origen;

-- EXISTS
SELECT v.origen, MIN(v.distancia) AS min_distancia
FROM vuelos v
WHERE EXISTS (
    SELECT 1 FROM aviones a
    WHERE a.tipo = v.tipo_avion AND a.butacas < (SELECT AVG(butacas) FROM aviones)
)
GROUP BY v.origen
ORDER BY v.origen;


+------------------------+----------------+ 
| origen                 | min(distancia) | 
+------------------------+----------------+ 
| ALICANTE               |            300 | 
| ALMERIA                |            240 | 
| AMSTERDAM              |           1380 | 
| BARCELONA              |            330 | 
| BILBAO                 |            330 | 
| BUENOS AIRES           |           2520 | 
| CASABLANCA             |           3810 | 
| FUERTEVENTURA          |            210 | 
| GRAN CANARIA           |            180 | 
| LA CORU+æA             |            600 | 
| LISBOA                 |           1500 | 
| MADRID                 |             60 | 
| PALMA MALLORCA         |            660 | 
| PARIS                  |            930 | 
| ROMA                   |            840 | 
| SANTIAGO DE CHILE      |            900 | 
| SANTIAGO DE COMPOSTELA |            600 | 
| SEVILLA                |            330 | 
| TENERIFE               |            180 | 
+------------------------+----------------+ 
19 rows IN set (0.01 sec) 
 
9. Indique el total de plazas reservadas existentes para cada número de vuelo de Iberia.

SELECT num_vuelo, SUM(plazas) AS total_plazas
FROM reservas
WHERE num_vuelo LIKE 'IB%'
GROUP BY num_vuelo
ORDER BY num_vuelo;

 
+-----------+-------------+ 
| num_vuelo | sum(plazas) | 
+-----------+-------------+ 
| IB0103    |         255 | 
| IB0543    |         193 | 
| IB0554    |          70 | 
| IB0557    |          70 | 
| IB0845    |         420 | 
| IB1000    |         231 | 
| IB2614    |         408 | 
+-----------+-------------+ 
7 rows IN set (0.00 sec) 
 
 
10. Indique a cuántos destinos diferentes se vuela desde cada uno de los orígenes, 
mostrando la salida ordenada de mayor a menor número de destinos. 

SELECT origen, COUNT(DISTINCT destino) AS num_destinos_diferentes
FROM vuelos
GROUP BY origen
ORDER BY num_destinos_diferentes DESC, origen;


+------------------------+-------------------------+ 
| origen                 | count(distinct destino) | 
+------------------------+-------------------------+ 
| BARCELONA              |                      10 | 
| MADRID                 |                       9 | 
| BUENOS AIRES           |                       7 | 
| ALICANTE               |                       6 | 
| GRAN CANARIA           |                       5 | 
| BILBAO                 |                       5 | 
| ALMERIA                |                       4 | 
| AMSTERDAM              |                       3 | 
| TENERIFE               |                       3 | 
| LISBOA                 |                       2 | 
| FUERTEVENTURA          |                       2 | 
| LA CORU+æA             |                       2 | 
| ROMA                   |                       2 | 
| SANTIAGO DE CHILE      |                       1 | 
| CASABLANCA             |                       1 | 
| SANTIAGO DE COMPOSTELA |                       1 | 
| SEVILLA                |                       1 | 
| PALMA MALLORCA         |                       1 | 
| PARIS                  |                       1 | 
| LA HABANA              |                       1 | 
+------------------------+-------------------------+ 
20 rows IN set (0.00 sec) 
 
 
11. Indique cuántos tipos de aviones diferentes salen de cada origen de la tabla vuelos, 
mostrando la salida ordenada de mayor a menor número de aviones. Sólo nos interesan 
aquellos orígenes de los que salen más de tres tipos de aviones diferentes. 

SELECT origen, COUNT(DISTINCT tipo_avion) AS num_tipos_avion_diferentes
FROM vuelos
GROUP BY origen
HAVING COUNT(DISTINCT tipo_avion) > 3
ORDER BY num_tipos_avion_diferentes DESC, origen;


+--------------+----------------------------+ 
| origen       | count(distinct tipo_avion) | 
+--------------+----------------------------+ 
| MADRID       |                          8 |  
| BARCELONA    |                          6 | 
| BUENOS AIRES |                          5 | 
| ALICANTE     |                          4 | 
| ALMERIA      |                          4 | 
| GRAN CANARIA |                          4 | 
| BILBAO       |                          4 | 
+--------------+----------------------------+ 
7 rows IN set (0.00 sec) 
 
 
12. ¿Cuántas horas de salida diferentes hay para cada tramo (origen - destino) de la tabla 
vuelos? 

SELECT origen, destino, COUNT(DISTINCT hora_salida) AS horas_salida_diferentes
FROM vuelos
GROUP BY origen, destino
ORDER BY origen, destino;


+------------------------+------------------------+-------+ 
| origen                 | destino                | Horas | 
+------------------------+------------------------+-------+ 
| AMSTERDAM              | ALICANTE               |     2 | 
| BARCELONA              | ALICANTE               |     2 | 
| BILBAO                 | ALICANTE               |     1 | 
| AMSTERDAM              | ALMERIA                |     1 | 
| BARCELONA              | ALMERIA                |     1 | 
| ALICANTE               | AMSTERDAM              |     3 | 
| BILBAO                 | AMSTERDAM              |     2 | 
| BUENOS AIRES           | AMSTERDAM              |     2 | 
| ALICANTE               | BARCELONA              |     4 | 
| ALMERIA                | BARCELONA              |     1 | 
| BILBAO                 | BARCELONA              |     2 | 
| BUENOS AIRES           | BARCELONA              |     1 | 
| LA CORU+æA             | BARCELONA              |     1 | 
| MADRID                 | BARCELONA              |     5 | 
| ROMA                   | BARCELONA              |     2 | 
| ALICANTE               | BERLIN                 |     1 | 
| ALICANTE               | BILBAO                 |     1 | 
| BARCELONA              | BILBAO                 |     2 | 
| BUENOS AIRES           | BOGOTA                 |     1 | 
| MADRID                 | BUENOS AIRES           |     1 | 
| SANTIAGO DE CHILE      | BUENOS AIRES           |     2 | 
| BUENOS AIRES           | CANCUN                 |     1 | 
| BUENOS AIRES           | CARACAS                |     1 | 
| MADRID                 | CASABLANCA             |     1 | 
| GRAN CANARIA           | FUERTEVENTURA          |     2 | 
| ALICANTE               | GRAN CANARIA           |     1 | 
| FUERTEVENTURA          | GRAN CANARIA           |     2 | 
| LISBOA                 | GRAN CANARIA           |     1 | 
| TENERIFE               | GRAN CANARIA           |     2 | 
| BARCELONA              | HANOVER                |     1 | 
| GRAN CANARIA           | HIERRO                 |     1 | 
| TENERIFE               | HIERRO                 |     1 | 
| BARCELONA              | LA CORU+æA             |     2 | 
| BUENOS AIRES           | LA CORU+æA             |     1 | 
| MADRID                 | LA CORU+æA             |     2 | 
| MADRID                 | LA HABANA              |     1 | 
| BARCELONA              | LANZAROTE              |     1 | 
| GRAN CANARIA           | LANZAROTE              |     2 | 
| MADRID                 | LISBOA                 |     2 | 
| ALMERIA                | LONDRES                |     1 | 
| ALICANTE               | MADRID                 |     2 | 
| ALMERIA                | MADRID                 |     1 | 
| AMSTERDAM              | MADRID                 |     2 | 
| BARCELONA              | MADRID                 |     6 | 
| BILBAO                 | MADRID                 |     3 | 
| BUENOS AIRES           | MADRID                 |     2 | 
| GRAN CANARIA           | MADRID                 |     2 | 
| LA CORU+æA             | MADRID                 |     1 | 
| LA HABANA              | MADRID                 |     1 | 
| LISBOA                 | MADRID                 |     1 | 
| PALMA MALLORCA         | MADRID                 |     2 | 
| PARIS                  | MADRID                 |     3 | 
| ROMA                   | MADRID                 |     2 | 
| SANTIAGO DE COMPOSTELA | MADRID                 |     3 | 
| SEVILLA                | MADRID                 |     2 | 
| TENERIFE               | MADRID                 |     1 | 
| BARCELONA              | MALAGA                 |     3 | 
| BILBAO                 | MALAGA                 |     1 | 
| ALMERIA                | MELILLA                |     1 | 
| CASABLANCA             | PARIS                  |     1 | 
| MADRID                 | PARIS                  |     2 | 
| MADRID                 | ROMA                   |     2 | 
| BARCELONA              | SANTIAGO DE COMPOSTELA |     3 | 
| MADRID                 | SANTIAGO DE COMPOSTELA |     2 | 
| BARCELONA              | SEVILLA                |     2 | 
| FUERTEVENTURA          | TENERIFE               |     2 | 
| GRAN CANARIA           | TENERIFE               |     2 | 
+------------------------+------------------------+-------+ 
67 rows IN set (0.00 sec) 


13. Obtenga, para cada número de vuelo, el total de plazas reservadas de los vuelos que 
recorren distancias mayores que la media de las distancias recorridas por vuelos de la misma 
compaña. 
Sólo nos interesan aquellos vuelos en los que el total de plazas reservadas es mayor que 
la media de plazas reservadas para los vuelos de Iberia. 

SELECT r.num_vuelo, SUM(r.plazas) AS total_plazas_reservadas
FROM reservas r
JOIN vuelos v ON r.num_vuelo = v.num_vuelo
JOIN partes p ON v.num_vuelo = p.num_vuelo
JOIN flota f ON p.mat = f.matricula    
WHERE v.distancia > (
        SELECT AVG(v_comp.distancia)
        FROM vuelos v_comp
        JOIN partes p_comp ON v_comp.num_vuelo = p_comp.num_vuelo
        JOIN flota f_comp ON p_comp.mat = f_comp.matricula    
        WHERE f_comp.compania = f.compania
    )
GROUP BY r.num_vuelo
HAVING SUM(r.plazas) > (
        SELECT AVG(total_plazas_por_vuelo)
        FROM (
            SELECT SUM(plazas) AS total_plazas_por_vuelo
            FROM reservas
            WHERE num_vuelo LIKE 'IB%'
            GROUP BY num_vuelo
        ) AS plazas_iberia
    )
ORDER BY r.num_vuelo;


Empty set (0.01 sec) 


14. Obtenga la hora de salida más temprana para cada uno de los orígenes de los vuelos 
realizados por aviones con un alcance menor que 2/3 de la media del alcance de los otros 
aviones. 

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


+------------------------+------------------+ 
| origen                 | min(hora_salida) | 
+------------------------+------------------+ 
| ALICANTE               | 08:05:00         | 
| ALMERIA                | 09:25:00         | 
| AMSTERDAM              | 11:20:00         | 
| BARCELONA              | 07:35:00         | 
| BILBAO                 | 10:55:00         | 
| CASABLANCA             | 15:05:00         | 
| FUERTEVENTURA          | 08:45:00         | 
| GRAN CANARIA           | 06:50:00         | 
| LA CORU+æA             | 09:35:00         | 
| LISBOA                 | 09:05:00         | 
| MADRID                 | 07:50:00         | 
| PALMA MALLORCA         | 07:50:00         | 
| PARIS                  | 07:05:00         | 
| ROMA                   | 18:50:00         | 
| SANTIAGO DE CHILE      | 07:00:00         | 
| SANTIAGO DE COMPOSTELA | 07:10:00         | 
| SEVILLA                | 18:15:00         | 
| TENERIFE               | 08:00:00         | 
+------------------------+------------------+ 
18 rows IN set (0.00 sec) 


15. Obtenga los números de parte de los partes que corresponden a vuelos que recorren 
una distancia mayor que la media de la distancia de los otros vuelos. 

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


+-----------+ 
| num_parte | 
+-----------+ 
|       408 | 
|       409 | 
|       413 | 
|       414 | 
|       415 | 
|       416 | 
|       417 | 
|       418 | 
|       419 | 
|       393 | 
|       394 | 
|       395 | 
|       396 | 
|       397 | 
|       402 | 
|       425 | 
|       444 | 
|       445 | 
|       455 | 
|       461 | 
|       471 | 
|       472 | 
|       478 | 
|       479 | 
|       490 | 
|       497 | 
|       498 | 
|       506 | 
|       507 | 
|       518 | 
+-----------+ 
30 rows IN set (0.01 sec) 


16. Obtenga el número de butacas de aquellos aviones con más butacas que la media de 
los otros aviones y envergadura menor que la media de las diferentes envergaduras de 
los otros aviones. 

-- subselect
SELECT butacas
FROM aviones a1
WHERE butacas > (SELECT AVG(butacas) FROM aviones)
AND envergadura < (SELECT AVG(DISTINCT envergadura) FROM aviones)
ORDER BY butacas;

-- join
SELECT a.butacas
FROM aviones a
INNER JOIN (SELECT AVG(butacas) AS media_butacas FROM aviones) AS calc_avg_butacas
INNER JOIN (SELECT AVG(DISTINCT envergadura) AS media_dist_envergadura FROM aviones) AS calc_avg_env
WHERE a.butacas > calc_avg_butacas.media_butacas
  AND a.envergadura < calc_avg_env.media_dist_envergadura
ORDER BY a.butacas;

-- EXISTS
SELECT a1.butacas
FROM aviones a1
WHERE EXISTS (
    SELECT 1
    FROM (
        SELECT AVG(butacas) as avg_b, AVG(DISTINCT envergadura) as avg_e
        FROM aviones
    ) AS medias
    WHERE a1.butacas > medias.avg_b AND a1.envergadura < medias.avg_e
)
ORDER BY a1.butacas;

+---------+ 
| butacas | 
+---------+ 
|     200 | 
+---------+ 
1 row IN set (0.00 sec) 


17. Obtenga la longitud de aquellos aviones con longitud menor que la media de los otros 
aviones y capacidad mayor que la media de las diferentes capacidades de los otros aviones. 

-- subselect
SELECT longitud
FROM aviones a1
WHERE longitud < (SELECT AVG(longitud) FROM aviones)
AND butacas > (SELECT AVG(DISTINCT butacas) FROM aviones)
ORDER BY longitud;

-- join
SELECT a.longitud
FROM aviones a
INNER JOIN (SELECT AVG(longitud) AS media_longitud FROM aviones) AS calc_avg_lon
INNER JOIN (SELECT AVG(DISTINCT butacas) AS media_dist_butacas FROM aviones) AS calc_avg_but
WHERE a.longitud < calc_avg_lon.media_longitud
  AND a.butacas > calc_avg_but.media_dist_butacas
ORDER BY a.longitud;

-- EXISTS
SELECT a1.longitud
FROM aviones a1
WHERE EXISTS (
    SELECT 1
    FROM (
        SELECT AVG(longitud) as avg_l, AVG(DISTINCT butacas) as avg_b
        FROM aviones
    ) AS medias
    WHERE a1.longitud < medias.avg_l AND a1.butacas > medias.avg_b
)
ORDER BY a1.longitud;


Empty set (0.00 sec) 
 
18. Obtenga la longitud de los aviones que realizan vuelos que recorren distancias 
mayores que la media de las distancias de los vuelos recorridos por la misma compaña. 

-- subselect
SELECT DISTINCT a.longitud
FROM aviones a
JOIN vuelos v ON a.tipo = v.tipo_avion     
JOIN partes p ON v.num_vuelo = p.num_vuelo 
JOIN flota f ON p.mat = f.matricula      
WHERE v.distancia > (
        SELECT AVG(v_comp.distancia)
        FROM vuelos v_comp
        JOIN partes p_comp ON v_comp.num_vuelo = p_comp.num_vuelo
        JOIN flota f_comp ON p_comp.mat = f_comp.matricula    
        WHERE f_comp.compania = f.compania
    )
ORDER BY a.longitud;
-- join
SELECT DISTINCT a.longitud
FROM aviones a
JOIN vuelos v ON a.tipo = v.tipo_avion
JOIN partes p ON v.num_vuelo = p.num_vuelo
JOIN flota f ON p.mat = f.matricula
JOIN (
    SELECT 
        f_avg.compania,
        AVG(v_avg.distancia) AS avg_distancia_compania
    FROM vuelos v_avg
    JOIN partes p_avg ON v_avg.num_vuelo = p_avg.num_vuelo
    JOIN flota f_avg ON p_avg.mat = f_avg.matricula
    GROUP BY f_avg.compania
) AS medias_compania ON f.compania = medias_compania.compania
WHERE v.distancia > medias_compania.avg_distancia_compania
ORDER BY a.longitud;

-- EXISTS
SELECT DISTINCT a.longitud
FROM aviones a
WHERE EXISTS (
    SELECT 1 FROM vuelos v
    JOIN partes p ON v.num_vuelo = p.num_vuelo
    JOIN flota f ON p.mat = f.matricula
    WHERE v.tipo_avion = a.tipo
    AND v.distancia > (
        SELECT AVG(v_comp.distancia)
        FROM vuelos v_comp
        JOIN partes p_comp ON v_comp.num_vuelo = p_comp.num_vuelo
        JOIN flota f_comp ON p_comp.mat = f_comp.matricula
        WHERE f_comp.compania = f.compania
    )
)
ORDER BY
    a.longitud;


+----------+ 
| longitud | 
+----------+ 
|    63.70 | 
|    46.66 | 
|    48.03 | 
|    47.32 | 
|    21.40 | 
|    53.57 | 
|    55.35 | 
|    36.35 | 
|    39.70 | 
|    45.08 | 
|    27.12 | 
+----------+ 
11 rows IN set (0.03 sec) 
 
 
 
19. Saliendo en el primer vuelo Sevilla - Madrid, averigüe la hora de salida del primer 
vuelo que se puede coger en Madrid con destino a Barcelona. 

-- subselect
SELECT MIN(v_mad_bcn.hora_salida) AS primera_salida_mad_bcn
FROM vuelos v_mad_bcn
WHERE v_mad_bcn.origen = 'MADRID'
AND v_mad_bcn.destino = 'BARCELONA'
AND v_mad_bcn.hora_salida > (
    SELECT MIN(v_svq_mad.hora_llegada)
    FROM vuelos v_svq_mad
    WHERE v_svq_mad.origen = 'SEVILLA'
    AND v_svq_mad.destino = 'MADRID'
    AND v_svq_mad.hora_salida = (SELECT MIN(hora_salida) FROM vuelos WHERE origen = 'SEVILLA' AND destino = 'MADRID')
);

-- join
SELECT MIN(v2.hora_salida) AS primera_salida_mad_bcn
FROM vuelos v1
JOIN vuelos v2 ON v1.destino = v2.origen
WHERE v1.origen = 'SEVILLA' AND v1.destino = 'MADRID'
AND v2.origen = 'MADRID' AND v2.destino = 'BARCELONA'
AND v1.hora_salida = (SELECT MIN(hora_salida) FROM vuelos WHERE origen = 'SEVILLA' AND destino = 'MADRID')
AND v2.hora_salida > v1.hora_llegada;

-- EXISTS
SELECT MIN(v_mad_bcn.hora_salida) AS primera_salida_mad_bcn
FROM vuelos v_mad_bcn
WHERE
    v_mad_bcn.origen = 'MADRID' AND v_mad_bcn.destino = 'BARCELONA'
AND EXISTS (
    SELECT 1
    FROM vuelos v_svq_mad
    WHERE v_svq_mad.origen = 'SEVILLA'
    AND v_svq_mad.destino = 'MADRID'
    AND v_svq_mad.hora_salida = (SELECT MIN(hora_salida) FROM vuelos WHERE origen = 'SEVILLA' AND destino = 'MADRID')
    AND v_mad_bcn.hora_salida > v_svq_mad.hora_llegada
);


+------------------+ 
| min(hora_salida) | 
+------------------+ 
| 10:00:00         | 
+------------------+ 
1 row IN set (0.00 sec) 



20. Obtenga el total de plazas reservadas para vuelos de Iberia cada día entre cada dos 
ciudades, ordenados de mayor a menor número de plazas reservadas. 

-- subselect
SELECT
    r.fecha,
    (SELECT v.origen FROM vuelos v WHERE v.num_vuelo = r.num_vuelo) AS origen,
    (SELECT v.destino FROM vuelos v WHERE v.num_vuelo = r.num_vuelo) AS destino,
    SUM(r.plazas) AS total_plazas_por_vuelo
FROM reservas r
WHERE r.num_vuelo LIKE 'IB%'
GROUP BY r.fecha, r.num_vuelo
ORDER BY total_plazas_por_vuelo DESC;

-- join
SELECT r.fecha, v.origen, v.destino, SUM(r.plazas) AS total_plazas
FROM reservas r
JOIN vuelos v ON r.num_vuelo = v.num_vuelo
WHERE r.num_vuelo LIKE 'IB%'
GROUP BY r.fecha, v.origen, v.destino
ORDER BY total_plazas DESC;

-- EXISTS
SELECT r.fecha, v.origen, v.destino, SUM(r.plazas) AS total_plazas
FROM reservas r
JOIN vuelos v ON r.num_vuelo = v.num_vuelo
WHERE EXISTS (
    SELECT 1
    FROM flota f
    JOIN partes p ON f.matricula = p.mat
    WHERE p.num_vuelo = r.num_vuelo AND f.compania = 'IB'
)
GROUP BY r.fecha, v.origen, v.destino
ORDER BY total_plazas DESC;


+------------+------------------------+------------------------+---------------+ 
| fecha      | origen                 | destino                | SUM(R.plazas) | 
+------------+------------------------+------------------------+---------------+ 
| 2001-03-30 | SEVILLA                | MADRID                 |           255 | 
| 2001-02-05 | MADRID                 | BARCELONA              |           231 | 
| 2001-02-04 | BARCELONA              | MADRID                 |           227 | 
| 2001-02-04 | MADRID                 | BARCELONA              |           215 | 
| 2001-02-03 | MADRID                 | BARCELONA              |           193 | 
| 2001-02-03 | BARCELONA              | MADRID                 |           193 | 
| 2001-02-03 | SANTIAGO DE COMPOSTELA | MADRID                 |           120 | 
| 2001-02-02 | SANTIAGO DE COMPOSTELA | MADRID                 |            73 | 
| 2001-03-25 | MADRID                 | SANTIAGO DE COMPOSTELA |            70 | 
| 2001-03-30 | SANTIAGO DE COMPOSTELA | MADRID                 |            70 | 
+------------+------------------------+------------------------+---------------+ 
10 rows IN set (0.00 sec) 



21. Obtenga los diferentes recorridos que se pueden realizar desde una ciudad hasta 
Madrid y haciendo escala llegar a otra ciudad. 

SELECT DISTINCT v1.origen AS origen_inicial, v1.destino AS escala, v2.destino AS destino_final
FROM vuelos v1
JOIN vuelos v2 ON v1.destino = v2.origen
WHERE v1.destino = 'MADRID'
AND v1.origen != v2.destino
AND v1.origen != 'MADRID'
AND v2.destino != 'MADRID'
ORDER BY v1.origen, v2.destino;


+------------------------+---------+------------------------+ 
| origen                 | destino | destino                | 
+------------------------+---------+------------------------+ 
| LA CORU+æA             | MADRID  | BARCELONA              | 
| LA CORU+æA             | MADRID  | BUENOS AIRES           | 
| LA CORU+æA             | MADRID  | CASABLANCA             | 
| LA CORU+æA             | MADRID  | LA CORU+æA             | 
| LA CORU+æA             | MADRID  | LA HABANA              |  
| LA CORU+æA             | MADRID  | LISBOA                 | 
| LA CORU+æA             | MADRID  | PARIS                  | 
| LA CORU+æA             | MADRID  | ROMA                   | 
| LA CORU+æA             | MADRID  | SANTIAGO DE COMPOSTELA | 
| PALMA MALLORCA         | MADRID  | BARCELONA              | 
| PALMA MALLORCA         | MADRID  | BUENOS AIRES           | 
| PALMA MALLORCA         | MADRID  | CASABLANCA             | 
| PALMA MALLORCA         | MADRID  | LA CORU+æA             | 
| PALMA MALLORCA         | MADRID  | LA HABANA              | 
| PALMA MALLORCA         | MADRID  | LISBOA                 | 
| PALMA MALLORCA         | MADRID  | PARIS                  | 
| PALMA MALLORCA         | MADRID  | ROMA                   | 
| PALMA MALLORCA         | MADRID  | SANTIAGO DE COMPOSTELA | 
| ALMERIA                | MADRID  | BARCELONA              | 
| ALMERIA                | MADRID  | BUENOS AIRES           | 
| ALMERIA                | MADRID  | CASABLANCA             | 
| ALMERIA                | MADRID  | LA CORU+æA             | 
| ALMERIA                | MADRID  | LA HABANA              | 
| ALMERIA                | MADRID  | LISBOA                 | 
| ALMERIA                | MADRID  | PARIS                  | 
| ALMERIA                | MADRID  | ROMA                   | 
| ALMERIA                | MADRID  | SANTIAGO DE COMPOSTELA | 
| ALICANTE               | MADRID  | BARCELONA              | 
| ALICANTE               | MADRID  | BUENOS AIRES           | 
| ALICANTE               | MADRID  | CASABLANCA             | 
| ALICANTE               | MADRID  | LA CORU+æA             | 
| ALICANTE               | MADRID  | LA HABANA              | 
| ALICANTE               | MADRID  | LISBOA                 | 
| ALICANTE               | MADRID  | PARIS                  | 
| ALICANTE               | MADRID  | ROMA                   | 
| ALICANTE               | MADRID  | SANTIAGO DE COMPOSTELA | 
| BUENOS AIRES           | MADRID  | BARCELONA              | 
| BUENOS AIRES           | MADRID  | BUENOS AIRES           | 
| BUENOS AIRES           | MADRID  | CASABLANCA             | 
| BUENOS AIRES           | MADRID  | LA CORU+æA             | 
| BUENOS AIRES           | MADRID  | LA HABANA              | 
| BUENOS AIRES           | MADRID  | LISBOA                 | 
| BUENOS AIRES           | MADRID  | PARIS                  | 
| BUENOS AIRES           | MADRID  | ROMA                   | 
| BUENOS AIRES           | MADRID  | SANTIAGO DE COMPOSTELA | 
| SEVILLA                | MADRID  | BARCELONA              | 
| SEVILLA                | MADRID  | BUENOS AIRES           | 
| SEVILLA                | MADRID  | CASABLANCA             | 
| SEVILLA                | MADRID  | LA CORU+æA             | 
| SEVILLA                | MADRID  | LA HABANA              | 
| SEVILLA                | MADRID  | LISBOA                 | 
| SEVILLA                | MADRID  | PARIS                  | 
| SEVILLA                | MADRID  | ROMA                   | 
| SEVILLA                | MADRID  | SANTIAGO DE COMPOSTELA | 
| BILBAO                 | MADRID  | BARCELONA              | 
| BILBAO                 | MADRID  | BUENOS AIRES           | 
| BILBAO                 | MADRID  | CASABLANCA             | 
| BILBAO                 | MADRID  | LA CORU+æA             | 
| BILBAO                 | MADRID  | LA HABANA              | 
| BILBAO                 | MADRID  | LISBOA                 | 
| BILBAO                 | MADRID  | PARIS                  | 
| BILBAO                 | MADRID  | ROMA                   | 
| BILBAO                 | MADRID  | SANTIAGO DE COMPOSTELA | 
| SANTIAGO DE COMPOSTELA | MADRID  | BARCELONA              | 
| SANTIAGO DE COMPOSTELA | MADRID  | BUENOS AIRES           | 
| SANTIAGO DE COMPOSTELA | MADRID  | CASABLANCA             | 
| SANTIAGO DE COMPOSTELA | MADRID  | LA CORU+æA             | 
| SANTIAGO DE COMPOSTELA | MADRID  | LA HABANA              | 
| SANTIAGO DE COMPOSTELA | MADRID  | LISBOA                 | 
| SANTIAGO DE COMPOSTELA | MADRID  | PARIS                  | 
| SANTIAGO DE COMPOSTELA | MADRID  | ROMA                   | 
| SANTIAGO DE COMPOSTELA | MADRID  | SANTIAGO DE COMPOSTELA | 
| GRAN CANARIA           | MADRID  | BARCELONA              | 
| GRAN CANARIA           | MADRID  | BUENOS AIRES           | 
| GRAN CANARIA           | MADRID  | CASABLANCA             | 
| GRAN CANARIA           | MADRID  | LA CORU+æA             | 
| GRAN CANARIA           | MADRID  | LA HABANA              | 
| GRAN CANARIA           | MADRID  | LISBOA                 | 
| GRAN CANARIA           | MADRID  | PARIS                  | 
| GRAN CANARIA           | MADRID  | ROMA                   | 
| GRAN CANARIA           | MADRID  | SANTIAGO DE COMPOSTELA | 
| BARCELONA              | MADRID  | BARCELONA              | 
| BARCELONA              | MADRID  | BUENOS AIRES           | 
| BARCELONA              | MADRID  | CASABLANCA             | 
| BARCELONA              | MADRID  | LA CORU+æA             | 
| BARCELONA              | MADRID  | LA HABANA              | 
| BARCELONA              | MADRID  | LISBOA                 | 
| BARCELONA              | MADRID  | PARIS                  | 
| BARCELONA              | MADRID  | ROMA                   | 
| BARCELONA              | MADRID  | SANTIAGO DE COMPOSTELA | 
| TENERIFE               | MADRID  | BARCELONA              | 
| TENERIFE               | MADRID  | BUENOS AIRES           | 
| TENERIFE               | MADRID  | CASABLANCA             | 
| TENERIFE               | MADRID  | LA CORU+æA             | 
| TENERIFE               | MADRID  | LA HABANA              | 
| TENERIFE               | MADRID  | LISBOA                 | 
| TENERIFE               | MADRID  | PARIS                  | 
| TENERIFE               | MADRID  | ROMA                   | 
| TENERIFE               | MADRID  | SANTIAGO DE COMPOSTELA | 
| LISBOA                 | MADRID  | BARCELONA              | 
| LISBOA                 | MADRID  | BUENOS AIRES           | 
| LISBOA                 | MADRID  | CASABLANCA             | 
| LISBOA                 | MADRID  | LA CORU+æA             | 
| LISBOA                 | MADRID  | LA HABANA              | 
| LISBOA                 | MADRID  | LISBOA                 | 
| LISBOA                 | MADRID  | PARIS                  | 
| LISBOA                 | MADRID  | ROMA                   | 
| LISBOA                 | MADRID  | SANTIAGO DE COMPOSTELA | 
| AMSTERDAM              | MADRID  | BARCELONA              | 
| AMSTERDAM              | MADRID  | BUENOS AIRES           | 
| AMSTERDAM              | MADRID  | CASABLANCA             | 
| AMSTERDAM              | MADRID  | LA CORU+æA             | 
| AMSTERDAM              | MADRID  | LA HABANA              | 
| AMSTERDAM              | MADRID  | LISBOA                 | 
| AMSTERDAM              | MADRID  | PARIS                  | 
| AMSTERDAM              | MADRID  | ROMA                   | 
| AMSTERDAM              | MADRID  | SANTIAGO DE COMPOSTELA | 
| PARIS                  | MADRID  | BARCELONA              | 
| PARIS                  | MADRID  | BUENOS AIRES           | 
| PARIS                  | MADRID  | CASABLANCA             | 
| PARIS                  | MADRID  | LA CORU+æA             | 
| PARIS                  | MADRID  | LA HABANA              | 
| PARIS                  | MADRID  | LISBOA                 | 
| PARIS                  | MADRID  | PARIS                  | 
| PARIS                  | MADRID  | ROMA                   | 
| PARIS                  | MADRID  | SANTIAGO DE COMPOSTELA | 
| ROMA                   | MADRID  | BARCELONA              | 
| ROMA                   | MADRID  | BUENOS AIRES           | 
| ROMA                   | MADRID  | CASABLANCA             | 
| ROMA                   | MADRID  | LA CORU+æA             | 
| ROMA                   | MADRID  | LA HABANA              | 
| ROMA                   | MADRID  | LISBOA                 | 
| ROMA                   | MADRID  | PARIS                  | 
| ROMA                   | MADRID  | ROMA                   | 
| ROMA                   | MADRID  | SANTIAGO DE COMPOSTELA | 
| LA HABANA              | MADRID  | BARCELONA              | 
| LA HABANA              | MADRID  | BUENOS AIRES           | 
| LA HABANA              | MADRID  | CASABLANCA             | 
| LA HABANA              | MADRID  | LA CORU+æA             | 
| LA HABANA              | MADRID  | LA HABANA              | 
| LA HABANA              | MADRID  | LISBOA                 | 
| LA HABANA              | MADRID  | PARIS                  | 
| LA HABANA              | MADRID  | ROMA                   | 
| LA HABANA              | MADRID  | SANTIAGO DE COMPOSTELA | 
+------------------------+---------+------------------------+ 
144 rows IN set (0.01 sec) 



22. Obtenga, en una sola columna, los nombres de todas las ciudades que aparecen en la 
tabla de vuelos, ordenados alfabéticamente. 
 
SELECT origen AS ciudad FROM vuelos
UNION
SELECT destino AS ciudad FROM vuelos
ORDER BY ciudad;


+------------------------+ 
| origen                 | 
+------------------------+ 
| ALICANTE               | 
| ALMERIA                | 
| AMSTERDAM              | 
| BARCELONA              | 
| BERLIN                 | 
| BILBAO                 | 
| BOGOTA                 | 
| BUENOS AIRES           | 
| CANCUN                 | 
| CARACAS                | 
| CASABLANCA             | 
| FUERTEVENTURA          | 
| GRAN CANARIA           | 
| HANOVER                | 
| HIERRO                 | 
| LA CORU+æA             | 
| LA HABANA              | 
| LANZAROTE              | 
| LISBOA                 | 
| LONDRES                | 
| MADRID                 | 
| MALAGA                 | 
| MELILLA                | 
| PALMA MALLORCA         | 
| PARIS                  | 
| ROMA                   | 
| SANTIAGO DE CHILE      | 
| SANTIAGO DE COMPOSTELA | 
| SEVILLA                | 
| TENERIFE               | 
+------------------------+ 
30 rows IN set (0.01 sec) 
 
 
 
23. Obtenga en una sola columna el nombre de todas las ciudades origen de un vuelo y el 
de las que son destino de un vuelo. (Una misma ciudad puede aparecer como origen y 
como destino.) 
 
SELECT origen AS ciudad FROM vuelos
UNION ALL
SELECT destino AS ciudad FROM vuelos
ORDER BY ciudad;


+------------------------+
| origen                 | 
+------------------------+ 
| ALICANTE               | 
| ALMERIA                | 
| AMSTERDAM              | 
| BARCELONA              | 
| BILBAO                 | 
| BUENOS AIRES           | 
| CASABLANCA             | 
| FUERTEVENTURA          | 
| GRAN CANARIA           | 
| LA CORU+æA             | 
| LA HABANA              | 
| LISBOA                 | 
| MADRID                 | 
| PALMA MALLORCA         | 
| PARIS                  | 
| ROMA                   | 
| SANTIAGO DE CHILE      | 
| SANTIAGO DE COMPOSTELA | 
| SEVILLA                | 
| TENERIFE               | 
| ALICANTE               | 
| ALMERIA                | 
| AMSTERDAM              | 
| BARCELONA              | 
| BERLIN                 | 
| BILBAO                 | 
| BOGOTA                 | 
| BUENOS AIRES           | 
| CANCUN                 | 
| CARACAS                | 
| CASABLANCA             | 
| FUERTEVENTURA          | 
| GRAN CANARIA           | 
| HANOVER                | 
| HIERRO                 | 
| LA CORU+æA             | 
| LA HABANA              | 
| LANZAROTE              | 
| LISBOA                 | 
| LONDRES                | 
| MADRID                 | 
| MALAGA                 | 
| MELILLA                | 
| PARIS                  | 
| ROMA                   | 
| SANTIAGO DE COMPOSTELA | 
| SEVILLA                | 
| TENERIFE               | 
+------------------------+ 
48 rows IN set (0.00 sec) 
 
24. Obtenga en dos columnas, para cada ciudad que es origen, el número de vuelos que 
salen de ella y luego para cada una que es destino, el número de vuelos que recibe. 

SELECT origen AS ciudad, COUNT(*) AS vuelos_salen
FROM vuelos
GROUP BY origen

UNION

SELECT destino AS ciudad, COUNT(*) AS vuelos_llegan
FROM vuelos
GROUP BY destino

ORDER BY ciudad;


+------------------------+----------------+ 
| destino                | count(destino) | 
+------------------------+----------------+ 
| ALICANTE               |              6 | 
| ALMERIA                |              3 | 
| AMSTERDAM              |              9 | 
| BARCELONA              |             16 | 
| BERLIN                 |              1 | 
| BILBAO                 |              3 | 
| BOGOTA                 |              1 | 
| BUENOS AIRES           |              4 | 
| CANCUN                 |              1 | 
| CARACAS                |              1 | 
| CASABLANCA             |              1 | 
| FUERTEVENTURA          |              2 | 
| GRAN CANARIA           |              6 | 
| HANOVER                |              1 | 
| HIERRO                 |              2 | 
| LA CORU+æA             |              5 | 
| LA HABANA              |              1 | 
| LANZAROTE              |              3 | 
| LISBOA                 |              2 | 
| LONDRES                |              2 | 
| MADRID                 |             35 | 
| MALAGA                 |              4 | 
| MELILLA                |              1 | 
| PARIS                  |              3 | 
| ROMA                   |              2 | 
| SANTIAGO DE COMPOSTELA |              5 | 
| SEVILLA                |              2 | 
| TENERIFE               |              4 | 
| ALICANTE               |             14 | 
| ALMERIA                |              6 | 
| AMSTERDAM              |              7 | 
| BARCELONA              |             23 | 
| BILBAO                 |              9 | 
| BUENOS AIRES           |              9 | 
| FUERTEVENTURA          |              4 | 
| GRAN CANARIA           |              9 | 
| LA CORU+æA             |              2 | 
| MADRID                 |             19 | 
| PALMA MALLORCA         |              2 | 
| ROMA                   |              4 | 
| SANTIAGO DE CHILE      |              2 | 
| SANTIAGO DE COMPOSTELA |              3 | 
+------------------------+----------------+ 
42 rows IN set (0.00 sec) 
 
 
25. Obtenga en tres columnas, para cada ciudad que aparece en la tabla vuelos, su 
nombre ordenado alfabéticamente, el total de vuelos que parten de ella y el total de 
vuelos que llegan a ella. Si no llega o no parte ningún vuelo, debe aparecer cero en la 
columna correspondiente. 
 

SELECT
    origen AS ciudad, 
    COUNT(*) AS salidas,
    0 AS llegadas    
FROM vuelos
GROUP BY origen

UNION

SELECT
    destino AS ciudad,
    0 AS salidas,     
    COUNT(*) AS llegadas
FROM vuelos
GROUP BY destino

ORDER BY ciudad, salidas DESC;


+------------------------+----+----------------+ 
| destino                | 0  | count(destino) | 
+------------------------+----+----------------+ 
| ALICANTE               |  0 |              6 | 
| ALICANTE               | 14 |              0 | 
| ALMERIA                |  0 |              3 | 
| ALMERIA                |  6 |              0 | 
| AMSTERDAM              |  0 |              9 | 
| AMSTERDAM              |  7 |              0 | 
| BARCELONA              |  0 |             16 | 
| BARCELONA              | 23 |              0 | 
| BERLIN                 |  0 |              1 | 
| BILBAO                 |  0 |              3 | 
| BILBAO                 |  9 |              0 | 
| BOGOTA                 |  0 |              1 | 
| BUENOS AIRES           |  0 |              4 | 
| BUENOS AIRES           |  9 |              0 | 
| CANCUN                 |  0 |              1 | 
| CARACAS                |  0 |              1 | 
| CASABLANCA             |  0 |              1 | 
| CASABLANCA             |  1 |              0 | 
| FUERTEVENTURA          |  0 |              2 | 
| FUERTEVENTURA          |  4 |              0 | 
| GRAN CANARIA           |  0 |              6 | 
| GRAN CANARIA           |  9 |              0 | 
| HANOVER                |  0 |              1 | 
| HIERRO                 |  0 |              2 | 
| LA CORU+æA             |  0 |              5 | 
| LA CORU+æA             |  2 |              0 | 
| LA HABANA              |  0 |              1 | 
| LA HABANA              |  1 |              0 | 
| LANZAROTE              |  0 |              3 | 
| LISBOA                 |  0 |              2 | 
| LISBOA                 |  2 |              0 | 
| LONDRES                |  0 |              2 | 
| MADRID                 |  0 |             35 | 
| MADRID                 | 19 |              0 | 
| MALAGA                 |  0 |              4 | 
| MELILLA                |  0 |              1 | 
| PALMA MALLORCA         |  2 |              0 | 
| PARIS                  |  0 |              3 | 
| PARIS                  |  3 |              0 | 
| ROMA                   |  0 |              2 | 
| ROMA                   |  4 |              0 | 
| SANTIAGO DE CHILE      |  2 |              0 | 
| SANTIAGO DE COMPOSTELA |  0 |              5 | 
| SANTIAGO DE COMPOSTELA |  3 |              0 | 
| SEVILLA                |  0 |              2 | 
| SEVILLA                |  2 |              0 | 
| TENERIFE               |  0 |              4 | 
| TENERIFE               |  4 |              0 | 
+------------------------+----+----------------+ 
48 rows IN set (0.00 sec) 
 
 
26. Obtenga en dos columnas, las diferentes fechas de llegada reflejadas en los partes de 
vuelo con el menor combustible consumido en cada una de ellas y, a continuación, estas 
mismas fechas con el mayor combustible consumido en cada una de ellas. 

SELECT fecha, consumo
FROM (
    SELECT
        fecha,
        MAX(comb_consumido) AS consumo,
        1 AS tipo_resultado
    FROM partes
    GROUP BY fecha

    UNION

    SELECT
        fecha,
        MIN(comb_consumido) AS consumo,
        2 AS tipo_resultado
    FROM partes
    GROUP BY fecha
) AS resultados_combinados
ORDER BY tipo_resultado ASC, fecha ASC;         
 
+------------+---------------------+ 
| fecha      | max(comb_consumido) | 
+------------+---------------------+ 
| 1996-01-05 |                9660 | 
| 1996-01-06 |               11500 | 
| 1996-01-07 |               10235 | 
| 1996-01-08 |               10350 | 
| 1996-01-09 |               10350 | 
| 1996-01-10 |                5175 | 
| 1996-01-11 |                2530 | 
| 1996-01-12 |                5175 | 
| 1996-01-14 |                3450 | 
| 1996-01-15 |                2300 | 
| 1996-01-16 |                2875 | 
| 1996-01-17 |                2875 | 
| 1996-01-18 |                3105 | 
| 1996-01-19 |                2875 | 
| 1996-01-20 |                9660 | 
| 1996-01-21 |                2300 | 
| 1996-01-22 |                1265 | 
| 1996-02-01 |                2645 | 
| 1996-02-02 |                9660 | 
| 1996-02-03 |               14605 | 
| 1996-02-04 |                2300 | 
| 1996-02-05 |                1150 | 
| 1996-02-06 |                7590 | 
| 1996-02-07 |                2875 | 
| 1996-02-08 |                2300 | 
| 1996-02-09 |               10120 | 
| 1996-02-10 |                2300 | 
| 1996-02-11 |                NULL | 
| 1996-02-12 |                2300 | 
| 1996-02-14 |                8165 | 
| 1996-02-15 |                5060 | 
| 1996-02-16 |                5060 | 
| 1996-02-17 |                5175 | 
| 1996-02-18 |                5175 | 
| 1996-02-19 |                3450 | 
| 1996-02-20 |                2300 | 
| 1996-02-21 |                 690 | 
| 1996-02-22 |                7705 | 
| 1996-01-05 |                5290 | 
| 1996-01-06 |                1265 | 
| 1996-01-07 |                1265 | 
| 1996-01-08 |                1150 | 
| 1996-01-09 |                 920 | 
| 1996-01-10 |                1265 | 
| 1996-01-12 |                2300 | 
| 1996-01-16 |                2300 | 
| 1996-01-18 |                2875 | 
| 1996-01-19 |                2300 | 
| 1996-01-20 |                9430 | 
| 1996-01-21 |                1265 | 
| 1996-02-03 |                 805 | 
| 1996-02-04 |                 805 | 
| 1996-02-05 |                 805 | 
| 1996-02-06 |                 690 | 
| 1996-02-07 |                 805 | 
| 1996-02-09 |                5750 | 
| 1996-02-12 |                 920 | 
| 1996-02-14 |                 230 | 
| 1996-02-15 |                3450 | 
| 1996-02-16 |                2530 | 
| 1996-02-17 |                3220 | 
| 1996-02-18 |                3450 | 
| 1996-02-19 |                2300 | 
| 1996-02-20 |                1265 | 
| 1996-02-22 |                 920 | 
+------------+---------------------+ 
65 rows IN set (0.00 sec) 