/*
================================================================================
   EJERCICIO: TRIGGERS AVANZADOS (Sustituye archivo corrupto)
================================================================================
   OBJETIVO: Implementar lógica de negocio compleja mediante disparadores.
   ESCENARIO: Gestión de Stock y Pedidos.
*/

CREATE DATABASE IF NOT EXISTS almacen_avanzado;
USE almacen_avanzado;

-- 1. ESTRUCTURA
-- -----------------------------------------------------------------------------
CREATE TABLE productos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    stock INT,
    stock_minimo INT DEFAULT 10,
    precio DECIMAL(10,2)
);

CREATE TABLE pedidos_proveedor (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    cantidad INT,
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP,
    estado ENUM('Pendiente', 'Recibido') DEFAULT 'Pendiente',
    FOREIGN KEY (producto_id) REFERENCES productos(id)
);

CREATE TABLE historial_precios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    producto_id INT,
    precio_anterior DECIMAL(10,2),
    precio_nuevo DECIMAL(10,2),
    fecha_cambio DATETIME DEFAULT CURRENT_TIMESTAMP,
    usuario_cambio VARCHAR(50)
);

INSERT INTO productos (nombre, stock, stock_minimo, precio) VALUES
('Monitor 24"', 15, 5, 120.00),
('Teclado Mecánico', 8, 10, 45.50), -- Stock bajo
('Ratón Gaming', 50, 5, 25.00);


-- 2. EJERCICIOS A REALIZAR
-- -----------------------------------------------------------------------------

/*
   EJERCICIO 1: Reabastecimiento Automático
   Crea un trigger 'tg_reponer_stock' (AFTER UPDATE en productos).
   Condición: Si el stock baja del 'stock_minimo' Y no hay ya un pedido 'Pendiente' para ese producto.
   Acción: Insertar un pedido automático en 'pedidos_proveedor' de 50 unidades.
*/

DELIMITER //

CREATE TRIGGER tg_reponer_stock
AFTER UPDATE ON productos
FOR EACH ROW
BEGIN
    DECLARE v_pedido_pendiente INT;
    
    -- Verificar si ya hay pedido pendiente
    SELECT COUNT(*) INTO v_pedido_pendiente 
    FROM pedidos_proveedor 
    WHERE producto_id = NEW.id AND estado = 'Pendiente';
    
    -- Si el stock actual es menor al mínimo Y no hay pedidos en curso
    IF NEW.stock < NEW.stock_minimo AND v_pedido_pendiente = 0 THEN
        INSERT INTO pedidos_proveedor (producto_id, cantidad, estado)
        VALUES (NEW.id, 50, 'Pendiente');
    END IF;
END //

DELIMITER ;


/*
   EJERCICIO 2: Auditoría y Control de Precios
   Crea un trigger 'tg_control_precios' (BEFORE UPDATE en productos).
   Logica:
   1. Si el precio cambia, registrar el cambio en 'historial_precios'.
   2. IMPEDIR (Signal SQLState) que el precio suba más de un 20% de golpe.
*/

DELIMITER //

CREATE TRIGGER tg_control_precios
BEFORE UPDATE ON productos
FOR EACH ROW
BEGIN
    -- Solo si cambia el precio
    IF NEW.precio <> OLD.precio THEN
        
        -- Control de subida excesiva (> 20%)
        IF NEW.precio > OLD.precio * 1.20 THEN
            SIGNAL SQLSTATE '45000' 
            SET MESSAGE_TEXT = 'Error: No se permite subir el precio más de un 20%';
        END IF;

        -- Auditoría
        INSERT INTO historial_precios (producto_id, precio_anterior, precio_nuevo, usuario_cambio)
        VALUES (OLD.id, OLD.precio, NEW.precio, CURRENT_USER());
    END IF;
END //

DELIMITER ;


/*
   EJERCICIO 3: Actualización de Stock al Recibir Pedido
   Crea un trigger 'tg_recepcion_pedido' (AFTER UPDATE en pedidos_proveedor).
   Condición: Cuando el estado cambie de 'Pendiente' a 'Recibido'.
   Acción: Sumar la cantidad del pedido al stock del producto correspondiente.
*/

DELIMITER //

CREATE TRIGGER tg_recepcion_pedido
AFTER UPDATE ON pedidos_proveedor
FOR EACH ROW
BEGIN
    -- Si ha cambiado a recibido
    IF OLD.estado = 'Pendiente' AND NEW.estado = 'Recibido' THEN
        UPDATE productos 
        SET stock = stock + NEW.cantidad 
        WHERE id = NEW.producto_id;
    END IF;
END //

DELIMITER ;


-- 3. PRUEBAS
-- -----------------------------------------------------------------------------

-- Prueba Ejercicio 1 (Bajamos stock para disparar pedido)
UPDATE productos SET stock = 4 WHERE id = 1; 
-- SELECT * FROM pedidos_proveedor; -- Debería haber un pedido nuevo

-- Prueba Ejercicio 2 (Subida ilegal)
-- UPDATE productos SET precio = 200 WHERE id = 1; -- Debería fallar (120 -> 200 es > 20%)

-- Prueba Ejercicio 3 (Recibir pedido)
-- UPDATE pedidos_proveedor SET estado = 'Recibido' WHERE id = 1;
-- SELECT * FROM productos; -- El stock debería haber aumentado
