-- Crea un trigger llamado actualizarTotalComprasCliente en la base de datos "ventas".
-- Este trigger debe ejecutarse automáticamente después de eliminar un registro en la tabla pedido.
-- Su función es recalcular el total de compras realizado por el cliente asociado al pedido recién eliminado.
-- La actualización debe consistir en sumar nuevamente los totales de todos los pedidos del cliente
-- y actualizar el campo total_compras en la tabla cliente. 

DROP TRIGGER IF EXISTS actualizarTotalComprasCliente;
DELIMITER //
CREATE TRIGGER actualizarTotalComprasCliente
AFTER DELETE ON pedido FOR EACH ROW
BEGIN
DECLARE total_nuevo FLOAT;
SET total_nuevo = (SELECT SUM(total) FROM pedido WHERE id_cliente = OLD.id_cliente);
UPDATE cliente 
SET total_compras = total_nuevo
WHERE id = OLD.id_cliente;
END //
DELIMITER ;

-- Borrar un pedido para probar el trigger
DELETE FROM pedido WHERE id = 19;

-- Mostrar triggers
SELECT TRIGGER_NAME FROM information_schema.triggers
WHERE TRIGGER_SCHEMA = DATABASE();





--Imagina que tenemos una tienda y queremos saber si un cliente puede pedir a crédito. Cada vez que un cliente hace un pedido, revisamos cuánto ha gastado en total en nuestra tienda.
-- Si ha gastado más de 5000 euros, decimos que su crédito está "aprobado" y puede seguir comprando a crédito. Si no ha gastado tanto, su crédito sigue estando "pendiente". Es decir, el ejercicio consiste en actualizar automáticamente el estado de crédito de un cliente cada vez que realiza un nuevo pedido, basándonos en el total de sus compras.

DROP TRIGGER IF EXISTS actualizarCreditoDespuesPedido;
DELIMITER //
CREATE TRIGGER actualizarCreditoDespuesPedido
AFTER INSERT ON pedido FOR EACH ROW
BEGIN
    DECLARE total INT;
    DECLARE nuevo_estado VARCHAR(20);

    SET total = (SELECT SUM(p.total) FROM pedido p WHERE p.id_cliente = NEW.id_cliente);  

    IF total > 5000 THEN  
        SET nuevo_estado = 'Aprobado';  
    ELSE  
        SET nuevo_estado = 'Pendiente';  
    END IF;  

    UPDATE cliente  
    SET estado_credito = nuevo_estado  
    WHERE id = NEW.id_cliente;  
END //
DELIMITER ;

-- Insertar un pedido para probar el trigger
INSERT INTO pedido (total, id_cliente, id_comercial, fecha)
VALUES (5001, 4, 2, NOW());

-- Mostrar triggers
SELECT TRIGGER_NAME FROM information_schema.triggers
WHERE TRIGGER_SCHEMA = DATABASE();



-- Hacer un trigger en la BBDD de datos de ventas. Cada vez que se borre un pedido
-- queremos que se le reste comisión al comercial.
-- Si el pedido era de menos de 1000 euros que se le reste 0,01 y si era mas 0,02.


DROP TRIGGER IF EXISTS restarComisionDespuesBorrarPedido;
DELIMITER //
CREATE TRIGGER restarComisionDespuesBorrarPedido
AFTER DELETE ON pedido FOR EACH ROW
BEGIN
    IF OLD.total < 1000 THEN
        UPDATE comercial 
        SET comisión = comisión - 0.01 
        WHERE id = OLD.id_comercial;
    ELSE
        UPDATE comercial 
        SET comisión = comisión - 0.02 
        WHERE id = OLD.id_comercial;
    END IF;
END //
DELIMITER ;

-- Insertar un pedido para probar el trigger
DELETE FROM pedido WHERE id = 23;

-- Mostrar triggers
SELECT TRIGGER_NAME FROM information_schema.triggers
WHERE TRIGGER_SCHEMA = DATABASE();



-- Hacer un trigger que almacene en auditoria un registro cuando insertemos una fila en la tabla de clientes.
DROP TRIGGER IF EXISTS cliente_after_insert;
DELIMITER //
CREATE TRIGGER cliente_after_insert
AFTER INSERT ON cliente
FOR EACH ROW
BEGIN
    INSERT INTO auditoria (tabla_afectada, id_registro_afectado, accion, usuario, detalles)
    VALUES ('cliente', NEW.id, 'Insertar datos', USER(), 'Nuevo cliente insertado');
END //
DELIMITER ;

-- Insertar un cliente para probar el trigger
INSERT INTO cliente (nombre, apellido1, apellido2, ciudad, categoría, total_compras, estado_credito)
VALUES ('Juan', 'Gómez', 'López', 'Sevilla', 100, 0, 'Pendiente');

-- Mostrar triggers
SELECT TRIGGER_NAME FROM information_schema.triggers
WHERE TRIGGER_SCHEMA = DATABASE();



-- Hacer un trigger que almacene en auditoria un registro cuando se ACTUALIZA un comercial
DROP TRIGGER IF EXISTS comercial_after_update;
DELIMITER //
CREATE TRIGGER comercial_after_update
AFTER UPDATE ON comercial 
FOR EACH ROW
BEGIN
    INSERT INTO auditoria (tabla_afectada, id_registro_afectado, accion, usuario, detalles)
    VALUES ('comercial', NEW.id, 'actualizar datos', USER(), 'Comercial actualizado')
END //
DELIMITER ;

-- ¿como hariamos un trigger para un borrado de un comercial en la tabla auditoria?
DROP TRIGGER IF EXISTS comercial_after_delete;
DELIMITER //
CREATE TRIGGER comercial_after_delete
BEFORE DELETE ON comercial 
FOR EACH ROW
BEGIN
    DECLARE detalles VARCHAR(255);
    SET detalles = CONCAT('Comercial eliminado - Nombre: ', OLD.nombre, 'Apellido: ', OLD.apellido1, ' ', OLD.apellido2);
    INSERT INTO auditoria (tabla_afectada, id_registro_afectado, accion, usuario, detalles)
    VALUES ('comercial', OLD.id, 'borrar datos', USER(), detalles);
END //
DELIMITER ;