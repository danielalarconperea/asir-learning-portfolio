/*
PROBLEMA 4: Trigger de validación de precios (Auditoría)

Necesitamos un trigger que valide los precios de nuevos productos comparándolos con el 
promedio de su categoría. Si un producto se inserta con un precio menor al 50% del 
promedio o mayor al 200%, se debe ajustar el límite correspondiente y registrar el cambio 
en auditoría. Esto previene errores de digitación extremos manteniendo precios coherentes por categoría.

Lógica:
1. Calcule el precio promedio de los productos activos en la misma categoría.
2. Si el nuevo precio es menor al 50% del promedio:
   - Ajuste el precio al 50% del promedio.
   - Registre en auditoria_precios con el motivo 'Ajuste por precio bajo'.
3. Si el nuevo precio es mayor al 200% del promedio:
   - Ajuste el precio al 200% del promedio.
   - Registre en auditoria_precios con el motivo 'Ajuste por precio alto'.
4. Si no hay productos en la categoría, no haga ajustes.
*/

DELIMITER //

CREATE TRIGGER tr_validar_precio
BEFORE INSERT ON productos
FOR EACH ROW
BEGIN
    -- Escribe aquí tu solución
END //

DELIMITER ;
