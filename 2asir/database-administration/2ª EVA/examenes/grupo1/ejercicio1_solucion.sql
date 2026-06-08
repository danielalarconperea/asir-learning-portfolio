-- Ejercicio 1: Procedimiento de reporte de ventas por cliente (simulando empleado) y categoría
DELIMITER //

DROP PROCEDURE IF EXISTS sp_reporte_ventas_empleado_categoria //

CREATE PROCEDURE sp_reporte_ventas_empleado_categoria(IN fecha_inicio DATE, IN fecha_fin DATE)
BEGIN
    DECLARE total_periodo DECIMAL(10,2);
    
    -- Calculamos el ingreso total del periodo para el cálculo de porcentajes
    SELECT SUM(total) INTO total_periodo 
    FROM pedidos 
    WHERE DATE(fecha_pedido) BETWEEN fecha_inicio AND fecha_fin
    AND estado != 'cancelado';

    -- Si no hay ventas, evitamos división por cero asignando 1 temporalmente o manejando el caso
    IF total_periodo IS NULL OR total_periodo = 0 THEN
        SET total_periodo = 1;
    END IF;

    SELECT 
        c.nombre AS Cliente_Empleado,
        cat.nombre AS Categoria_Producto,
        SUM(dp.cantidad) AS Unidades_Vendidas,
        SUM(dp.subtotal) AS Ingreso_Generado,
        -- Comisión del 5% solo en ventas individuales superiores a 10€
        SUM(CASE WHEN dp.subtotal > 10 THEN dp.subtotal * 0.05 ELSE 0 END) AS Comision_Calculada,
        -- Porcentaje del ingreso total del periodo
        ROUND((SUM(dp.subtotal) / total_periodo) * 100, 2) AS Porcentaje_Contribucion
    FROM clientes c
    JOIN pedidos p ON c.id_cliente = p.id_cliente
    JOIN detalle_pedido dp ON p.id_pedido = dp.id_pedido
    JOIN productos pr ON dp.id_producto = pr.id_producto
    JOIN categorias cat ON pr.id_categoria = cat.id_categoria
    WHERE DATE(p.fecha_pedido) BETWEEN fecha_inicio AND fecha_fin
    AND p.estado != 'cancelado'
    GROUP BY c.id_cliente, cat.id_categoria;
END //

DELIMITER ;
