<?php
require_once 'session_config.php';

function verificar_autenticacion()
{
    if (!isset($_SESSION['user_id'])) {
        header("Location: ../auth/login.php");
        exit();
    }
}
?>