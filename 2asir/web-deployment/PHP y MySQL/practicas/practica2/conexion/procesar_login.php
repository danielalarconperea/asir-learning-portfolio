<?php
// procesar_login.php - ESQUELETO PARA COMPLETAR
require_once 'database_config.php';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = sanear($_POST['email']);
    $password = $_POST['password'];
    
    // TODO: Comprobar intentos fallidos recientes
    
    // TODO: Consultar usuario en base de datos
    
    // TODO: Verificar contraseña (usar password_verify)
    
    // TODO: Si credenciales correctas, iniciar sesión
    
    // TODO: Registrar intento exitoso
    
    // TODO: Redirigir según rol
    
    // TODO: Si credenciales incorrectas, registrar intento fallido
    
    // TODO: Redirigir con error
}
?>