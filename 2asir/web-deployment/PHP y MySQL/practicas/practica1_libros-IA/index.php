<?php
$user = "root";
$pass = "asdf";
$dbname = "biblioteca_escolar";

$conn = mysqli_connect("localhost", $user, $pass, $dbname);

if (!$conn) {
    die("Connection failed: " . mysqli_connect_error());
} else {
    mysqli_set_charset($conn, "utf8mb4");

    $conlib = 'SELECT COUNT(id_libro) FROM libros';
    $conest = 'SELECT COUNT(id_estudiante) FROM estudiantes';
    $conpre = 'SELECT COUNT(id_prestamo) FROM prestamos';

    $resultlib = mysqli_query($conn, $conlib);
    $resultest = mysqli_query($conn, $conest);
    $resultpre = mysqli_query($conn, $conpre);

    $lib = mysqli_fetch_array($resultlib)[0];
    $est = mysqli_fetch_array($resultest)[0];
    $pre = mysqli_fetch_array($resultpre)[0];
}
?>
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biblioteca Escolar - Inicio</title>
    <link rel="icon" type="image/svg+xml"
        href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%231abc9c'><path d='M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 9H9V9h10v2zm-4 4H9v-2h6v2zm4-8H9V5h10v2z'/></svg>">
    <link rel="stylesheet" href="css/estilos.css">
</head>

<body>
    <div class="container">
        <header>
            <h1>📚 Biblioteca Escolar</h1>
            <nav class="main-menu">
                <a href="libros/libros.html">Libros</a>
                <a href="estudiantes/estudiantes.html">Estudiantes</a>
                <a href="prestamos/prestamos.html">Préstamos</a>
            </nav>
        </header>

        <main>
            <section class="welcome">
                <h2>Bienvenido al Sistema de Gestión de Biblioteca</h2>
                <p>Seleccione una categoría del menú superior para comenzar.</p>

                <div class="stats">
                    <div class="stat-card">
                        <h3>Libros disponibles</h3>
                        <p class="stat-number">
                            <?php echo $lib; ?>
                        </p>
                    </div>
                    <div class="stat-card">
                        <h3>Estudiantes registrados</h3>
                        <p class="stat-number">
                            <?php echo $est; ?>
                        </p>
                    </div>
                    <div class="stat-card">
                        <h3>Préstamos activos</h3>
                        <p class="stat-number">
                            <?php echo $pre; ?>
                        </p>
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
