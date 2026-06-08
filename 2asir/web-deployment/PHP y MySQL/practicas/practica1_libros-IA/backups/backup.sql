-- Crear base de datos
CREATE DATABASE IF NOT EXISTS biblioteca_escolar;
USE biblioteca_escolar;

-- Tabla Libros
CREATE TABLE Libros (
    id_libro INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(100),
    autor VARCHAR(100),
    editorial VARCHAR(50),
    isbn VARCHAR(20),
    anio_publicacion INTEGER,
    disponible BOOLEAN DEFAULT true,
    portada VARCHAR(300),
    PRIMARY KEY(id_libro)
);

-- Tabla Estudiantes
CREATE TABLE Estudiantes (
    id_estudiante INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    password VARCHAR(100),
    nombre VARCHAR(50),
    apellidos VARCHAR(100),
    codigo_estudiante VARCHAR(20) UNIQUE,
    curso VARCHAR(30),
    telefono VARCHAR(15),
    PRIMARY KEY(id_estudiante)
);

-- Tabla Prestamos
CREATE TABLE Prestamos (
    id_prestamo INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    id_estudiante INTEGER UNSIGNED,
    id_libro INTEGER UNSIGNED,
    fecha_prestamo DATETIME,
    fecha_devolucion DATETIME,
    devuelto BOOLEAN DEFAULT false,
    PRIMARY KEY(id_prestamo),
    FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_estudiante) ON DELETE CASCADE,
    FOREIGN KEY (id_libro) REFERENCES Libros(id_libro) ON DELETE CASCADE
);

-- Insertar datos de ejemplo en Libros
INSERT INTO Libros (titulo, autor, editorial, isbn, anio_publicacion, disponible, portada) VALUES
('Cien anios de soledad', 'Gabriel García Márquez', 'Sudamericana', '978-0307474728', 1967, true, 'cien_anos.jpg'),
('El principito', 'Antoine de Saint-Exupéry', 'Reynal & Hitchcock', '978-0156013987', 1943, true, 'principito.jpg'),
('1984', 'George Orwell', 'Secker & Warburg', '978-0451524935', 1949, false, '1984.jpg'),
('Don Quijote de la Mancha', 'Miguel de Cervantes', 'Francisco de Robles', '978-8424116196', 1605, true, 'quijote.jpg'),
('Harry Potter y la piedra filosofal', 'J.K. Rowling', 'Bloomsbury', '978-8478884452', 1997, true, 'harry_potter.jpg');

-- Insertar datos de ejemplo en Estudiantes
INSERT INTO Estudiantes (nombre, apellidos, codigo_estudiante, curso, telefono, password) VALUES
('María', 'González Pérez', 'EST2024001', '4º ESO', '611223344', 'rootroot'),
('Carlos', 'Ruiz López', 'EST2024002', '1º Bachillerato', '622334455', 'rootroot'),
('Ana', 'Martínez Sánchez', 'EST2024003', '3º ESO', '633445566', 'rootroot'),
('Javier', 'Fernández Díaz', 'EST2024004', '2º Bachillerato', '644556677', 'rootroot');

-- Insertar datos de ejemplo en Prestamos
INSERT INTO Prestamos (id_estudiante, id_libro, fecha_prestamo, fecha_devolucion, devuelto) VALUES
(1, 3, '2024-01-15 10:30:00', '2024-02-15 10:30:00', false),
(2, 1, '2024-01-20 14:00:00', '2024-02-20 14:00:00', true),
(3, 2, '2024-02-01 09:15:00', '2024-03-01 09:15:00', false);


-- Insertar los libros restantes que tienen portada en la carpeta /portadas
INSERT INTO Libros (titulo, autor, editorial, isbn, anio_publicacion, disponible, portada) VALUES
('El Aleph', 'Jorge Luis Borges', 'Alianza Editorial', '978-8420633128', 1949, true, 'aleph.png'),
('El amor en los tiempos del cólera', 'Gabriel García Márquez', 'Debolsillo', '978-8497592161', 1985, true, 'amor_colera.png'),
('La casa de los espíritus', 'Isabel Allende', 'Debolsillo', '978-8483462034', 1982, true, 'casa_espiritus.png'),
('La ciudad y los perros', 'Mario Vargas Llosa', 'Punto de Lectura', '978-8466309158', 1962, true, 'ciudad_perros.png'),
('El código Da Vinci', 'Dan Brown', 'Umbriel', '978-8495618603', 2003, true, 'codigo_davinci.png'),
('Crónica de una muerte anunciada', 'Gabriel García Márquez', 'Cátedra', '978-8437604534', 1981, true, 'cronica_muerte.png'),
('Crónicas marcianas', 'Ray Bradbury', 'Minotauro', '978-8445070536', 1950, true, 'cronicas_marcianas.png'),
('Los detectives salvajes', 'Roberto Bolaño', 'Anagrama', '978-8433966638', 1998, true, 'detectives_salvajes.png'),
('Ensayo sobre la ceguera', 'José Saramago', 'Alfaguara', '978-8420471211', 1995, true, 'ensayo_ceguera.png'),
('Fahrenheit 451', 'Ray Bradbury', 'Minotauro', '978-8445077955', 1953, true, 'farenheit_451.png'),
('Ficciones', 'Jorge Luis Borges', 'Alianza Editorial', '978-8420633111', 1944, true, 'ficciones.png'),
('El guardián entre el centeno', 'J.D. Salinger', 'Alianza Editorial', '978-8420674209', 1951, true, 'guardian_centeno.png'),
('Harry Potter y la cámara secreta', 'J.K. Rowling', 'Salamandra', '978-8478884957', 1998, true, 'harry_potter_2.png'),
('El Hobbit', 'J.R.R. Tolkien', 'Minotauro', '978-8445000656', 1937, true, 'hobbit.png'),
('La metamorfosis', 'Franz Kafka', 'Alianza Editorial', '978-8420651361', 1915, true, 'metamorfosis.png'),
('El nombre de la rosa', 'Umberto Eco', 'Lumen', '978-8426403568', 1980, true, 'nombre_rosa.png'),
('Pedro Páramo', 'Juan Rulfo', 'Cátedra', '978-8437604183', 1955, true, 'pedro_paramo.png'),
('Los pilares de la Tierra', 'Ken Follett', 'Plaza & Janés', '978-8401328510', 1989, true, 'pilares_tierra.png'),
('Rayuela', 'Julio Cortázar', 'Cátedra', '978-8437604213', 1963, true, 'rayuela.png'),
('La sombra del viento', 'Carlos Ruiz Zafón', 'Planeta', '978-8408081128', 2001, true, 'sombra_viento.png'),
('Verity', 'Colleen Hoover', 'Planeta', '978-8408269755', 2018, true, '71M8IoER7JL._AC_UF894,1000_QL80_.jpg');