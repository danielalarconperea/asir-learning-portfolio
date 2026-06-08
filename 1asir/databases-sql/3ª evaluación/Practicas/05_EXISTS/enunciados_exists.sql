/*
Obtener el resultado de las siguientes consultas con:
- join
- subconsulta
- exists
*/


/* 1.-Listar los nombres de los empleados que trabajan en el departamento de 'SALES'. */
SELECT ename FROM emp e
WHERE EXISTS (
    SELECT 1 FROM dept d
    WHERE e.deptno = d.deptno
    AND dname = 'SALES'
);

SELECT ename FROM emp e 
INNER JOIN dept d ON e.deptno = d.deptno
WHERE dname = 'SALES';

SELECT ename FROM emp
WHERE deptno IN (
    SELECT deptno FROM dept
    WHERE dname = 'SALES'
);


/* 2.- Mostrar los nombres departamentos donde el salario de alguno de sus empleados es superior a 2500. */
SELECT dname FROM dept d
WHERE EXISTS (
    SELECT 1 FROM emp e
    WHERE e.deptno = d.deptno
    AND sal > 2500
);

SELECT dname FROM dept d 
INNER JOIN emp e ON e.deptno = d.deptno
WHERE sal > 2500;

SELECT dname FROM dept
WHERE deptno IN (
    SELECT deptno FROM emp
    WHERE sal > 2500
);


/* 3.-Listar los nombres de los empleados que trabajan en departamentos ubicados en 'Chicago' o 'Dallas'. */ 
SELECT ename FROM emp e
WHERE EXISTS (
    SELECT 1 FROM dept d
    WHERE e.deptno = d.deptno
    AND loc IN ('Chicago', 'Dallas')
);

SELECT ename FROM emp e 
INNER JOIN dept d ON e.deptno = d.deptno
WHERE loc IN ('Chicago', 'Dallas');

SELECT ename FROM emp
WHERE deptno IN (
    SELECT deptno FROM dept
    WHERE loc IN ('Chicago', 'Dallas')
);