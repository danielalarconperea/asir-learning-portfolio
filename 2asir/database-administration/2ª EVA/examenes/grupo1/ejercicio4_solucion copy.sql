-- Solución Ejercicio 4 - Examen DDBB Restaurante
-- Objeto: Trigger para validar precios de productos según el promedio de su categoría

-- 1. Preparación: La tabla auditoria_precios no tiene la columna 'motivo' en el dump original.
-- El enunciado pide registrar el motivo, por lo que primero añadimos la columna.
ALTER TABLE `auditoria_precios` ADD COLUMN `motivo` VARCHAR(100);

-- 2. Creación del Trigger
DELIMITER //

DROP TRIGGER IF EXISTS tr_validar_precio_nuevo //

CREATE TRIGGER tr_validar_precio_nuevo
BEFORE INSERT ON productos
FOR EACH ROW
BEGIN
    DECLARE v_promedio_cat DECIMAL(10,2);
    DECLARE v_precio_original DECIMAL(10,2);
    DECLARE v_motivo_ajuste VARCHAR(100) DEFAULT NULL;

    -- Obtener el precio promedio de productos activos en la misma categoría
    SELECT AVG(precio) INTO v_promedio_cat
    FROM productos
    WHERE id_categoria = NEW.id_categoria 
      AND activo = 1;

    -- Si no hay productos en la categoría, no se realizan ajustes (v_promedio_cat IS NULL)
    IF v_promedio_cat IS NOT NULL THEN
        SET v_precio_original = NEW.precio;

        -- Caso A: Precio menor al 50% del promedio
        IF v_precio_original < (v_promedio_cat * 0.50) THEN
            SET NEW.precio = v_promedio_cat * 0.50;
            SET v_motivo_ajuste = 'Ajuste por precio bajo';

        -- Caso B: Precio mayor al 200% del promedio
        ELSEIF v_precio_original > (v_promedio_cat * 2.00) THEN
            SET NEW.precio = v_promedio_cat * 2.00;
            SET v_motivo_ajuste = 'Ajuste por precio alto';
        END IF;

        -- Registrar en auditoría si hubo algún ajuste
        IF v_motivo_ajuste IS NOT NULL THEN
            INSERT INTO auditoria_precios (
                id_producto,        -- Será NULL ya que en BEFORE INSERT el ID auto-incremental aún no se ha generado
                precio_anterior, 
                precio_nuevo, 
                diferencia, 
                porcentaje_cambio, 
                usuario, 
                motivo
            ) VALUES (
                NULL, 
                v_precio_original, 
                NEW.precio, 
                (NEW.precio - v_precio_original),
                ((NEW.precio - v_precio_original) / v_precio_original) * 100,
                USER(),
                v_motivo_ajuste
            );
        END IF;
    END IF;
END //

DELIMITER ;

-- 3. Pruebas (Opcional - Documentación)
/*
-- Para probar el trigger, primero hay que tener productos en una categoría (ej: Bebidas ID 1)
-- El promedio de Bebidas en el dump es (2.50 + 1.50 + 3.00 + 4.50 + 5.00) / 5 = 3.30
-- Límite bajo: 1.65 | Límite alto: 6.60

-- Prueba precio bajo:
INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria, activo) 
VALUES ('Refresco Mini', 'Prueba Bajo', 0.50, 10, 1, 1);
-- Result: El precio debería quedar en 1.65 y crearse un log.

-- Prueba precio alto:
INSERT INTO productos (nombre, descripcion, precio, stock, id_categoria, activo) 
VALUES ('Champagne Imperial', 'Prueba Alto', 50.00, 5, 1, 1);
-- Result: El precio debería quedar en 6.60 y crearse un log.
*/
