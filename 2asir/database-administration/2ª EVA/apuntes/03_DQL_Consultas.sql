/*
================================================================================
   APUNTES COMPLETOS MYSQL - BLOQUE 3: DQL (Data Query Language)
   CONSULTAS BÁSICAS Y AVANZADAS
================================================================================
*/

USE apuntes_asir;

-- -----------------------------------------------------------------------------
-- 1. CONSULTA BÁSICA (SELECT)
-- -----------------------------------------------------------------------------

SELECT * FROM empleados; -- Todas las columnas y filas (Evitar en producción)

-- Proyección: Elegir columnas específicas y Alias (AS)
SELECT nombre AS 'Nombre Pila', salario * 12 AS 'Salario Anual' 
FROM empleados;

-- Filtrado: WHERE
-- Operadores: =, != (o <>), >, <, >=, <=
-- Lógicos: AND, OR, NOT
-- Rangos: BETWEEN 1000 AND 2000
-- Listas: IN (1, 2, 5)
-- Nulos: IS NULL / IS NOT NULL (Nunca usar = NULL)
SELECT * FROM empleados 
WHERE (dept_id = 2 OR salario > 2000) 
  AND jefe_id IS NOT NULL;

-- Patrones de texto: LIKE
-- % : Cualquier cadena de caracteres (0 o más)
-- _ : Un único carácter cualquiera
SELECT * FROM empleados WHERE primer_apellido LIKE 'G__ez'; -- Empieza por G, 2 letras, acaba en ez
SELECT * FROM empleados WHERE nombre LIKE '%a%'; -- Contiene una 'a'


-- -----------------------------------------------------------------------------
-- 2. ORDENACIÓN Y LIMITACIÓN
-- -----------------------------------------------------------------------------

SELECT nombre, salario 
FROM empleados 
ORDER BY salario DESC, nombre ASC -- Ordena por salario (mayor a menor), desempata por nombre
LIMIT 3 OFFSET 0; -- Los 3 primeros (Paginación) OFFSET es el número de filas a saltar


-- -----------------------------------------------------------------------------
-- 3. FUNCIONES DE AGREGADO Y AGRUPAMIENTO (GROUP BY)
-- -----------------------------------------------------------------------------
/*
   Regla de Oro: Si usas GROUP BY, en el SELECT solo puedes poner:
   1. Las columnas por las que agrupa.
   2. Funciones de agregado (COUNT, SUM, AVG, MAX, MIN).
*/

-- Contar empleados por departamento
SELECT dept_id, COUNT(*) AS num_empleados, AVG(salario) AS sueldo_medio
FROM empleados
WHERE salario > 1000       -- Filtra FILAS antes de agrupar
GROUP BY dept_id
HAVING AVG(salario) > 1500; -- Filtra GRUPOS después de agrupar


-- -----------------------------------------------------------------------------
-- 4. CONSULTAS MULTITABLA (JOINS)
-- -----------------------------------------------------------------------------

-- INNER JOIN: Solo filas que coinciden en AMBAS tablas
SELECT e.nombre, d.nombre AS departamento
FROM empleados e
INNER JOIN departamentos d ON e.dept_id = d.dept_id;

-- LEFT JOIN (OUTER): Todas las de la IZQUIERDA (empleados), coincidan o no.
-- Si un empleado no tiene departamento, sale NULL en las columnas de d.
SELECT e.nombre, d.nombre
FROM empleados e
LEFT JOIN departamentos d ON e.dept_id = d.dept_id;

-- RIGHT JOIN: Todas las de la DERECHA (departamentos).
-- Muestra departamentos vacíos (sin empleados), con NULL en columnas de e.
SELECT d.nombre, e.nombre
FROM empleados e
RIGHT JOIN departamentos d ON e.dept_id = d.dept_id;

-- SELF JOIN: Unir una tabla consigo misma (Jerarquía Jefe-Empleado)
SELECT trab.nombre AS trabajador, jefe.nombre AS jefe
FROM empleados trab
LEFT JOIN empleados jefe ON trab.jefe_id = jefe.emp_id;


-- -----------------------------------------------------------------------------
-- 5. SUBCONSULTAS (SUBQUERIES)
-- -----------------------------------------------------------------------------

-- Escalar (Devuelve un solo valor)
-- Empleados que ganan más que la media
SELECT nombre, salario 
FROM empleados 
WHERE salario > (SELECT AVG(salario) FROM empleados);

-- Lista (Devuelve columna de valores)
-- Departamentos que tienen empleados que ganan más de 3000
SELECT nombre FROM departamentos 
WHERE dept_id IN (SELECT DISTINCT dept_id FROM empleados WHERE salario > 3000);

-- Tabla correlacionada (Se ejecuta fila a fila)
-- Empleados que ganan más que la media DE SU DEPARTAMENTO
SELECT e1.nombre, e1.salario
FROM empleados e1
WHERE salario > (
    SELECT AVG(salario) 
    FROM empleados e2 
    WHERE e2.dept_id = e1.dept_id
);


-- -----------------------------------------------------------------------------
-- 6. UNIÓN DE CONSULTAS (SET OPERATORS)
-- -----------------------------------------------------------------------------

-- UNION: Combina resultados y ELIMINA DUPLICADOS
-- UNION ALL: Combina resultados y MANTIENE DUPLICADOS (Más rápido)
-- Requisito: Mismo número de columnas y tipos compatibles.
SELECT nombre FROM empleados
UNION
SELECT nombre FROM departamentos; -- (Ejemplo tonto, pero funcional)

/*
   RESUMEN ORDEN DE EJECUCIÓN:
   1. FROM & JOIN
   2. WHERE
   3. GROUP BY
   4. HAVING
   5. SELECT
   6. ORDER BY
   7. LIMIT
*/
