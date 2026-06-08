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


/* 1. Devuelve un listado con todos los pedidos que se han realizado. Los pedidos deben estar 
      ordenados por la fecha de realización, mostrando en primer lugar los pedidos más recientes.*/;
      SELECT * FROM pedido ORDER BY fecha DESC;

/* 2. Devuelve todos los datos de los dos pedidos de mayor valor.*/;
      SELECT * FROM pedido ORDER BY total DESC LIMIT 2;

/* 3. Devuelve un listado con los identificadores de los clientes que han realizado algún pedido. Tenga
      en cuenta que no debe mostrar identificadores que estén repetidos.*/;
      SELECT DISTINCT id_cliente FROM pedido;

/* 4. Devuelve un listado de todos los pedidos que se realizaron durante el año 2017, cuya cantidad sea superior a 500€.*/;
      SELECT * FROM pedido WHERE YEAR(fecha) = 2017 AND total > 500;

/* 5. Devuelve un listado con el nombre y los apellidos de los comerciales que tienen una comisión entre 0.05 y 0.11.*/;
      SELECT nombre, apellido1, apellido2 FROM comercial WHERE comisión BETWEEN 0.05 AND 0.11;

/* 6. Devuelve el valor de la comisión de mayor valor que existe en la tabla comercial.*/;
      SELECT comisión FROM comercial ORDER BY comisión DESC LIMIT 1;

/* 7. Devuelve el identificador, nombre y primer apellido de aquellos clientes cuyo segundo apellido no 
      es NULL. El listado deberá estar ordenado alfabéticamente por apellidos y nombre.*/;
      SELECT id, nombre, apellido1 FROM cliente WHERE apellido2 IS NOT NULL ORDER BY apellido1, nombre;

/* 8. Devuelve un listado de los nombres de los clientes que empiezan por A y terminan por n y
      también los nombres que empiezan por P. El listado deberá estar ordenado alfabéticamente.*/;
      SELECT nombre FROM cliente WHERE nombre LIKE 'A%n' OR nombre LIKE 'P%';

/* 9. Devuelve un listado de los nombres de los clientes que no empiezan por A. El listado deberá estar ordenado alfabéticamente.*/;
      SELECT nombre FROM cliente WHERE nombre NOT LIKE 'A%' ORDER BY nombre ASC;

/* 10.Devuelve un listado con los nombres de los comerciales que terminan por “o”. Tenga en cuenta
      que se deberán eliminar los nombres repetidos.*/;
      SELECT DISTINCT nombre FROM comercial WHERE nombre LIKE '%o';

/* 11.Devuelve un listado con el identificador, nombre y los apellidos de todos los clientes que han
      realizado algún pedido. El listado debe estar ordenado alfabéticamente y se deben eliminar los elementos repetidos.*/;
      SELECT DISTINCT cliente.id, cliente.nombre, cliente.apellido1, cliente.apellido2
      FROM cliente, pedido
      WHERE cliente.id = pedido.id_cliente
      ORDER BY cliente.nombre, cliente.apellido1, cliente.apellido2;

/* 12.Devuelve un listado que muestre todos los pedidos que ha realizado cada cliente. El resultado
      debe mostrar todos los datos de los pedidos y del cliente. El listado debe mostrar los datos de los clientes ordenados alfabéticamente.*/;
      SELECT cliente.*, pedido.*
      FROM cliente, pedido
      WHERE cliente.id = pedido.id_cliente
      ORDER BY cliente.nombre, cliente.apellido1, cliente.apellido2;

/* 13.Devuelve un listado que muestre todos los pedidos en los que ha participado un comercial. El 
      resultado debe mostrar todos los datos de los pedidos y de los comerciales. El listado debe 
      mostrar los datos de los comerciales ordenados alfabéticamente.*/;
      SELECT comercial.*, pedido.* 
      FROM comercial, pedido 
      WHERE comercial.id = pedido.id_comercial 
      ORDER BY comercial.nombre, comercial.apellido1, comercial.apellido2;

/* 14.Calcula la cantidad total de todos los pedidos que aparecen en la tabla pedido.*/;
      SELECT SUM(total) AS TotalPedidos FROM pedido;

/* 15.Calcula la cantidad media de todos los pedidos que aparecen en la tabla pedido.*/;
      SELECT AVG(total) AS MediaPedidos FROM pedido;

/* 16.Calcula el número total de clientes que aparecen en la tabla cliente.*/;
      SELECT COUNT(*) AS TotalClientes FROM cliente;

/* 17.Calcula cuál es la mayor cantidad que aparece en la tabla pedido.*/;
      SELECT MAX(total) AS MaximoPedido FROM pedido;

/* 18.Calcula cuál es el valor máximo de categoría para cada una de las ciudades que aparece en la tabla cliente.*/;
      SELECT ciudad, MAX(categoría) AS MaxCategoria 
      FROM cliente 
      GROUP BY ciudad;

/* 19.Calcula cuál es el máximo valor de los pedidos realizados durante el mismo día para cada uno de */;
/* los clientes. Es decir, el mismo cliente puede haber realizado varios pedidos de diferentes */;
/* cantidades el mismo día. Se pide que se calcule cuál es el pedido de máximo valor para cada uno */;
/* de los días en los que un cliente ha realizado un pedido. Muestra el identificador del cliente, */;
/* nombre, apellidos, la fecha y el valor de la cantidad.*/;
      SELECT cliente.id, cliente.nombre, cliente.apellido1, cliente.apellido2, pedido.fecha, MAX(pedido.total) 
      FROM cliente, pedido 
      WHERE cliente.id = pedido.id_cliente 
      GROUP BY cliente.id, pedido.fecha;

/* 20.Calcula cuál es el máximo valor de los pedidos realizados durante el mismo día para cada uno de */;
/* los clientes, teniendo en cuenta que sólo queremos mostrar aquellos pedidos que superen la cantidad de 2000 €.*/;
      SELECT cliente.id, cliente.nombre, pedido.fecha, MAX(pedido.total) 
      FROM cliente, pedido 
      WHERE cliente.id = pedido.id_cliente 
      GROUP BY cliente.id, pedido.fecha 
      HAVING MAX(pedido.total) > 2000;

/* 21.Devuelve el pedido más caro que existe en la tabla pedido usando algún tipo de subconsulta.*/;
      SELECT * 
      FROM pedido 
      WHERE total = (SELECT MAX(total) FROM pedido);

/* 22.Calcula el máximo valor de los pedidos realizados para cada uno de los comerciales durante el año
      2019. Muestra el identificador del comercial, nombre, apellidos y total.*/;
      SELECT comercial.id, comercial.nombre, comercial.apellido1, comercial.apellido2, MAX(pedido.total) 
      FROM comercial, pedido 
      WHERE comercial.id = pedido.id_comercial 
      AND YEAR(pedido.fecha) = 2019 
      GROUP BY comercial.id;

/* 23.Devuelve un listado con el identificador de cliente, nombre y apellidos y el número total de
      pedidos que ha realizado cada uno de clientes. */;
      SELECT cliente.id, cliente.nombre, cliente.apellido1, cliente.apellido2, COUNT(pedido.id) 
      FROM cliente, pedido 
      WHERE cliente.id = pedido.id_cliente 
      GROUP BY cliente.id;

/* 24.Devuelve un listado con el identificador de cliente, nombre y apellidos y el número total de
      pedidos que ha realizado cada uno de clientes durante el año 2020.*/;
      SELECT cliente.id, cliente.nombre, cliente.apellido1, cliente.apellido2, COUNT(pedido.id) 
      FROM cliente, pedido 
      WHERE cliente.id = pedido.id_cliente 
      AND YEAR(pedido.fecha) = 2020 
      GROUP BY cliente.id;

/* 25.Devuelve un listado que muestre el identificador de cliente, nombre, primer apellido y el valor de 
      la máxima cantidad del pedido realizado por cada uno de los clientes. El resultado debe mostrar 
      aquellos clientes que no han realizado ningún pedido indicando que la máxima cantidad de sus 
      pedidos realizados es 0. Puede hacer uso de la función IFNULL.*/;
      SELECT cliente.id, cliente.nombre, cliente.apellido1, IFNULL(MAX(pedido.total), 0) 
      FROM cliente 
      LEFT JOIN pedido ON cliente.id = pedido.id_cliente 
      GROUP BY cliente.id;

/* 26.Devuelve cuál ha sido el pedido de máximo valor que se ha realizado cada año.*/;
      SELECT YEAR(fecha) AS Año, MAX(total) AS MaximoTotal 
      FROM pedido 
      GROUP BY Año;

/* 27.Devuelve un listado con todos los pedidos que ha realizado Adela Salas Díaz. */;
      SELECT pedido.* 
      FROM cliente, pedido 
      WHERE cliente.id = pedido.id_cliente 
      AND cliente.nombre = 'Adela' 
      AND cliente.apellido1 = 'Salas' 
      AND cliente.apellido2 = 'Díaz';

/* 28.Devuelve el número de pedidos en los que ha participado el comercial Daniel Sáez Vega. */;
      SELECT COUNT(pedido.id) 
      FROM comercial, pedido 
      WHERE comercial.id = pedido.id_comercial 
      AND comercial.nombre = 'Daniel' 
      AND comercial.apellido1 = 'Sáez' 
      AND comercial.apellido2 = 'Vega';

/* 29.Devuelve los datos del cliente que realizó el pedido más caro en el año 2019. */;
      SELECT cliente.* 
      FROM cliente, pedido 
      WHERE cliente.id = pedido.id_cliente 
      AND YEAR(pedido.fecha) = 2019 
      ORDER BY pedido.total DESC 
      LIMIT 1;

/* 30.Devuelve un listado con los datos de los clientes y los pedidos, de todos los clientes que han 
      realizado un pedido durante el año 2020 con un valor mayor o igual al valor medio de los pedidos 
      realizados durante ese mismo año*/;
      SELECT cliente.*, pedido.* 
      FROM cliente, pedido 
      WHERE cliente.id = pedido.id_cliente 
      AND YEAR(pedido.fecha) = 2020 
      AND pedido.total >= (SELECT AVG(total) FROM pedido WHERE YEAR(fecha) = 2020);