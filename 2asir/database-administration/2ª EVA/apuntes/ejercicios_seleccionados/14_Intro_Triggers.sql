-- Este trigger asegurará que la comisión del comercial
-- se ajuste automáticamente cada vez que se registre un nuevo pedido en la base
-- de datos

Drop trigger actualizarComision;
DELIMITER //
CREATE TRIGGER actualizarComision
AFTER INSERT
ON pedido FOR EACH ROW
BEGIN
-- Actualizar la comisión del comercial
UPDATE comercial
SET comisión = comisión + 0.02
WHERE id = NEW.id_comercial;
END //
DELIMITER ;

-- Insertar un nuevo pedido para probarlo
INSERT INTO pedido (total, id_cliente, id_comercial, fecha)
VALUES (1000, 7, 8, NOW());

-- Mostrar triggers
show triggers;
SELECT TRIGGER_NAME FROM information_schema.triggers
WHERE TRIGGER_SCHEMA = DATABASE();