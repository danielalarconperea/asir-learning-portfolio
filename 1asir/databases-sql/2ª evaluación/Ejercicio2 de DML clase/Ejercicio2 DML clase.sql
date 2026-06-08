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

-- Selecciona los nombres de los fabricantes cuyo nombre contiene la letra "o".
SELECT nombre 
FROM fabricante 
WHERE nombre LIKE '%o%';
-- Selecciona los nombres y precios de los productos cuyo precio es mayor a 50 y menor o igual a 300.
SELECT nombre, precio 
FROM producto 
WHERE precio > 50 
AND precio <= 300;
-- Selecciona los nombres de los productos que contienen la palabra "GeForce".
SELECT nombre 
FROM producto 
WHERE nombre LIKE '%GeForce%';
-- Selecciona los nombres de los fabricantes cuyo nombre no comienza con "A".
SELECT nombre 
FROM fabricante 
WHERE nombre NOT LIKE 'A%';
-- Selecciona los nombres de los productos cuyo precio es menor a 200 y que no son fabricados por el fabricante con ID 6.
SELECT nombre 
FROM producto 
WHERE precio < 200 
AND id_fabricante != 6;
-- Selecciona los nombres de los productos cuyo precio es mayor a 500 o fabricados por el fabricante con ID 8.
SELECT nombre 
FROM producto 
WHERE precio > 500 
OR id_fabricante = 8;
-- Selecciona los nombres de los fabricantes cuyo nombre termina con "e".
SELECT nombre 
FROM fabricante 
WHERE nombre LIKE '%e' ;
-- Selecciona los nombres y precios de los productos fabricados por el fabricante con ID 4 y cuyo precio supera los 100.
SELECT nombre, precio 
FROM producto 
WHERE id_fabricante = 4 
AND precio > 100;
-- Selecciona los nombres de los productos cuyo precio es menor a 150 o el fabricante tiene un nombre que empieza con "L".
SELECT producto.nombre 
FROM producto 
JOIN fabricante ON producto.id_fabricante = fabricante.id 
WHERE producto.precio < 150 
OR fabricante.nombre LIKE 'L%';
-- Selecciona los nombres de los fabricantes cuyo nombre no contiene la letra "a".
SELECT nombre 
FROM fabricante 
WHERE nombre NOT LIKE '%a%';
-- Selecciona los nombres y precios de los productos cuyo precio no está entre 100 y 500.
SELECT nombre, precio 
FROM producto 
WHERE precio 
NOT BETWEEN 100 AND 500;
-- Selecciona los nombres de los productos cuyo nombre comienza con "D" y tienen un precio mayor a 50.
SELECT nombre 
FROM producto 
WHERE nombre LIKE 'D%' 
AND precio > 50;
-- Selecciona los nombres de los fabricantes cuyo nombre contiene la letra "u" y no termina con "e".
SELECT nombre 
FROM fabricante 
WHERE nombre LIKE '%u%' 
AND nombre NOT LIKE '%e';
-- Selecciona los nombres y precios de los productos cuyo precio es mayor a 100 y cuyo nombre no contiene la palabra "RAM".
SELECT nombre, precio 
FROM producto 
WHERE precio > 100 
AND nombre NOT LIKE '%RAM%';
-- Selecciona los nombres de los fabricantes cuyo nombre es más largo de 5 caracteres.
SELECT nombre 
FROM fabricante 
WHERE nombre LIKE '%_____%';
-- Selecciona los nombres de los productos que no tienen un precio superior a 300.
SELECT nombre 
FROM producto 
WHERE NOT precio > 300;
-- Selecciona los nombres de los productos que no contienen la palabra "Disco".
SELECT nombre 
FROM producto 
WHERE nombre NOT LIKE '%Disco%';
-- Selecciona los nombres de los fabricantes que contienen la letra "x" o comienzan con "H".
SELECT nombre 
FROM fabricante
 WHERE nombre LIKE '%x%' 
 OR nombre LIKE 'H%'
-- Selecciona los nombres y precios de los productos ordenados primero por precio ascendente y luego por nombre descendente.
SELECT nombre, precio 
FROM producto 
ORDER BY precio ASC, nombre DESC;
-- Selecciona los nombres de los fabricantes cuyo nombre comienza con una vocal.
SELECT nombre 
FROM fabricante 
WHERE nombre LIKE '[aeiou]%'
