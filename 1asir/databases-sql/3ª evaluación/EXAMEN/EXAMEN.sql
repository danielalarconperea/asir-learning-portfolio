-- Examen 3º Evaluación

-- 1º

SELECT * FROM aviones
WHERE butacas > 200
AND envergadura > 100;

-- 2º

SELECT * FROM vuelos
WHERE origen = 'Madrid'
AND hora_salida BETWEEN '08:00' AND '12:00';

-- 3º -----

SELECT COUNT(r.num_vuelo), a.nombre FROM reservas r
INNER JOIN agencias a ON r.agencia=a.code
WHERE r.plazas > 50
GROUP BY r.agencia;

-- 4º

SELECT AVG(v.distancia) AS 'distancia promedio' FROM vuelos v 
INNER JOIN aviones a ON a.tipo=v.tipo_avion
WHERE a.descripcion = 'Airbus A320';

-- 5º

SELECT * FROM companias
WHERE code NOT IN (SELECT SUBSTR(num_vuelo, 1, 2) FROM reservas);

-- 6º

SELECT * FROM partes 
WHERE SUBSTR(fecha,1,4) = '1996'
AND comb_consumido IN (SELECT max(comb_consumido) FROM partes GROUP BY mat);

-- 7º

SELECT v.num_vuelo, v.destino FROM vuelos v
WHERE EXISTS (
    SELECT 1 FROM aviones a 
    WHERE a.tipo=v.tipo_avion
    AND v.distancia > (
        SELECT AVG(distancia) FROM vuelos v1
        WHERE EXISTS (
            SELECT 1 FROM aviones a1 
            WHERE a1.tipo=v1.tipo_avion
            AND SUBSTR(a1.descripcion,1,2)='Ai'
        )
    )
    AND a.butacas >= 150
);

-- 8º

SELECT 
    c.nombre, 
    COUNT(a.tipo) AS número_de_aviones, 
    COUNT(DISTINCT a.tipo) AS 'número de modelos diferentes'
FROM vuelos v
RIGHT JOIN companias c ON SUBSTR(v.num_vuelo,1,2)=c.code
INNER JOIN aviones a ON a.tipo = v.tipo_avion
GROUP BY c.code
HAVING COUNT(a.tipo) > 5
ORDER BY número_de_aviones DESC;

-- 9º

SELECT origen FROM vuelos
UNION
SELECT destino FROM vuelos;

-- 10º

SELECT v.num_vuelo, c.nombre FROM vuelos v
INNER JOIN companias c ON SUBSTR(v.num_vuelo,1,2)=c.code
WHERE c.code = 'IB'
UNION
SELECT v.num_vuelo, c.nombre FROM vuelos v
INNER JOIN companias c ON SUBSTR(v.num_vuelo,1,2)=c.code
WHERE c.code = 'AE';