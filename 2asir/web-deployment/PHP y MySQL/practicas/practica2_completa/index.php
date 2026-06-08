<?php
require_once 'includes/session_config.php';
require_once 'conexion.php';

// Redirección si ya está logueado
if (isset($_SESSION['rol'])) {
    if ($_SESSION['rol'] == 'administrador') {
        header("Location: admin/index.php");
        exit();
    } elseif ($_SESSION['rol'] == 'profesor' || $_SESSION['rol'] == 'estudiante') {
        header("Location: usuario/index.php");
        exit();
    }
}

// Estadísticas para visitante
$conlib = 'SELECT COUNT(id_libro) FROM Libros WHERE disponible = 1';
$conest = 'SELECT COUNT(id_estudiante) FROM Estudiantes';
$conpre = 'SELECT COUNT(id_prestamo) FROM Prestamos WHERE devuelto = 0';

$lib = mysqli_fetch_array(mysqli_query($conn, $conlib))[0];
$est = mysqli_fetch_array(mysqli_query($conn, $conest))[0];
$pre = mysqli_fetch_array(mysqli_query($conn, $conpre))[0];
?>
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Biblioteca Escolar - Inicio</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="css/estilos.css">
    <style>
        .cta-buttons {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 30px;
        }

        .btn-cta {
            padding: 15px 30px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            transition: transform 0.3s;
        }

        .btn-cta:hover {
            transform: translateY(-3px);
        }

        .btn-primary {
            background-color: #3498db;
            color: white;
        }

        .btn-secondary {
            background-color: #2ecc71;
            color: white;
        }
    </style>
</head>

<body>
    <div class="container">
        <header>
            <h1>📚 Biblioteca Escolar</h1>
            <nav class="main-menu">
                <a href="publico/catalogo.php">Catálogo</a>
                <a href="auth/login.php">Acceder</a>
                <a href="auth/registro.php">Registrarse</a>
            </nav>
        </header>

        <main>
            <section class="welcome">
                <h2>Bienvenido a tu Biblioteca Digital</h2>
                <p>Gestiona reservas, consulta libros y mucho más.</p>

                <div class="cta-buttons">
                    <a href="auth/login.php" class="btn-cta btn-primary">Iniciar Sesión</a>
                    <a href="publico/catalogo.php" class="btn-cta btn-secondary">Ver Catálogo</a>
                </div>

                <div class="stats">
                    <div class="stat-card">
                        <h3>Libros disponibles</h3>
                        <p class="stat-number"><?php echo $lib; ?></p>
                    </div>
                    <div class="stat-card">
                        <h3>Usuarios activos</h3>
                        <p class="stat-number"><?php echo $est; ?></p>
                    </div>
                </div>
            </section>
        </main>

        <footer>
            <p>Sistema de Gestión de Biblioteca Escolar &copy; 2025</p>
        </footer>
    </div>
</body>

</html>