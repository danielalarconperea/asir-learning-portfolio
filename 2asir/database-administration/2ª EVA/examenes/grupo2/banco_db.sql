-- MySQL dump 10.13  Distrib 8.0.17, for Win64 (x86_64)
--
-- Host: localhost    Database: banco_db
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
-- Table structure for table `auditoria_transacciones`
--

DROP TABLE IF EXISTS `auditoria_transacciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auditoria_transacciones` (
  `id_auditoria` int(11) NOT NULL AUTO_INCREMENT,
  `id_transaccion` int(11) DEFAULT NULL,
  `id_cuenta` int(11) DEFAULT NULL,
  `monto_anterior` decimal(15,2) DEFAULT NULL,
  `monto_nuevo` decimal(15,2) DEFAULT NULL,
  `tipo_operacion` varchar(50) DEFAULT NULL,
  `usuario` varchar(100) DEFAULT NULL,
  `fecha_auditoria` datetime DEFAULT CURRENT_TIMESTAMP,
  `descripcion` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id_auditoria`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auditoria_transacciones`
--

LOCK TABLES `auditoria_transacciones` WRITE;
/*!40000 ALTER TABLE `auditoria_transacciones` DISABLE KEYS */;
INSERT INTO `auditoria_transacciones` VALUES (1,1,1,NULL,NULL,'Depósito','SISTEMA','2026-01-28 09:22:24','Transacción automática');
/*!40000 ALTER TABLE `auditoria_transacciones` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clientes`
--

DROP TABLE IF EXISTS `clientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL AUTO_INCREMENT,
  `dni` varchar(20) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(150) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `fecha_registro` date DEFAULT (curdate()),
  `categoria` enum('Normal','Premium','VIP') DEFAULT 'Normal',
  PRIMARY KEY (`id_cliente`),
  UNIQUE KEY `dni` (`dni`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clientes`
--

LOCK TABLES `clientes` WRITE;
/*!40000 ALTER TABLE `clientes` DISABLE KEYS */;
INSERT INTO `clientes` VALUES (1,'12345678A','Carlos','García','carlos@email.com','600111222','2026-01-28','Premium'),(2,'23456789B','Ana','Martínez','ana@email.com','600222333','2026-01-28','Normal'),(3,'34567890C','Luis','Rodríguez','luis@email.com','600333444','2026-01-28','VIP'),(4,'45678901D','María','López','maria@email.com','600444555','2026-01-28','Premium'),(5,'56789012E','Pedro','Sánchez','pedro@email.com','600555666','2026-01-28','Normal'),(6,'67890123F','Laura','Fernández','laura@email.com','600666777','2026-01-28','Normal'),(7,'78901234G','Javier','Gómez','javier@email.com','600777888','2026-01-28','Premium'),(8,'89012345H','Elena','Díaz','elena@email.com','600888999','2026-01-28','VIP'),(9,'90123456I','David','Ruiz','david@email.com','600999000','2026-01-28','Normal'),(10,'01234567J','Sofía','Hernández','sofia@email.com','600000111','2026-01-28','Premium'),(11,'11223344K','Miguel','Torres','miguel@email.com','611222333','2026-01-28','Normal'),(12,'22334455L','Carmen','Vázquez','carmen@email.com','622333444','2026-01-28','VIP');
/*!40000 ALTER TABLE `clientes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cuentas`
--

DROP TABLE IF EXISTS `cuentas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cuentas` (
  `id_cuenta` int(11) NOT NULL AUTO_INCREMENT,
  `numero_cuenta` varchar(20) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `tipo_cuenta` enum('Ahorro','Corriente','Nómina') DEFAULT 'Ahorro',
  `saldo` decimal(15,2) DEFAULT '0.00',
  `fecha_apertura` date DEFAULT (curdate()),
  `activa` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id_cuenta`),
  UNIQUE KEY `numero_cuenta` (`numero_cuenta`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `cuentas_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cuentas`
--

LOCK TABLES `cuentas` WRITE;
/*!40000 ALTER TABLE `cuentas` DISABLE KEYS */;
INSERT INTO `cuentas` VALUES (1,'ES001234567800000001',1,'Corriente',15000.00,'2023-01-15',1),(2,'ES001234567800000002',1,'Ahorro',5000.00,'2023-01-15',1),(3,'ES001234567800000003',2,'Nómina',3000.00,'2023-02-20',1),(4,'ES001234567800000004',3,'Corriente',25000.00,'2023-03-10',1),(5,'ES001234567800000005',4,'Ahorro',12000.00,'2023-04-05',1),(6,'ES001234567800000006',5,'Corriente',8000.00,'2023-05-12',1),(7,'ES001234567800000007',6,'Nómina',4500.00,'2023-06-18',1),(8,'ES001234567800000008',7,'Ahorro',18000.00,'2023-07-22',1),(9,'ES001234567800000009',8,'Corriente',35000.00,'2023-08-30',1),(10,'ES001234567800000010',9,'Ahorro',6000.00,'2023-09-14',1),(11,'ES001234567800000011',10,'Nómina',9000.00,'2023-10-25',1),(12,'ES001234567800000012',11,'Corriente',7000.00,'2023-11-08',1);
/*!40000 ALTER TABLE `cuentas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prestamos`
--

DROP TABLE IF EXISTS `prestamos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `prestamos` (
  `id_prestamo` int(11) NOT NULL AUTO_INCREMENT,
  `id_cliente` int(11) NOT NULL,
  `monto_solicitado` decimal(15,2) NOT NULL,
  `monto_aprobado` decimal(15,2) DEFAULT NULL,
  `tasa_interes` decimal(5,2) NOT NULL,
  `plazo_meses` int(11) NOT NULL,
  `fecha_solicitud` date DEFAULT (curdate()),
  `estado` enum('Solicitado','Aprobado','Rechazado','Pagado') DEFAULT 'Solicitado',
  PRIMARY KEY (`id_prestamo`),
  KEY `id_cliente` (`id_cliente`),
  CONSTRAINT `prestamos_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prestamos`
--

LOCK TABLES `prestamos` WRITE;
/*!40000 ALTER TABLE `prestamos` DISABLE KEYS */;
INSERT INTO `prestamos` VALUES (1,1,10000.00,10000.00,5.50,36,'2026-01-28','Aprobado'),(2,2,5000.00,4000.00,6.00,24,'2026-01-28','Aprobado'),(3,3,20000.00,20000.00,4.50,48,'2026-01-28','Aprobado'),(4,4,15000.00,12000.00,5.00,36,'2026-01-28','Aprobado'),(5,5,8000.00,8000.00,6.50,24,'2026-01-28','Aprobado'),(6,6,3000.00,NULL,7.00,12,'2026-01-28','Rechazado'),(7,7,25000.00,20000.00,4.00,60,'2026-01-28','Aprobado'),(8,8,30000.00,30000.00,3.50,48,'2026-01-28','Aprobado'),(9,9,4000.00,4000.00,6.00,18,'2026-01-28','Aprobado'),(10,10,12000.00,10000.00,5.50,36,'2026-01-28','Aprobado'),(11,11,6000.00,6000.00,6.00,24,'2026-01-28','Aprobado');
/*!40000 ALTER TABLE `prestamos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transacciones`
--

DROP TABLE IF EXISTS `transacciones`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transacciones` (
  `id_transaccion` int(11) NOT NULL AUTO_INCREMENT,
  `id_cuenta` int(11) NOT NULL,
  `tipo` enum('Depósito','Retiro','Transferencia') NOT NULL,
  `monto` decimal(15,2) NOT NULL,
  `fecha_hora` datetime DEFAULT CURRENT_TIMESTAMP,
  `concepto` varchar(200) DEFAULT NULL,
  `estado` enum('Pendiente','Completada','Rechazada') DEFAULT 'Completada',
  PRIMARY KEY (`id_transaccion`),
  KEY `id_cuenta` (`id_cuenta`),
  CONSTRAINT `transacciones_ibfk_1` FOREIGN KEY (`id_cuenta`) REFERENCES `cuentas` (`id_cuenta`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transacciones`
--

LOCK TABLES `transacciones` WRITE;
/*!40000 ALTER TABLE `transacciones` DISABLE KEYS */;
INSERT INTO `transacciones` VALUES (1,1,'Depósito',2000.00,'2024-01-15 10:30:00','Ingreso nómina','Completada'),(2,1,'Retiro',500.00,'2024-01-16 14:20:00','Cajero automático','Completada'),(3,2,'Depósito',1000.00,'2024-01-17 09:15:00','Ahorro mensual','Completada'),(4,3,'Transferencia',300.00,'2024-01-18 11:45:00','Pago factura','Completada'),(5,4,'Depósito',5000.00,'2024-01-19 16:30:00','Ingreso extraordinario','Completada'),(6,5,'Retiro',800.00,'2024-01-20 13:10:00','Gastos personales','Completada'),(7,6,'Transferencia',1200.00,'2024-01-21 10:00:00','Envío familiar','Completada'),(8,7,'Depósito',700.00,'2024-01-22 15:45:00','Reintegro','Completada'),(9,8,'Retiro',1500.00,'2024-01-23 12:30:00','Compra electrodoméstico','Completada'),(10,9,'Depósito',10000.00,'2024-01-24 09:00:00','Ingreso inversión','Completada'),(11,10,'Transferencia',400.00,'2024-01-25 14:15:00','Pago servicio','Completada'),(12,11,'Retiro',600.00,'2024-01-26 11:20:00','Cajero automático','Completada');
/*!40000 ALTER TABLE `transacciones` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-01-28  9:22:50

SELECT * FROM cuentas;
SELECT * FROM clientes;
select * from transacciones;
select * from prestamos;
select * from auditoria_transacciones;

DROP TRIGGER IF EXISTS tg_actualizar_saldo_transaccion;

DELIMITER //
CREATE TRIGGER tg_actualizar_saldo_transaccion 
AFTER INSERT ON transacciones
FOR EACH ROW
BEGIN
  DECLARE saldo_actual DECIMAL(15,2);
  select saldo into saldo_actual from cuentas where id_cuenta = NEW.id_cuenta;
  IF NEW.tipo = 'Depósito' THEN
    UPDATE cuentas
    SET saldo = saldo + NEW.monto
    WHERE id_cuenta = NEW.id_cuenta;
  ELSEIF NEW.tipo = 'Retiro' THEN
    IF saldo_actual > NEW.monto THEN
      UPDATE cuentas
      SET saldo = saldo - NEW.monto
      WHERE id_cuenta = NEW.id_cuenta;
    END IF;
  END IF;
END //
DELIMITER ;

INSERT INTO transacciones(id_cuenta, tipo, monto, fecha_hora, concepto, estado)
VALUES (1, 'Depósito', 1000, '2024-01-15 10:30:00', 'Ingreso nómina', 'Completada');
      
INSERT INTO transacciones(id_cuenta, tipo, monto, fecha_hora, concepto, estado)
VALUES (2, 'Retiro', 100000, '2024-01-15 10:30:00', 'Ingreso nómina', 'Completada');
      
INSERT INTO transacciones(id_cuenta, tipo, monto, fecha_hora, concepto, estado)
VALUES (2, 'Retiro', 1000, '2024-01-15 10:30:00', 'Ingreso nómina', 'Completada');



DROP IF EXISTS tg_detectar_transaccion_sospechosas;

DELIMITER //
CREATE TRIGGER tg_detectar_transaccion_sospechosas
BEFORE INSERT ON transacciones
FOR EACH ROW
BEGIN
  declare promedio_historico_superado INT;
  DECLARE total_cuenta INT;
  select saldo into total_cuenta 
  from cuentas
  where id_cuenta = NEW.id_cuenta;
  SELECT AVG(monto)*3 into promedio_historico FROM transacciones
  IF NEW.monto > promedio_historico_superado OR NEW.monto > total_cuenta THEN
    INSERT auditoria_transacciones(id_transaccion, id_cuenta, monto_anterior, monto_nuevo, tipo_operacion, usuario, fecha_auditoria, descripcion)
    VALUES (NEW.id_transaccion, NEW.id_cuenta, NULL, NEW.monto, NEW.tipo, 'SISTEMA', NOW(), 'ALERTA_SOSPECHOSA');
  END IF;
END //
DELIMITER ;

INSERT INTO transacciones(id_cuenta, tipo, monto, fecha_hora, concepto, estado)
VALUES (2, 'Retiro', 100000, '2024-01-15 10:30:00', 'Ingreso nómina', 'Completada');

SELECT * FROM auditoria_transacciones;

SELECT * FROM transacciones;

DELETE FROM transacciones WHERE id_cuenta = 2;



select saldo 
  from cuentas
  where id_cuenta = 3;
      

DROP procedure if exists sp_reporte_ventas_empleado_categoria;

DELIMITER //

CREATE PROCEDURE sp_reporte_ventas_empleado_categoria(IN año_especifico INT)
BEGIN
  select c.categoria, c.nombre c.apellido AS nombre_completo , sum(cu.saldo), count(t.id_cuenta), avg(t.monto), avg(cu.saldo)
  from clientes c
  inner join cuentas cu on c.id_cliente = cu.id_cliente
  inner join transacciones t on cu.id_cuenta = t.id_cuenta
  where year(t.fecha_hora) = year(año_especifico)
  group by cu.id_cliente;
END //

DELIMITER ;

call sp_reporte_ventas_empleado_categoria(2024);

Select year(fecha_hora) from transacciones;

drop function if exists fn_calcular_capacidad_endeudamiento;
DELIMITER //
-- (saldo_total*0.3) + (numero_cuentas*1000) + (transacciones_mes*50)
CREATE FUNCTION fn_calcular_capacidad_endeudamiento(id_cli INT)
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
  DECLARE saldo_total DECIMAL(10,2);
  DECLARE numero_cuentas INT;
  DECLARE transacciones_mes INT;

  IF id_cli IS NULL THEN
    RETURN 0.00;
  END IF;
  IF NOT EXISTS (SELECT * FROM cuentas where id_cliente = id_cli) THEN
    RETURN 0.00;
  END IF;
  
  SELECT SUM(saldo) INTO saldo_total
  FROM cuentas
  WHERE id_cliente = id_cli;
  
  SELECT COUNT(*) INTO numero_cuentas
  FROM cuentas
  WHERE id_cliente = id_cli;
  
  SELECT COUNT(*) INTO transacciones_mes
  FROM transacciones
  WHERE id_cuenta IN (SELECT id_cuenta FROM cuentas WHERE id_cliente = id_cli)
  AND MONTH(fecha_hora) = MONTH(CURRENT_DATE());
  
  RETURN (saldo_total*0.3) + (numero_cuentas*1000) + (transacciones_mes*50);
END //
DELIMITER ;
Select DISTINCT nombre, fn_calcular_capacidad_endeudamiento(1) AS capacidad from clientes;




  -- SELECT COUNT(*) 
  -- FROM transacciones
  -- WHERE id_cuenta IN (SELECT id_cuenta FROM cuentas WHERE id_cliente = 1)
  -- AND MONTH(fecha_hora) = MONTH(CURRENT_DATE());


  -- SELECT COUNT(*) FROM cuentas
  -- WHERE id_cliente = 1;

  -- SELECT SUM(saldo) 
  -- FROM cuentas
  -- WHERE id_cliente = 1;


DELIMITER //

DROP FUNCTION IF EXISTS fn_valor_stock_categoria //

CREATE FUNCTION fn_valor_stock_categoria(cat_id INT) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE valor_total DECIMAL(10,2);
    
    -- Calculamos la suma de precio * stock filtrando por categoría, activos y stock mínimo
    SELECT SUM(precio * stock) INTO valor_total
    FROM productos
    WHERE id_categoria = cat_id
    AND activo = TRUE        -- Solo productos activos
    AND stock >= 5;       -- Excluir productos en reposición (< 5)
    
    -- Si la categoría no existe o no hay productos, devolvemos 0.00
    IF valor_total IS NULL THEN
        RETURN 0.00;
    END IF;
    
    RETURN valor_total;
END //

DELIMITER ;
