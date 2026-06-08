-- Ejercicio 2: Función para calcular el valor total del stock por categoría
DELIMITER //

DROP FUNCTION IF EXISTS fn_valor_stock_categoria //

CREATE FUNCTION fn_valor_stock_categoria(cat_id INT) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE valor_total DECIMAL(10,2);
    
    -- Calculamos la suma de precio * stock filtrando por categoría, activos y stock mínimo
    SELECT SUM(precio * stock) INTO valor_total
    FROM productos
    WHERE id_categoria = cat_id
    AND activo = TRUE        -- Solo productos activos
    AND stock >= 5;       -- Excluir productos en reposición (< 5)
    
    -- Si la categoría no existe o no hay productos, devolvemos 0.00
    IF valor_total IS NULL THEN
        RETURN 0.00;
    END IF;
    
    RETURN valor_total;
END //

DELIMITER ;
