<?php
// Configuración de la base de datos
$host = "localhost";
$user = "root";
$pass = "asdf";
$db = "biblioteca_escolar";

// Crear conexión
$conn = mysqli_connect($host, $user, $pass, $db);

// Verificar conexión
if (!$conn) {
    die("Error de conexión: " . mysqli_connect_error());
}

// Configurar charset a utf8mb4
mysqli_set_charset($conn, "utf8mb4");
?>
