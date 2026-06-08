-- MODIFICACIONES FASE 2: AUTENTICACIÓN Y ROLES

-- 1. Ampliar tabla Estudiantes con campos de autenticación y roles
ALTER TABLE Estudiantes
ADD COLUMN rol ENUM('estudiante', 'profesor', 'administrador') DEFAULT 'estudiante',
ADD COLUMN email VARCHAR(100) UNIQUE,
ADD COLUMN fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP;

-- 2. Crear tabla de auditoría de intentos de login
CREATE TABLE Intentos_Login (
    id_intento INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    email VARCHAR(100),
    ip_address VARCHAR(45),
    intento DATETIME DEFAULT CURRENT_TIMESTAMP,
    exito BOOLEAN,
    PRIMARY KEY(id_intento)
);

-- 3. Índices para optimización
CREATE INDEX idx_email ON Estudiantes(email);
CREATE INDEX idx_rol ON Estudiantes(rol);
CREATE INDEX idx_disponible ON Libros(disponible);

-- 4. Insertar usuario administrador inicial
-- Password: admin123 (Hash generado con PASSWORD_DEFAULT)
-- Nota: En un entorno real, genera este hash con PHP: echo password_hash('admin123', PASSWORD_DEFAULT);
-- El hash abajo es un ejemplo válido para $2y$10$...
INSERT INTO Estudiantes (nombre, apellidos, email, password, rol, codigo_estudiante)
VALUES ('Admin', 'Sistema', 'admin@biblioteca.local', '$2y$10$e.g./Use.PHP.to.gen.hash.For.admin123', 'administrador', 'ADMIN001');
