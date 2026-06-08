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

--Actualizar el nombre del fabricante
UPDATE fabricante SET nombre = 'Asus Inc.' WHERE id=1;

--Actualizar el precio del producto
UPDATE producto SET precio = 95.99 WHERE id=1;

--Cambial el fabricante de un producto
UPDATE producto SET id_fabricante = 2 WHERE id=3;

--Incrementar el precio de todos los productos en un 10%
UPDATE producto SET precio = precio * 1.10;

SELECT * FROM fabricante;
SELECT * FROM producto;



--Eliminar todo:¡¡Cuidado!!
DELETE FROM producto;

--Eliminar un fabricante específico:
DELETE FROM fabricante WHERE id = 9;
SELECT * FROM fabricante;

--Eliminar todos los productos con un precio menor a 100
DELETE FROM producto WHERE precio < 100;
SELECT * FROM producto;



--Seleccionar todos los nombres de los fabricantes
SELECT nombre FROM fabricante;

--Seleccionar los nombres y os precios de todos los productos
SELECT nombre, precio FROM producto;

--Seleccionar los nombres de los productos cuyo precio es mayor a 100
SELECT nombre FROM producto WHERE precio > 100;

--Seleccionar el nombre de los productos fabricados por el fabricante con ID 5
SELECT nombre FROM producto WHERE id_fabricante = 5;

--Seleccionar los nombres de los fabricantes que no son Asus
SELECT nombre FROM fabricante WHERE nombre != 'Asus';

--Seleccionar los nombres de los productos ordenados por su precio de manera ascendente
SELECT nombre FROM producto 
ORDER BY precio ASC;

--Seleccionar los nombre de los fabricantes ordenados alfabéticamente de manera descendente
SELECT nombre FROM fabricante 
ORDER BY nombre DESC;

--Seleccionar el nombre y precio de los productos que valen más de 300 euros ordenados por precio
SELECT nombre, precio FROM producto WHERE precio > 300 
ORDER BY precio;