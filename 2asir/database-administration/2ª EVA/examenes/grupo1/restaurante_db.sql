-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: restaurante_db
-- ------------------------------------------------------
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

--
-- Table structure for table `auditoria_precios`
--

DROP TABLE IF EXISTS `auditoria_precios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auditoria_precios` (
  `id_auditoria` int(11) NOT NULL AUTO_INCREMENT,
  `id_producto` int(11) DEFAULT NULL,
  `precio_anterior` decimal(10,2) DEFAULT NULL,
  `precio_nuevo` decimal(10,2) DEFAULT NULL,
  `diferencia` decimal(10,2) DEFAULT NULL,
  `porcentaje_cambio` decimal(5,2) DEFAULT NULL,
  `usuario` varchar(100) DEFAULT NULL,
  `fecha_cambio` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_auditoria`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `auditoria_precios_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auditoria_precios`
--

LOCK TABLES `auditoria_precios` WRITE;
/*!40000 ALTER TABLE `auditoria_precios` DISABLE KEYS */;
/*!40000 ALTER TABLE `auditoria_precios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorias`
--

DROP TABLE IF EXISTS `categorias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorias` (
  `id_categoria` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `descripcion` text,
  PRIMARY KEY (`id_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorias`
--

LOCK TABLES `categorias` WRITE;
/*!40000 ALTER TABLE `categorias` DISABLE KEYS */;
INSERT INTO `categorias` VALUES (1,'Bebidas','Refrescos, jugos y bebidas alcohólicas'),(2,'Entradas','Aperitivos y entradas'),(3,'Platos Fuertes','Platos principales'),(4,'Postres','Dulces y postres'),(5,'Ensaladas','Ensaladas frescas'),(6,'Sopas','Sopas y cremas'),(7,'Pizzas','Pizzas de varios tipos'),(8,'Hamburguesas','Hamburguesas y sandwiches'),(9,'Mariscos','Platos de mariscos'),(10,'Vegetariano','Platos sin carne'),(11,'Infantil','Menú para niños'),(12,'Especiales','Platos especiales del chef');
/*!40000 ALTER TABLE `categorias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `fecha_registro` date DEFAULT (curdate()),
  PRIMARY KEY (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'Juan Pérez','juan@email.com','555-0101','2024-01-15'),(2,'María García','maria@email.com','555-0102','2024-01-20'),(3,'Carlos López','carlos@email.com','555-0103','2024-02-05'),(4,'Ana Rodríguez','ana@email.com','555-0104','2024-02-10'),(5,'Pedro Martínez','pedro@email.com','555-0105','2024-02-15'),(6,'Laura Sánchez','laura@email.com','555-0106','2024-03-01'),(7,'Miguel Hernández','miguel@email.com','555-0107','2024-03-05'),(8,'Elena Gómez','elena@email.com','555-0108','2024-03-10'),(9,'David Fernández','david@email.com','555-0109','2024-03-15'),(10,'Sofía Díaz','sofia@email.com','555-0110','2024-03-20'),(11,'Javier Ruiz','javier@email.com','555-0111','2024-04-01'),(12,'Carmen Torres','carmen@email.com','555-0112','2024-04-05'),(13,'Alejandro Vázquez','alejandro@email.com','555-0113','2024-04-10');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_pedido`
--

DROP TABLE IF EXISTS `detalle_pedido`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_pedido` (
  `id_detalle` int(11) NOT NULL AUTO_INCREMENT,
  `id_pedido` int(11) DEFAULT NULL,
  `id_producto` int(11) DEFAULT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) GENERATED ALWAYS AS ((`cantidad` * `precio_unitario`)) STORED,
  PRIMARY KEY (`id_detalle`),
  KEY `id_pedido` (`id_pedido`),
  KEY `id_producto` (`id_producto`),
  CONSTRAINT `detalle_pedido_ibfk_1` FOREIGN KEY (`id_pedido`) REFERENCES `pedidos` (`id_pedido`),
  CONSTRAINT `detalle_pedido_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`)
) ENGINE=InnoDB AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_pedido`
--

LOCK TABLES `detalle_pedido` WRITE;
/*!40000 ALTER TABLE `detalle_pedido` DISABLE KEYS */;
INSERT INTO `detalle_pedido` (`id_detalle`, `id_pedido`, `id_producto`, `cantidad`, `precio_unitario`) VALUES (1,1,1,2,2.50),(2,1,6,1,8.50),(3,2,7,1,10.00),(4,2,1,2,2.50),(5,2,12,1,4.00),(6,2,13,1,3.00),(7,3,9,1,7.50),(8,3,2,2,1.50),(9,3,12,1,4.00),(10,3,13,1,3.50),(11,3,1,1,2.50),(12,4,15,1,11.00),(13,4,19,2,4.50),(14,4,12,2,4.00),(15,4,13,1,3.50),(16,5,8,1,12.00),(17,6,6,1,8.50),(18,7,10,2,9.50),(19,7,1,2,2.50),(20,8,14,1,8.00),(21,8,19,1,4.50),(22,8,12,2,4.00),(23,9,7,1,10.00),(24,9,1,2,2.50),(25,9,13,1,3.50),(26,10,18,1,15.00),(27,10,19,2,4.50),(28,10,12,1,4.00),(29,11,11,2,4.50),(30,11,3,2,3.00),(31,12,6,2,8.50),(32,12,1,2,2.50),(33,13,4,1,5.50),(34,13,2,2,1.50),(35,13,13,1,3.50);
/*!40000 ALTER TABLE `detalle_pedido` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pedidos`
--

DROP TABLE IF EXISTS `pedidos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pedidos` (
  `id_pedido` int(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` int(11) DEFAULT NULL,
  `fecha_pedido` datetime DEFAULT CURRENT_TIMESTAMP,
  `estado` enum('pendiente','preparando','entregado','cancelado') DEFAULT 'pendiente',
  `total` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id_pedido`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pedidos`
--

LOCK TABLES `pedidos` WRITE;
/*!40000 ALTER TABLE `pedidos` DISABLE KEYS */;
INSERT INTO `pedidos` VALUES (1,1,'2024-04-01 12:30:00','entregado',15.50),(2,2,'2024-04-01 13:15:00','entregado',22.00),(3,3,'2024-04-02 14:00:00','entregado',18.75),(4,4,'2024-04-02 19:30:00','entregado',32.50),(5,5,'2024-04-03 12:45:00','preparando',12.00),(6,6,'2024-04-03 13:20:00','pendiente',8.50),(7,7,'2024-04-04 14:10:00','entregado',24.00),(8,8,'2024-04-04 20:00:00','entregado',19.50),(9,9,'2024-04-05 12:15:00','cancelado',16.00),(10,10,'2024-04-05 13:45:00','entregado',27.25),(11,11,'2024-04-06 14:30:00','preparando',14.00),(12,12,'2024-04-06 19:15:00','pendiente',21.50),(13,13,'2024-04-07 12:00:00','entregado',11.00);
/*!40000 ALTER TABLE `pedidos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

DROP TABLE IF EXISTS `productos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  `precio` decimal(10,2) NOT NULL,
  `stock` int(11) DEFAULT '0',
  `id_categoria` int(11) DEFAULT NULL,
  `activo` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id_producto`),
  KEY `id_categoria` (`id_categoria`),
  CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_categoria`) REFERENCES `categorias` (`id_categoria`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` VALUES (1,'Coca Cola','Refresco de cola 500ml',2.50,100,1,1),(2,'Agua Mineral','Agua sin gas 500ml',1.50,150,1,1),(3,'Jugo de Naranja','Jugo natural 300ml',3.00,80,1,1),(4,'Nachos con Queso','Nachos con salsa de queso',5.50,50,2,1),(5,'Alitas de Pollo','Alitas picantes con salsa',7.00,40,2,1),(6,'Hamburguesa Clásica','Carne, queso, lechuga, tomate',8.50,30,8,1),(7,'Pizza Margarita','Queso mozzarella y tomate',10.00,25,7,1),(8,'Pizza Pepperoni','Pizza con pepperoni',12.00,25,7,1),(9,'Ensalada César','Lechuga, pollo, croutons',7.50,35,5,1),(10,'Lasaña','Lasaña de carne con bechamel',9.50,20,3,1),(11,'Sopa del Día','Sopa según disponibilidad',4.50,60,6,1),(12,'Tarta de Chocolate','Postre de chocolate',4.00,40,4,1),(13,'Helado de Vainilla','2 bolas de helado',3.50,50,4,1),(14,'Pasta Alfredo','Pasta con salsa alfredo',8.00,25,3,1),(15,'Camarones Fritos','Camarones empanizados',11.00,15,9,1),(16,'Ensalada Vegetariana','Ensalada sin productos animales',6.50,30,10,1),(17,'Menú Infantil','Hamburguesa pequeña con papas',6.00,20,11,1),(18,'Filete Mignon','Filete con guarniciones',15.00,10,12,1),(19,'Vino Tinto','Copa de vino tinto de la casa',4.50,70,1,1),(20,'Cerveza Artesanal','Cerveza local 500ml',5.00,90,1,1);
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-28  9:18:38
