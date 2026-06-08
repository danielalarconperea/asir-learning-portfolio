<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?>
<header>
    <h1>📚 Biblioteca Escolar</h1>
    <nav class="main-menu">
        <?php if (isset($_SESSION['rol'])): ?>

            <!-- Menú Administrador -->
            <?php if ($_SESSION['rol'] == 'administrador'): ?>
                <a href="../admin/index.php">Dashboard</a>
                <a href="../libros/libros_listar.php">Libros</a>
                <a href="../admin/usuarios.php">Usuarios</a>
                <a href="../admin/logs_acceso.php">Logs</a>
            <?php endif; ?>

            <!-- Menú Profesor/Estudiante -->
            <?php if ($_SESSION['rol'] == 'profesor' || $_SESSION['rol'] == 'estudiante'): ?>
                <a href="../usuario/index.php">Mi cuenta</a>
                <a href="../usuario/reservar.php">Reservar</a>
                <a href="../usuario/mis_prestamos.php">Mis Préstamos</a>
            <?php endif; ?>

            <!-- Común para todos registrados -->
            <a href="../publico/catalogo.php">Catálogo</a>
            <div class="user-info" style="display:inline-block; margin-left: 20px; color: #ecf0f1;">
                Hola, <strong>
                    <?php echo htmlspecialchars($_SESSION['nombre'] ?? 'Usuario'); ?>
                </strong>
                (
                <?php echo ucfirst($_SESSION['rol']); ?>)
            </div>
            <a href="../auth/logout.php" style="background-color: #e74c3c;">Salir</a>
        <?php else: ?>
            <!-- Menú Público -->
            <a href="../index.php">Inicio</a>
            <a href="../publico/catalogo.php">Catálogo</a>
            <a href="../auth/login.php">Acceder</a>
            <a href="../auth/registro.php">Registrarse</a>
        <?php endif; ?>
    </nav>
</header>