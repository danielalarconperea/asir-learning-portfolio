<?php
/**
 * ============================================================================
 *               📓 APUNTES DE PHP Y MYSQL - GUÍA DE ESTUDIO
 * ============================================================================
 * 
 * Este archivo contiene la teoría y ejemplos prácticos extraídos de los 
 * ejercicios de clase. Lee el código y los comentarios para estudiar.
 * 
 * ÍNDICE:
 * 1. FUNDAMENTOS DE SQL (Bases de Datos y Tablas)
 * 2. CONEXIÓN PHP -> MYSQL
 * 3. OPERACIONES CRUD (Consultas, Inserciones, Ediciones)
 * 4. SEGURIDAD (Inyección SQL)
 * 5. CONTROL DE SESIONES
 * 6. DICCIONARIO DE FUNCIONES
 */

/* ----------------------------------------------------------------------------
 * 1. FUNDAMENTOS DE SQL
 * ----------------------------------------------------------------------------
 * El lenguaje SQL se usa para comunicarnos con la base de datos.
 * 
 * -- CREAR BD:
 * CREATE DATABASE IF NOT EXISTS mi_base_datos;
 * 
 * -- CREAR TABLA:
 * CREATE TABLE Usuarios (
 *     id INT AUTO_INCREMENT PRIMARY KEY,
 *     nombre VARCHAR(50) NOT NULL,
 *     email VARCHAR(100) UNIQUE
 * );
 * 
 * -- CRUD EN SQL:
 * INSERT INTO Usuarios (nombre, email) VALUES ('Pepe', 'pepe@mail.com');
 * SELECT * FROM Usuarios WHERE id = 1;
 * UPDATE Usuarios SET nombre = 'Jose' WHERE id = 1;
 * DELETE FROM Usuarios WHERE id = 1;
 */


/* ----------------------------------------------------------------------------
 * 2. CONEXIÓN PHP -> MYSQL
 * ----------------------------------------------------------------------------
 * Usamos la extensión 'mysqli' para conectar PHP con el servidor de base de datos.
 */

$host = "localhost";
$user = "root";
$pass = "asdf";
$db   = "biblioteca_escolar";

// Establecer la conexión
// @ suprime errores (si haces control de errores no es obligatorio)
$conexion = @mysqli_connect($host, $user, $pass, $db);

if (!$conexion) {
    // Si falla, detenemos el script y mostramos el error
    // die("Error crítico: " . mysqli_connect_error());
} else {
    // Configurar charset para que tildes y Ñs se vean bien
    mysqli_set_charset($conexion, "utf8mb4");
}


/* ----------------------------------------------------------------------------
 * 3. OPERACIONES CRUD EN PHP
 * ----------------------------------------------------------------------------
 */

// --- A. LISTAR (SELECT) ---
// 1. Ejecutar consulta
$sql = "SELECT * FROM Estudiantes";
$resultado = mysqli_query($conexion, $sql);

// 2. Comprobar si hay filas y recorrerlas
if ($resultado && mysqli_num_rows($resultado) > 0) {
    while ($fila = mysqli_fetch_assoc($resultado)) {
        // Accedemos por el nombre de la columna en la BD
        // echo "Nombre: " . $fila['nombre']; 
    }
}

// --- B. INSERTAR (INSERT) ---
if (isset($_POST['guardar'])) {
    $nom = $_POST['nombre'];
    $ins = "INSERT INTO Estudiantes (nombre) VALUES ('$nom')";
    mysqli_query($conexion, $ins);
}

// --- C. BORRAR (DELETE) ---
// "DELETE FROM Estudiantes WHERE id_estudiante = 5";


/* ----------------------------------------------------------------------------
 * 4. SEGURIDAD: EVITAR INYECCIÓN SQL
 * ----------------------------------------------------------------------------
 * NUNCA metas variables de $_POST o $_GET directamente en un string SQL.
 * Usa mysqli_real_escape_string para "limpiar" los datos.
 */

$sucio = "O'Reilly; DROP TABLE Usuarios;"; // Ejemplo de hack
$limpio = mysqli_real_escape_string($conexion, $sucio);

// Ahora $limpio es seguro para usar en una consulta.


/* ----------------------------------------------------------------------------
 * 5. CONTROL DE SESIONES
 * ----------------------------------------------------------------------------
 * Permiten que el servidor "recuerde" al usuario en distintas páginas.
 */

// REGLA DE ORO: Debe ser lo primero del archivo
session_start();

// Guardar datos
$_SESSION['usuario_logueado'] = "Admin";

// Leer datos
if (isset($_SESSION['usuario_logueado'])) {
    // echo "Hola de nuevo!";
}

// Cerrar sesión
session_destroy(); 


/* ----------------------------------------------------------------------------
 * 6. DICCIONARIO DE FUNCIONES (RESUMEN)
 * ----------------------------------------------------------------------------
 * */
mysqli_connect()           // Abre conexión a MySQL.
mysqli_query()             // Envía una orden (SQL) a la BD.
mysqli_fetch_assoc()       // Convierte una fila de la BD en un array de PHP.
mysqli_num_rows()          // Cuenta cuántas filas devolvió el SELECT.
mysqli_real_escape_string()// Protege contra inyecciones SQL.
mysqli_close()             // Cierra la conexión (buena práctica).

isset()                    // Mira si una variable existe (muy usado en IFs).
empty()                    // Mira si una variable está vacía.
trim()                     // Quita espacios en blanco sobrantes.
header("Location: ...")    // Salto de página automático.

// Fin de los apuntes.
?>
