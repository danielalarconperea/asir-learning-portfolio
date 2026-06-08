-- Ejemplo de Examen SGBD 
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

-- 1. Encuentra a todos los empleados cuyo salario sea mayor a 2000. 
SELECT ename 
FROM emp 
WHERE sal > 2000;
-- 2. Busca a los empleados que trabajan en el departamento de Ventas (Sales). 
SELECT emp.ename 
FROM dept, emp 
WHERE dept.deptno=emp.deptno 
AND dept.dname = 'sales';
-- 3. Obtén los datos de los empleados contratados después del 1 de enero de 1982. 
SELECT * 
FROM emp 
WHERE hiredate > '82-01-01';
-- 4. Encuentra a los empleados que trabajan en la ciudad de Dallas. 
SELECT emp.ename 
FROM emp, dept 
WHERE dept.deptno=emp.deptno 
AND dept.loc = 'Dallas'; 
-- 5. Muestra los datos de los empleados cuyo nombre empiece por 'S'. 
SELECT * 
FROM emp 
WHERE ename LIKE 'S%';
-- 6. Encuentra a los empleados cuyo salario esté entre 1500 y 2500. 
SELECT ename 
FROM EMP 
WHERE sal BETWEEN 1500 AND 2500;
-- 7. Obtén los datos de los empleados que trabajan en los departamentos 20 o 30. 
SELECT * 
FROM emp 
WHERE deptno IN(20,30);
-- 8. Muestra a los empleados contratados entre el 1 de enero de 1981 y el 31 de diciembre de 1982. 
SELECT ename 
FROM emp 
WHERE hiredate BETWEEN '82-01-01' AND '82-12-31';
-- 9. Busca a los empleados cuyo trabajo sea 'Clerk' o 'Salesman'. 
SELECT ename 
FROM emp 
WHERE job IN('Clerk', 'Salesman');
-- 10. Encuentra a los empleados que trabajan en los departamentos 10, 20, o 30 y cuyo salario sea mayor a 2000. 
SELECT ename 
FROM emp 
WHERE deptno IN(10,20,30) 
AND sal < 2000;
-- 11. Muestra los empleados cuyo nombre termine en 's'. 
SELECT ename 
FROM emp 
WHERE ename LIKE '%s';
-- 12. Busca a los empleados cuyo nombre tenga la letra 'a' en la tercera posición. 
SELECT ename 
FROM emp 
WHERE ename LIKE '__a%'; 
-- 13. Encuentra a los empleados cuyo nombre contenga la cadena 'ar'. 
SELECT ename 
FROM emp 
WHERE ename LIKE '%ar%';
-- 14. Muestra a los empleados cuyo nombre empiece por 'S' o 'M'.
SELECT ename 
FROM emp 
WHERE ename 
LIKE 'S%' 
OR ename LIKE 'M%';
-- 15. Busca a los empleados cuyo trabajo no contenga la letra 'a'. 
SELECT ename 
FROM emp 
WHERE job 
NOT LIKE '%a%';
-- 16. alcula el salario promedio de todos los empleados. 
SELECT AVG(sal) 
FROM emp;
-- 17. Encuentra el empleado con el salario más alto.
SELECT ename, sal 
FROM emp 
WHERE sal = (SELECT MAX(sal)
             FROM emp);
-- o
SELECT ename, sal 
FROM emp 
ORDER BY sal DESC 
LIMIT 1;
-- 18. Cuenta cuántos empleados hay en cada departamento. 
SELECT deptno, COUNT(empno) AS numero_empleados 
FROM emp 
GROUP BY deptno;
-- o mejor
SELECT dept.dname, COUNT(emp.empno) AS numero_empleados 
FROM emp, dept 
WHERE dept.deptno=emp.deptno 
GROUP BY dept.dname;
-- 19. Calcula el salario total de cada departamento. 
SELECT dept.dname, SUM(sal) AS salario_total
FROM emp, dept 
WHERE dept.deptno=emp.deptno 
GROUP BY dept.dname;
-- 20. Encuentra el empleado más antiguo de cada departamento. 
SELECT dept.dname, emp.ename AS empleado_mas_antiguo, hiredate
FROM emp, dept 
WHERE dept.deptno=emp.deptno 
AND hiredate = (SELECT MIN(hiredate) 
                FROM emp 
                WHERE emp.deptno = dept.deptno);
-- 21. Encuentra a los empleados que tienen un salario mayor que el salario promedio. 
SELECT ename
FROM emp
WHERE sal > (SELECT AVG(sal)
             FROM emp);
-- 22. Obtén los empleados que trabajan en el mismo departamento que 'Allen'. 
SELECT ename 
FROM emp 
WHERE deptno = (SELECT deptno 
                FROM emp 
                WHERE ename = 'Allen') 
AND ename != 'Allen';
-- 23. Busca a los empleados que tienen un salario mayor que el salario máximo de los empleados del departamento 30.
SELECT ename 
FROM emp 
WHERE sal > (SELECT MAX(sal) 
             FROM emp 
             WHERE deptno = 30);
-- 24. Encuentra a los empleados que no son gerentes.
SELECT ename 
FROM emp 
WHERE empno NOT IN(SELECT DISTINCT mgr 
                   FROM emp 
                   WHERE mgr IS NOT NULL);
-- 25. Obtén los empleados que fueron contratados antes que cualquier empleado del departamento 20. 
SELECT ename 
FROM emp 
WHERE hiredate < (SELECT MIN(hiredate) 
             FROM emp 
             WHERE deptno = 20);
-- 26. Encuentra el nombre y el salario de los empleados que tienen el salario más alto en cada departamento. 
SELECT ename, sal AS salario_mas_alto
FROM emp
WHERE (deptno, sal) IN (SELECT deptno, MAX(sal) 
                        FROM emp 
                        GROUP BY deptno);
-- 27. Obtén una lista de todos los departamentos y el número de empleados en cada uno. 
SELECT dname, COUNT(empno) AS numero_empleados
FROM emp, dept
WHERE dept.deptno=emp.deptno
GROUP BY dname;
-- 28. Muestra el nombre del empleado, su trabajo y el nombre del departamento donde trabaja. 
SELECT emp.ename, emp.job, dept.dname
FROM emp, dept
WHERE emp.deptno=dept.deptno;
-- 29. Encuentra a todos los empleados que no tienen un gerente asignado. 
SELECT ename 
FROM emp 
WHERE mgr IS NULL;
-- 30. Obtén una lista de todos los departamentos, incluso si no tienen empleados. 
SELECT dept.dname, emp.ename 
FROM dept, emp 
WHERE dept.deptno = emp.deptno 
ORDER BY dept.dname;