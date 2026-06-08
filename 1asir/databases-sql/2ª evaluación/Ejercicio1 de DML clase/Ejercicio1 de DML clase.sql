-- Ejercicio Clase 1 DML 
CREATE DATABASE tienda;
USE tienda;
CREATE TABLE fabricante (
  id INT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL
);
CREATE TABLE producto (
  id INT PRIMARY KEY,
  nombre VARCHAR(100) NOT NULL,
  precio FLOAT NOT NULL,
  id_fabricante INT REFERENCES fabricante(id)
);

INSERT INTO fabricante VALUES(1, 'Asus');
INSERT INTO fabricante VALUES(2, 'Lenovo');
INSERT INTO fabricante VALUES(3, 'Hewlett-Packard');
INSERT INTO fabricante VALUES(4, 'Samsung');
INSERT INTO fabricante VALUES(5, 'Seagate');
INSERT INTO fabricante VALUES(6, 'Crucial');
INSERT INTO fabricante VALUES(7, 'Gigabyte');
INSERT INTO fabricante VALUES(8, 'Huawei');
INSERT INTO fabricante VALUES(9, 'Xiaomi');
SELECT * FROM fabricante;

INSERT INTO producto VALUES(1, 'Disco duro SATA3 1TB', 86.99, 5);
INSERT INTO producto VALUES(2, 'Memoria RAM DDR4 8GB', 120, 6);
INSERT INTO producto VALUES(3, 'Disco SSD 1 TB', 150.99, 4);
INSERT INTO producto VALUES(4, 'GeForce GTX 1050Ti', 185, 7);
INSERT INTO producto VALUES(5, 'GeForce GTX 1080 Xtreme', 755, 6);
INSERT INTO producto VALUES(6, 'Monitor 24 LED Full HD', 202, 1);
INSERT INTO producto VALUES(7, 'Monitor 27 LED Full HD', 245.99, 1);
INSERT INTO producto VALUES(8, 'Portátil Yoga 520', 559, 2);
INSERT INTO producto VALUES(9, 'Portátil Ideapd 320', 444, 2);
INSERT INTO producto VALUES(10, 'Impresora HP Deskjet 3720', 59.99, 3);
INSERT INTO producto VALUES(11, 'Impresora HP Laserjet Pro M26nw', 180, 3);
SELECT * FROM producto;

-- Consultas:
-- • Inserta un nuevo fabricante
INSERT INTO fabricante VALUES(10, 'Nvidia');
-- • Inserta un nuevo producto .
INSERT INTO producto VALUES(12, 'RTX 5090', 199.99, 9);
-- • Elimina el fabricante Asus. ¿Es posible eliminarlo? 
DELETE FROM fabricante WHERE id = 1; --No es posible eliminarlo, porque hay una clave ajena
-- • Elimina el fabricante Xiaomi. ¿Es posible eliminarlo? 
DELETE FROM fabricante WHERE id = 9; --Si es posible eliminarlo
-- • Actualiza el código del fabricante Lenovo y asígnale el valor 20 como código, ¿es posible? 
-- NO, primero hay que actualizar en producto para evitar conflicto de clave externa 
UPDATE producto SET id_fabricante = 20 WHERE id_fabricante = 2;
UPDATE fabricante SET id = 20 WHERE id = 2;
-- • Actualiza el nombre del fabricante 3 por “HP”. 
UPDATE fabricante SET nombre = 'HP' WHERE id = 3;
-- • Actualiza el nombre del producto con id 2 por “ Memoria RAM DDR4 16GB”
UPDATE producto SET nombre = 'Memoria RAM DDR4 16GB' WHERE id = 2;
-- • Actualiza el precio de todos los productos sumándole 5 € al precio actual.
UPDATE producto SET precio = precio + 5;
-- • Muestra todos los productos que cuesten más de 100 euros. 
SELECT * FROM producto WHERE precio > 100;
-- • Muestra todos los productos del fabricante 1. 
SELECT * FROM producto WHERE id_fabricante = 1;
-- • Muestra las columnas nombre y precio de todos los productos. 
SELECT nombre, precio FROM producto;
-- • Selecciona los nombres de todos los fabricantes.
SELECT nombre FROM fabricante;
-- • Selecciona los nombres y precios de los productos cuyo precio es mayor a 100.
SELECT nombre, precio FROM producto WHERE precio > 100;
-- • Selecciona el nombre de todos los fabricantes ordenados alfabéticamente.
SELECT nombre FROM fabricante 
ORDER BY nombre ASC;
-- • Selecciona los nombres de los productos cuyo precio es mayor a 150, ordenados por precio descendente.
SELECT nombre FROM producto WHERE precio > 150
ORDER BY precio DESC;
-- • Selecciona todos los productos fabricados por el fabricante con ID 3.
SELECT * FROM producto WHERE id_fabricante = 3;
-- • Seleccionar productos cuyo nombre sea Disco SSD 1 TB
SELECT * FROM producto WHERE nombre = 'Disco SSD 1 TB';
-- • Seleccionar productos cuyo nombre NO sea Disco SSD 1 TB
SELECT * FROM producto WHERE nombre != 'Disco SSD 1 TB'
-- • Seleccionar fabricantes con id mayor a 5 y ordenalo por nombre
SELECT * FROM fabricante WHERE id > 5
ORDER BY nombre;