<?php
// database_config.php
session_start();

// Configuración de la base de datos
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', 'rootroot');
define('DB_NAME', 'biblioteca_escolar');

// Configuración de seguridad
define('MAX_LOGIN_ATTEMPTS', 5);
define('LOCKOUT_TIME', 900); // 15 minutos en segundos

// Función para conectar a la base de datos
function conectarBD() {
    $conexion = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);
    
    if ($conexion->connect_error) {
        die("Error de conexión: " . $conexion->connect_error);
    }
    
    $conexion->set_charset("utf8");
    return $conexion;
}

// Función para verificar si el usuario está logueado
function estaLogueado() {
    return isset($_SESSION['id_usuario']) && isset($_SESSION['rol']);
}

// Función para verificar rol específico
function tieneRol($rolRequerido) {
    return estaLogueado() && $_SESSION['rol'] === $rolRequerido;
}

// Función para redirigir si no tiene el rol requerido
function requerirRol($rolRequerido) {
    if (!tieneRol($rolRequerido)) {
        header('Location: index.php');
        exit();
    }
}

// Función para sanear datos de entrada
function sanear($dato) {
    global $conexion;
    $dato = trim($dato);
    $dato = stripslashes($dato);
    $dato = htmlspecialchars($dato);
    return $conexion->real_escape_string($dato);
}
?>