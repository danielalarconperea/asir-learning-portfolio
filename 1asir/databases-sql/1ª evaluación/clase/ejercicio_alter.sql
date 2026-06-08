-- Diseña una base de datos para un sistema de gestión de proyectos 

-- Empleados: 
-- id_empleado (INT) - Clave primaria, identificador único de cada empleado.
-- nombre (VARCHAR) - Nombre del empleado, campo obligatorio.
-- apellido (VARCHAR) - Apellido del empleado, campo obligatorio.
-- email (VARCHAR) - Correo electrónico del empleado, debe ser único.

-- Proyectos: 
-- id_proyecto (INT) - Clave primaria, identificador único de cada proyecto.
-- nombre (VARCHAR) - Nombre del proyecto, campo obligatorio.
-- fecha_inicio (DATE) - Fecha de inicio del proyecto, campo obligatorio.
-- presupuesto (float) - Presupuesto asignado al proyecto

-- Tareas: 
-- id_empleado (INT) - Clave foránea que se refiere a id_empleado en la tabla Empleados.
-- id_proyecto (INT) - Clave foránea que se refiere a id_proyecto en la tabla Proyectos.
-- descripcion (VARCHAR) - Descripción de la tarea, campo obligatorio.


-- Ejericios Alter:
-- Añadir una columna a la tabla Empleados para almacenar el teléfono del empleado.
-- Modificar el tamaño del campo nombre en la tabla Proyectos a 150 caracteres.
-- Agregar una restricción de clave única en el campo nombre de la tabla Proyectos para evitar duplicados
-- Eliminar la columna telefono de la tabla Empleados

CREATE DATABASE sistema_de_gestión_de_proyectos;
USE sistema_de_gestión_de_proyectos;
create table Empleados(
    id_empleado INT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    email VARCHAR(50) unique);
create table Proyectos(
    id_proyecto INT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    fecha_inicio DATE NOT NULL,
    presupuesto float);
CREATE TABLE Tareas (
    id_empleado INT REFERENCES Empleados(id_empleado),
    id_proyecto INT REFERENCES Proyectos(id_proyecto),
    descripcion VARCHAR(200) NOT NULL,
    PRIMARY KEY(id_empleado,id_proyecto));

describe Empleados;
describe Proyectos;
describe Tareas;

ALTER TABLE Empleados ADD teléfono INT;
describe Empleados;
ALTER TABLE Proyectos MODIFY nombre VARCHAR(150) NOT NULL;
describe Proyectos;
ALTER TABLE Proyectos MODIFY nombre varchar(150) unique NOT NULL;
describe Proyectos;
ALTER TABLE Empleados DROP teléfono;
describe Empleados;
DROP DATABASE sistema_de_gestión_de_proyectos