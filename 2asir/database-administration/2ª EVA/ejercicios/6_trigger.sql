--Este trigger registra en contabilidad comercial
--la diferencia entre el nuevo total del pedido
--y el total anterior cuando se actualiza un pedido.

DELIMITER //

CREATE TRIGGER pedido_after_update
AFTER UPDATE ON pedido
FOR EACH ROW
BEGIN
  DECLARE total_pedido_anterior FLOAT;
  SELECT total INTO total_pedido_anterior
  FROM pedido
  WHERE id = OLD.id;
  IF NEW.total != total_pedido_anterior THEN  
    INSERT INTO contabilidad_comercial (id_comercial, tipo_accion, total_pedido)  
    VALUES (NEW.id_comercial, 'UPDATE', NEW.total - total_pedido_anterior);  
  END IF;
END //

DELIMITER ;

-- ejemplo de update
UPDATE pedido SET total = 200 WHERE id = 18;

SELECT * FROM contabilidad_comercial;
