<?php

session_start();

// Verificar si hay una sesión activa
if (!isset($_SESSION['nombre'])) {
    echo 'No hay una sesión activa.';
} else {
    echo 'Sesión activa - ID de sesión: ' . session_id();
}
?>

<h2>Datos almacenados en la sesión:</h2>
<p><strong>nombre:</strong> <?php echo htmlspecialchars($_SESSION['nombre']); ?></p>
<p><strong>Apellido 1:</strong> <?php echo htmlspecialchars($_SESSION['apellido1']); ?></p>
<p><strong>Apellido 2:</strong> <?php echo htmlspecialchars($_SESSION['apellido2']); ?></p>

<br>
<a href="index.php">Volver al inicio</a>