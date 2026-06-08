USE colegio_db;

-- ##########################################################################
-- ### PREGUNTA 1: PROCEDIMIENTO ALMACENADO
-- ##########################################################################

DROP PROCEDURE IF EXISTS sp_reporte_rendimiento_profesores;

DELIMITER //

CREATE PROCEDURE sp_reporte_rendimiento_profesores(IN p_anio INT)
BEGIN
    SELECT 
        CONCAT(p.nombre, ' ', p.apellido) AS profesor_nombre,
        p.especialidad,
        COUNT(DISTINCT c.id_curso) AS cursos_impartidos,
        COUNT(i.id_inscripcion) AS total_estudiantes,
        ROUND(AVG(i.calificacion), 2) AS promedio_general,
        ROUND((SUM(CASE WHEN i.estado = 'Aprobado' THEN 1 ELSE 0 END) / NULLIF(COUNT(i.id_inscripcion), 0)) * 100, 2) AS porcentaje_aprobacion,
        SUM(c.creditos) AS total_creditos
    FROM profesores p
    JOIN cursos c ON p.id_profesor = c.id_profesor
    LEFT JOIN inscripciones i ON c.id_curso = i.id_curso
    WHERE (YEAR(i.fecha_inscripcion) = p_anio OR i.fecha_inscripcion IS NULL)
    GROUP BY p.id_profesor, p.especialidad;
END //

DELIMITER ;

-- Ejemplo de llamada:
-- CALL sp_reporte_rendimiento_profesores(2024);


-- ##########################################################################
-- ### PREGUNTA 2: FUNCIÓN
-- ##########################################################################

DROP FUNCTION IF EXISTS fn_calcular_indice_academico;

DELIMITER //

CREATE FUNCTION fn_calcular_indice_academico(p_id_estudiante INT) 
RETURNS DECIMAL(4,2)
DETERMINISTIC
READS SQL DATA
BEGIN
    DECLARE v_existe INT;
    DECLARE v_indice DECIMAL(4,2);
    
    -- 5. Verificar si el estudiante existe
    SELECT COUNT(*) INTO v_existe FROM estudiantes WHERE id_estudiante = p_id_estudiante;
    IF v_existe = 0 THEN
        RETURN NULL;
    END IF;
    
    -- 2. Calcular el índice: SUM(calificacion * creditos) / SUM(creditos)
    -- 3. Considerar solo cursos 'Aprobado'
    SELECT SUM(i.calificacion * c.creditos) / SUM(c.creditos) INTO v_indice
    FROM inscripciones i
    JOIN cursos c ON i.id_curso = c.id_curso
    WHERE i.id_estudiante = p_id_estudiante AND i.estado = 'Aprobado';
    
    -- 4. Si no tiene cursos aprobados retornar 0.00
    IF v_indice IS NULL THEN
        RETURN 0.00;
    END IF;
    
    RETURN v_indice;
END //

DELIMITER ;


-- ##########################################################################
-- ### PREGUNTA 3: TRIGGER (CUPO)
-- ##########################################################################

DROP TRIGGER IF EXISTS tg_verificar_cupo_curso;

DELIMITER //

CREATE TRIGGER tg_verificar_cupo_curso
BEFORE INSERT ON inscripciones
FOR EACH ROW
BEGIN
    DECLARE v_actuales INT;
    DECLARE v_maximo INT;
    
    -- 2. Contar estudiantes actuales (excluyendo 'Retirado')
    SELECT COUNT(*) INTO v_actuales 
    FROM inscripciones 
    WHERE id_curso = NEW.id_curso AND estado != 'Retirado';
    
    -- 3. Obtener cupo máximo
    SELECT cupo_maximo INTO v_maximo FROM cursos WHERE id_curso = NEW.id_curso;
    
    -- 4. Si el cupo está lleno, rechazar inserción
    IF v_actuales >= v_maximo THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Error: El cupo máximo para este curso ya ha sido alcanzado.';
    END IF;
    
    -- 5. Si hay cupo, por defecto entra como 'Inscrito' (definido en el DEFAULT de la tabla)
END //

DELIMITER ;


-- ##########################################################################
-- ### PREGUNTA 4: TRIGGER (AUDITORÍA)
-- ##########################################################################

DROP TRIGGER IF EXISTS tg_auditar_cambios_calificacion;

DELIMITER //

CREATE TRIGGER tg_auditar_cambios_calificacion
BEFORE UPDATE ON inscripciones
FOR EACH ROW
BEGIN
    DECLARE v_sospechoso BOOLEAN DEFAULT FALSE;
    DECLARE v_motivo VARCHAR(200) DEFAULT '';

    -- 2. Detectar cambios en la calificación
    IF NOT (NEW.calificacion <=> OLD.calificacion) THEN
        -- 6. Actualizar automáticamente el estado según la nueva calificación
        IF NEW.calificacion >= 5.0 THEN
            SET NEW.estado = 'Aprobado';
        ELSE
            SET NEW.estado = 'Reprobado';
        END IF;

        -- 3. Verificar si es sospechoso (> 2 puntos o cambio de estado aprobado/suspenso)
        IF ABS(NEW.calificacion - OLD.calificacion) > 2 THEN
            SET v_sospechoso = TRUE;
            SET v_motivo = 'Diferencia de calificación superior a 2 puntos.';
        END IF;

        IF (OLD.calificacion < 5.0 AND NEW.calificacion >= 5.0) OR (OLD.calificacion >= 5.0 AND NEW.calificacion < 5.0) THEN
            SET v_sospechoso = TRUE;
            SET v_motivo = CONCAT(v_motivo, ' Alteración del estado académico.');
        END IF;

        -- 4. Registrar en auditoría si es sospechoso
        IF v_sospechoso THEN
            INSERT INTO auditoria_calificaciones (
                id_inscripcion, 
                calificacion_anterior, 
                calificacion_nueva, 
                diferencia, 
                usuario, 
                motivo
            ) VALUES (
                OLD.id_inscripcion,
                OLD.calificacion,
                NEW.calificacion,
                NEW.calificacion - OLD.calificacion,
                'SISTEMA',
                v_motivo
            );
        END IF;
    END IF;
END //

DELIMITER ;