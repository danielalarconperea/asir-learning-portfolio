create database practica12;
use practica12;
create table dept(
deptno int,
dname varchar(14),
loc varchar(13),
primary key (deptno)
);
insert into dept values (10,"AcCOUNTing","New york");
insert into dept values (20,"Research","Dallas");
insert into dept values (30,"Sales","Chicago");
insert into dept values (40,"Operation","Boston");

create table emp(
empno int,
ename varchar(10),
job varchar(9),
mgr int, 
hiredate date,
sal float,
comm float,
deptno int references dept (deptno),
primary key (empno) 
);

insert into emp values (7369, "Smith", "Clerk", 7902, "80-12-17", 800, NULL,20);
insert into emp values (7499, "Allen", "Salesman", 7698, "81-2-20", 1600, 300,30);
insert into emp values (7521, "Ward", "Salesman", 7698, "81-2-22", 1250, 500, 30);
insert into emp values (7566, "Jones", "Manager", 7839, "81-4-02", 2975, NULL, 20);
insert into emp values (7654, "Martin", "Salesman", 7698, "81-9-28", 1250, 1400,30);
insert into emp values (7698, "Blake", "Manager", 7839, "81-5-01", 2850, NULL,30);
insert into emp values (7782, "Clark", "Manager", 7839, "81-06-09", 2450, NULL, 10);
insert into emp values (7788, "Scott", "Analyst", 7566, "82-12-9", 3000, NULL, 20);
insert into emp values (7839, "King", "President", NULL,"81-11-17", 5000, NULL, 10);
insert into emp values (7844, "Turner", "Salesman", 7698, "81-9-08", 1500, 0, 30);
insert into emp values (7876, "Adams", "Clerk", 7788, "83-1-12", 1100, NULL, 20);
insert into emp values (7900, "James", "Clerk", 7698, "81-12-3", 950, NULL, 30);
insert into emp values (7902, "Ford", "Analyst", 7566, "81-12-3", 3000, NULL, 20);
insert into emp values (7934, "Miller", "Clerk", 7782, "82-7-23", 1300, NULL, 10);


/*1. Muestra la versión de Mysql */;
SELECT VERSION();

/*2. Muestra la fecha y hora actual */;
SELECT NOW();

/*3. Compara las cadenas (“Salesianos”, y “SALESIANOS”) */;
SELECT STRCMP('Salesianos','SALESIANOS');

/*4. Muestra la longitud de la cadena de los “ename” de la tabla EMP. */;
SELECT CHAR_LENGTH(ename) AS Longitud_Nombre FROM emp;

/*5. Concatena los “Ename” y los “job” de todos los empleados, separándolos con un guión (“-“). */;
SELECT CONCAT(ename, '-', job) AS Ename_Job FROM emp;

/*6. Muéstra los “loc” alreves de la tabla DEPT. */;
SELECT REVERSE(loc) AS Reverse_loc FROM dept;

/*7. Rellena con puntos “.” por la derecha hasta 20 caracteres los ename de la tabla emp. */;
SELECT RPAD(ename,20,'.') AS Ename_Relleno FROM emp;

/*8. Muestra en mayúsculas todos Dname de la tabla DEPT. */;
SELECT UPPER(dname) AS Dname_Mayus FROM dept;

/*9. Muestra el nombre y el año (solo el año de la fecha) de todos los empleados. */;
SELECT ename, YEAR(hiredate) AS Año_Contratacion FROM emp;

/*10.  Muestra la hora actual. */;
SELECT CURTIME() AS Hora_Actual;

/*11.  Muestra el día de la semana de hoy. */;
SELECT DAYNAME(NOW()) AS Dia_Semana;

/*12.  Muestra la fecha de hoy en formato: 7 de Febrero de 2021 */;
SELECT DATE_FORMAT(NOW(), '%e de %M de %Y') AS Fecha_Formateada;

/*13.  Muestra la fecha de la tabla emp en formato: 7 de Febrero de 2021 */;
SELECT DATE_FORMAT(hiredate, '%e de %M de %Y') AS Fecha_Contrato FROM emp;

/*14.  Muestra el salario más alto de la tabla emp. */;
SELECT MAX(sal) AS Salario_mas_alto FROM emp;

/*15.  Muestra el primer empleado contratado en la empresa. */;
SELECT * FROM emp ORDER BY hiredate ASC LIMIT 1;

/*16.  Calcula el salario medio de la empresa. */;
SELECT AVG(sal) AS Salario_Promedio FROM emp;

/*17.  Halla la media de los salarios de los departamentos cuyo salario mínimo supera a 1000. */;
SELECT deptno, AVG(sal) AS salario_medio FROM emp GROUP BY deptno HAVING MIN(sal) > 1000;

/*18.  Muestra cuantos empleados no tienen comisión. */;
SELECT COUNT(*) AS numero_empleados FROM emp WHERE comm IS NULL;

/*19.  Muestra la media de salario de los departamentos agrupado por departamento. */;
SELECT deptno, AVG(sal) AS Media_Salarial FROM emp GROUP BY deptno;

/*20.  Muestra la suma de salario de los departamentos agrupado por departamento cuya suma sea mayor de 2000. */;
SELECT deptno, SUM(sal) AS Suma_Salarial FROM emp GROUP BY deptno HAVING SUM(sal) > 2000;

/*21.  Prueba las funciones con números de prueba: SIN(), COT(), ACOS(), ASIN(), EXP(), LN(), LOG(), POWER(), SQRT()*/;
SELECT 
    SIN(1) AS Seno,
    COT(1) AS Cotangente,
    ACOS(1) AS Arcocoseno,
    ASIN(1) AS Arcoseno,
    EXP(1) AS Exponencial,
    LN(2) AS Log_Natural,
    LOG(10, 100) AS Log_Base10,
    POWER(2, 3) AS Potencia,
    SQRT(16) AS Raiz_Cuadrada;


/*Parte2 */;
/*Crea una base de datos "ejercicio3", en la que guardaremos información sobre selecciones nacionales de baloncesto.  */;
/*Para ello tendremos: una tabla "PAIS" y una tabla "JUGADOR".  */;
/*De cada país guardaremos el nombre (por ejemplo, "España") y un código que actuará como clave primaria (por ejemplo, “ESP”). */;
/*De cada jugador anotaremos código, nombre, apellidos, posición y código de la selección a la que pertenece. */;

/*1. Añade los países: 
      ▪ ESP, España 
      ▪ ARG, Argentina 
      ▪ AUS, Australia 
      ▪ LIT, Lituania */;

/*2. Añade los jugadores: 
      ▪ RUB, Ricky, Rubio, Base,ESP  
      ▪ NAV, Sergio, Lull, Alero,ESP 
      ▪ SCO, Luis, Scola, Ala-Pivot,ARG  
      ▪ DEL, Carlos, Delfino, Escolta,ARG 
      ▪ MAC, Jonas, Maciulis, Alero,LIT 
      ▪ BOG, Andrew, Bogut, Pivot,AUS  */;

/*Puedes añadir más datos de prueba. */;
/*Crea con funciones lo siguiente: */;

CREATE DATABASE ejercicio3;
USE ejercicio3;

CREATE TABLE PAIS (
    codigo VARCHAR(3) PRIMARY KEY,
    nombre VARCHAR(50)
);

CREATE TABLE JUGADOR (
    codigo VARCHAR(3) PRIMARY KEY,
    nombre VARCHAR(50),
    apellidos VARCHAR(50),
    posicion VARCHAR(50),
    seleccion VARCHAR(3),
    FOREIGN KEY (seleccion) REFERENCES PAIS(codigo)
);

INSERT INTO PAIS VALUES ('ESP', 'España');
INSERT INTO PAIS VALUES ('ARG', 'Argentina');
INSERT INTO PAIS VALUES ('AUS', 'Australia');
INSERT INTO PAIS VALUES ('LIT', 'Lituania');

INSERT INTO JUGADOR VALUES ('RUB', 'Ricky', 'Rubio', 'Base', 'ESP');
INSERT INTO JUGADOR VALUES ('NAV', 'Sergio', 'Lull', 'Alero', 'ESP');
INSERT INTO JUGADOR VALUES ('SCO', 'Luis', 'Scola', 'Ala-Pivot', 'ARG');
INSERT INTO JUGADOR VALUES ('DEL', 'Carlos', 'Delfino', 'Escolta', 'ARG');
INSERT INTO JUGADOR VALUES ('MAC', 'Jonas', 'Maciulis', 'Alero', 'LIT');
INSERT INTO JUGADOR VALUES ('BOG', 'Andrew', 'Bogut', 'Pivot', 'AUS');

/*1. Muestra los nombres y apellidos de todos los jugadores, en mayúsculas, ordenados por apellido y nombre. */;
SELECT UPPER(nombre) AS Nombre, UPPER(apellidos) AS Apellidos
FROM JUGADOR
ORDER BY apellidos, nombre;

/*2. Muestra el nombre y apellidos del jugador o jugadores cuyo apellido es el más largo (formado por más letras). */;
SELECT nombre, apellidos
FROM JUGADOR
WHERE CHAR_LENGTH(apellidos) = (SELECT MAX(CHAR_LENGTH(apellidos)) FROM JUGADOR);

/*3. Muestra el apellido, una coma, un espacio y después el nombre de todos los jugadores de 
     "España" (aparecerán datos como "Rubio, Ricky"). Para ello, usa la función "CONCAT". */;
SELECT CONCAT(apellidos, ', ', nombre) AS NombreCompleto
FROM JUGADOR
WHERE seleccion = 'ESP';

/*4. Muestra las 4 primeras letras de los apellidos de los jugadores de "Argentina", ordenados de forma descendente. */;
SELECT LEFT(apellidos, 4) AS ApellidoCorto
FROM JUGADOR
WHERE seleccion = 'ARG'
ORDER BY apellidos DESC;

/*5. Muestra los nombres de todos los jugadores, reemplazando "Ricky" por "Ricardo". */;
SELECT REPLACE(nombre, 'Ricky', 'Ricardo') AS NombreModificado, apellidos
FROM JUGADOR;

/*6. Muestra los valores: "Don " seguido del nombre y del apellido de los jugadores 
     (aparecerán datos como "Don Andrew Bogut"), usando "CONCAT"  */;
SELECT CONCAT('Don ', nombre, ' ', apellidos) AS DonNombreCompleto
FROM JUGADOR;

/*7. Muestra el nombre y apellidos de todos los jugadores cuyo país contenga una N en el 
     nombre. Debes eliminar los espacios iníciales y finales de ambos campos, en caso de que existan. */;
SELECT TRIM(JUGADOR.nombre) AS Nombre, TRIM(JUGADOR.apellidos) AS Apellidos
FROM JUGADOR, PAIS
WHERE JUGADOR.seleccion = PAIS.codigo 
    AND PAIS.nombre LIKE '%N%';

/*8. Muestra al revés el apellido de los jugadores de Australia.  */;
SELECT REVERSE(apellidos) AS ApellidoAlRevés
FROM JUGADOR
WHERE seleccion = 'AUS';

/*9. Muestra una cadena formada por 10 guiones, Nombre y otros 10 guiones.*/;
SELECT CONCAT(REPEAT('-', 10), nombre, REPEAT('-', 10)) AS NombreDecorado
FROM JUGADOR;
