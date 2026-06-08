-- Usando la BBDD EMP-DEPT

DROP DATABASE IF EXISTS emp_dept;
CREATE DATABASE emp_dept;
USE emp_dept;
CREATE TABLE dept (
    deptno INT PRIMARY KEY,
    dname VARCHAR(14),
    loc VARCHAR(13)
);

CREATE TABLE emp (
    empno INT PRIMARY KEY,
    ename VARCHAR(10),
    job VARCHAR(9),
    mgr INT, 
    hiredate DATE,
    sal FLOAT,
    comm FLOAT,
    deptno INT REFERENCES dept(deptno)
);


-- 1.- Crear un trigger sobre la tabla EMP para que no permita nuevos empleados en
-- departamentos que no existen.



-- 2.- Crear un trigger para impedir que se aumente el salario de un empleado en más de un 50%.

-- 3.- Crear una tabla emp_baja:
CREATE TABLE emp_baja (
    dni char(4) PRIMARY KEY,
    nomemp varchar2(15),
    mng char(4),
    salario integer,
    usuario varchar2(15),
    fecha date
);

-- Crear un trigger que inserte una fila en la tabla emp_baja cuando se borre una fila en la tabla empleados.

-- 4.- Crea un trigger para que me avise que el salario total por departamento (suma de los salarios de los empleados por departamento) sea superior a 7.000. Usarlo con update.

-- 5.- Crear un trigger para impedir que un empleado nuevo y su jefe pertenezcan a departamentos distintos.

-- 6.- Crea un trigger que cada vez que se borre un departamento, se borren todos los empleados de ese departamento.