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

--AND OR NOT
--Seleccionar productos con precio entre 100 y 200
SELECT * FROM producto WHERE precio BETWEEN 100 AND 200;

SELECT * FROM producto WHERE precio >= 100 AND precio <= 200;

--Uso OR: seleccionar productos con precion > 200 o Id_fabricante < 3
SELECT * FROM producto WHERE precio >= 200 OR id_fabricante < 3;

--Uso NOT: muestrame los productos que no sean del fabricante '2', ordenado por precio.
SELECT * FROM producto WHERE NOT id_fabricante = 2 ORDER BY precio;
SELECT * FROM producto WHERE id_fabricante != 2 ORDER BY precio;

--Uso IN:
SELECT * FROM producto WHERE Id_fabricante IN(1, 3, 5);
SELECT * FROM producto WHERE id_fabricante = 1 OR id_fabricante = 3 OR id_fabricante = 5;

--Uso LIKE:
-- Selecciona todos los registros donde la columna 'nombre' comienza con 's'
SELECT * FROM producto WHERE nombre LIKE 's%';  -- Ejemplo: 'silla', 'sombrero'

-- Selecciona todos los registros donde la columna 'nombre' termina con 's'
SELECT * FROM producto WHERE nombre LIKE '%s';  -- Ejemplo: 'gatos', 'naranjas'

-- Selecciona todos los registros donde la columna 'nombre' contiene 'an' en cualquier posición
SELECT * FROM producto WHERE nombre LIKE '%an%';  -- Ejemplo: 'manzana', 'plátano'

-- Selecciona todos los registros donde la columna 'nombre' tiene una 'a' seguida de cualquier carácter y luego una 'e'
SELECT * FROM producto WHERE nombre LIKE 'a_e%';  -- Ejemplo: 'aceite', 'arete'

-- Selecciona todos los registros donde la columna 'nombre' tiene una vocal (a, e, i, o, u) en una posición específica
SELECT * FROM producto WHERE nombre LIKE 'p[aeiou]tern';  -- Ejemplo: 'petern', 'patern'

-- Selecciona todos los registros donde la columna 'nombre' tiene una letra entre 'a' y 'c' en una posición específica
SELECT * FROM producto WHERE nombre LIKE 'p[a-c]trón';  -- Ejemplo: 'patrón', 'pbtrón'

-- Selecciona todos los registros donde la columna 'nombre' no tiene una vocal en una posición específica
SELECT * FROM producto WHERE nombre LIKE 'p%[^aeiou]ttern';  -- Ejemplo: 'p1ttern', 'pxttern'