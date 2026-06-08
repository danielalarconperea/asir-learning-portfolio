Okay, here are the solutions to the exercises from the provided PDF, using the `aeropuerto.txt` schema. Each query is presented in the three requested formats (Subquery, JOIN, EXISTS) where applicable and logical.

---

**Schema Overview (Relevant Tables for Queries):**

*   `aviones`: Information about aircraft types (tipo, longitud, envergadura, butacas, alcance).
*   `vuelos`: Flight details (num_vuelo, origen, destino, hora_salida, hora_llegada, distancia, tipo_avion).
*   `partes`: Flight reports (num_parte, num_vuelo, mat, fecha, hora_salida, hora_llegada, comb_consumido).
*   `flota`: Links specific aircraft (matricula) to types (tipo_avion) and companies (compania).
*   `reservas`: Reservations (num_vuelo, fecha, agencia, plazas).
*   `aeropuertos`: Airport codes (IATA) and locations (localidad).
*   `companias`: Airline companies (code, nombre).

---

**1. Obtenga los tipos de avión, el doble de su envergadura y el cuadrado de su longitud para aquellos aviones con longitud menor que la media y que realizan vuelos con origen o destino en una ciudad que comience por la letra 'M', ordenándolos de mayor a menor envergadura.**

*   **Subquery:**
    ```sql
    SELECT DISTINCT
        tipo,
        envergadura * 2 AS doble_envergadura,
        longitud * longitud AS longitud_cuadrado
    FROM
        aviones
    WHERE
        longitud < (SELECT AVG(longitud) FROM aviones)
      AND tipo IN (SELECT DISTINCT tipo_avion
                   FROM vuelos
                   WHERE origen LIKE 'M%' OR destino LIKE 'M%')
    ORDER BY
        doble_envergadura DESC;
    ```
*   **JOIN:**
    ```sql
    SELECT DISTINCT
        a.tipo,
        a.envergadura * 2 AS doble_envergadura,
        a.longitud * a.longitud AS longitud_cuadrado
    FROM
        aviones a
    JOIN
        vuelos v ON a.tipo = v.tipo_avion
    WHERE
        a.longitud < (SELECT AVG(longitud) FROM aviones)
      AND (v.origen LIKE 'M%' OR v.destino LIKE 'M%')
    ORDER BY
        doble_envergadura DESC;
    ```
*   **EXISTS:**
    ```sql
    SELECT DISTINCT
        a.tipo,
        a.envergadura * 2 AS doble_envergadura,
        a.longitud * a.longitud AS longitud_cuadrado
    FROM
        aviones a
    WHERE
        a.longitud < (SELECT AVG(longitud) FROM aviones)
      AND EXISTS (SELECT 1
                  FROM vuelos v
                  WHERE v.tipo_avion = a.tipo
                    AND (v.origen LIKE 'M%' OR v.destino LIKE 'M%'))
    ORDER BY
        doble_envergadura DESC;
    ```

**2. Obtenga las tres primeras letras de los orígenes y destinos de los vuelos realizados por aviones con longitud mayor que la media y envergadura menor que 2/3 la máxima envergadura, ordenados alfabéticamente por destino.**

*   **Subquery:**
    ```sql
    SELECT
        LEFT(v.origen, 3) AS origen_3,
        LEFT(v.destino, 3) AS destino_3
    FROM
        vuelos v
    WHERE
        v.tipo_avion IN (SELECT tipo
                         FROM aviones
                         WHERE longitud > (SELECT AVG(longitud) FROM aviones)
                           AND envergadura < (SELECT MAX(envergadura) * 2/3 FROM aviones))
    ORDER BY
        destino_3;
    ```
*   **JOIN:**
    ```sql
    SELECT
        LEFT(v.origen, 3) AS origen_3,
        LEFT(v.destino, 3) AS destino_3
    FROM
        vuelos v
    JOIN
        aviones a ON v.tipo_avion = a.tipo
    WHERE
        a.longitud > (SELECT AVG(longitud) FROM aviones)
      AND a.envergadura < (SELECT MAX(envergadura) * 2/3 FROM aviones)
    ORDER BY
        destino_3;
    ```
*   **EXISTS:**
    ```sql
    SELECT
        LEFT(v.origen, 3) AS origen_3,
        LEFT(v.destino, 3) AS destino_3
    FROM
        vuelos v
    WHERE EXISTS (SELECT 1
                  FROM aviones a
                  WHERE a.tipo = v.tipo_avion
                    AND a.longitud > (SELECT AVG(longitud) FROM aviones)
                    AND a.envergadura < (SELECT MAX(envergadura) * 2/3 FROM aviones))
    ORDER BY
        destino_3;
    ```

**3. Obtenga los dos primeros caracteres de los números de vuelo y el origen de los vuelos a los que corresponden partes con número de parte entre 400 y 450 y que recorren distancias mayores que la media, ordenándolos alfabéticamente por origen.**

*   **Subquery:**
    ```sql
    SELECT DISTINCT
        LEFT(v.num_vuelo, 2) AS vuelo_2,
        v.origen
    FROM
        vuelos v
    WHERE
        v.num_vuelo IN (SELECT num_vuelo FROM partes WHERE num_parte BETWEEN 400 AND 450)
      AND v.distancia > (SELECT AVG(distancia) FROM vuelos WHERE distancia IS NOT NULL) -- Added IS NOT NULL check for AVG
    ORDER BY
        v.origen;
    ```
*   **JOIN:**
    ```sql
    SELECT DISTINCT
        LEFT(v.num_vuelo, 2) AS vuelo_2,
        v.origen
    FROM
        vuelos v
    JOIN
        partes p ON v.num_vuelo = p.num_vuelo
    WHERE
        p.num_parte BETWEEN 400 AND 450
      AND v.distancia > (SELECT AVG(distancia) FROM vuelos WHERE distancia IS NOT NULL)
    ORDER BY
        v.origen;
    ```
*   **EXISTS:**
    ```sql
    SELECT DISTINCT
        LEFT(v.num_vuelo, 2) AS vuelo_2,
        v.origen
    FROM
        vuelos v
    WHERE
        EXISTS (SELECT 1
                FROM partes p
                WHERE p.num_vuelo = v.num_vuelo
                  AND p.num_parte BETWEEN 400 AND 450)
      AND v.distancia > (SELECT AVG(distancia) FROM vuelos WHERE distancia IS NOT NULL)
    ORDER BY
        v.origen;
    ```

**4. Obtenga los números de vuelo, las tres primeras letras del origen y las tres primeras letras del destino para los vuelos realizados por aviones cuyo alcance sea mayor que la media de todos y con longitud menor que 2/3 la máxima longitud, ordenándolos por número de vuelo.**

*   **Subquery:**
    ```sql
    SELECT
        v.num_vuelo,
        LEFT(v.origen, 3) AS origen_3,
        LEFT(v.destino, 3) AS destino_3
    FROM
        vuelos v
    WHERE
        v.tipo_avion IN (SELECT tipo
                         FROM aviones
                         WHERE alcance > (SELECT AVG(alcance) FROM aviones)
                           AND longitud < (SELECT MAX(longitud) * 2/3 FROM aviones))
    ORDER BY
        v.num_vuelo;
    ```
*   **JOIN:**
    ```sql
    SELECT
        v.num_vuelo,
        LEFT(v.origen, 3) AS origen_3,
        LEFT(v.destino, 3) AS destino_3
    FROM
        vuelos v
    JOIN
        aviones a ON v.tipo_avion = a.tipo
    WHERE
        a.alcance > (SELECT AVG(alcance) FROM aviones)
      AND a.longitud < (SELECT MAX(longitud) * 2/3 FROM aviones)
    ORDER BY
        v.num_vuelo;
    ```
*   **EXISTS:**
    ```sql
    SELECT
        v.num_vuelo,
        LEFT(v.origen, 3) AS origen_3,
        LEFT(v.destino, 3) AS destino_3
    FROM
        vuelos v
    WHERE EXISTS (SELECT 1
                  FROM aviones a
                  WHERE a.tipo = v.tipo_avion
                    AND a.alcance > (SELECT AVG(alcance) FROM aviones)
                    AND a.longitud < (SELECT MAX(longitud) * 2/3 FROM aviones))
    ORDER BY
        v.num_vuelo;
    ```

**5. Recupere todas las características de los aviones que nunca han pasado por Barcelona.** (Pasar por = origen o destino)

*   **Subquery (NOT IN):**
    ```sql
    SELECT *
    FROM aviones
    WHERE tipo NOT IN (SELECT DISTINCT tipo_avion
                       FROM vuelos
                       WHERE origen = 'BARCELONA' OR destino = 'BARCELONA');
    ```
*   **LEFT JOIN / IS NULL:** (JOIN based approach)
    ```sql
    SELECT a.*
    FROM aviones a
    LEFT JOIN (SELECT DISTINCT tipo_avion FROM vuelos WHERE origen = 'BARCELONA' OR destino = 'BARCELONA') AS v_bcn
        ON a.tipo = v_bcn.tipo_avion
    WHERE v_bcn.tipo_avion IS NULL;
    ```
    *Alternative JOIN (less efficient usually):*
    ```sql
    SELECT a.*
    FROM aviones a
    LEFT JOIN vuelos v
        ON a.tipo = v.tipo_avion AND (v.origen = 'BARCELONA' OR v.destino = 'BARCELONA')
    GROUP BY a.tipo -- Group by all columns of aviones or just the PK
    HAVING COUNT(v.num_vuelo) = 0;
    ```
*   **EXISTS (NOT EXISTS):**
    ```sql
    SELECT *
    FROM aviones a
    WHERE NOT EXISTS (SELECT 1
                      FROM vuelos v
                      WHERE v.tipo_avion = a.tipo
                        AND (v.origen = 'BARCELONA' OR v.destino = 'BARCELONA'));
    ```

**6. Indique los tipos de avión, el doble de su longitud y su envergadura, para los aviones con envergadura mayor que la media y que realicen vuelos desde o hacia Madrid, ordenándolos de mayor a menor longitud.**

*   **Subquery:**
    ```sql
    SELECT DISTINCT
        tipo,
        longitud * 2 AS doble_longitud,
        envergadura
    FROM
        aviones
    WHERE
        envergadura > (SELECT AVG(envergadura) FROM aviones)
      AND tipo IN (SELECT DISTINCT tipo_avion
                   FROM vuelos
                   WHERE origen = 'MADRID' OR destino = 'MADRID')
    ORDER BY
        longitud DESC; -- Order by original longitud
    ```
*   **JOIN:**
    ```sql
    SELECT DISTINCT
        a.tipo,
        a.longitud * 2 AS doble_longitud,
        a.envergadura
    FROM
        aviones a
    JOIN
        vuelos v ON a.tipo = v.tipo_avion
    WHERE
        a.envergadura > (SELECT AVG(envergadura) FROM aviones)
      AND (v.origen = 'MADRID' OR v.destino = 'MADRID')
    ORDER BY
        a.longitud DESC;
    ```
*   **EXISTS:**
    ```sql
    SELECT DISTINCT
        a.tipo,
        a.longitud * 2 AS doble_longitud,
        a.envergadura
    FROM
        aviones a
    WHERE
        a.envergadura > (SELECT AVG(envergadura) FROM aviones)
      AND EXISTS (SELECT 1
                  FROM vuelos v
                  WHERE v.tipo_avion = a.tipo
                    AND (v.origen = 'MADRID' OR v.destino = 'MADRID'))
    ORDER BY
        a.longitud DESC;
    ```

**7. Obtenga, para cada destino, la mayor distancia recorrida hacia él, por vuelos realizados por aviones con longitud mayor que la media, ordenados alfabéticamente.**

*   **Subquery:** (Harder to do purely with subqueries without aggregation in outer query)
    ```sql
    -- This structure requires aggregation in the outer query, naturally lending itself to JOIN/GROUP BY
    SELECT
        v.destino,
        MAX(v.distancia) AS max_distancia
    FROM
        vuelos v
    WHERE
        v.tipo_avion IN (SELECT tipo FROM aviones WHERE longitud > (SELECT AVG(longitud) FROM aviones))
      AND v.distancia IS NOT NULL -- Ensure distance is not NULL for MAX
    GROUP BY
        v.destino
    ORDER BY
        v.destino;
    ```
*   **JOIN:**
    ```sql
    SELECT
        v.destino,
        MAX(v.distancia) AS max_distancia
    FROM
        vuelos v
    JOIN
        aviones a ON v.tipo_avion = a.tipo
    WHERE
        a.longitud > (SELECT AVG(longitud) FROM aviones)
      AND v.distancia IS NOT NULL
    GROUP BY
        v.destino
    ORDER BY
        v.destino;
    ```
*   **EXISTS:** (Similar to subquery, EXISTS checks condition, outer query aggregates)
    ```sql
    SELECT
        v.destino,
        MAX(v.distancia) AS max_distancia
    FROM
        vuelos v
    WHERE EXISTS (SELECT 1
                  FROM aviones a
                  WHERE a.tipo = v.tipo_avion
                    AND a.longitud > (SELECT AVG(longitud) FROM aviones))
      AND v.distancia IS NOT NULL
    GROUP BY
        v.destino
    ORDER BY
        v.destino;
    ```

**8. Obtenga, para cada origen, la menor distancia recorrida desde él por vuelos realizados por aviones con menos butacas que la media, ordenados alfabéticamente.**

*   **Subquery:**
    ```sql
    SELECT
        v.origen,
        MIN(v.distancia) AS min_distancia
    FROM
        vuelos v
    WHERE
        v.tipo_avion IN (SELECT tipo FROM aviones WHERE butacas < (SELECT AVG(butacas) FROM aviones))
      AND v.distancia IS NOT NULL
    GROUP BY
        v.origen
    ORDER BY
        v.origen;
    ```
*   **JOIN:**
    ```sql
    SELECT
        v.origen,
        MIN(v.distancia) AS min_distancia
    FROM
        vuelos v
    JOIN
        aviones a ON v.tipo_avion = a.tipo
    WHERE
        a.butacas < (SELECT AVG(butacas) FROM aviones)
      AND v.distancia IS NOT NULL
    GROUP BY
        v.origen
    ORDER BY
        v.origen;
    ```
*   **EXISTS:**
    ```sql
    SELECT
        v.origen,
        MIN(v.distancia) AS min_distancia
    FROM
        vuelos v
    WHERE EXISTS (SELECT 1
                  FROM aviones a
                  WHERE a.tipo = v.tipo_avion
                    AND a.butacas < (SELECT AVG(butacas) FROM aviones))
      AND v.distancia IS NOT NULL
    GROUP BY
        v.origen
    ORDER BY
        v.origen;
    ```

**9. Indique el total de plazas reservadas existentes para cada número de vuelo de Iberia.** (Assuming Iberia is company 'IB')

*   **Subquery:** (Less direct, needs linking flight numbers to company 'IB')
    ```sql
    SELECT
        r.num_vuelo,
        SUM(r.plazas) AS total_plazas
    FROM
        reservas r
    WHERE
        r.num_vuelo IN ( -- Need to find IB flights. Assumes num_vuelo format doesn't directly indicate company
             SELECT DISTINCT p.num_vuelo -- Use partes table to link flight number to a plane...
             FROM partes p
             JOIN flota f ON p.mat = f.matricula
             WHERE f.compania = 'IB'
             -- Alternative: If num_vuelo *prefix* indicates company (like 'IBxxxx'):
             -- WHERE r.num_vuelo LIKE 'IB%' -- This depends on naming convention
        )
    GROUP BY
        r.num_vuelo
    ORDER BY
        r.num_vuelo;

    -- Simpler if assuming flight number prefix 'IB' means Iberia:
    SELECT
        num_vuelo,
        SUM(plazas) AS total_plazas
    FROM
        reservas
    WHERE num_vuelo LIKE 'IB%' -- Assumption about num_vuelo format
    GROUP BY
        num_vuelo
    ORDER BY
        num_vuelo;
    ```
*   **JOIN:** (Assuming 'IB%' prefix for Iberia flights)
    ```sql
    -- If assumption holds:
    SELECT
        r.num_vuelo,
        SUM(r.plazas) AS total_plazas
    FROM
        reservas r
    WHERE r.num_vuelo LIKE 'IB%' -- Filter directly
    GROUP BY
        r.num_vuelo
    ORDER BY
        r.num_vuelo;
    -- If assumption doesn't hold, need more joins:
    SELECT
        r.num_vuelo,
        SUM(r.plazas) AS total_plazas
    FROM
        reservas r
    JOIN -- Requires linking reservas -> vuelos -> partes -> flota -> companias - Complex!
         -- Let's assume the 'IB%' prefix is intended based on the data.
        partes p ON r.num_vuelo = p.num_vuelo AND r.fecha = p.fecha -- Need date potentially? Schema ambiguous. Let's ignore date for simplicity or assume one part per flight.
    JOIN
        flota f ON p.mat = f.matricula
    WHERE
        f.compania = 'IB'
    GROUP BY
        r.num_vuelo
    ORDER BY
        r.num_vuelo;
     -- The simplest interpretation (and likely intended one) relies on num_vuelo starting with 'IB'
    ```
*   **EXISTS:** (Assuming 'IB%' prefix)
    ```sql
    -- If assumption holds:
     SELECT
        num_vuelo,
        SUM(plazas) AS total_plazas
    FROM
        reservas r
    WHERE r.num_vuelo LIKE 'IB%'
    GROUP BY
        num_vuelo
    ORDER BY
        num_vuelo;
    -- If assumption doesn't hold (EXISTS is awkward for this aggregation)
    -- EXISTS is typically for filtering rows, not for selecting rows based on a related property needed for the group. The JOIN or Subquery (with prefix assumption) is more natural.
    ```
    *Note: Based on the sample output showing only 'IBxxxx' flights, the assumption `WHERE num_vuelo LIKE 'IB%'` seems correct and simplest.*

**10. Indique a cuántos destinos diferentes se vuela desde cada uno de los orígenes, mostrando la salida ordenada de mayor a menor número de destinos.**

*   **Subquery/JOIN/EXISTS:** These forms are not distinct for a simple `GROUP BY` aggregation on a single table.
    ```sql
    SELECT
        origen,
        COUNT(DISTINCT destino) AS num_destinos_diferentes
    FROM
        vuelos
    GROUP BY
        origen
    ORDER BY
        num_destinos_diferentes DESC, origen; -- Added secondary sort by origen for tie-breaking
    ```

**11. Indique cuántos tipos de aviones diferentes salen de cada origen de la tabla vuelos, mostrando la salida ordenada de mayor a menor número de aviones. Sólo nos interesan aquellos orígenes de los que salen más de tres tipos de aviones diferentes.**

*   **Subquery/JOIN/EXISTS:** Again, these forms are not distinct for a `GROUP BY` with `HAVING` on a single table.
    ```sql
    SELECT
        origen,
        COUNT(DISTINCT tipo_avion) AS num_tipos_avion
    FROM
        vuelos
    GROUP BY
        origen
    HAVING
        COUNT(DISTINCT tipo_avion) > 3
    ORDER BY
        num_tipos_avion DESC, origen;
    ```

**12. ¿Cuántas horas de salida diferentes hay para cada tramo (origen - destino) de la tabla vuelos?**

*   **Subquery/JOIN/EXISTS:** Not distinct forms for `GROUP BY` on a single table.
    ```sql
    SELECT
        origen,
        destino,
        COUNT(DISTINCT hora_salida) AS num_horas_salida
    FROM
        vuelos
    GROUP BY
        origen, destino
    ORDER BY
        origen, destino;
    ```

**13. Obtenga, para cada número de vuelo, el total de plazas reservadas de los vuelos que recorren distancias mayores que la media de las distancias recorridas por vuelos de la misma compaña. Sólo nos interesan aquellos vuelos en los que el total de plazas reservadas es mayor que la media de plazas reservadas para los vuelos de Iberia.**

*   *This is quite complex, requiring multiple levels of aggregation and linking across tables. Let's break it down.*
    *   *Condition 1: `v.distancia > AVG(distance for same company)`*
    *   *Condition 2: `SUM(r.plazas) for the flight > AVG(SUM(plazas) for IB flights)`*
    *   *Needed: Link `reservas` to `vuelos` (for distance) and `vuelos` to `companias`.*

*   **Subquery / Common Table Expressions (CTEs) are best here:**
    ```sql
    WITH CompanyAvgDist AS (
        -- Calculate average distance per company
        SELECT f.compania, AVG(v.distancia) as avg_dist
        FROM vuelos v
        JOIN partes p ON v.num_vuelo = p.num_vuelo -- Link flight to a part
        JOIN flota f ON p.mat = f.matricula       -- Link part to a plane/company
        WHERE v.distancia IS NOT NULL
        GROUP BY f.compania
    ),
    FlightCompany AS (
        -- Determine the company for each flight number (simplified: assumes one company per flight number)
        SELECT DISTINCT p.num_vuelo, f.compania
        FROM partes p
        JOIN flota f ON p.mat = f.matricula
    ),
    FlightTotalPlazas AS (
        -- Calculate total plazas per flight (num_vuelo, assuming date doesn't matter for total)
        SELECT num_vuelo, SUM(plazas) as total_plazas
        FROM reservas
        GROUP BY num_vuelo
    ),
    AvgIberiaPlazas AS (
        -- Calculate the average total plazas for Iberia flights
        SELECT AVG(total_plazas) as avg_ib_plazas
        FROM FlightTotalPlazas ftp
        WHERE ftp.num_vuelo LIKE 'IB%' -- Using prefix assumption for Iberia
    )
    SELECT
        ftp.num_vuelo,
        ftp.total_plazas
    FROM
        FlightTotalPlazas ftp
    JOIN
        vuelos v ON ftp.num_vuelo = v.num_vuelo
    JOIN
        FlightCompany fc ON ftp.num_vuelo = fc.num_vuelo
    JOIN
        CompanyAvgDist cad ON fc.compania = cad.compania
    WHERE
        v.distancia > cad.avg_dist  -- Condition 1
      AND ftp.total_plazas > (SELECT avg_ib_plazas FROM AvgIberiaPlazas) -- Condition 2
    ORDER BY
        ftp.num_vuelo;

    -- Note: This query is complex and makes simplifying assumptions (like one company per flight number, date ignored in total plazas).
    -- The "Empty set" result in the example suggests no flights meet *all* these complex criteria.
    ```
*   **JOIN (without CTEs - becomes very nested and hard to read):** Possible but extremely convoluted. CTEs are preferred.
*   **EXISTS:** Possible for the filtering conditions, but the aggregations still require GROUP BY and potentially CTEs or nested subqueries for clarity.

**14. Obtenga la hora de salida más temprana para cada uno de los orígenes de los vuelos realizados por aviones con un alcance menor que 2/3 de la media del alcance de los otros aviones.** ("Otros aviones" means excluding the current one being evaluated - tricky interpretation. Assuming it means "< 2/3 of overall avg alcance").

*   **Subquery:**
    ```sql
    SELECT
        v.origen,
        MIN(v.hora_salida) AS primera_salida
    FROM
        vuelos v
    WHERE
        v.tipo_avion IN (SELECT tipo
                         FROM aviones
                         WHERE alcance < (SELECT AVG(alcance) * 2/3 FROM aviones))
    GROUP BY
        v.origen
    ORDER BY
        v.origen;
    ```
*   **JOIN:**
    ```sql
    SELECT
        v.origen,
        MIN(v.hora_salida) AS primera_salida
    FROM
        vuelos v
    JOIN
        aviones a ON v.tipo_avion = a.tipo
    WHERE
        a.alcance < (SELECT AVG(alcance) * 2/3 FROM aviones)
    GROUP BY
        v.origen
    ORDER BY
        v.origen;
    ```
*   **EXISTS:**
    ```sql
    SELECT
        v.origen,
        MIN(v.hora_salida) AS primera_salida
    FROM
        vuelos v
    WHERE EXISTS (SELECT 1
                  FROM aviones a
                  WHERE a.tipo = v.tipo_avion
                    AND a.alcance < (SELECT AVG(alcance) * 2/3 FROM aviones))
    GROUP BY
        v.origen
    ORDER BY
        v.origen;
    ```

**15. Obtenga los números de parte de los partes que corresponden a vuelos que recorren una distancia mayor que la media de la distancia de los otros vuelos.** (Again, "otros vuelos" likely means > overall average distance).

*   **Subquery:**
    ```sql
    SELECT
        p.num_parte
    FROM
        partes p
    WHERE
        p.num_vuelo IN (SELECT num_vuelo
                        FROM vuelos
                        WHERE distancia > (SELECT AVG(distancia) FROM vuelos WHERE distancia IS NOT NULL));
    ```
*   **JOIN:**
    ```sql
    SELECT
        p.num_parte
    FROM
        partes p
    JOIN
        vuelos v ON p.num_vuelo = v.num_vuelo
    WHERE
        v.distancia > (SELECT AVG(distancia) FROM vuelos WHERE distancia IS NOT NULL);
    ```
*   **EXISTS:**
    ```sql
    SELECT
        p.num_parte
    FROM
        partes p
    WHERE EXISTS (SELECT 1
                  FROM vuelos v
                  WHERE v.num_vuelo = p.num_vuelo
                    AND v.distancia > (SELECT AVG(distancia) FROM vuelos WHERE distancia IS NOT NULL));
    ```

**16. Obtenga el número de butacas de aquellos aviones con más butacas que la media de los otros aviones y envergadura menor que la media de las diferentes envergaduras de los otros aviones.** (Interpreting "otros aviones" as all planes for the average calculation).

*   **Subquery:**
    ```sql
    SELECT butacas
    FROM aviones
    WHERE butacas > (SELECT AVG(butacas) FROM aviones)
      AND envergadura < (SELECT AVG(envergadura) FROM aviones);
    ```
*   **JOIN:** (Not applicable, single table query)
*   **EXISTS:** (Not applicable, single table query)

**17. Obtenga la longitud de aquellos aviones con longitud menor que la media de los otros aviones y capacidad mayor que la media de las diferentes capacidades de los otros aviones.** (Capacity = butacas? Assuming yes. "Otros aviones" = all planes).

*   **Subquery:**
    ```sql
    SELECT longitud
    FROM aviones
    WHERE longitud < (SELECT AVG(longitud) FROM aviones)
      AND butacas > (SELECT AVG(butacas) FROM aviones);
    ```
*   **JOIN:** (Not applicable)
*   **EXISTS:** (Not applicable)
    *Note: The sample output is "Empty set", so no planes meet both conditions.*

**18. Obtenga la longitud de los aviones que realizan vuelos que recorren distancias mayores que la media de las distancias de los vuelos recorridos por la misma compaña.**

*   **Subquery:** (Using CTEs for clarity)
    ```sql
    WITH CompanyAvgDist AS (
        SELECT f.compania, AVG(v.distancia) as avg_dist
        FROM vuelos v
        JOIN partes p ON v.num_vuelo = p.num_vuelo
        JOIN flota f ON p.mat = f.matricula
        WHERE v.distancia IS NOT NULL
        GROUP BY f.compania
    )
    SELECT DISTINCT a.longitud -- Distinct longitud values
    FROM aviones a
    JOIN flota f ON a.tipo = f.tipo_avion -- Link plane type to specific plane/company
    JOIN partes p ON f.matricula = p.mat
    JOIN vuelos v ON p.num_vuelo = v.num_vuelo
    JOIN CompanyAvgDist cad ON f.compania = cad.compania
    WHERE v.distancia > cad.avg_dist;
    ```
*   **JOIN:** (Can be done directly, similar logic to CTE)
    ```sql
    SELECT DISTINCT a.longitud
    FROM aviones a
    JOIN flota f ON a.tipo = f.tipo_avion
    JOIN partes p ON f.matricula = p.mat
    JOIN vuelos v ON p.num_vuelo = v.num_vuelo
    JOIN (SELECT f.compania, AVG(v.distancia) as avg_dist
          FROM vuelos v
          JOIN partes p ON v.num_vuelo = p.num_vuelo
          JOIN flota f ON p.mat = f.matricula
          WHERE v.distancia IS NOT NULL
          GROUP BY f.compania) as cad ON f.compania = cad.compania
    WHERE v.distancia > cad.avg_dist;
    ```
*   **EXISTS:** (More complex for comparing against a group average)
    ```sql
    -- EXISTS is less natural here because we need the average distance *per company* to compare against.
    -- It's possible but involves correlated subqueries calculating the average, less efficient usually.
    SELECT DISTINCT a.longitud
    FROM aviones a
    WHERE EXISTS (
        SELECT 1
        FROM flota f
        JOIN partes p ON f.matricula = p.mat
        JOIN vuelos v ON p.num_vuelo = v.num_vuelo
        WHERE f.tipo_avion = a.tipo
          AND v.distancia > ( -- Correlated subquery for company average
              SELECT AVG(v2.distancia)
              FROM vuelos v2
              JOIN partes p2 ON v2.num_vuelo = p2.num_vuelo
              JOIN flota f2 ON p2.mat = f2.matricula
              WHERE f2.compania = f.compania -- Match the company
                AND v2.distancia IS NOT NULL
          )
    );
    ```

**19. Saliendo en el primer vuelo Sevilla - Madrid, averigüe la hora de salida del primer vuelo que se puede coger en Madrid con destino a Barcelona.**

*   **Subquery:**
    ```sql
    SELECT MIN(v_mad_bcn.hora_salida) AS hora_salida_mad_bcn
    FROM vuelos v_mad_bcn
    WHERE v_mad_bcn.origen = 'MADRID'
      AND v_mad_bcn.destino = 'BARCELONA'
      AND v_mad_bcn.hora_salida > (SELECT MIN(v_sev_mad.hora_llegada) -- Must depart *after* arriving from Sevilla
                                   FROM vuelos v_sev_mad
                                   WHERE v_sev_mad.origen = 'SEVILLA'
                                     AND v_sev_mad.destino = 'MADRID');
    -- Note: This assumes instantaneous transfer. A real scenario would add buffer time.
    -- Also assumes the *earliest arriving* flight from Sevilla is the one taken.
    -- The question asks about the *first departing* flight from Sevilla, let's adjust:
     SELECT MIN(v_mad_bcn.hora_salida) AS hora_salida_mad_bcn
     FROM vuelos v_mad_bcn
     WHERE v_mad_bcn.origen = 'MADRID'
       AND v_mad_bcn.destino = 'BARCELONA'
       AND v_mad_bcn.hora_salida > (SELECT v_sev_mad.hora_llegada -- Get arrival time of the first departing flight
                                    FROM vuelos v_sev_mad
                                    WHERE v_sev_mad.origen = 'SEVILLA'
                                      AND v_sev_mad.destino = 'MADRID'
                                    ORDER BY v_sev_mad.hora_salida
                                    LIMIT 1); -- Find the first departing flight's arrival time
    ```
*   **JOIN:** (Less intuitive for this sequential logic)
    ```sql
    -- Using CTE to find the arrival time of the first SVQ-MAD flight
    WITH FirstSevMadArrival AS (
        SELECT hora_llegada
        FROM vuelos
        WHERE origen = 'SEVILLA' AND destino = 'MADRID'
        ORDER BY hora_salida
        LIMIT 1
    )
    SELECT MIN(v_mad_bcn.hora_salida) AS hora_salida_mad_bcn
    FROM vuelos v_mad_bcn, FirstSevMadArrival fsma
    WHERE v_mad_bcn.origen = 'MADRID'
      AND v_mad_bcn.destino = 'BARCELONA'
      AND v_mad_bcn.hora_salida > fsma.hora_llegada;
    ```
*   **EXISTS:** (Not suitable for finding the MIN value based on a comparison)

**20. Obtenga el total de plazas reservadas para vuelos de Iberia cada día entre cada dos ciudades, ordenados de mayor a menor número de plazas reservadas.** (Assuming 'IB%' prefix again)

*   **Subquery/JOIN/EXISTS:** Not distinct forms for this aggregation.
    ```sql
    SELECT
        r.fecha,
        v.origen,
        v.destino,
        SUM(r.plazas) AS total_plazas_reservadas
    FROM
        reservas r
    JOIN
        vuelos v ON r.num_vuelo = v.num_vuelo
    WHERE
        r.num_vuelo LIKE 'IB%' -- Filter for Iberia flights
    GROUP BY
        r.fecha, v.origen, v.destino
    ORDER BY
        total_plazas_reservadas DESC;
    ```

**21. Obtenga los diferentes recorridos que se pueden realizar desde una ciudad hasta Madrid y haciendo escala llegar a otra ciudad.** (Flights X -> MAD, then MAD -> Y)

*   **Subquery:** (Possible but less direct than JOIN)
    ```sql
    SELECT DISTINCT v1.origen, v1.destino AS escala, v2.destino AS destino_final
    FROM vuelos v1
    WHERE v1.destino = 'MADRID'
      AND v1.origen != 'MADRID' -- Cannot start from Madrid
      AND v1.origen IN (SELECT DISTINCT v2.destino -- Check if the final destination is reachable from MAD
                        FROM vuelos v2
                        WHERE v2.origen = 'MADRID' AND v2.destino != v1.origen) -- Cannot fly back to origin
      AND EXISTS (SELECT 1 FROM vuelos v2 -- Ensure there's a flight FROM Madrid
                  WHERE v2.origen = 'MADRID'
                    AND v2.destino != v1.origen -- Cannot be a flight back to the origin city
                    AND v2.hora_salida > v1.hora_llegada); -- Simplistic check for valid connection timing
    ```
    *Correction:* The above is overly complex. We need pairs of flights: X -> MAD and MAD -> Y.
    ```sql
    SELECT DISTINCT v1.origen AS origen_inicial, v1.destino AS escala, v2.destino AS destino_final
    FROM vuelos v1, vuelos v2
    WHERE v1.destino = 'MADRID'      -- First leg ends in Madrid
      AND v2.origen = 'MADRID'       -- Second leg starts in Madrid
      AND v1.origen != 'MADRID'      -- Can't start in Madrid
      AND v2.destino != 'MADRID'     -- Can't end in Madrid
      AND v1.origen != v2.destino    -- Can't fly back to the original city
      AND v2.hora_salida > v1.hora_llegada -- Simplistic check: depart after arrival
    ORDER BY origen_inicial, destino_final;
    ```

*   **JOIN:** (Most natural way)
    ```sql
    SELECT DISTINCT
        v1.origen AS origen_inicial,
        v1.destino AS escala, -- which is always MADRID here
        v2.destino AS destino_final
    FROM
        vuelos v1 -- Flights arriving at Madrid
    JOIN
        vuelos v2 ON v1.destino = v2.origen -- Join where v1 destination is v2 origin
    WHERE
        v1.destino = 'MADRID' -- Ensure the connection point is Madrid
      AND v2.origen = 'MADRID'   -- Redundant due to JOIN condition but explicit
      AND v1.origen != 'MADRID'  -- Cannot start at Madrid
      AND v2.destino != 'MADRID' -- Cannot end at Madrid
      AND v1.origen != v2.destino -- Cannot fly X -> MAD -> X
      AND v2.hora_salida > v1.hora_llegada -- Flight 2 must depart after Flight 1 arrives (simple check)
    ORDER BY
        origen_inicial, destino_final;
    ```
*   **EXISTS:** (Less natural for finding combinations)
    ```sql
    SELECT DISTINCT v1.origen AS origen_inicial, v1.destino AS escala, v2.destino AS destino_final
    FROM vuelos v1
    CROSS JOIN vuelos v2 -- Need to consider pairs
    WHERE v1.destino = 'MADRID'
      AND v2.origen = 'MADRID'
      AND v1.origen != 'MADRID'
      AND v2.destino != 'MADRID'
      AND v1.origen != v2.destino
      AND v2.hora_salida > v1.hora_llegada -- Still need direct comparison
      -- EXISTS isn't providing much benefit here over JOIN or self-join.
    ORDER BY origen_inicial, destino_final;
    ```
    *The JOIN approach is the clearest and most standard for this type of path query.*

**22. Obtenga, en una sola columna, los nombres de todas las ciudades que aparecen en la tabla de vuelos, ordenados alfabéticamente.**

*   **Subquery/JOIN/EXISTS:** Not applicable (uses UNION)
    ```sql
    SELECT origen FROM vuelos
    UNION -- UNION automatically handles DISTINCT
    SELECT destino FROM vuelos
    ORDER BY origen; -- The column name in ORDER BY refers to the final combined column
    ```

**23. Obtenga en una sola columna el nombre de todas las ciudades origen de un vuelo y el de las que son destino de un vuelo. (Una misma ciudad puede aparecer como origen y como destino.)**

*   **Subquery/JOIN/EXISTS:** Not applicable (uses UNION ALL)
    ```sql
    SELECT origen FROM vuelos
    UNION ALL -- UNION ALL includes duplicates
    SELECT destino FROM vuelos
    ORDER BY origen;
    ```

**24. Obtenga en dos columnas, para cada ciudad que es origen, el número de vuelos que salen de ella y luego para cada una que es destino, el número de vuelos que recibe.**

*   *This requires combining two separate aggregations. UNION ALL is a common way.*
*   **Subquery/JOIN/EXISTS:** Not distinct methods for the core logic.
    ```sql
    SELECT origen AS ciudad, COUNT(*) AS vuelos_salen, 0 AS vuelos_llegan
    FROM vuelos
    GROUP BY origen
    UNION ALL
    SELECT destino AS ciudad, 0 AS vuelos_salen, COUNT(*) AS vuelos_llegan
    FROM vuelos
    GROUP BY destino
    ORDER BY ciudad;
    -- To get the desired output format (one row per city with both counts), we need to aggregate *after* the UNION or use JOINs/Subqueries differently.

    -- Method using full outer join simulation or CTEs:
    WITH Departures AS (
        SELECT origen AS ciudad, COUNT(*) as num_departures
        FROM vuelos GROUP BY origen
    ), Arrivals AS (
        SELECT destino AS ciudad, COUNT(*) as num_arrivals
        FROM vuelos GROUP BY destino
    ), AllCities AS (
        SELECT origen AS ciudad FROM vuelos UNION SELECT destino AS ciudad FROM vuelos
    )
    SELECT
        ac.ciudad,
        COALESCE(d.num_departures, 0) AS vuelos_salen, -- COALESCE handles cities with 0 departures/arrivals
        COALESCE(a.num_arrivals, 0) AS vuelos_llegan
    FROM AllCities ac
    LEFT JOIN Departures d ON ac.ciudad = d.ciudad
    LEFT JOIN Arrivals a ON ac.ciudad = a.ciudad
    ORDER BY ac.ciudad;
    -- Note: The sample output in the PDF looks like two separate lists rather than combined rows. Let's provide the first UNION ALL query which matches that structure.

    -- Query matching the structure of the sample output (two lists appended):
    SELECT origen AS ciudad_origen, COUNT(*) AS num_vuelos
    FROM vuelos
    GROUP BY origen
    ORDER BY ciudad_origen;
    -- Followed by:
    SELECT destino AS ciudad_destino, COUNT(*) AS num_vuelos
    FROM vuelos
    GROUP BY destino
    ORDER BY ciudad_destino;

    -- If the request means *literally* two columns titled 'origen' and 'destino' with counts, that's ambiguous. Assuming it means "list origins and counts, then list destinations and counts":
    SELECT origen, COUNT(*) AS count_origen FROM vuelos GROUP BY origen
    UNION ALL
    SELECT destino, COUNT(*) AS count_destino FROM vuelos GROUP BY destino;
    -- This still doesn't quite match the PDF output structure. The most likely intent matching the PDF visual is two separate queries or a UNION presenting them sequentially.
    ```
    *Let's provide the query that most closely produces the *data* shown, even if the formatting implies two separate result sets:*
    ```sql
    -- For the departure counts:
    SELECT origen, COUNT(*) AS 'count(origen)'
    FROM vuelos
    GROUP BY origen
    ORDER BY origen;

    -- For the arrival counts:
    SELECT destino, COUNT(*) AS 'count(destino)'
    FROM vuelos
    GROUP BY destino
    ORDER BY destino;
    ```

**25. Obtenga en tres columnas, para cada ciudad que aparece en la tabla vuelos, su nombre ordenado alfabéticamente, el total de vuelos que parten de ella y el total de vuelos que llegan a ella. Si no llega o no parte ningún vuelo, debe aparecer cero en la columna correspondiente.**

*   **Subquery/JOIN/EXISTS:** Not distinct methods, combines aggregations. CTEs or simulated FULL JOIN needed.
    ```sql
    WITH Departures AS (
        SELECT origen AS ciudad, COUNT(*) as num_departures
        FROM vuelos GROUP BY origen
    ), Arrivals AS (
        SELECT destino AS ciudad, COUNT(*) as num_arrivals
        FROM vuelos GROUP BY destino
    ), AllCities AS (
        SELECT origen AS ciudad FROM vuelos UNION SELECT destino AS ciudad FROM vuelos
    )
    SELECT
        ac.ciudad,
        COALESCE(d.num_departures, 0) AS vuelos_parten,
        COALESCE(a.num_arrivals, 0) AS vuelos_llegan
    FROM AllCities ac
    LEFT JOIN Departures d ON ac.ciudad = d.ciudad
    LEFT JOIN Arrivals a ON ac.ciudad = a.ciudad
    ORDER BY ac.ciudad;
    ```

**26. Obtenga en dos columnas, las diferentes fechas de llegada reflejadas en los partes de vuelo con el menor combustible consumido en cada una de ellas y, a continuación, estas mismas fechas con el mayor combustible consumido en cada una de ellas.**

*   *Similar to Q24, this seems to ask for two separate lists/results combined.*
*   **Subquery/JOIN/EXISTS:** Not distinct methods for the core logic.
    ```sql
    -- Finding the MIN fuel for each date
    SELECT fecha, MIN(comb_consumido) AS min_combustible
    FROM partes
    WHERE comb_consumido IS NOT NULL
    GROUP BY fecha

    UNION ALL

    -- Finding the MAX fuel for each date
    SELECT fecha, MAX(comb_consumido) AS max_combustible
    FROM partes
    WHERE comb_consumido IS NOT NULL
    GROUP BY fecha
    ORDER BY fecha, min_combustible; -- Ordering might interleave results, maybe run separately?

    -- To match the PDF output format (Min list then Max list):
    -- Query 1 (Min):
    SELECT fecha, MIN(comb_consumido) AS min_combustible
    FROM partes
    WHERE comb_consumido IS NOT NULL
    GROUP BY fecha
    ORDER BY fecha;

    -- Query 2 (Max):
    SELECT fecha, MAX(comb_consumido) AS max_combustible
    FROM partes
    WHERE comb_consumido IS NOT NULL
    GROUP BY fecha
    ORDER BY fecha;
    ```
    *Let's provide the two separate queries as that best matches the PDF's presentation.*

    *   **Query for MIN fuel per date:**
        ```sql
        SELECT fecha, MIN(comb_consumido) AS min_comb_consumido
        FROM partes
        WHERE comb_consumido IS NOT NULL
        GROUP BY fecha
        ORDER BY fecha;
        ```
    *   **Query for MAX fuel per date:**
        ```sql
        SELECT fecha, MAX(comb_consumido) AS max_comb_consumido
        FROM partes
        WHERE comb_consumido IS NOT NULL
        GROUP BY fecha
        ORDER BY fecha;
        ```

---
Remember to execute these queries against the `aeropuerto` database after creating and populating it using the provided `aeropuerto.txt` file. The interpretation of some questions (like "otros aviones" or the exact output format for combined results) might vary, but these solutions follow standard SQL practices and the likely intent based on the examples.