create database practica12;
use practica12;
create table dept(
deptno int,
dname varchar(14),
loc varchar(13),
primary key (deptno)
);
insert into dept values (10,"Accounting","New york");
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

insert into emp values (7369, "Smith", "Clerk", 7902, "80-12-17", 800, Null,20);
insert into emp values (7499, "Allen", "Salesman", 7698, "81-2-20", 1600, 300,30);
insert into emp values (7521, "Ward", "Salesman", 7698, "81-2-22", 1250, 500, 30);
insert into emp values (7566, "Jones", "Manager", 7839, "81-4-02", 2975, Null, 20);
insert into emp values (7654, "Martin", "Salesman", 7698, "81-9-28", 1250, 1400,30);
insert into emp values (7698, "Blake", "Manager", 7839, "81-5-01", 2850, Null,30);
insert into emp values (7782, "Clark", "Manager", 7839, "81-06-09", 2450, Null, 10);
insert into emp values (7788, "Scott", "Analyst", 7566, "82-12-9", 3000, Null, 20);
insert into emp values (7839, "King", "President", NULL,"81-11-17", 5000, Null, 10);
insert into emp values (7844, "Turner", "Salesman", 7698, "81-9-08", 1500, 0, 30);
insert into emp values (7876, "Adams", "Clerk", 7788, "83-1-12", 1100, Null, 20);
insert into emp values (7900, "James", "Clerk", 7698, "81-12-3", 950, Null, 30);
insert into emp values (7902, "Ford", "Analyst", 7566, "81-12-3", 3000, Null, 20);
insert into emp values (7934, "Miller", "Clerk", 7782, "82-7-23", 1300, Null, 10);


--Sumar salarios por departamento
SELECT deptno, SUM(sal) AS total_salarios
FROM emp
GROUP BY deptno;

--deptno | total_salarios
--------------------------
--10     | 8750
--20     | 10875
--30     | 9400

--Contar empleados por puesto
SELECT job, COUNT(*) AS numero_empleados
FROM emp
GROUP BY job;

--job      | numero_empleados
-----------------------------
--Clerk    | 4
--Salesman | 4
--Manager  | 3
--Analyst  | 2
--President| 1

--Salario promedio por departamento
SELECT deptno, AVG(sal) AS salario_promedio
FROM emp
GROUP BY deptno;

--deptno | salario_promedio
---------------------------
--10     | 2916.67
--20     | 2175.00
--30     | 1566.67

--Máximo y mínimo salario por departamento
SELECT deptno, MAX(sal) AS salario_maximo, MIN(sal) AS salario_minimo
FROM emp
GROUP BY deptno;

--deptno | salario_maximo | salario_minimo
------------------------------------------
--10     | 5000           | 1300
--20     | 3000           | 800
--30     | 2850           | 950

--Departamentos con un salario total mayor a 5000
SELECT deptno, SUM(sal) AS total_salarios
FROM emp
GROUP BY deptno
HAVING SUM(sal) > 5000;

--deptno | total_salarios
--------------------------
--10     | 8750
--20     | 10875
--30     | 9400

--Encontrar empleados con salarios superiores al promedio
SELECT empno, ename, sal
FROM emp
WHERE sal > (SELECT AVG(sal) FROM emp);

--empno | ename | sal
---------------------
--7566  | Jones | 2975
--7698  | Blake | 2850
--7788  | Scott | 3000
--7839  | King  | 5000
--7902  | Ford  | 3000

--Listar empleados que trabajan en departamentos con más de 4 empleados
SELECT empno, ename, deptno
FROM emp
WHERE deptno IN (SELECT deptno FROM emp GROUP BY deptno HAVING COUNT(*) > 4);

--empno | ename  | deptno
-------------------------
--7369  | Smith  | 20
--7499  | Allen  | 30
--7521  | Ward   | 30
--7566  | Jones  | 20
--7654  | Martin | 30
--7698  | Blake  | 30
--7788  | Scott  | 20
--7844  | Turner | 30
--7876  | Adams  | 20
--7900  | James  | 30
--7902  | Ford   | 20

--Encontrar el nombre y salario de los empleados que tienen el mismo salario que algún gerente
SELECT ename, sal
FROM emp
WHERE sal IN (SELECT sal FROM emp WHERE job = 'Manager');

--ename  | sal
-----------------
--Blake  | 2850
--Jones  | 2975
--Blake  | 2850
--Jones  | 2975


--El INNER JOIN selecciona registros que tienen valores coincidentes en ambas tablas.
SELECT emp.ename, emp.job, dept.dname
FROM emp
INNER JOIN dept ON emp.deptno = dept.deptno;

-- ename  | job       | dname
-- -----------------------------
-- Smith  | Clerk     | Research
-- Allen  | Salesman  | Sales
-- Ward   | Salesman  | Sales
-- Jones  | Manager   | Research
-- Martin | Salesman  | Sales
-- Blake  | Manager   | Sales
-- Clark  | Manager   | Accounting
-- Scott  | Analyst   | Research
-- King   | President | Accounting
-- Turner | Salesman  | Sales
-- Adams  | Clerk     | Research
-- James  | Clerk     | Sales
-- Ford   | Analyst   | Research
-- Miller | Clerk     | Accounting


--El LEFT JOIN selecciona todos los registros de la tabla izquierda (emp) y los registros coincidentes de la tabla derecha (dept). 
--Si no hay coincidencia, el resultado es NULL.
SELECT emp.ename, emp.job, dept.dname
FROM emp
LEFT JOIN dept ON emp.deptno = dept.deptno;

-- ename  | job       | dname
-- -----------------------------
-- Smith  | Clerk     | Research
-- Allen  | Salesman  | Sales
-- Ward   | Salesman  | Sales
-- Jones  | Manager   | Research
-- Martin | Salesman  | Sales
-- Blake  | Manager   | Sales
-- Clark  | Manager   | Accounting
-- Scott  | Analyst   | Research
-- King   | President | Accounting
-- Turner | Salesman  | Sales
-- Adams  | Clerk     | Research
-- James  | Clerk     | Sales
-- Ford   | Analyst   | Research
-- Miller | Clerk     | Accounting


--El RIGHT JOIN selecciona todos los registros de la tabla derecha (dept) y los registros coincidentes de la tabla izquierda (emp). 
--Si no hay coincidencia, el resultado es NULL.
SELECT emp.ename, emp.job, dept.dname
FROM emp
RIGHT JOIN dept ON emp.deptno = dept.deptno;

-- ename  | job       | dname
-- -----------------------------
-- Clark  | Manager   | Accounting
-- King   | President | Accounting
-- Miller | Clerk     | Accounting
-- Smith  | Clerk     | Research
-- Jones  | Manager   | Research
-- Scott  | Analyst   | Research
-- Adams  | Clerk     | Research
-- Ford   | Analyst   | Research
-- Allen  | Salesman  | Sales
-- Ward   | Salesman  | Sales
-- Martin | Salesman  | Sales
-- Blake  | Manager   | Sales
-- Turner | Salesman  | Sales
-- James  | Clerk     | Sales
-- NULL   | NULL      | Operation


--Encuentra la ciudad y la media de los salarios agrupados por departamento.
SELECT loc, AVG(sal) AS 'media_salario' 
FROM dept, emp 
WHERE emp.deptno=dept.deptno 
GROUP BY loc;


--Muestra el nombre de departamento, con el numero de empleados que tiene
SELECT dname, COUNT(*) 
WHERE emp.deptno = dept,deptno
GROUP BY dname;


--Muestra el nombre del departamento, con el número de empleados siempre que el número de empleados sea menor de 4;
SELECT dname, COUNT(*) 
WHERE emp.deptno = dept,deptno
GROUP BY dname
HAVING COUNT(*) < 4;