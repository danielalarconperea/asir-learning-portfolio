-- Practica de Triggers
-- 1. Necesitamos almacenar en una tabla llamada "usuarios" los datos de los usuarios de un sitio web. Cada vez que el usuario cambia su clave se debe almacenar en otra tabla llamada "claves_ant" el dato de la clave antigua.
-- Creamos ambas tablas con las siguientes estructuras:
CREATE TABLE usuarios(
 nombre varchar(30) primary key,
 clave varchar(30)
);
CREATE TABLE claves_ant(
 id int auto_increment primary key,
 nombre varchar(30),
 clave varchar(30)
);

-- Inserta valores de prueba para comprobarlo.
INSERT INTO usuarios (nombre, clave) VALUES ('dani', '1234'), ('pepe', '5678');

UPDATE usuarios SET clave = 'abcd' WHERE nombre = 'dani';

UPDATE usuarios SET clave = 'abcd' WHERE nombre = 'dani';

SELECT * FROM usuarios;
SELECT * FROM claves_ant;

-- Realizar un trigger que cada vez que se cambie la clave en la tabla “usuarios”, se añada una nueva fila a la tabla “claves_ant”.

DROP TRIGGER IF EXISTS trigger_claves_ant;

DELIMITER //
CREATE TRIGGER trigger_claves_ant
BEFORE UPDATE ON usuarios
FOR EACH ROW
BEGIN
 IF OLD.clave <> NEW.clave THEN
  INSERT INTO claves_ant(nombre, clave) VALUES (OLD.nombre, OLD.clave);
 END IF;
END //
DELIMITER ;


-- 2. Administrar los datos de dos tablas llamadas: "libros" y "ventas". Cada vez que se produzca la venta de libros reducir el campo stock de la tabla "libros" mediante un trigger definido en la tabla ventas.
create table libros(
idlibro int auto_increment primary key,
 titulo varchar(50),
 autor varchar(50),
 precio float, 
 stock int
);
create table ventas(
idventa int auto_increment primary key,
 idlibro int,
 precio float,
 cantidad int
);

-- Inserta valores de prueba para comprobarlo.
INSERT INTO libros (titulo, autor, precio, stock) VALUES 
('Don Quijote', 'Cervantes', 20.5, 10),
('El Principito', 'Saint-Exupéry', 15.0, 5);

-- Realizamos una venta (debe restar stock)
INSERT INTO ventas (idlibro, precio, cantidad) VALUES (1, 20.5, 2);
-- Verificamos reducción (quijote debería tener 8)
SELECT * FROM libros;

-- Borramos una venta (debe devolver stock)
DELETE FROM ventas WHERE idventa = 1;
-- Verificamos devolución (quijote debería volver a 10)
SELECT * FROM libros;

-- Realizar un trigger que cada vez que se añade una fila a la tabla ventas, se modifique en cantidad(campo de la tabla ventas) el stock de la tabla libros.
-- Realizar un trigger, para controlar las devoluciones de los libros, cada vez que se borre una fila de la tabla de ventas, se tiene que devolver esos libros al stock de la tabla libros.

DROP TRIGGER IF EXISTS trigger_ventas;
DELIMITER //
CREATE TRIGGER trigger_ventas
AFTER INSERT ON ventas
FOR EACH ROW
BEGIN
 UPDATE libros SET stock = stock - NEW.cantidad WHERE idlibro = NEW.idlibro;
END //
DELIMITER ;

DROP TRIGGER IF EXISTS trigger_devoluciones;
DELIMITER //
CREATE TRIGGER trigger_devoluciones
AFTER DELETE ON ventas
FOR EACH ROW
BEGIN 
 UPDATE libros SET stock = stock + OLD.cantidad WHERE idlibro = OLD.idlibro;
END //
DELIMITER ;



-- 3. Crea una base de datos llamada que contenga una tabla llamada alumnos.
-- Tabla alumnos:
CREATE TABLE alumnos (
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 nombre VARCHAR(50) NOT NULL,
 apellido1 VARCHAR(50) NOT NULL,
 apellido2 VARCHAR(50), 
 email VARCHAR(50)
);
-- 1. Escriba un procedimiento almacenado llamado crear_email que dados los parámetros de entrada: nombre, apellido1, apellido2 y dominio, cree una dirección de email y la devuelva como salida.
-- La dirección de correo electrónico con el siguiente formato:
-- • El primer carácter del parámetro nombre.
-- • Los tres primeros caracteres del parámetro apellido1.
-- • Los tres primeros caracteres del parámetro apellido2.
-- • El carácter @.
-- • El dominio pasado como parámetro.

DROP PROCEDURE IF EXISTS crear_email;
DELIMITER //
CREATE PROCEDURE crear_email(
    IN nombre VARCHAR(50),
    IN apellido1 VARCHAR(50),
    IN apellido2 VARCHAR(50),
    IN dominio VARCHAR(50),
    OUT email VARCHAR(100)
)BEGIN
    SET email = CONCAT(
        LEFT(nombre, 1),
        LEFT(apellido1, 3),
        LEFT(apellido2, 3),
        "@", dominio
    );
END //
DELIMITER ;

-- 2.- Escribe un trigger que se ejecuta sobre la tabla alumnos.
-- Vamos a controlar la inserción, si el nuevo valor del email que se quiere insertar es NULL, entonces se le creará automáticamente una dirección de email y se insertará en la tabla.
-- Si el nuevo valor del email no es NULL se guardará en la tabla el valor del email.
-- Para crear la nueva dirección de email se deberá hacer uso del procedimiento crear_email creado anteriormente.

DROP TRIGGER IF EXISTS trigger_alumnos_email;
DELIMITER //

CREATE TRIGGER trigger_alumnos_email
BEFORE INSERT ON alumnos
FOR EACH ROW
BEGIN
    DECLARE email_generado VARCHAR(100);
    IF NEW.email IS NULL THEN
        call crear_email(NEW.nombre, NEW.apellido1, NEW.apellido2, "gmail.com", email_generado);
        SET NEW.email = email_generado;
    END IF;
END //
DELIMITER ;

-- 3. La tabla log_cambios_email contiene los siguientes campos:
CREATE TABLE log_cambios_email (
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 id_alumno INT UNSIGNED,
 fecha_hora DATETIME,
 old_email VARCHAR(50) NOT NULL,
 new_email VARCHAR(50) NOT NULL);
-- Añade un nuevo trigger que se ejecuta después de una operación de actualización.
-- Cada vez que un alumno modifique su dirección de email se deberá insertar un nuevo registro en una tabla llamada log_cambios_email.

DROP TRIGGER IF EXISTS guardar_log_email;
DELIMITER //

CREATE TRIGGER guardar_log_email
AFTER UPDATE ON alumnos
FOR EACH ROW
BEGIN
    IF OLD.email <> NEW.email THEN
        INSERT INTO log_cambios_email(id_alumno, fecha_hora, old_email, new_email) 
        VALUES (NEW.id, NOW(), OLD.email, NEW.email);
    END IF;
END //
DELIMITER ;

-- 4. La tabla log_alumnos_eliminados contiene los siguientes campos:
CREATE TABLE log_alumnos_eliminados (
 id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
 id_alumno INT UNSIGNED,
 fecha_hora DATETIME,
 nombre VARCHAR(50) NOT NULL,
 apellido1 VARCHAR(50) NOT NULL,
 apellido2 VARCHAR(50), 
 email VARCHAR(50)
);
-- Añade un nuevo trigger que cada vez que se elimine un alumno de la tabla alumnos se deberá insertar un nuevo registro en una tabla llamada log_alumnos_eliminados.

DROP TRIGGER IF EXISTS trigger_alumnos_eliminados;
DELIMITER // 

CREATE TRIGGER trigger_alumnos_eliminados
AFTER DELETE ON alumnos
FOR EACH ROW 
BEGIN
    INSERT INTO log_alumnos_eliminados(id_alumno, fecha_hora, nombre, apellido1, apellido2, email)
    VALUES (OLD.id, NOW(), OLD.nombre, OLD.apellido1, OLD.apellido2, OLD.email);
END //
DELIMITER ;

-- PRUEBAS EJERCICIO 3
-- 1. Insertar alumno con email NULL (debe generarlo el trigger)
INSERT INTO alumnos (nombre, apellido1, apellido2) 
VALUES ('Daniel', 'Lopez', 'Garcia');

-- 2. Insertar alumno con email personalizado (no debe cambiarlo)
INSERT INTO alumnos (nombre, apellido1, apellido2, email) 
VALUES ('Maria', 'Perez', 'Ruiz', 'maria@educa.madrid.org');

-- Ver resultados inserción
SELECT * FROM alumnos;

-- 3. Modificar email de un alumno (debe saltar al log)
UPDATE alumnos SET email = 'danitriggers@gmail.com' WHERE nombre = 'Daniel';
-- Modificar nombre pero no email (no debe saltar al log)
UPDATE alumnos SET nombre = 'Dani' WHERE nombre = 'Daniel';

-- Ver log de cambios
SELECT * FROM log_cambios_email;

-- 4. Eliminar un alumno (debe ir al log de alumnos eliminados)
DELETE FROM alumnos WHERE nombre = 'Maria';

-- Ver log de eliminados
SELECT * FROM log_alumnos_eliminados;
