/* Enocontrar el nombre de los empleados que trabajan en departamentos ubicados en "New York" */

SELECT ename FROM emp e
WHERE EXISTS (
    SELECT 1
    FROM dept d
    WHERE d.deptno = e.deptno
    AND d.loc = "New York"
);

SELECT ename FROM emp e, dept d
WHERE e.deptno = d.deptno
AND d.loc = "New York";

SELECT ename FROM emp
WHERE deptno IN (SELECT deptno FROM dept WHERE loc = "New York");


/* Listar departamentos que tienen al menos un empleado */

SELECT dname FROM dept d
WHERE EXISTS (
    SELECT 1
    FROM emp e
    WHERE d.deptno = e.deptno
);

SELECT DISTINCT dname
FROM emp e INNER JOIN dept d
ON e.deptno = d.deptno;

SELECT dname FROM dept
WHERE deptno IN (SELECT DISTINCT deptno FROM emp);


/* Mostrar los empleados que tengan jefe (cuyo jefe existe) */

SELECT ename FROM emp e
WHERE EXISTS (
    SELECT 1
    FROM emp j
    WHERE j.empno = e.mgr
);

SELECT e.ename FROM emp e
INNER JOIN emp j ON e.mgr = j.empno;

Select ename AS empleado FROM emp
WHERE mgr IN (SELECT empno FROM emp);

/* Mostrar el nombre de los departamentos que no tengan empleados */

SELECT dname FROM dept d
WHERE NOT EXISTS (
    SELECT 1
    FROM emp e
    WHERE e.deptno = d.deptno
);

SELECT dname FROM dept d
LEFT JOIN emp e ON e.deptno = d.deptno
WHERE e.empno IS NULL;

SELECT dname FROM dept
WHERE deptno not IN (
    SELECT DISTINCT deptno FROM emp 
    WHERE deptno IS NOT NULL
    );