<?php
// header.php - Incluir en todas las páginas que requieran sesión
session_start();
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biblioteca Escolar</title>
    <link rel="stylesheet" href="css/estilos.css">
    <link rel="stylesheet" href="css/auth.css">
</head>
<body>
    <div class="container">
        <header>
            <div class="header-top">
                <h1>📚 Biblioteca Escolar</h1>
                <div class="user-info">
                    <?php if (isset($_SESSION['nombre'])): ?>
                        <span>Bienvenido, <?php echo htmlspecialchars($_SESSION['nombre']); ?></span>
                        <a href="logout.php" class="btn-logout">Cerrar Sesión</a>
                    <?php else: ?>
                        <a href="login.php" class="btn-login">Iniciar Sesión</a>
                        <a href="registro.php" class="btn-register">Registrarse</a>
                    <?php endif; ?>
                </div>
            </div>
            
            <nav class="main-menu">
                <a href="index.php">Inicio</a>
                <a href="catalogo.php">Catálogo</a>
                
                <?php if (isset($_SESSION['id_usuario'])): ?>
                    <?php if ($_SESSION['rol'] === 'administrador'): ?>
                        <a href="admin_libros.php">Libros (Admin)</a>
                        <a href="admin_usuarios.php">Usuarios (Admin)</a>
                        <a href="admin_prestamos.php">Préstamos (Admin)</a>
                    <?php else: ?>
                        <a href="mis_prestamos.php">Mis Préstamos</a>
                        <a href="reservar.php">Reservar Libro</a>
                    <?php endif; ?>
                    
                    <?php if ($_SESSION['rol'] === 'profesor'): ?>
                        <a href="estudiantes_grupo.php">Mis Estudiantes</a>
                    <?php endif; ?>
                <?php endif; ?>
                
                <a href="contacto.php">Contacto</a>
            </nav>
        </header>
        
        <main>