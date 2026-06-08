CREATE TABLE contabilidad_comercial (
id INT(10) NOT NULL AUTO_INCREMENT,
id_comercial INT(10) UNSIGNED,
tipo_accion VARCHAR(10) NOT NULL,
fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
total_pedido FLOAT,
PRIMARY KEY (id),
FOREIGN KEY (id_comercial) REFERENCES comercial (id)
);

--Este trigger registra en contabilidad comercial
--el total del pedido cuando se inserta un nuevo pedido


DELIMITER //

CREATE TRIGGER pedido_after_insert
AFTER INSERT ON pedido
FOR EACH ROW
BEGIN
INSERT INTO contabilidad_comercial (id_comercial, tipo_accion, total_pedido)
VALUES (NEW.id_comercial, 'INSERT', NEW.total);
END //

DELIMITER ;

-- ejemplo de insert
INSERT INTO pedido VALUES (18,100,'2025-01-19',4,2);

SELECT * FROM contabilidad_comercial;