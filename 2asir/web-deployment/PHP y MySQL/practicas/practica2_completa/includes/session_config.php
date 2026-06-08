<?php
// Configuración segura de sesiones
ini_set('session.cookie_httponly', 1);
ini_set('session.use_strict_mode', 1);

session_set_cookie_params([
    'lifetime' => 1800,
    'path' => '/',
    'httponly' => true,
    'samesite' => 'Strict'
]);

session_start();

// Regenerar ID de sesión periódicamente para prevenir secuestro
if (!isset($_SESSION['last_regeneration'])) {
    session_regenerate_id(true);
    $_SESSION['last_regeneration'] = time();
} else {
    $interval = 60 * 30; // 30 minutos
    if (time() - $_SESSION['last_regeneration'] >= $interval) {
        session_regenerate_id(true);
        $_SESSION['last_regeneration'] = time();
    }
}

// Timeout de inactividad
$timeout = 1800; // 30 minutos
if (isset($_SESSION['ultimo_acceso']) && (time() - $_SESSION['ultimo_acceso'] > $timeout)) {
    session_unset();
    session_destroy();
    if (basename($_SERVER['PHP_SELF']) != 'login.php') {
        header("Location: ../auth/login.php?timeout=1");
        exit();
    }
}
$_SESSION['ultimo_acceso'] = time();
?>