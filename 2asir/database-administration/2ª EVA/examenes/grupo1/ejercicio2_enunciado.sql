DELIMITER //

CREATE FUNCTION fn_valor_stock_categoria(cat_id INT) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN

    declare valor_total DECIMAL(10,2);
    
    SELECT SUM(precio * stock) INTO valor_total
    FROM productos
    WHERE id_categoria = cat_id
    AND activo = 1        -- Solo productos activos
    AND stock >= 5;       -- Excluir productos en reposición (< 5)
    
    -- Si la categoría no existe o no hay productos, devolvemos 0.00
    IF valor_total IS NULL THEN
        RETURN 0.00;
    END IF;
    
    RETURN valor_total;

    
END //

DELIMITER ;
