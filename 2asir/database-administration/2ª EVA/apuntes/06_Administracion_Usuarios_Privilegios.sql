/*
================================================================================
   APUNTES COMPLETOS MYSQL - BLOQUE 6: ADMINISTRACIÓN Y SEGURIDAD (2º ASIR)
================================================================================
   Gestión de usuarios, permisos y roles.
*/

-- -----------------------------------------------------------------------------
-- 1. CREACIÓN DE USUARIOS
-- -----------------------------------------------------------------------------
/*
   Usuario en MySQL = 'nombre'@'host'
   'juan'@'localhost' -> Solo conecta desde la máquina local.
   'juan'@'%' -> Conecta desde cualquier IP (Menos seguro).
   'juan'@'192.168.1.50' -> Solo desde esa IP específica.
*/

-- Crear usuario con contraseña nativa
CREATE USER 'becario'@'localhost' IDENTIFIED BY 'contraseña_segura_123';

-- Ver usuarios existentes
-- SELECT user, host FROM mysql.user;

-- Cambiar contraseña (MySQL 8.0+)
ALTER USER 'becario'@'localhost' IDENTIFIED BY 'nueva_pass_456';

-- Eliminar usuario
-- DROP USER 'becario'@'localhost';


-- -----------------------------------------------------------------------------
-- 2. GESTIÓN DE PRIVILEGIOS (GRANT / REVOKE)
-- -----------------------------------------------------------------------------
/*
   Niveles de privilegios:
   1. Global (*.*): Superusuario.
   2. Base de Datos (colegio.*): Admin de esa BD.
   3. Tabla (colegio.empleados): Específico.
   4. Columna: (Muy específico, poco usado por complejidad).
*/

-- Dar permiso de lectura y escritora en la BD apuntes_asir
GRANT SELECT, INSERT, UPDATE ON apuntes_asir.* TO 'becario'@'localhost';

-- Dar permiso total (Administrador) sobre una BD
GRANT ALL PRIVILEGES ON apuntes_asir.* TO 'becario'@'localhost';

-- Permiso para ejecutar procedimientos almacenados
GRANT EXECUTE ON apuntes_asir.* TO 'becario'@'localhost';

-- Quitar permisos (REVOKE)
REVOKE INSERT, UPDATE ON apuntes_asir.* FROM 'becario'@'localhost';

-- Quitar TODOS los permisos
REVOKE ALL PRIVILEGES, GRANT OPTION FROM 'becario'@'localhost';

-- Recargar tabla de permisos (A veces necesario si se toca mysql.user directamente)
FLUSH PRIVILEGES;


-- -----------------------------------------------------------------------------
-- 3. ROLES (MySQL 8.0+)
-- -----------------------------------------------------------------------------
/*
   Simplifica la gestión agrupando permisos en un "rol" y asignando el rol a usuarios.
*/

-- Creación del Rol
CREATE ROLE 'rol_desarrollador';

-- Asignar permisos al Rol
GRANT SELECT, INSERT, UPDATE, DELETE ON apuntes_asir.* TO 'rol_desarrollador';
GRANT CREATE ROUTINE, ALTER ROUTINE ON apuntes_asir.* TO 'rol_desarrollador';

-- Asignar el Rol a un usuario
GRANT 'rol_desarrollador' TO 'becario'@'localhost';

-- ¡IMPORTANTE! El rol suele estar inactivo al hacer login. Hay que activarlo.
-- Activar rol por defecto para ese usuario
SET DEFAULT ROLE 'rol_desarrollador' TO 'becario'@'localhost';

-- Ver permisos de un usuario
SHOW GRANTS FOR 'becario'@'localhost';
