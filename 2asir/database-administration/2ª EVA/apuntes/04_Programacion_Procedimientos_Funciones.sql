/*
================================================================================
   APUNTES COMPLETOS MYSQL - BLOQUE 4: PROGRAMACIÓN (2º ASIR)
   PROCEDIMIENTOS ALMACENADOS, FUNCIONES Y ESTRUCTURAS DE CONTROL
================================================================================
*/

USE apuntes_asir;

-- -----------------------------------------------------------------------------
-- 1. ESTRUCTURAS DE CONTROL DE FLUJO (Solo en Procedimientos/Funciones)
-- -----------------------------------------------------------------------------

/*
   DELIMITER //
   Cambia el terminador de sentencia de ; a // para poder escribir el ; dentro
   del cuerpo del procedimiento sin que MySQL crea que ha terminado la instrucción.
*/

DROP PROCEDURE IF EXISTS ejemplo_estructuras;

DELIMITER //

CREATE PROCEDURE ejemplo_estructuras(IN nota INT, OUT resultado VARCHAR(20))
BEGIN
    -- IF / ELSEIF / ELSE
    IF nota >= 9 THEN
        SET resultado = 'Sobresaliente';
    ELSEIF nota >= 5 THEN
        SET resultado = 'Aprobado';
    ELSE
        SET resultado = 'Suspenso';
    END IF;
    
    -- CASE
    CASE nota
        WHEN 10 THEN SET resultado = 'Matrícula';
        ELSE BEGIN END; -- Bloque vacío
    END CASE;
    
    -- WHILE LOOP
    DECLARE i INT DEFAULT 0;
    WHILE i < 5 DO
        SET i = i + 1;
        -- ITERATE termina la iteración actual (como continue)
        -- LEAVE termina el bucle (como break)
    END WHILE;
END //

DELIMITER ;


-- -----------------------------------------------------------------------------
-- 2. PROCEDIMIENTOS ALMACENADOS (STORED PROCEDURES)
-- -----------------------------------------------------------------------------
/*
   Diferencias clave con funciones:
   1. Se invocan con CALL.
   2. No devuelven un valor en el nombre, usan parámetros OUT o INOUT.
   3. Pueden ejecutar transacciones (COMMIT/ROLLBACK) y SQL dinámico.
   4. Pueden devolver múltiples ResultSets (SELECTs).
*/

DROP PROCEDURE IF EXISTS sp_subir_salario_departamento;

DELIMITER //

CREATE PROCEDURE sp_subir_salario_departamento(
    IN p_dept_id INT, 
    IN p_porcentaje DECIMAL(5,2)
)
BEGIN
    -- Manejo de errores (HANDLER)
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        SELECT 'Error: No se pudo actualizar el salario' AS mensaje;
        ROLLBACK;
    END;

    START TRANSACTION;
        
    UPDATE empleados 
    SET salario = salario * (1 + p_porcentaje / 100)
    WHERE dept_id = p_dept_id;
    
    -- Devolver información
    SELECT CONCAT('Filas afectadas: ', ROW_COUNT()) AS resultado;
    
    COMMIT;
END //

DELIMITER ;

-- Ejecución:
-- CALL sp_subir_salario_departamento(1, 10.5);


-- -----------------------------------------------------------------------------
-- 3. FUNCIONES DEFINIDAS POR EL USUARIO (UDF)
-- -----------------------------------------------------------------------------
/*
   Diferencias:
   1. Se invocan dentro de un SELECT o expresión.
   2. DEBEN devolver un valor único (RETURNS tipo).
   3. DETERMINISTIC: Si para la misma entrada da siempre la misma salida (cacheable).
   4. NO pueden hacer commit/rollback ni devolver resultsets.
*/

DROP FUNCTION IF EXISTS fn_calcular_neto;

DELIMITER //

CREATE FUNCTION fn_calcular_neto(salario_bruto DECIMAL(10,2)) 
RETURNS DECIMAL(10,2)
DETERMINISTIC
BEGIN
    DECLARE neto DECIMAL(10,2);
    DECLARE irpf DECIMAL(4,2) DEFAULT 0.15; -- 15%
    
    IF salario_bruto > 3000 THEN
        SET irpf = 0.20;
    END IF;
    
    SET neto = salario_bruto * (1 - irpf);
    
    RETURN neto;
END //

DELIMITER ;

-- Uso:
-- SELECT nombre, salario, fn_calcular_neto(salario) FROM empleados;


-- -----------------------------------------------------------------------------
-- 4. CURSORES (Procesar filas una a una)
-- -----------------------------------------------------------------------------
/*
   Pasos obligatorios: DECLARE -> OPEN -> FETCH -> CLOSE
   Importante: Declarar handlers para saber cuándo termina el cursor.
*/

DROP PROCEDURE IF EXISTS sp_listar_empleados_cursor;

DELIMITER //

CREATE PROCEDURE sp_listar_empleados_cursor()
BEGIN
    DECLARE hecho INT DEFAULT FALSE;
    DECLARE v_nombre VARCHAR(50);
    
    -- 1. Declarar cursor
    DECLARE cur_empleados CURSOR FOR 
        SELECT nombre FROM empleados WHERE salario > 2000;
        
    -- 2. Declarar handler de fin (NOT FOUND)
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET hecho = TRUE;
    
    -- 3. Abrir
    OPEN cur_empleados;
    
    read_loop: LOOP
        -- 4. Leer fila
        FETCH cur_empleados INTO v_nombre;
        
        IF hecho THEN
            LEAVE read_loop;
        END IF;
        
        -- Hacer algo con v_nombre (ej: insertarlo en log)
        -- INSERT INTO log_table VALUES (v_nombre);
        
    END LOOP;
    
    -- 5. Cerrar
    CLOSE cur_empleados;
END //

DELIMITER ;
