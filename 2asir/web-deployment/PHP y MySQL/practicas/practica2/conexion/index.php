<?php
// index.php
require_once 'database_config.php';

// Conectar a la base de datos para estadísticas
$conexion = conectarBD();

// Obtener estadísticas
$stats = [
    'total_libros' => 0,
    'libros_disponibles' => 0,
    'usuarios_registrados' => 0,
    'prestamos_activos' => 0
];

// Consultas para estadísticas (ejemplo - completar según estructura real)
// $result = $conexion->query("SELECT COUNT(*) as total FROM Libros");
// $stats['total_libros'] = $result->fetch_assoc()['total'];
// ... otras consultas

$conexion->close();
?>

<?php include 'header.php'; ?>

<section class="welcome">
    <h2>Bienvenido al Sistema de Gestión de Biblioteca</h2>
    
    <?php if (estaLogueado()): ?>
        <div class="welcome-user">
            <p>Hola <strong><?php echo htmlspecialchars($_SESSION['nombre']); ?></strong>, 
            bienvenido de nuevo.</p>
            
            <?php if (tieneRol('administrador')): ?>
                <div class="admin-alert">
                    <p>⚠️ Tienes permisos de administrador. Accede al panel de administración desde el menú.</p>
                </div>
            <?php endif; ?>
        </div>
    <?php else: ?>
        <p>Consulta nuestro catálogo o <a href="registro.php">regístrate</a> para reservar libros.</p>
    <?php endif; ?>
    
    <div class="stats">
        <div class="stat-card">
            <h3>Libros disponibles</h3>
            <p class="stat-number"><?php echo $stats['libros_disponibles']; ?></p>
        </div>
        <div class="stat-card">
            <h3>Usuarios registrados</h3>
            <p class="stat-number"><?php echo $stats['usuarios_registrados']; ?></p>
        </div>
        <div class="stat-card">
            <h3>Préstamos activos</h3>
            <p class="stat-number"><?php echo $stats['prestamos_activos']; ?></p>
        </div>
    </div>
    
    <div class="quick-actions">
        <a href="catalogo.php" class="btn-action">
            <span>🔍</span>
            <span>Consultar Catálogo</span>
        </a>
        
        <?php if (estaLogueado() && !tieneRol('administrador')): ?>
            <a href="reservar.php" class="btn-action">
                <span>📖</span>
                <span>Reservar Libro</span>
            </a>
        <?php endif; ?>
        
        <?php if (tieneRol('administrador')): ?>
            <a href="admin_dashboard.php" class="btn-action admin">
                <span>⚙️</span>
                <span>Panel de Administración</span>
            </a>
        <?php endif; ?>
    </div>
</section>

<?php include 'footer.php'; ?>