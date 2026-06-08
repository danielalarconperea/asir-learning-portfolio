/*
================================================================================
   APUNTES COMPLETOS MYSQL - BLOQUE 5: TRIGGERS Y EVENTOS (2º ASIR)
================================================================================
   Estos objetos se ejecutan automáticamente por el sistema ante ciertos sucesos.
*/

USE apuntes_asir;

-- Tabla de auditoría para ejemplos
CREATE TABLE IF NOT EXISTS auditoria_salarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    empleado_id INT,
    salario_anterior DECIMAL(10,2),
    salario_nuevo DECIMAL(10,2),
    usuario VARCHAR(50),
    fecha DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- -----------------------------------------------------------------------------
-- 1. DISPARADORES (TRIGGERS)
-- -----------------------------------------------------------------------------
/*
   Sintaxis:
   CREATE TRIGGER nombre_trigger
   [BEFORE | AFTER] [INSERT | UPDATE | DELETE] ON nombre_tabla
   FOR EACH ROW
   BEGIN ... END;
   
   NEW.campo : Valor nuevo (disponible en INSERT y UPDATE)
   OLD.campo : Valor antiguo (disponible en UPDATE y DELETE)
*/

DROP TRIGGER IF EXISTS trg_valida_salario_before_insert;

DELIMITER //

-- EJEMPLO 1: Validación (BEFORE INSERT)
-- Impide insertar un sueldo negativo. Modifica los datos antes de guardarlos.
CREATE TRIGGER trg_valida_salario_before_insert
BEFORE INSERT ON empleados
FOR EACH ROW
BEGIN
    IF NEW.salario < 0 THEN
        -- Opción A: Corregirlo automáticamente
        SET NEW.salario = 0;
        
        -- Opción B: Lanzar error y abortar (MySQL 5.5+)
        -- SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Salario negativo no permitido';
    END IF;
END //

DELIMITER ;


DROP TRIGGER IF EXISTS trg_auditoria_after_update;

DELIMITER //

-- EJEMPLO 2: Auditoría (AFTER UPDATE)
-- Registra cambios en otra tabla. El cambio original YA se ha hecho.
CREATE TRIGGER trg_auditoria_after_update
AFTER UPDATE ON empleados
FOR EACH ROW
BEGIN
    -- Solo si el salario ha cambiado (Eficiencia)
    -- <=> Operador de igualdad 'seguro para NULL'
    IF NOT (NEW.salario <=> OLD.salario) THEN
        INSERT INTO auditoria_salarios 
        (empleado_id, salario_anterior, salario_nuevo, usuario)
        VALUES 
        (OLD.emp_id, OLD.salario, NEW.salario, CURRENT_USER());
    END IF;
END //

DELIMITER ;

/*
   NOTAS SOBRE TRIGGERS:
   - No pueden llamar a procedimientos que devuelvan datos.
   - No pueden hacer COMMIT/ROLLBACK implícito ni explícito.
   - Cuidado con la recursividad (Trigger A actualiza Tabla B, Trigger B actualiza Tabla A).
*/


-- -----------------------------------------------------------------------------
-- 2. EVENTOS PROGRAMADOS (EVENTS / JOB SCHEDULER)
-- -----------------------------------------------------------------------------
/*
   Alternativa al CRON de Linux dentro de MySQL.
   Requiere: SET GLOBAL event_scheduler = ON;
*/

-- Ver si está activado
-- SHOW VARIABLES LIKE 'event_scheduler';

DROP EVENT IF EXISTS evt_limpieza_logs_semanal;

DELIMITER //

CREATE EVENT evt_limpieza_logs_semanal
ON SCHEDULE EVERY 1 WEEK STARTS '2024-01-01 03:00:00'
DO
BEGIN
    -- Borrar logs de hace más de un año
    DELETE FROM auditoria_salarios 
    WHERE fecha < DATE_SUB(NOW(), INTERVAL 1 YEAR);
    
    -- Optimizar la tabla (Opcional)
    -- OPTIMIZE TABLE auditoria_salarios;
END //

DELIMITER ;

-- Deshabilitar temporalmente un evento
ALTER EVENT evt_limpieza_logs_semanal DISABLE;

-- Borrar evento
-- DROP EVENT evt_limpieza_logs_semanal;
