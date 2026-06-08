-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: empresas
-- /*
-- Server version	8.0.17

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/ empresas;
USE empresas;

--
-- Table structure for table `cliente`
--


DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido1` varchar(100) NOT NULL,
  `apellido2` varchar(100) DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `categoría` int(10) unsigned DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,'Aarón','Rivero','Gómez','Almería',100),(2,'Adela','Salas','Díaz','Granada',200),(3,'Adolfo','Rubio','Flores','Sevilla',NULL),(4,'Adrián','Suárez',NULL,'Jaén',300),(5,'Marcos','Loyola','Méndez','Almería',200),(6,'María','Santana','Moreno','Cádiz',100),(7,'Pilar','Ruiz',NULL,'Sevilla',300),(8,'Pepe','Ruiz','Santana','Huelva',200),(9,'Guillermo','López','Gómez','Granada',225),(10,'Daniel','Santana','Loyola','Sevilla',125);
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `comercial`
--

DROP TABLE IF EXISTS `comercial`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `comercial` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido1` varchar(100) NOT NULL,
  `apellido2` varchar(100) DEFAULT NULL,
  `comisión` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `comercial`
--

LOCK TABLES `comercial` WRITE;
/*!40000 ALTER TABLE `comercial` DISABLE KEYS */;
INSERT INTO `comercial` VALUES (1,'Daniel','Sáez','Vega',0.15),(2,'Juan','Gómez','López',0.13),(3,'Diego','Flores','Salas',0.11),(4,'Marta','Herrera','Gil',0.14),(5,'Antonio','Carretero','Ortega',0.12),(6,'Manuel','Domínguez','Hernández',0.13),(7,'Antonio','Vega','Hernández',0.11),(8,'Alfredo','Ruiz','Flores',0.05);
/*!40000 ALTER TABLE `comercial` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedido`
--

DROP TABLE IF EXISTS `pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedido` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `total` double NOT NULL,
  `fecha` date DEFAULT NULL,
  `id_cliente` int(10) unsigned NOT NULL,
  `id_comercial` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id_cliente` (`id_cliente`),
  KEY `id_comercial` (`id_comercial`),
  CONSTRAINT `pedido_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`),
  CONSTRAINT `pedido_ibfk_2` FOREIGN KEY (`id_comercial`) REFERENCES `comercial` (`id`)
) ENGINE=InnoDB;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedido`
--

LOCK TABLES `pedido` WRITE;
/*!40000 ALTER TABLE `pedido` DISABLE KEYS */;
INSERT INTO `pedido` VALUES (1,150.5,'2020-10-05',5,2),(2,270.65,'2018-09-10',1,5),(3,65.26,'2020-10-05',2,1),(4,110.5,'2018-08-17',8,3),(5,948.5,'2020-09-10',5,2),(6,2400.6,'2018-07-27',7,1),(7,5760,'2019-09-10',2,1),(8,1983.43,'2020-10-10',4,6),(9,2480.4,'2018-10-10',8,3),(10,250.45,'2015-06-27',8,2),(11,75.29,'2018-08-17',3,7),(12,3045.6,'2020-04-25',2,1),(13,545.75,'2019-01-25',6,1),(14,145.82,'2020-02-02',6,1),(15,370.85,'2019-03-11',1,5),(16,2389.23,'2019-03-11',1,5);
/*!40000 ALTER TABLE `pedido` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

/* Dump completed on 2021-01-26 11:02:20*/;




/* 1. Devuelve un listado con todos los pedidos ordenados por fecha más reciente */
SELECT * FROM pedido ORDER BY fecha DESC;

/* 2. Devuelve los dos pedidos de mayor valor */
SELECT * FROM pedido ORDER BY total DESC LIMIT 2;

/* 3. Listado de IDs de clientes con pedidos (sin repetir) */
SELECT DISTINCT id_cliente FROM pedido;

/* 4. Pedidos de 2017 con total superior a 500€ (no hay datos en 2017) */
SELECT * FROM pedido WHERE YEAR(fecha) = 2017 AND total > 500;

/* 5. Comerciales con comisión entre 0.05 y 0.11 */
SELECT nombre, apellido1, apellido2 
FROM comercial 
WHERE comisión BETWEEN 0.05 AND 0.11;

/* 6. Comisión de mayor valor */
SELECT MAX(comisión) AS max_comision FROM comercial;

/* 7. Clientes con segundo apellido no nulo, ordenados */
SELECT id, nombre, apellido1 
FROM cliente 
WHERE apellido2 IS NOT NULL 
ORDER BY apellido1, apellido2, nombre;

/* 8. Nombres que empiezan por A y terminan en n o empiezan por P */
SELECT nombre 
FROM cliente 
WHERE nombre LIKE 'A%n' OR nombre LIKE 'P%' 
ORDER BY nombre;

/* 9. Nombres que no empiezan por A, ordenados */
SELECT nombre 
FROM cliente 
WHERE nombre NOT LIKE 'A%' 
ORDER BY nombre;

/* 10. Comerciales con nombres terminados en 'o' (únicos) */
SELECT DISTINCT nombre 
FROM comercial 
WHERE nombre LIKE '%o';

/* 11. Clientes con pedidos (sin repetir y ordenados) */
SELECT DISTINCT c.id, c.nombre, c.apellido1, c.apellido2 
FROM cliente c, pedido p 
WHERE c.id = p.id_cliente 
ORDER BY c.nombre, c.apellido1, c.apellido2;

/* 12. Todos los pedidos con datos del cliente ordenados */
SELECT c.*, p.* 
FROM cliente c, pedido p 
WHERE c.id = p.id_cliente 
ORDER BY c.nombre, c.apellido1, c.apellido2;

/* 13. Todos los pedidos con datos del comercial ordenados */
SELECT co.*, p.* 
FROM comercial co, pedido p 
WHERE co.id = p.id_comercial 
ORDER BY co.nombre, co.apellido1, co.apellido2;

/* 14. Suma total de todos los pedidos */
SELECT SUM(total) AS total_pedidos FROM pedido;

/* 15. Valor medio de los pedidos */
SELECT AVG(total) AS media_pedidos FROM pedido;

/* 16. Número total de clientes */
SELECT COUNT(*) AS total_clientes FROM cliente;

/* 17. Mayor cantidad en pedidos */
SELECT MAX(total) AS max_pedido FROM pedido;

/* 18. Máxima categoría por ciudad */
SELECT ciudad, MAX(categoría) AS max_categoria 
FROM cliente 
GROUP BY ciudad;

/* 19. Máximo pedido por cliente y fecha */
SELECT c.id, c.nombre, c.apellido1, c.apellido2, p.fecha, MAX(p.total) AS max_total
FROM cliente c, pedido p
WHERE c.id = p.id_cliente
GROUP BY c.id, p.fecha;

/* 20. Máximo pedido diario por cliente mayor a 2000€ */
SELECT c.id, c.nombre, c.apellido1, c.apellido2, p.fecha, MAX(p.total) AS max_total
FROM cliente c, pedido p
WHERE c.id = p.id_cliente
GROUP BY c.id, p.fecha
HAVING MAX(p.total) > 2000;

/* 21. Pedido más caro usando subconsulta */
SELECT * 
FROM pedido 
WHERE total = (SELECT MAX(total) FROM pedido);

/* 22. Máximo pedido por comercial en 2019 */
SELECT co.id, co.nombre, co.apellido1, co.apellido2, MAX(p.total) AS max_total
FROM comercial co, pedido p
WHERE co.id = p.id_comercial AND YEAR(p.fecha) = 2019
GROUP BY co.id;

/* 23. Total de pedidos por cliente */
SELECT c.id, c.nombre, c.apellido1, c.apellido2, COUNT(p.id) AS total_pedidos
FROM cliente c
LEFT JOIN pedido p ON c.id = p.id_cliente
GROUP BY c.id;

/* 24. Pedidos por cliente en 2020 */
SELECT c.id, c.nombre, c.apellido1, c.apellido2, COUNT(p.id) AS total_pedidos_2020
FROM cliente c
LEFT JOIN pedido p ON c.id = p.id_cliente AND YEAR(p.fecha) = 2020
GROUP BY c.id;

/* 25. Máximo pedido por cliente incluyendo 0 */
SELECT c.id, c.nombre, c.apellido1, IFNULL(MAX(p.total), 0) AS max_cantidad
FROM cliente c
LEFT JOIN pedido p ON c.id = p.id_cliente
GROUP BY c.id;

/* 26. Pedido más caro por año */
SELECT p.*
FROM pedido p
INNER JOIN (
    SELECT YEAR(fecha) AS año, MAX(total) AS max_total
    FROM pedido
    GROUP BY YEAR(fecha)
) AS max_pedidos ON YEAR(p.fecha) = max_pedidos.año AND p.total = max_pedidos.max_total;

/* 27. Pedidos de Adela Salas Díaz */
SELECT p.*
FROM cliente c, pedido p
WHERE c.id = p.id_cliente 
AND c.nombre = 'Adela' 
AND c.apellido1 = 'Salas' 
AND c.apellido2 = 'Díaz';

/* 28. Número de pedidos de Daniel Sáez Vega */
SELECT COUNT(*) AS total_pedidos
FROM comercial co, pedido p
WHERE co.id = p.id_comercial 
AND co.nombre = 'Daniel' 
AND co.apellido1 = 'Sáez' 
AND co.apellido2 = 'Vega';

/* 29. Cliente con pedido más caro de 2019 */
SELECT c.*
FROM cliente c, pedido p
WHERE c.id = p.id_cliente 
AND YEAR(p.fecha) = 2019 
AND p.total = (SELECT MAX(total) FROM pedido WHERE YEAR(fecha) = 2019);

/* 30. Clientes con pedidos en 2020 >= media de 2020 */
SELECT c.*, p.*
FROM cliente c, pedido p
WHERE c.id = p.id_cliente 
AND YEAR(p.fecha) = 2020 
AND p.total >= (SELECT AVG(total) FROM pedido WHERE YEAR(fecha) = 2020);