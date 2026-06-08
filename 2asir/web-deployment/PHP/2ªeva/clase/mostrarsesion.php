<?php

session_start();

// Verificar si hay una sesión activa
if (!isset($_SESSION['usuario'])) {
    echo 'No hay una sesión activa.';
} else {
    echo 'Sesión activa - ID de sesión: ' . session_id();
}
?>

<h2>Datos almacenados en la sesión:</h2>
<p><strong>Usuario:</strong> <?php echo htmlspecialchars($_SESSION['usuario']); ?></p>
<p><strong>Email:</strong> <?php echo htmlspecialchars($_SESSION['email']); ?></p>
<p><strong>Último acceso:</strong> <?php echo $_SESSION['ultimo_acceso']; ?></p>