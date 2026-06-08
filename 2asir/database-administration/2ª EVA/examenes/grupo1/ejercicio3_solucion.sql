-- Ejercicio 3: Trigger para restaurar stock cuando un pedido se cancela
DELIMITER //

DROP TRIGGER IF EXISTS tr_restaurar_stock_cancelacion //

CREATE TRIGGER tr_restaurar_stock_cancelacion
AFTER UPDATE ON pedidos
FOR EACH ROW
BEGIN
    -- Se activa solo cuando el estado cambia a 'cancelado'
    IF NEW.estado = 'cancelado' AND OLD.estado != 'cancelado' THEN
        -- Restauramos el stock sumando la cantidad de vuelta al producto
        -- Usamos un JOIN para actualizar todos los productos del pedido a la vez
        UPDATE productos p
        INNER JOIN detalle_pedido dp ON p.id_producto = dp.id_producto
        SET p.stock = p.stock + dp.cantidad
        WHERE dp.id_pedido = NEW.id_pedido;
    END IF;
END //

DELIMITER ;
