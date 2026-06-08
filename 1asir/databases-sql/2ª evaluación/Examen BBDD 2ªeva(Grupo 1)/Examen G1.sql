-- Examen de Gestión de BBDD 2º Evaluación(grupo1)
-- Indica el comando SQL y una captura del resultado
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

-- 1. Encuentra a los empleados que fueron contratados en el año 1981.
SELECT ename
FROM emp 
WHERE hiredate BETWEEN '81-1-1' AND '81-12-31';
-- 2. Muestra todos los empleados y ordena a los empleados por salario de mayora menor.
SELECT ename, sal 
FROM emp 
ORDER BY sal DESC;
-- 3. Muestra el nombre del empleado con el salario más bajo.
SELECT ename, sal 
FROM emp 
WHERE sal = (SELECT min(sal) FROM emp);
-- 4. Encuentra a los empleados cuyo nombre contenga la palabra "an".
SELECT ename
FROM emp 
WHERE ename LIKE '%an%';
-- 5. Obtén los departamentos ordenados alfabéticamente por nombre.
SELECT dname
FROM dept 
ORDER BY dname;
-- 6. Calcula el número total de empleados en la empresa.
SELECT COUNT(*)
FROM emp;
-- 7. Encuentra el salario máximo, mínimo y promedio de todos los empleados.
SELECT MAX(sal), MIN(sal), AVG(sal) FROM emp;
-- 8. Calcula el número de empleados por cada trabajo.
SELECT job, COUNT(*)
FROM emp 
GROUP BY job;
-- 9. Obtén el departamento con el mayor número de empleados.
SELECT dname
FROM emp, dept
WHERE dept.deptno=emp.deptno 
GROUP BY emp.deptno
ORDER BY COUNT(*)
LIMIT 1;
-- 10.Encuentra el salario promedio de los empleados en cada departamento. 
SELECT dname, AVG(sal)
FROM emp, dept
WHERE dept.deptno=emp.deptno 
GROUP BY emp.deptno;
-- 11.Encuentra a los empleados que tienen un salario mayor que el promedio de su departamento.
SELECT e.ename, e.sal, e.deptno
FROM emp e
WHERE e.sal > (
    SELECT AVG(e2.sal)
    FROM emp e2
    WHERE e2.deptno = e.deptno
);
-- 12.Obtén los departamentos donde todos los empleados tienen un salario mayor a 2000.
SELECT d.dname
FROM emp e, dept d
WHERE d.deptno=e.deptno 
GROUP BY d.dname
HAVING MIN(e.sal) > 2000;
-- 13.Encuentra a los empleados que fueron contratados después del empleado más antiguo del departamento 30.
SELECT ename, hiredate
FROM emp
WHERE hiredate > (SELECT MIN(hiredate) FROM emp WHERE deptno = 30);
-- 14.Obtén una lista de los empleados que no tienen subordinados.
SELECT ename FROM emp WHERE mgr is NULL;

SELECT empno, ename
FROM emp
WHERE empno NOT IN (
    SELECT DISTINCT mgr
    FROM emp
    WHERE mgr IS NOT NULL
);
-- 15.Encuentra a los empleados que tienen el mismo trabajo que el empleado con el ID 7369.
SELECT ename FROM emp WHERE job = (SELECT job FROM emp WHERE empno = 7369);
-- 16.Muestra el nombre del empleado, su trabajo y el nombre de su gerente. 
SELECT ename, job, mgr FROM emp;
-- 17.Encuentra los departamentos que no tienen ningún empleado.
SELECT d.deptno, d.dname, d.loc
FROM dept d
WHERE d.deptno NOT IN (
    SELECT DISTINCT e.deptno
    FROM emp e
);
-- 18.Obtén una lista de todos los trabajos y el número de empleados que realizan cada trabajo.
SELECT job, COUNT(*) FROM emp GROUP BY job;
-- 19.Encuentra a los empleados que trabajan en la misma ciudad que su gerente. 
SELECT emp.ename AS Employee, 
       (SELECT mgr.ename 
        FROM emp AS mgr 
        WHERE mgr.empno = emp.mgr) AS Manager, 
       emp.job, 
       dept.loc 
FROM emp, dept, emp AS mgr_dept
WHERE emp.deptno = dept.deptno
  AND emp.mgr = mgr_dept.empno
  AND dept.loc = (SELECT loc 
                  FROM dept 
                  WHERE dept.deptno = mgr_dept.deptno);

-- o

SELECT e.ename AS Employee, 
       m.ename AS Manager, 
       e.job, 
       d.loc AS Employee_Location, 
       dm.loc AS Manager_Location
FROM emp e, dept d, emp m, dept dm
WHERE d.deptno = e.deptno
  AND e.mgr = m.empno
  AND m.deptno = dm.deptno
  AND d.loc = dm.loc;

-- 20.Muestra el nombre del empleado, su salario y el porcentaje que representa su salario respecto al salario máximo de la empresa.
SELECT ename, sal, (sal/(SELECT max(sal) FROM emp)*100) FROM emp;