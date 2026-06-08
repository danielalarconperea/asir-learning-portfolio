SELECT * FROM emp CROSS JOIN dept; /* El cross funciona como el antiguo join sin la palabra join */
SELECT * FROM emp LEFT JOIN dept ON emp.deptno = dept.deptno;

INSERT INTO emp VALUES(2222, "Carlos", "teacher", 7839, "2025-3-13", 1000, 200, NULL);

SELECT * FROM emp INNER JOIN dept ON emp.deptno = dept.deptno;

SELECT * FROM emp LEFT JOIN dept ON emp.deptno = dept.deptno;

SELECT * FROM emp RIGHT JOIN dept ON emp.deptno = dept.deptno;


/* SELECT * FROM emp FULL JOIN dept ON emp.deptno = dept.deptno; ESTO NO SE PUEDE HACER PERO SI DE OTRA FORMA: */;

SELECT * FROM emp LEFT JOIN dept ON emp.deptno = dept.deptno
UNION
SELECT * FROM emp RIGHT JOIN dept ON emp.deptno = dept.deptno;

