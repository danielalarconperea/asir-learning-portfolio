<?php
function verificar_rol($roles_permitidos)
{
    // Asegurarse de que la sesión está iniciada
    if (session_status() === PHP_SESSION_NONE) {
        session_start();
    }

    if (!isset($_SESSION['user_id'])) {
        header("Location: ../auth/login.php");
        exit();
    }

    if (!in_array($_SESSION['rol'], $roles_permitidos)) {
        header("Location: ../error/403.php");
        exit();
    }
}
?>