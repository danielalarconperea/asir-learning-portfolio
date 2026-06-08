/*Ejercicio 1:Listar los nombres de empleados que trabajan 
en departamentos ubicados en 'Chicago' o 'Boston'.*/;
SELECT ename FROM emp 
WHERE deptno IN (SELECT deptno FROM dept 
                 WHERE loc IN ('Chicago', 'Boston'));

/*Ejercicio 2:Mostrar los empleados que ganan más que al menos 
un empleado del departamento de 'Accounting' (deptno = 10).*/;
SELECT ename FROM emp
WHERE sal > ANY (SELECT sal FROM emp 
                 WHERE deptno = (SELECT deptno FROM dept 
                                 WHERE dname LIKE 'Accounting'));

/*Ejercicio 3 :Encontrar los empleados cuyo salario 
es mayor que todos los salarios de los 'Clerk'.*/;
SELECT ename FROM emp 
WHERE sal > ALL (SELECT sal FROM emp
                 WHERE job LIKE 'Clerk');

/*Ejercicio 4 :Obtener los departamentos cuyo salario promedio 
es mayor que el salario promedio de toda la empresa.*/;
SELECT dname, deptno FROM dept 
WHERE deptno IN (SELECT deptno FROM emp 
                 GROUP BY deptno 
                 HAVING AVG(sal) 
                 > (SELECT AVG(sal) FROM emp));

/*Ejercicio 5: Mostrar los empleados que ganan más 
que el salario promedio de su propio departamento.*/;
SELECT ename, sal, deptno FROM emp e
WHERE e.sal > ALL (SELECT AVG(sal) FROM emp WHERE e.deptno = deptno);

/*Ejercicio 6 :Listar los departamentos que no tienen empleados.*/;
SELECT dname FROM dept 
WHERE deptno NOT IN (SELECT deptno FROM emp);