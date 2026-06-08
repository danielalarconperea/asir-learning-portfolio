-- Creación de la base de datos (opcional, asumiendo que ya existe o se usa una)
-- CREATE DATABASE IF NOT EXISTS ventas;
-- USE ventas;

-- Tabla cliente
DROP TABLE IF EXISTS cliente;
CREATE TABLE cliente (
  id int(10) unsigned NOT NULL AUTO_INCREMENT,
  nombre varchar(100) NOT NULL,
  apellido1 varchar(100) NOT NULL,
  apellido2 varchar(100) DEFAULT NULL,
  ciudad varchar(100) DEFAULT NULL,
  categoría int(10) unsigned DEFAULT NULL,
  total_compras float DEFAULT '0',
  estado_credito varchar(20) DEFAULT 'Pendiente',
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4;

INSERT INTO cliente VALUES 
(1,'Aarón','Rivero','Gómez','Almería',100,3030.73,'Pendiente'),
(2,'Adela','Salas','Díaz','Granada',200,0,'Pendiente'),
(3,'Adolfo','Rubio','Flores','Sevilla',NULL,0,'Pendiente'),
(4,'Adrián','Suárez',NULL,'Jaén',300,0,'Pendiente'),
(5,'Marcos','Loyola','Méndez','Almería',200,0,'Aprobado'),
(6,'María','Santana','Moreno','Cádiz',100,0,'Pendiente'),
(7,'Pilar','Ruiz',NULL,'Sevilla',300,0,'Pendiente'),
(8,'Pepe','Ruiz','Santana','Huelva',200,0,'Pendiente'),
(9,'Guillermo','López','Gómez','Granada',225,0,'Pendiente'),
(10,'Daniel','Santana','Loyola','Sevilla',125,0,'Pendiente');

-- Tabla comercial
DROP TABLE IF EXISTS comercial;
CREATE TABLE comercial (
  id int(10) unsigned NOT NULL AUTO_INCREMENT,
  nombre varchar(100) NOT NULL,
  apellido1 varchar(100) NOT NULL,
  apellido2 varchar(100) DEFAULT NULL,
  comisión float DEFAULT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4;

INSERT INTO comercial VALUES 
(1,'Daniel','Sáez','Vega',0.17),
(2,'Juan','Gómez','López',0.13),
(3,'Diego','Flores','Salas',0.11),
(4,'Marta','Herrera','Gil',0.14),
(5,'Antonio','Carretero','Ortega',0.12),
(6,'Manuel','Domínguez','Hernández',0.13),
(7,'Antonio','Vega','Hernández',0.11),
(8,'Alfredo','Ruiz','Flores',0.07);

-- Tabla pedido
DROP TABLE IF EXISTS pedido;
CREATE TABLE pedido (
  id int(10) unsigned NOT NULL AUTO_INCREMENT,
  total double NOT NULL,
  fecha date DEFAULT NULL,
  id_cliente int(10) unsigned NOT NULL,
  id_comercial int(10) unsigned NOT NULL,
  PRIMARY KEY (id),
  KEY id_cliente (id_cliente),
  KEY id_comercial (id_comercial),
  CONSTRAINT pedido_ibfk_1 FOREIGN KEY (id_cliente) REFERENCES cliente (id),
  CONSTRAINT pedido_ibfk_2 FOREIGN KEY (id_comercial) REFERENCES comercial (id)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;

INSERT INTO pedido VALUES 
(1,5000,'2017-10-05',5,2),
(2,270.65,'2016-09-10',1,5),
(3,65.26,'2017-10-05',2,1),
(4,110.5,'2016-08-17',8,3),
(5,948.5,'2017-09-10',5,2),
(6,2400.6,'2016-07-27',7,1),
(7,5760,'2015-09-10',2,1),
(8,1983.43,'2017-10-10',4,6),
(9,2480.4,'2016-10-10',8,3),
(10,250.45,'2015-06-27',8,2),
(11,75.29,'2016-08-17',3,7),
(12,3045.6,'2017-04-25',2,1),
(13,545.75,'2019-01-25',6,1),
(14,145.82,'2017-02-02',6,1),
(15,370.85,'2019-03-11',1,5),
(16,2389.23,'2019-03-11',1,5),
(17,500,'2024-01-09',2,1);

CREATE TABLE auditoria (
  id INT(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  tabla_afectada VARCHAR(50) NOT NULL,
  id_registro_afectado INT(10) UNSIGNED,
  accion VARCHAR(10) NOT NULL,
  fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  usuario VARCHAR(100),
  detalles TEXT,
  PRIMARY KEY (id)
);


-- Triggers
-- DELIMITER ;;

-- CREATE TRIGGER actualizarComision AFTER INSERT ON pedido FOR EACH ROW 
-- BEGIN
--     UPDATE comercial
--     SET comisión = comisión + 0.02
--     WHERE id = NEW.id_comercial;
-- END;;

-- CREATE TRIGGER actualizarCreditoDespuesPedido AFTER UPDATE ON pedido FOR EACH ROW 
-- BEGIN
--     DECLARE nuevo_estado_credito VARCHAR(20);
--     SET nuevo_estado_credito = (
--         SELECT IF(SUM(p.total) > 5000, 'Aprobado', 'Pendiente')
--         FROM pedido p
--         WHERE p.id_cliente = NEW.id_cliente
--     );
--     UPDATE cliente c
--     SET estado_credito = nuevo_estado_credito
--     WHERE c.id = NEW.id_cliente;
-- END;;

-- CREATE TRIGGER actualizarTotalComprasCliente AFTER DELETE ON pedido FOR EACH ROW 
-- BEGIN
--     UPDATE cliente
--     SET total_compras = (
--         SELECT SUM(total)
--         FROM pedido
--         WHERE pedido.id_cliente = cliente.id
--     )
--     WHERE cliente.id = OLD.id_cliente;
-- END;;

-- DELIMITER ;
