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

--1. Obtener todos los datos de todos los empleados.;
SELECT * FROM emp;
--2. Obtener todos los datos de todos los departamentos.;
SELECT * FROM dept;
--3. Obtener todos los datos de los administrativos (su trabajo es, en inglés, ’CLERK’).;
SELECT * 
FROM emp 
WHERE job = 'clerk';
--4. Igual que el anterior, pero ordenado por el nombre.;
SELECT * 
FROM emp 
WHERE job = 'clerk' 
ORDER BY ename;
--5. Obtén el mismo resultado de la pregunta anterior, pero modificando la sentencia SQL.;
SELECT empno, ename, job, mgr, hiredate, sal, comm, deptno
FROM emp 
WHERE job = 'clerk'
ORDER BY ename;
--6. Obtén el número (código), nombre y salario de los empleados.;
SELECT empno, ename, sal 
FROM emp;
--7. Lista los nombres de todos los departamentos.;
SELECT dname 
FROM dept;
--8. Igual al anterior, pero ordenándolos por nombre.;
SELECT dname 
FROM dept 
ORDER BY dname;
--9. Igual al anterior, pero ordenándolo por la ciudad (no se debe seleccionar la ciudad en el resultado).;
SELECT dname 
FROM dept 
ORDER BY loc;
--10. Igual al anterior, pero el resultado debe mostrarse ordenado por la ciudad en orden inverso.;
SELECT dname 
FROM dept 
ORDER BY loc;
--11. Obtener el nombre y empleo de todos los empleados, ordenado por salario.;
SELECT ename, job 
FROM emp 
ORDER BY sal;
--12. Obtener el nombre y empleo de todos los empleados, ordenado primero por su trabajo y luego por su salario.;
SELECT ename, job 
FROM emp 
ORDER BY job, sal;
--13. Igual al anterior, pero ordenando inversamente por empleo y normalmente por salario.;
SELECT ename, job 
FROM emp 
ORDER BY ename DESC, sal;
--14. Obtén los salarios y las comisiones de los empleados del departamento 30.;
SELECT sal, comm 
FROM emp 
WHERE deptno = 30; 
--15. Igual al anterior, pero ordenado por comisión.;
SELECT sal, comm 
FROM emp 
WHERE deptno = 30 
ORDER BY comm;
--16. Obtén las comisiones de los empleados de forma que no se repitan.;
SELECT DISTINCT comm 
FROM emp;
--17. Obtén el nombre de empleado y su comisión SIN FILas repetidas.;
SELECT DISTINCT ename, comm 
FROM emp;
--18. Obtén los nombres de los empleados y sus salarios, de forma que no se repitan filas.;
SELECT DISTINCT ename, sal 
FROM emp;
--19. Obtén las comisiones de los empleados y sus números de departamento, de forma que no se repitan filas.;
SELECT DISTINCT comm, deptno 
FROM emp;
--20. Obtén los nuevos salarios de los empleados del departamento 30, que resultarían de sumar a su salario una ;
--gratificación de 1000. Muestra también los nombres de los empleados.;
SELECT ename, sal + 1000 
FROM emp 
WHERE deptno = 30;
--21. Lo mismo que la anterior, pero mostrando también su salario original, y haz que la columna que almacena ;
--el nuevo salario se denomine NUEVO SALARIO.;
SELECT ename, sal, sal + 1000 AS "NUEVO SALARIO" 
FROM emp 
WHERE deptno = 30;
--22. Halla los empleados que tienen una comisión superior a la mitad de su salario.;
SELECT ename 
FROM emp 
WHERE comm > sal/2;
--23. Halla los empleados que no tienen comisión, o que la tengan menor o igual que el 25% de su salario.;
SELECT ename 
FROM emp 
WHERE comm IS NULL 
OR comm <= 0.25*sal; 
--24. Obtén una lista de nombres de empleados y sus salarios ordenado por salario;
SELECT ename, sal 
FROM emp
ORDER BY sal;
--25. Hallar el código, salario y comisión de los empleados cuyo código sea mayor que 7500.;
SELECT empno, sal, comm 
FROM emp 
WHERE empno > 7500;
--26. Obtén todos los datos de los empleados que contengan la letra “J”;
SELECT * 
FROM emp 
WHERE ename LIKE '%J%';
--27. Obtén el salario, comisión y salario total (salario+comision) de los empleados con comisión(NO sea NULL), ;
--ordenando el resultado por número de empleado.;
SELECT sal, comm, sal + comm AS salario_total
FROM emp 
WHERE comm IS NOT NULL 
ORDER BY empno;
--28. Lista la misma información que el anterior, pero para todos los empleados.;
SELECT sal, comm, ifNULL(sal + comm, sal) AS salario_total 
FROM emp 
ORDER BY empno;
--29. Muestra el nombre de los empleados que, teniendo un salario superior a 1000, tengan como jefe al ;
--empleado cuyo código es 7698.;
SELECT ename 
FROM emp 
WHERE sal > 1000 
AND mgr = 7698;
--30. Halla los datos contrarios del resultado del ejercicio anterior(usando NOT).;
SELECT ename 
FROM emp 
WHERE NOT (sal > 1000 AND mgr = 7698);
--31. Indica para cada empleado el porcentaje que supone su comisión sobre su salario, ordenando el resultado ;
--por el nombre del mismo.;
SELECT ename, (comm / sal * 100) AS porcentaje_comisión_sobre_salario
FROM emp 
WHERE comm IS NOT NULL 
ORDER BY ename;
--32. Hallar los empleados del departamento 10 cuyo nombre no contiene la cadena ‘LA.’;
SELECT ename 
FROM emp 
WHERE deptno = 10 
AND ename NOT LIKE '%LA.%';
--33. Obtén los empleados que no son supervisados por ningún otro.;
SELECT ename 
FROM emp 
WHERE mgr IS NULL;
--34. Obtén los nombres de los departamentos que no sean Ventas (SALES) ni investigación (RESEARCH). Ordena el ;
--resultado por la localidad del departamento.;
SELECT dname 
FROM dept 
WHERE dname NOT IN ('Sales', 'Research') 
ORDER BY loc;
--35. Deseamos conocer el nombre de los empleados y el código del departamento de los administrativos(CLERK) ;
--que no trabajan en el departamento 10, y cuyo salario es superior a 800, ordenado por fecha de contratación.;
SELECT ename, deptno 
FROM emp 
WHERE job = 'Clerk' 
AND deptno != 10 
AND sal > 800 
ORDER BY hiredate;
--36. Para los empleados que tengan comisión, obtén sus nombres y el cociente entre su salario y su comisión ;
--(excepto cuando la comisión sea cero), ordenando el resultado por nombre.;
SELECT ename, sal/comm 
FROM emp
WHERE comm > 0 
ORDER BY ename;
--37. Lista toda la información sobre los empleados cuyo nombre completo tenga exactamente 5 caracteres.;
SELECT * 
FROM emp 
WHERE ename LIKE '_____';
--38. Lo mismo, pero para los empleados cuyo nombre tenga tres letras.;
SELECT * 
FROM emp 
WHERE ename LIKE '___';
--39. Halla los datos de los empleados que, o bien su nombre empieza por A y su salario es superior a 1000, o ;
--bien reciben comisión y trabajan en el departamento 30.;
SELECT * 
FROM emp 
WHERE (ename LIKE 'A%' AND sal > 1000) 
OR (comm > 0 AND deptno = 30);
--40. Halla el nombre, el salario y el sueldo total (salario+comision) de todos los empleados, ordenando el ;
--resultado primero por salario y luego por el sueldo total.;
SELECT ename, sal, ifNULL(sal+comm, sal) AS sueldo_total 
FROM emp 
ORDER BY sal, sueldo_total;
--41. Obtén el nombre, salario y la comisión de los empleados que perciben un salario que está entre la mitad de ;
--la comisión y la propia comisión.;
SELECT ename, sal, comm 
FROM emp 
WHERE sal BETWEEN comm/2 AND comm;
--42. Obtén el complementario del anterior. Son los empleados que NO cumplen esa condición.;
SELECT ename, sal, comm 
FROM emp 
WHERE sal NOT BETWEEN comm/2 AND comm;
--43. Lista los nombres y empleos de aquellos empleados cuyo empleo acaba en MAN y cuyo nombre empieza por A.;
SELECT ename, job 
FROM emp 
WHERE job LIKE '%MAN' 
AND ename LIKE 'A%';
--44. Lista los empleos de aquellos empleados cuyo empleo acaba en MAN y comienzan por A.;
SELECT job 
FROM emp 
WHERE job LIKE 'A%MAN';
--45. Halla los nombres de los empleados cuyo nombre no contengan la letra A ni la B.;
SELECT ename 
FROM emp 
WHERE ename NOT LIKE '%A%' AND ename NOT LIKE '%B%';
--46. Suponiendo que el año próximo la subida del sueldo total de cada empleado será del 6%, halla los nombres ;
--y el salario total actual, del año próximo de cada empleado;
SELECT ename, sal, sal+sal*0.06 AS salario_proximo_año
FROM emp;
--47. Lista los nombres y fecha de contratación de aquellos empleados que no son vendedores (SALESMAN).;
SELECT ename, hiredate 
FROM emp 
WHERE job != 'salesman';
--48. Obtén la información disponible de los empleados cuyo número es uno de los siguientes: 7844, 7900, 7521,;
--7521, 7782, 7934, 7678 y 7369, pero que no sea uno de los siguientes: 7902, 7839, 7499 ni 7878. La sentencia ;
--no debe complicarse innecesariamente, y debe dar el resultado correcto independientemente de lo ;
--empleados almacenados en la base de datos.;
SELECT * 
FROM emp 
WHERE empno IN (7844, 7900, 7521, 7782, 7934, 7678, 7369) 
AND empno NOT IN (7902, 7839, 7499, 7878);
--49. Ordena los empleados por su código de departamento, y luego de manera descendente por su número de empleado.;
SELECT * 
FROM emp 
ORDER BY deptno, empno DESC;
--50. Para los empleados que tengan como jefe a un empleado con código mayor que el suyo, obtén los que ;
--reciben de salario más de 1000 y menos de 2000, o que están en el departamento 30.;
SELECT * 
FROM emp 
WHERE empno < mgr 
AND (sal BETWEEN 1000 AND 2000 OR deptno = 30);
--51. Obtén el salario más alto de la empresa, el total destinado a comisiones y el número de empleados.;
SELECT MAX(sal), SUM(comm), COUNT(ename) 
FROM emp;
--52. Halla los datos de los empleados cuyo salario es mayor que el del empleado de código 7934, ordenando por el salario.;
SELECT * 
FROM emp 
WHERE sal > (SELECT sal 
             FROM emp 
             WHERE empno = 7934) 
ORDER BY sal;
--53. Obtén información en la que se reflejen los nombres, empleos y salarios tanto de los empleados que ;
--superan en salario a Allen como del propio Allen.;
SELECT ename, job, sal 
FROM emp 
WHERE sal >= (SELECT sal 
              FROM emp 
              WHERE ename = 'Allen');
--54. Halla el nombre el último empleado por orden alfabético.;
SELECT MAX(ename) 
FROM emp; 
--55. Halla el salario más alto, el más bajo, y la diferencia entre ellos.;
SELECT MAX(sal) AS salario_maximo, MIN(sal) AS salario_minimo, MAX(sal) - MIN(sal) AS diferencia 
FROM emp;
--56. Sin conocer los resultados del ejercicio anterior, ¿quienes reciben el salario más alto y el más bajo, y a ;
--cuánto ascienden estos salarios?;
SELECT * FROM emp WHERE sal = (SELECT MAX(sal) FROM emp)
UNION
SELECT * FROM emp WHERE sal = (SELECT MIN(sal) FROM emp);
--57. Considerando empleados con salario menor de 5000, halla la media de los salarios de los departamentos ;
--cuyo salario mínimo supera a 900. Muestra también el código y el nombre de los departamentos.;
SELECT dept.deptno, dept.dname, AVG(emp.sal) AS media_salario
FROM dept, emp
WHERE dept.deptno = emp.deptno
AND emp.sal < 5000
AND dept.deptno IN (SELECT emp.deptno
                    FROM emp
                    GROUP BY emp.deptno
                    HAVING MIN(emp.sal) > 900)
GROUP BY dept.deptno, dept.dname;
--58. ¿Qué empleados trabajan en ciudades de más de cinco letras? Ordena el resultado inversamente por ;
--ciudades y normalmente por los nombres de los empleados.;
SELECT emp.* 
FROM emp, dept
WHERE emp.deptno = dept.deptno
AND dept.loc LIKE '_____%'
ORDER BY dept.loc DESC, emp.ename asC;
--59. Halla los empleados cuyo salario supera o coincide con la media del salario de la empresa.;
SELECT * 
FROM emp 
WHERE sal >= (SELECT AVG(sal) FROM emp);
--60. Obtén los empleados cuyo salario supera al de sus compañeros de departamento.;
SELECT *
FROM emp 
WHERE (deptno, sal) 
       IN (SELECT deptno, MAX(sal) 
           FROM emp 
           GROUP BY deptno)
--61. ¿Cuántos empleos diferentes, cuántos empleados, y cuantos salarios diferentes encontramos en el ;
--departamento 30, y a cuánto asciende la suma de salarios de dicho departamento?;
SELECT COUNT(DISTINCT job) AS empleos_diferentes, 
       COUNT(empno) AS numero_empleados, 
       COUNT(DISTINCT sal) AS salarios_diferentes, 
       SUM(sal) AS suma_salarios
FROM emp
WHERE deptno = 30;
--62. ¿Cuántos empleados tienen comisión?;
SELECT COUNT(empno) AS empleados_con_comision FROM emp WHERE comm IS NOT NULL;
--63. ¿Cuántos empleados tiene el departamento 20?;
SELECT COUNT(empno) AS n_de_empleados 
FROM emp 
WHERE deptno = 20;
--64. Halla los departamentos que tienen más de tres empleados, y el número de empleados de los mismos.;
SELECT dept.dname, COUNT(emp.empno) AS numero_empleados
FROM dept, emp
WHERE dept.deptno = emp.deptno
GROUP BY dept.dname
HAVING COUNT(emp.empno) > 3;
--65. Obtén los empleados del departamento 10 que tienen el mismo empleo que alguien del departamento de ;
--Ventas. Desconocemos el código de dicho departamento.;
SELECT * 
FROM emp 
WHERE deptno = 10 
AND job IN (SELECT job 
            FROM emp 
            WHERE deptno = (SELECT deptno 
                            FROM dept 
                            WHERE dname = 'Sales'));
--66. Halla los empleados que tienen por lo menos un empleado a su mando, ordenados inversamente por nombre.;
SELECT * 
FROM emp 
WHERE empno IN (SELECT DISTINCT mgr FROM emp) 
ORDER BY ename DESC;
--67. Obtén información sobre los empleados que tienen el mismo trabajo que algún empleado que trabaje en Chicago.;
SELECT *
FROM emp
WHERE job IN (SELECT job 
              FROM emp 
              WHERE deptno = (SELECT deptno 
                              FROM dept 
                              WHERE loc = 'Chicago'));
--68. ¿Qué empleos distintos encontramos en la empresa, y cuántos empleados desempeñan cada uno de ellos?;
SELECT DISTINCT job, COUNT(*) AS numero_empleados
FROM emp
GROUP BY job;
--69. Halla la suma de salarios de cada departamento.;
SELECT deptno, SUM(sal) AS salario_departamento
FROM emp
GROUP BY deptno;
--70. Obtén todos los departamentos sin empleados.;
SELECT deptno, dname
FROM dept
WHERE deptno NOT IN (SELECT deptno FROM emp);
--71. Halla los empleados que no tienen a otro empleado a sus ordenes.;
SELECT ename 
FROM emp 
WHERE empno NOT IN (SELECT mgr FROM emp WHERE mgr IS NOT NULL);
--72. ¿Cuántos empleados hay en cada departamento, y cuál es la media anual del salario de cada uno (el salario ;
--almacenado es mensual)? Indique el nombre del departamento para clarificar el resultado.;
SELECT dept.dname AS nombre_departamento, COUNT(emp.empno) AS numero_empleados, AVG(emp.sal * 12) AS salario_anual_medio
FROM emp, dept
WHERE emp.deptno = dept.deptno     
GROUP BY dept.dname;
--73. Halla los empleados del departamento 30, por orden descendente de comisión;
SELECT ename 
FROM emp 
WHERE deptno = 30 
ORDER BY comm DESC;
--74. Obtén los empleados que trabajan en Dallas o New York.;
SELECT emp.ename AS nombre_emplado 
FROM emp, dept 
WHERE emp.deptno = dept.deptno 
AND dept.loc IN ('Dallas', 'New York');
