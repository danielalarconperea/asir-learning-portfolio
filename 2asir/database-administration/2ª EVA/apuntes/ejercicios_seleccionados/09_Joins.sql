CREATE DATABASE Ejercicio_JOIN;
USE Ejercicio_JOIN

CREATE TABLE Empleados (
    id INT PRIMARY KEY,
    nombre VARCHAR(50),
    departamento_id INT
);

CREATE TABLE Departamentos (
    id INT PRIMARY KEY,
    nombre VARCHAR(50)
);

-- Insertar más empleados
INSERT INTO Empleados VALUES 
(5, 'Laura', 2), 
(6, 'Pedro', 4), 
(7, 'Sofía', NULL), 
(8, 'Diego', 5), 
(9, 'Elena', 5), 
(10, 'Miguel', 2), 
(1, 'Ana', 1), 
(2, 'Carlos', 2), 
(3, 'María', 1), 
(4, 'Juan', NULL);

-- Insertar más departamentos
INSERT INTO Departamentos VALUES 
(4, 'Finanzas'), 
(5, 'Tecnología'), 
(6, 'Soporte Técnico'), 
(1, 'Ventas'), 
(2, 'Marketing'), 
(3, 'Recursos Humanos');



/*1.- Muestra el nombre de los empleados y el nombre de sus departamentos.*/;
SELECT empleados.nombre, Departamentos.nombre FROM Empleados INNER JOIN Departamentos ON empleados.departamento_id = Departamentos.id;

/*2.-Muestra todos los departamentos y los empleados asignados a ellos, incluyendo departamentos sin empleados.*/;
SELECT Departamentos.nombre, empleados.nombre FROM Empleados RIGHT JOIN Departamentos ON empleados.departamento_id = Departamentos.id;

/*3.-Muestra todos los empleados y sus departamentos, incluyendo aquellos que no tienen departamento asignado.*/;
SELECT empleados.nombre, Departamentos.nombre FROM Empleados LEFT JOIN Departamentos ON empleados.departamento_id = Departamentos.id;

/*4.-Muestra todos los empleados y todos los departamentos, incluyendo empleados sin departamento y departamentos sin empleados.*/;
SELECT empleados.nombre, Departamentos.nombre FROM Empleados RIGHT JOIN Departamentos ON empleados.departamento_id = Departamentos.id
UNION
SELECT empleados.nombre, Departamentos.nombre FROM Empleados LEFT JOIN Departamentos ON empleados.departamento_id = Departamentos.id;

/*5.-Muestra el nombre de los empleados que no tienen un departamento asignado.*/;
SELECT empleados.nombre FROM Empleados LEFT JOIN Departamentos ON empleados.departamento_id = Departamentos.id WHERE departamento_id IS NULL;

/*6.-Muestra el nombre de los departamentos que no tienen empleados asignados.*/;
SELECT Departamentos.nombre FROM Empleados RIGHT JOIN Departamentos ON empleados.departamento_id = Departamentos.id WHERE Empleados.nombre IS NULL;