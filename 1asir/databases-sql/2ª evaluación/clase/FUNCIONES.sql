/* Creación de la base de datos y selección de la misma */
CREATE DATABASE practica12;
USE practica12;

/* Creación de la tabla 'dept' que almacena información de departamentos */
CREATE TABLE dept (
    deptno INT,                /* Número de departamento */
    dname VARCHAR(14),         /* Nombre del departamento */
    loc VARCHAR(13),           /* Localización del departamento */
    PRIMARY KEY (deptno)       /* Clave primaria */
);

/* Inserción de datos en la tabla 'dept' */
INSERT INTO dept VALUES (10, "Accounting", "New York");
INSERT INTO dept VALUES (20, "Research", "Dallas");
INSERT INTO dept VALUES (30, "Sales", "Chicago");
INSERT INTO dept VALUES (40, "Operation", "Boston");

/* Creación de la tabla 'emp' que almacena información de empleados */
CREATE TABLE emp (
    empno INT,                 /* Número de empleado */
    ename VARCHAR(10),         /* Nombre del empleado */
    job VARCHAR(9),            /* Puesto del empleado */
    mgr INT,                   /* Número del manager del empleado */
    hiredate DATE,             /* Fecha de contratación */
    sal FLOAT,                 /* Salario */
    comm FLOAT,                /* Comisión */
    deptno INT,                /* Número de departamento (clave foránea) */
    PRIMARY KEY (empno),       /* Clave primaria */
    FOREIGN KEY (deptno) REFERENCES dept(deptno) /* Clave foránea */
);

/* Inserción de datos en la tabla 'emp' */
INSERT INTO emp VALUES (7369, "Smith", "Clerk", 7902, "80-12-17", 800, NULL, 20);
INSERT INTO emp VALUES (7499, "Allen", "Salesman", 7698, "81-2-20", 1600, 300, 30);
INSERT INTO emp VALUES (7521, "Ward", "Salesman", 7698, "81-2-22", 1250, 500, 30);
INSERT INTO emp VALUES (7566, "Jones", "Manager", 7839, "81-4-02", 2975, NULL, 20);
INSERT INTO emp VALUES (7654, "Martin", "Salesman", 7698, "81-9-28", 1250, 1400, 30);
INSERT INTO emp VALUES (7698, "Blake", "Manager", 7839, "81-5-01", 2850, NULL, 30);
INSERT INTO emp VALUES (7782, "Clark", "Manager", 7839, "81-06-09", 2450, NULL, 10);
INSERT INTO emp VALUES (7788, "Scott", "Analyst", 7566, "82-12-9", 3000, NULL, 20);
INSERT INTO emp VALUES (7839, "King", "President", NULL, "81-11-17", 5000, NULL, 10);
INSERT INTO emp VALUES (7844, "Turner", "Salesman", 7698, "81-9-08", 1500, 0, 30);
INSERT INTO emp VALUES (7876, "Adams", "Clerk", 7788, "83-1-12", 1100, NULL, 20);
INSERT INTO emp VALUES (7900, "James", "Clerk", 7698, "81-12-3", 950, NULL, 30);
INSERT INTO emp VALUES (7902, "Ford", "Analyst", 7566, "81-12-3", 3000, NULL, 20);
INSERT INTO emp VALUES (7934, "Miller", "Clerk", 7782, "82-7-23", 1300, NULL, 10);

/*-----------------------------------------------------------*/
/* Funciones de cadena */
/*-----------------------------------------------------------*/

/* CHAR_LENGTH: Devuelve la longitud de una cadena */
SELECT CHAR_LENGTH('HOLA'); /* Resultado: 4 */

/* INSTR: Devuelve la posición de una subcadena dentro de una cadena */
SELECT ename, INSTR(ename, 'Allen') FROM emp; /* Resultado: 2 para 'Allen' */

/* STRCMP: Compara dos cadenas según el orden ASCII */
SELECT STRCMP('Ana', 'Pepe'); /* Resultado: -1 (Ana es menor que Pepe) */

/* CONCAT: Concatena dos o más cadenas */
SELECT CONCAT('Hola', 'Buenas'); /* Resultado: HolaBuenas */

/* REVERSE: Invierte una cadena */
SELECT REVERSE('Jose es muy alto'); /* Resultado: otla yum se esoJ */

/* LEFT: Devuelve los primeros n caracteres de una cadena */
SELECT LEFT('pepe es muy alto', 6); /* Resultado: pepe e */

/* RIGHT: Devuelve los últimos n caracteres de una cadena */
SELECT RIGHT('pepe es muy alto', 7); /* Resultado: uy alto */

/* LOWER: Convierte una cadena a minúsculas */
SELECT LOWER('Pepe Es Muy Alto'); /* Resultado: pepe es muy alto */

/* UPPER: Convierte una cadena a mayúsculas */
SELECT UPPER('Pepe Es Muy Alto'); /* Resultado: PEPE ES MUY ALTO */

/* LPAD: Rellena una cadena por la izquierda con un carácter específico */
SELECT LPAD('PEPE', 10, '@'); /* Resultado: @@@@@@PEPE */

/* RPAD: Rellena una cadena por la derecha con un carácter específico */
SELECT RPAD('PEPE', 10, '.'); /* Resultado: PEPE...... */

/* TRIM: Elimina espacios en blanco al inicio y final de una cadena */
SELECT TRIM('      MySQL  '); /* Resultado: MySQL */

/* SUBSTRING: Extrae una subcadena de una cadena */
SELECT SUBSTRING('Pepe es alto', 3); /* Resultado: pe es alto */
SELECT SUBSTRING('Pepe es alto', 3, 7); /* Resultado: pe es a */

/* SUBSTRING_INDEX: Extrae una subcadena basada en un delimitador */
SELECT SUBSTRING_INDEX('training@mysql.com', '@', 1); /* Resultado: training */
SELECT SUBSTRING_INDEX('www.mysql.com', '.', -2); /* Resultado: mysql.com */

/* REPEAT: Extrae una subcadena de una cadena */
REPEAT('-', 10)

/*-----------------------------------------------------------*/
/* Funciones de fecha y hora */
/*-----------------------------------------------------------*/

/* NOW: Devuelve la fecha y hora actual */
SELECT NOW();

/* DATE: Extrae la parte de la fecha de un datetime */
SELECT DATE(NOW());

/* TIME: Extrae la parte de la hora de un datetime */
SELECT TIME(NOW());

/* DAYNAME: Devuelve el nombre del día de la semana */
SELECT DAYNAME(NOW());

/* CURTIME: Devuelve la hora actual */
SELECT CURTIME();

/* DATE_FORMAT: Devuelve en formato esecífico */
SELECT DATE_FORMAT(hiredate, '%e de %M de %Y') FROM emp; /* 7 de Febrero de 2025 */

/*-----------------------------------------------------------*/
/* Funciones matemáticas */
/*-----------------------------------------------------------*/

/* TRUNCATE: Trunca un número a un número específico de decimales */
SELECT TRUNCATE(AVG(sal), 2) FROM emp; /* Resultado: Promedio de salarios truncado a 2 decimales */

/* FLOOR: Redondea un número hacia abajo */
SELECT FLOOR(4.7); /* Resultado: 4 */

/* CEILING: Redondea un número hacia arriba */
SELECT CEILING(4.7); /* Resultado: 5 */

/* ROUND: Redondea un número al entero más cercano */
SELECT ROUND(4.7); /* Resultado: 5 */

/* SQRT: Calcula la raíz cuadrada de un número */
SELECT SQRT(1024); /* Resultado: 32 */

/* POWER: Eleva un número a una potencia */
SELECT POWER(4, 6); /* Resultado: 4096 */

SELECT SIN(1) AS Seno;
SELECT COT(1) AS Cotangente;
SELECT ACOS(1) AS Arcocoseno;
SELECT ASIN(1) AS Arcoseno;
SELECT EXP(1) AS Exponencial;
SELECT LN(2) AS Log_Natural;
SELECT LOG(10, 100) AS Log_Base10;
SELECT POWER(2, 3) AS Potencia;
SELECT SQRT(16) AS Raiz_Cuadrada;

/*-----------------------------------------------------------*/
/* Ejemplos adicionales */
/*-----------------------------------------------------------*/

/* CONCAT con REVERSE y UPPER: Concatena el nombre invertido y en mayúsculas */
SELECT CONCAT(REVERSE(UPPER(ename)), '.....') FROM emp;

/* LOWER y UPPER aplicados a nombres de empleados */
SELECT LOWER(ename) FROM emp; /* Convierte todos los nombres a minúsculas */
SELECT UPPER(ename) FROM emp; /* Convierte todos los nombres a mayúsculas */

/* CONCAT con prefijo 'Sr/Sra' */
SELECT CONCAT('Sr/Sra ', ename) AS nombre FROM emp; /* Añade prefijo a los nombres */

/* REVERSE aplicado al puesto de trabajo */
SELECT REVERSE(job) FROM emp; /* Invierte el nombre del puesto de trabajo */

/* LEFT y RIGHT aplicados al puesto de trabajo */
SELECT LEFT(job, 7) FROM emp; /* Devuelve los primeros 7 caracteres del puesto */
SELECT RIGHT(job, 7) FROM emp; /* Devuelve los últimos 7 caracteres del puesto */