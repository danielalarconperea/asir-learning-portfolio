/* 
================================================================================
   APUNTES COMPLETOS MYSQL - BLOQUE 1: DDL (Data Definition Language)
================================================================================
   AUTOR: Generado para ASIR
   DESCRIPCIÓN: Este script explica cómo crear, modificar y eliminar la estructura
   de una base de datos. Cubre tablas, tipos de datos y restricciones (constraints).
   
   INSTRUCCIONES: Puedes ejecutar este script paso a paso para ver los resultados.
================================================================================
*/

-- -----------------------------------------------------------------------------
-- 1. GESTIÓN DE BASES DE DATOS
-- -----------------------------------------------------------------------------

-- Crear una base de datos si no existe (Best Practice)
-- CHARACTER SET utf8mb4: Soporta emojis y caracteres unicode completos.
-- COLLATE utf8mb4_spanish_ci: Ordenación insensible a mayúsculas/minúsculas para español.
CREATE DATABASE IF NOT EXISTS apuntes_asir 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_spanish_ci;

-- Seleccionar la base de datos para usarla
USE apuntes_asir;

-- Eliminar una base de datos (¡CUIDADO! Borra todo)
-- DROP DATABASE IF EXISTS apuntes_asir_temp;


-- -----------------------------------------------------------------------------
-- 2. CREACIÓN DE TABLAS (CREATE TABLE)
-- -----------------------------------------------------------------------------

/* 
   RESTRICCIONES (CONSTRAINTS) MÁS IMPORTANTES:
   - PRIMARY KEY (PK): Identifica unívocamente la fila. No puede ser NULL.
   - FOREIGN KEY (FK): Enlaza con la PK de otra tabla. Integridad Referencial.
   - NOT NULL: Obliga a tener un valor.
   - UNIQUE: No permite valores duplicados en la columna.
   - DEFAULT: Asigna un valor por defecto si no se especifica.
   - CHECK: Valida una condición lógica (MySQL 8.0.16+).
   - AUTO_INCREMENT: Genera secuencia numérica automática (solo para PK enteras).
*/

-- Primero borramos las tablas si existen para evitar errores al reejecutar (Orden inverso a dependencias)
DROP TABLE IF EXISTS empleados_proyectos;
DROP TABLE IF EXISTS empleados;
DROP TABLE IF EXISTS departamentos;

-- Tabla Padre: DEPARTAMENTOS
CREATE TABLE departamentos (
    dept_id INT AUTO_INCREMENT,              -- Entero autoincremental
    nombre VARCHAR(50) NOT NULL,             -- Texto variable obligatoro
    ubicacion VARCHAR(100) DEFAULT 'Madrid', -- Valor por defecto
    presupuesto DECIMAL(10, 2) CHECK (presupuesto > 0), -- Validación: debe ser positivo
    
    -- Definición de restricciones a nivel de tabla (recomendado para nombrar constraints)
    CONSTRAINT pk_departamentos PRIMARY KEY (dept_id),
    CONSTRAINT uq_nombre_dept UNIQUE (nombre) -- No puede haber dos departamentos con el mismo nombre
) ENGINE=InnoDB; -- Motor transaccional (estándar moderno)


-- Tabla Hija: EMPLEADOS (Tiene FK hacia Departamentos)
CREATE TABLE empleados (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,   -- Sintaxis corta de PK
    dni CHAR(9) NOT NULL UNIQUE,             -- Texto fijo (9 chars) único
    nombre VARCHAR(50) NOT NULL,
    apellido1 VARCHAR(50) NOT NULL,
    fecha_nacimiento DATE,
    fecha_alta DATETIME DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora actual por defecto
    salario DECIMAL(10, 2),
    dept_id INT,                             -- Columna para la FK (mismo tipo que la PK padre)
    jefe_id INT,                             -- Relación reflexiva (Referencia a la misma tabla)
    
    -- Definición de Foreign Keys
    -- ON DELETE RESTRICT: Impide borrar un departamento si tiene empleados (Por defecto)
    -- ON DELETE CASCADE: Si borro departamento, se borran sus empleados (¡Peligroso!)
    -- ON DELETE SET NULL: Si borro departamento, el campo dept_id pasa a NULL
    CONSTRAINT fk_emp_dept FOREIGN KEY (dept_id) 
        REFERENCES departamentos(dept_id) 
        ON DELETE SET NULL ON UPDATE CASCADE,
        
    CONSTRAINT fk_emp_jefe FOREIGN KEY (jefe_id) 
        REFERENCES empleados(emp_id)
);


-- Tabla N:M (Muchos a Muchos): EMPLEADOS_PROYECTOS
CREATE TABLE proyectos (
    proy_id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL
);

CREATE TABLE empleados_proyectos (
    emp_id INT,
    proy_id INT,
    horas_asignadas INT DEFAULT 0,
    
    -- Primary Key Compuesta (La combinación de ambos es única)
    CONSTRAINT pk_emp_proy PRIMARY KEY (emp_id, proy_id),
    
    CONSTRAINT fk_asign_emp FOREIGN KEY (emp_id) REFERENCES empleados(emp_id) ON DELETE CASCADE,
    CONSTRAINT fk_asign_proy FOREIGN KEY (proy_id) REFERENCES proyectos(proy_id) ON DELETE CASCADE
);


-- -----------------------------------------------------------------------------
-- 3. MODIFICACIÓN DE ESTRUCTURA (ALTER TABLE)
-- -----------------------------------------------------------------------------

/*
   ALTER TABLE permite añadir, borrar o modificar columnas y restricciones
   sin tener que borrar y recrear la tabla.
*/

-- AÑADIR columna
ALTER TABLE empleados ADD COLUMN email VARCHAR(100);

-- MODIFICAR columna (Tipo de dato o propiedades)
ALTER TABLE empleados MODIFY COLUMN email VARCHAR(150) NOT NULL;

-- RENOMBRAR columna (Requiere repetir la definición del tipo)
ALTER TABLE empleados CHANGE COLUMN apellido1 primer_apellido VARCHAR(50) NOT NULL;

-- BORRAR columna
ALTER TABLE empleados DROP COLUMN fecha_nacimiento;

-- AÑADIR Restricción (Constraint) después de crear la tabla
ALTER TABLE empleados ADD CONSTRAINT uq_email UNIQUE (email);

-- BORRAR Restricción
-- Para borrar PK: DROP PRIMARY KEY
-- Para borrar FK: DROP FOREIGN KEY nombre_constraint
ALTER TABLE empleados DROP FOREIGN KEY fk_emp_dept; (¡OJO! Rompe la integridad)


-- -----------------------------------------------------------------------------
-- 4. VISTAS (VIEWS)
-- -----------------------------------------------------------------------------
/*
   Una vista es una "tabla virtual" basada en una consulta SELECT.
   No almacena datos, solo la definición. Simplifica consultas complejas.
*/

CREATE OR REPLACE VIEW vista_resumen_dept AS
SELECT nombre, ubicacion, presupuesto 
FROM departamentos
WHERE presupuesto > 1000;

-- Se consulta igual que una tabla:
-- SELECT * FROM vista_resumen_dept;

/*
   RESUMEN FINAL:
   1. CREATE DATABASE -> Crea el contenedor.
   2. CREATE TABLE -> Estructura fundamental.
      - Definir tipos de datos correctos (INT, VARCHAR, DATE).
      - Definir Constraints (PK, FK, UNIQUE, CHECK).
   3. ALTER TABLE -> Modificaciones posteriores.
   4. DROP -> Eliminar objetos.
*/
