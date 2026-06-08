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


-- 1. Mostrar la versión de MySQL
SELECT VERSION();

-- 2. Mostrar la fecha y hora actual
SELECT NOW();

-- 3. Comparar las cadenas "Salesianos" y "SALESIANOS" (case-sensitive)
SELECT STRCMP('Salesianos', 'SALESIANOS');

-- 4. Longitud de los nombres (ename) en EMP
SELECT ename, LENGTH(ename) AS Longitud FROM emp;

-- 5. Concatenar Ename y Job con guión
SELECT CONCAT(ename, '-', job) AS Ename_Job FROM emp;

-- 6. Localizaciones (loc) al revés en DEPT
SELECT REVERSE(loc) AS Loc_Reversa FROM dept;

-- 7. Rellenar ename con puntos hasta 20 caracteres
SELECT RPAD(ename, 20, '.') AS Ename_Relleno FROM emp;

-- 8. Dname en mayúsculas
SELECT UPPER(dname) AS Dname_Mayus FROM dept;

-- 9. Nombre y año de contratación
SELECT ename, YEAR(hiredate) AS Anio_Contratacion FROM emp;

-- 10. Hora actual
SELECT CURTIME() AS Hora_Actual;

-- 11. Día de la semana de hoy
SELECT DAYNAME(NOW()) AS Dia_Semana;

-- 12. Fecha actual en formato específico
SELECT DATE_FORMAT(NOW(), '%e de %M de %Y') AS Fecha_Formateada;

-- 13. Fecha de contratación en formato específico
SELECT DATE_FORMAT(hiredate, '%e de %M de %Y') AS Fecha_Contrato FROM emp;

-- 14. Salario más alto
SELECT MAX(sal) AS Salario_Maximo FROM emp;

-- 15. Primer empleado contratado
SELECT * FROM emp ORDER BY hiredate ASC LIMIT 1;

-- 16. Salario medio
SELECT AVG(sal) AS Salario_Promedio FROM emp;

-- 17. Media salarial por departamento con salario mínimo > 1000
SELECT deptno, AVG(sal) AS Media_Salarial 
FROM emp 
GROUP BY deptno 
HAVING MIN(sal) > 1000;

-- 18. Empleados sin comisión
SELECT COUNT(*) AS Sin_Comision FROM emp WHERE comm IS NULL;

-- 19. Media salarial por departamento
SELECT deptno, AVG(sal) AS Media_Salarial 
FROM emp 
GROUP BY deptno;

-- 20. Suma salarial por departamento (suma > 2000)
SELECT deptno, SUM(sal) AS Suma_Salarial 
FROM emp 
GROUP BY deptno 
HAVING SUM(sal) > 2000;

-- 21. Probar funciones numéricas
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