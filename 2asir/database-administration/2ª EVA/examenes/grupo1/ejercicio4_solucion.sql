-- Versión ultra simplificada Ejercicio 4
DELIMITER //

CREATE TRIGGER tr_validar_precio_corto
BEFORE INSERT ON productos FOR EACH ROW
BEGIN
    DECLARE prom DECIMAL(10,2);
    DECLARE mot VARCHAR(50);

    SELECT AVG(precio) INTO prom FROM productos WHERE id_categoria = NEW.id_categoria AND activo = 1;

    IF prom IS NOT NULL THEN
        IF NEW.precio < prom * 0.5 THEN 
            SET mot = 'Ajuste por precio bajo', NEW.precio = prom * 0.5;
        ELSEIF NEW.precio > prom * 2.0 THEN 
            SET mot = 'Ajuste por precio alto', NEW.precio = prom * 2.0;
        END IF;

        IF mot IS NOT NULL THEN
            INSERT INTO auditoria_precios (precio_anterior, precio_nuevo, usuario, motivo) 
            VALUES (NEW.precio, NEW.precio, USER(), mot);
        END IF;
    END IF;
END //

DELIMITER ;
