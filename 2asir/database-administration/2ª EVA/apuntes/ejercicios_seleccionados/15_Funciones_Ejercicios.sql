-- 1. Consulta los pedidos de un cliente específico
-- Crea un procedimiento llamado ObtenerPedidosCliente que reciba como parámetro el id de un cliente y devuelva todos los pedidos asociados a ese cliente.
DELIMITER //
CREATE PROCEDURE ObtenerPedidosCliente(IN p_id_cliente INT)
BEGIN
    SELECT * FROM pedido WHERE id_cliente = p_id_cliente;
END //
DELIMITER ;

-- 2. Actualiza la comisión de un comercial
-- Crea un procedimiento llamado ActualizarComision que reciba como parámetros el id de un comercial y un nuevo valor de comisión. Este procedimiento debe actualizar la comisión en la tabla comercial.
DELIMITER //
CREATE PROCEDURE ActualizarComision(IN p_id_comercial INT, IN p_nueva_comision FLOAT)
BEGIN
    UPDATE comercial SET comisión = p_nueva_comision WHERE id = p_id_comercial;
END //
DELIMITER ;

-- 3. Inserta un nuevo pedido
-- Crea un procedimiento llamado AgregarPedido que permita insertar un nuevo pedido en la tabla pedido. Debe recibir como parámetros el total del pedido, la fecha, el id_cliente y el id_comercial.
DELIMITER //
CREATE PROCEDURE AgregarPedido(
    IN p_total DOUBLE,
    IN p_fecha DATE,
    IN p_id_cliente INT,
    IN p_id_comercial INT
)
BEGIN
    INSERT INTO pedido (total, fecha, id_cliente, id_comercial)
    VALUES (p_total, p_fecha, p_id_cliente, p_id_comercial);
END //
DELIMITER ;
