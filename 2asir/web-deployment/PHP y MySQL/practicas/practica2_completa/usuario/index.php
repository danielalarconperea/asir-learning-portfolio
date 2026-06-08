<?php
require_once '../includes/session_config.php';
require_once '../includes/auth_check.php';

verificar_autenticacion();
?>

<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Mi Panel - Biblioteca Escolar</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/estilos.css">
</head>

<body>
    <?php include '../includes/header.php'; ?>

    <div class="container">
        <h2>Mi Panel de Usuario</h2>
        <p>Bienvenido de nuevo, <strong>
                <?php echo htmlspecialchars($_SESSION['nombre']); ?>
            </strong>.</p>

        <section class="content" style="margin-top: 30px;">
            <div class="table-container">
                <div class="tarjeta" style="padding: 20px; text-align: center;">
                    <h3>📖 Catálogo</h3>
                    <p>Busca y reserva libros.</p>
                    <a href="../publico/catalogo.php" class="btn-editar"
                        style="margin-top: 10px; display:inline-block;">Ver Catálogo</a>
                </div>

                <div class="tarjeta" style="padding: 20px; text-align: center;">
                    <h3>📅 Mis Préstamos</h3>
                    <p>Consulta tus libros prestados.</p>
                    <a href="mis_prestamos.php" class="btn-editar" style="margin-top: 10px; display:inline-block;">Ver
                        Préstamos</a>
                </div>

                <div class="tarjeta" style="padding: 20px; text-align: center;">
                    <h3>👤 Mi Perfil</h3>
                    <p>Actualiza tus datos.</p>
                    <a href="mi_perfil.php" class="btn-editar" style="margin-top: 10px; display:inline-block;">Editar
                        Perfil</a>
                </div>
            </div>
        </section>
    </div>
</body>

</html>