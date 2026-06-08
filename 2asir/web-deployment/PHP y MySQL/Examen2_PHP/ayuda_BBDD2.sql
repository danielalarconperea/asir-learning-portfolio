-- Base de datos: red_social_db
CREATE DATABASE IF NOT EXISTS red_social_db;
USE red_social_db;

-- Tabla usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    fecha_nacimiento DATE,
    pais VARCHAR(50),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla publicaciones
CREATE TABLE IF NOT EXISTS publicaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT,
    contenido TEXT NOT NULL,
    fecha_publicacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    likes INT DEFAULT 0,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- Datos de ejemplo
INSERT INTO usuarios (username, nombre, email, fecha_nacimiento, pais) VALUES
('maria_g', 'María González', 'maria@email.com', '1995-03-15', 'España'),
('carlos_r', 'Carlos Rodríguez', 'carlos@email.com', '1992-08-22', 'México'),
('ana_m', 'Ana Martínez', 'ana@email.com', '1998-11-05', 'Colombia'),
('luis_f', 'Luis Fernández', 'luis@email.com', '1990-06-30', 'Argentina'),
('sofia_l', 'Sofía López', 'sofia@email.com', '1996-12-10', 'Chile');

INSERT INTO publicaciones (usuario_id, contenido, likes) VALUES
(1, '¡Hola a todos! Mi primera publicación en la red social. #inicio', 15),
(1, 'Disfrutando de un hermoso día de sol ☀️', 42),
(2, 'Acabo de terminar un proyecto importante en el trabajo 💼', 28),
(3, 'Recomendaciones de libros para el fin de semana? 📚', 37),
(4, 'Viajando a Buenos Aires, ¡qué emoción! ✈️', 56),
(5, 'Cocinando mi receta especial de pastel de chocolate 🍫', 64);