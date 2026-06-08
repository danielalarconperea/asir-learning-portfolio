/* Obtener el nombre del departamento donde 
trabaja el empleado con el salario más bajo */;

SELECT dname FROM dept
WHERE deptno = (SELECT deptno FROM empleado
                WHERE sal = (SELECT MIN(sal) FROM emp));

/* Obtener el nombre del empleado con  el salario más alto */;
SELECT ename FROM emp 
WHERE sal = (SELECT MAX(sal) FROM emp);

/* Obtener el nombre del empleado que tiene el segundo salario más alto*/;
SELECT ename, sal FROM emp 
WHERE sal = (SELECT MAX(sal) FROM emp
             WHERE sal < (SELECT MAX(sal) FROM emp));

/* Obtener los nombres de los empleados que trabajan en departamentos 
ubicados en 'Dallas' o 'Chicago' (hay que usar in) */;
SELECT ename FROM emp 
WHERE deptno in (SELECT deptno FROM dept 
                 WHERE loc in ('Dallas', 'Chicago'));

/* Listar los departamentos que tienen al menos 
un empleado con un salario superior a 3000 */;
SELECT dname FROM dept 
WHERE deptno in (SELECT deptno FROM emp 
                  WHERE sal > 3000);

/* Encontrar los empleados (mostramos nombre y salario)
que ganan más que todos los empleados del departamento 30 (usar ALL)*/;
SELECT ename, sal FROM emp 
WHERE sal > ALL (SELECT sal FROM emp 
                 WHERE deptno = 30);

/* Encontrar los empleados (mostramos nombre y salario) 
que ganan más que al menos un empleado del departamento 30 (usar ANY)*/;
SELECT ename, sal FROM emp 
WHERE sal > ANY (SELECT sal FROM emp 
                 WHERE deptno = 30);

/* Encontrar los empleados cuyo salario 
es menor que el salario de algún 'manager' */;
SELECT ename, sal FROM emp 
WHERE sal < ANY (SELECT sal FROM emp 
                 WHERE job = 'Manager');

/**/;
/**/;