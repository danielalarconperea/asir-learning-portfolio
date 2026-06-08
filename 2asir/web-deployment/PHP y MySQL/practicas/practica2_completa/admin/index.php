<?php
require_once '../includes/session_config.php';
require_once '../includes/role_check.php';

// Solo permitido para administradores
verificar_rol(['administrador']);
?>

<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Panel de Administración - Biblioteca Escolar</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/estilos.css">
</head>

<body>
    <?php include '../includes/header.php'; ?>

    <div class="container">
        <h2 style="color: #2c3e50; border-bottom: 2px solid #e74c3c; padding-bottom: 10px;">Panel de Administración</h2>
        <p>Bienvenido, <strong>
                <?php echo htmlspecialchars($_SESSION['nombre']); ?>
            </strong>.</p>

        <div class="submenu" style="justify-content: flex-start; margin-top: 20px;">
            <a href="../libros/libros_listar.php" style="background-color: #3498db;">Gestionar Libros</a>
            <a href="usuarios.php" style="background-color: #9b59b6;">Gestionar Usuarios</a>
            <a href="../prestamos/prestamos_listar.php" style="background-color: #f39c12;">Gestionar Préstamos</a>
            <a href="logs_acceso.php" style="background-color: #34495e;">Ver Logs de Acceso</a>
        </div>

        <section class="content">
            <h3>Resumen del Sistema</h3>
            <div class="stats">
                <!-- Aquí podrías incluir contadores similares a index.php pero más detallados -->
                <div class="stat-card">
                    <h3>Sesión Activa</h3>
                    <p>IP:
                        <?php echo $_SERVER['REMOTE_ADDR']; ?>
                    </p>
                </div>
            </div>
        </section>
    </div>
</body>

</html>