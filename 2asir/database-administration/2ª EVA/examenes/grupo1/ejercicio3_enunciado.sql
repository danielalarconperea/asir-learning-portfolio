/*
PROBLEMA 3: Trigger para integridad de inventario (Stock de vuelta)

Para mantener la integridad del inventario, necesitamos un trigger que actualice 
automáticamente el stock cuando se cancele un pedido. Actualmente, el stock solo se 
actualiza al crear el detalle del pedido, pero si un pedido se cancela, el stock debe 
volver a su estado original.

Este trigger asegurará que el inventario refleje siempre la situación real y evitará 
vender productos no disponibles. Se activará cuando el estado de un pedido cambie a 'cancelado'.

Pasos a seguir:
1. Crear un trigger que se active cuando el estado de un pedido cambie a 'cancelado'.
2. Recorrer todos los ítems del pedido cancelado en la tabla detalle_pedido.
3. Restaurar el stock sumando la cantidad vendida de vuelta al producto en la tabla productos.
*/

DELIMITER //

CREATE TRIGGER tr_restaurar_stock_cancelacion
AFTER UPDATE ON pedidos
FOR EACH ROW
BEGIN
    IF NEW.estado = 'cancelado' AND OLD.estado != 'cancelado' THEN
        UPDATE productos
        SET stock = stock + (SELECT SUM(cantidad) FROM detalle_pedido WHERE id_pedido = NEW.id_pedido)
        WHERE id_producto IN (SELECT id_producto FROM detalle_pedido WHERE id_pedido = NEW.id_pedido);
    END IF;
END //

DELIMITER ;
