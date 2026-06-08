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

-- Insertar listado de libros primero para que los IDs existan para los préstamos
INSERT INTO Libros (titulo, autor, editorial, isbn, anio_publicacion, disponible, portada) VALUES
('Cien años de soledad', 'Gabriel García Márquez', 'Sudamericana', '978-0307474728', 1967, true, 'cien_anos.jpg'),
('El principito', 'Antoine de Saint-Exupéry', 'Reynal & Hitchcock', '978-0156013987', 1943, true, 'principito.jpg'),
('1984', 'George Orwell', 'Secker & Warburg', '978-0451524935', 1949, true, '1984.jpg'),
('Don Quijote de la Mancha', 'Miguel de Cervantes', 'Francisco de Robles', '978-8424116196', 1605, true, 'quijote.jpg'),
('Harry Potter y la piedra filosofal', 'J.K. Rowling', 'Bloomsbury', '978-8478884452', 1997, true, 'harry_potter.jpg'),
('Alas de sangre', 'Rebecca Yarros', 'Planeta', '978-0307474723', 2023, true, '71M8IoER7JL._AC_UF894,1000_QL80_.jpg'),
('Rayuela', 'Julio Cortázar', 'Sudamericana', '978-8420412146', 1963, true, 'rayuela.png'),
('Pedro Páramo', 'Juan Rulfo', 'FCE', '978-8437603124', 1955, true, 'pedro_paramo.png'),
('La metamorfosis', 'Franz Kafka', 'Kurt Wolff', '978-8420651361', 1915, true, 'metamorfosis.png'),
('El Aleph', 'Jorge Luis Borges', 'Losada', '978-8420633114', 1949, true, 'aleph.png'),
('Ficciones', 'Jorge Luis Borges', 'Sur', '978-8420633138', 1944, true, 'ficciones.png'),
('El nombre de la rosa', 'Umberto Eco', 'Bompiani', '978-8426414113', 1980, true, 'nombre_rosa.png'),
('Crónica de una muerte anunciada', 'Gabriel García Márquez', 'Oveja Negra', '978-8437603094', 1981, true, 'cronica_muerte.png'),
('El amor en los tiempos del cólera', 'Gabriel García Márquez', 'Oveja Negra', '978-8437605968', 1985, true, 'amor_colera.png'),
('Ensayo sobre la ceguera', 'José Saramago', 'Caminho', '978-8420442655', 1995, true, 'ensayo_ceguera.png'),
('La ciudad y los perros', 'Mario Vargas Llosa', 'Seix Barral', '978-8432248238', 1963, true, 'ciudad_perros.png'),
('Los detectives salvajes', 'Roberto Bolaño', 'Anagrama', '978-8433973542', 1998, true, 'detectives_salvajes.png'),
('La sombra del viento', 'Carlos Ruiz Zafón', 'Planeta', '978-8408043645', 2001, true, 'sombra_viento.png'),
('La casa de los espíritus', 'Isabel Allende', 'Sudamericana', '978-8401340543', 1982, true, 'casa_espiritus.png'),
('El código Da Vinci', 'Dan Brown', 'Doubleday', '978-0385504201', 2003, true, 'codigo_davinci.png'),
('Harry Potter y la cámara secreta', 'J.K. Rowling', 'Bloomsbury', '978-8478884956', 1998, true, 'harry_potter_2.png'),
('Crónicas marcianas', 'Ray Bradbury', 'Minotauro', '978-8445071151', 1950, true, 'cronicas_marcianas.png'),
('Fahrenheit 451', 'Ray Bradbury', 'Ballantine', '978-8445071144', 1953, true, 'farenheit_451.png'),
('El Hobbit', 'J.R.R. Tolkien', 'Allen & Unwin', '978-8445071410', 1937, true, 'hobbit.png'),
('Los pilares de la Tierra', 'Ken Follett', 'Macmillan', '978-8401328510', 1989, true, 'pilares_tierra.png'),
('El guardián entre el centeno', 'J.D. Salinger', 'Little, Brown', '978-8420651330', 1951, true, 'guardian_centeno.png'),
('Los juegos del hambre', 'Suzanne Collins', 'Molino', '978-0307474745', 2014, true, 'los-juegos-del-hambre-1-los-juegos-del-hambre-edicion-especial.jpg'),
('Una corte de rosas y espinas', 'Sarah J. Maas', 'Crossbooks', '978-8408285298', 2016, true, 'entry442x614.avif');

-- Insertar datos de ejemplo en Estudiantes
INSERT INTO Estudiantes (nombre, apellidos, codigo_estudiante, curso, telefono, password) VALUES
('María', 'González Pérez', 'EST2024001', '4º ESO', '611223344', 'rootroot'),
('Carlos', 'Ruiz López', 'EST2024002', '1º Bachillerato', '622334455', 'rootroot'),
('Ana', 'Martínez Sánchez', 'EST2024003', '3º ESO', '633445566', 'rootroot'),
('Javier', 'Fernández Díaz', 'EST2024004', '2º Bachillerato', '644556677', 'rootroot'),
('Elena', 'Sánchez Torres', 'EST2024005', '1º ESO', '655667788', 'rootroot'),
('Pablo', 'Gómez Marín', 'EST2024006', '2º ESO', '666778899', 'rootroot'),
('Lucía', 'Vázquez Ramos', 'EST2024007', '3º ESO', '677889900', 'rootroot'),
('Diego', 'Castro Ortiz', 'EST2024008', '4º ESO', '688990011', 'rootroot'),
('Sofía', 'Navarro Gil', 'EST2024009', '1º Bachillerato', '699001122', 'rootroot'),
('Adrián', 'Morales Sanz', 'EST2024010', '2º Bachillerato', '600112233', 'rootroot'),
('Marta', 'Delgado Rubia', 'EST2024011', '1º ESO', '611223355', 'rootroot'),
('Alejandro', 'Ibáñez Medina', 'EST2024012', '2º ESO', '622334466', 'rootroot'),
('Paula', 'Cano Garrido', 'EST2024013', '3º ESO', '633445577', 'rootroot'),
('Marcos', 'Blanco Ortega', 'EST2024014', '4º ESO', '644556688', 'rootroot'),
('Irene', 'Suárez Molina', 'EST2024015', '1º Bachillerato', '655667799', 'rootroot'),
('Hugo', 'Guerrero Vidal', 'EST2024016', '2º Bachillerato', '666778811', 'rootroot'),
('Sara', 'Moya Soler', 'EST2024017', '1º ESO', '677889922', 'rootroot'),
('Daniel', 'Cortes Cabrera', 'EST2024018', '2º ESO', '688990033', 'rootroot'),
('Alba', 'Pascual Esteban', 'EST2024019', '3º ESO', '699001144', 'rootroot');

-- Insertar datos de ejemplo en Prestamos (id_estudiante 1-19, id_libro 1-28)
INSERT INTO Prestamos (id_estudiante, id_libro, fecha_prestamo, fecha_devolucion, devuelto) VALUES
(1, 1, '2024-01-15 10:30:00', '2024-02-15 10:30:00', true),
(2, 2, '2024-01-20 14:00:00', '2024-02-20 14:00:00', true),
(3, 3, '2024-02-01 09:15:00', '2024-03-01 09:15:00', false),
(4, 4, '2024-02-05 11:00:00', '2024-03-05 11:00:00', true),
