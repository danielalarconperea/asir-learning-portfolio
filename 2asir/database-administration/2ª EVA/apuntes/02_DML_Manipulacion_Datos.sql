/*
================================================================================
   APUNTES COMPLETOS MYSQL - BLOQUE 2: DML (Data Manipulation Language)
================================================================================
   DESCRIPCIÓN: Insertar, modificar, borrar y consultar datos.
   
   PRERREQUISITOS: Se asume que existen las tablas creadas en el Bloque 1.
================================================================================
*/

USE apuntes_asir;

-- -----------------------------------------------------------------------------
-- 1. INSERTAR DATOS (INSERT)
-- -----------------------------------------------------------------------------

-- Inserción completa (Especificando todos los campos - RECOMENDADO)
INSERT INTO departamentos (nombre, ubicacion, presupuesto) 
VALUES ('Contabilidad', 'Madrid', 50000.00);

-- Inserción parcial (Los campos no especificados toman NULL o su valor DEFAULT)
INSERT INTO departamentos (nombre, presupuesto) 
VALUES ('Ventas', 120000.50); -- 'ubicacion' serÃ¡ 'Madrid' por el DEFAULT

-- Inserción múltiple (Más eficiente que varios INSERT individuales)
INSERT INTO departamentos (nombre, ubicacion, presupuesto) VALUES 
('Desarrollo', 'Barcelona', 75000.00),
('Sistemas', 'Bilbao', 45000.00),
('Recursos Humanos', 'Sevilla', 30000.00);

-- INSERT ... SET (Sintaxis alternativa tipo UPDATE, legible para pocos campos)
INSERT INTO proyectos SET nombre = 'Migración SAP';
INSERT INTO proyectos SET nombre = 'Web Corporativa';


-- Inserción en tabla hija (EMPLEADOS)
-- Nota: 'dni' es UNIQUE y 'dept_id' es FK (debe existir el ID en departamentos)
-- Asumimos que los departamentos tienen IDs 1, 2, 3...
INSERT INTO empleados (dni, nombre, primer_apellido, salario, dept_id, jefe_id) VALUES
('12345678A', 'Juan', 'Perez', 2500.00, 1, NULL),
('87654321B', 'Maria', 'Gomez', 3000.00, 2, NULL), -- Jefe de sistemas
('11223344C', 'Luis', 'Lopez', 1800.00, 2, 2);    -- Empleado de sistemas (Jefe: Maria id=2)


-- Insertar resultados de una consulta SELECT (Copiar datos)
-- INSERT INTO tabla_historial SELECT * FROM tabla_actual WHERE año = 2023;


-- -----------------------------------------------------------------------------
-- 2. MODIFICAR DATOS (UPDATE)
-- -----------------------------------------------------------------------------
/*
   ¡IMPORTANTE!: Siempre usar WHERE. Si olvidamos el WHERE, modificamos TODA la tabla.
   Safe Updates mode (activado por defecto en Workbench) impide updates sin WHERE PK.
*/

-- Subir el salario un 10% a los empleados del departamento 2
UPDATE empleados 
SET salario = salario * 1.10 
WHERE dept_id = 2;

-- Modificar varios campos a la vez
UPDATE empleados
SET primer_apellido = 'Gómez-Sánchez', 
    email = 'maria.gomez@empresa.com'
WHERE emp_id = 2;

-- UPDATE con JOIN (Modificar datos basándose en otra tabla)
-- Ejemplo: Subir sueldo a empleados de departamentos en 'Barcelona'
UPDATE empleados e
JOIN departamentos d ON e.dept_id = d.dept_id
SET e.salario = e.salario + 500
WHERE d.ubicacion = 'Barcelona';


-- -----------------------------------------------------------------------------
-- 3. ELIMINAR DATOS (DELETE vs TRUNCATE)
-- -----------------------------------------------------------------------------

-- DELETE: Borra filas específicas. Es transaccional (se puede hacer ROLLBACK).
DELETE FROM empleados WHERE emp_id = 3;

-- Borrar todos los empleados de un departamento
DELETE FROM empleados WHERE dept_id = 4;

-- DELETE con ORDER BY y LIMIT (Borrar los 2 sueldos más bajos)
DELETE FROM empleados ORDER BY salario ASC LIMIT 2;

-- TRUNCATE: Vacía la tabla COMPLETA. 
-- Es DDL (no DML), resetea el AUTO_INCREMENT. NO se puede deshacer.
-- TRUNCATE TABLE log_accesos;


-- -----------------------------------------------------------------------------
-- 4. REEMPLAZAR (REPLACE / INSERT ON DUPLICATE)
-- -----------------------------------------------------------------------------

-- REPLACE: Si la PK/Unique existe, BORRA la fila y la INSERTA nueva. Si no, inserta.
REPLACE INTO proyectos (proy_id, nombre) VALUES (1, 'Migración SAP v2');

-- INSERT ... ON DUPLICATE KEY UPDATE (La forma "suave" de MySQL)
-- Si la clave existe, actualiza solo el campo indicado. Si no, inserta.
INSERT INTO empleados (dni, nombre, primer_apellido, salario) 
VALUES ('12345678A', 'Juan', 'Pérez', 2600.00)
ON DUPLICATE KEY UPDATE 
salario = 2600.00, nombre = 'Juan';

/*
   RESUMEN DML:
   - INSERT: Crear.
   - UPDATE: Modificar (¡Cuidado con el WHERE!).
   - DELETE: Borrar filas (Recuperable).
   - TRUNCATE: Vaciar tabla (Irrecuperable, resetea IDs).
*/
