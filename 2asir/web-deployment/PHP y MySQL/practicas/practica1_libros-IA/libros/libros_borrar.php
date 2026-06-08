<?php
$host = "localhost";
$user = "root";
$pass = "asdf";
$db = "biblioteca_escolar";

// Intentar conectar con supresión de errores para manejo personalizado
$conexion = @mysqli_connect($host, $user, $pass, $db);

if ($conexion) {
    mysqli_set_charset($conexion, "utf8mb4");
    if (isset($_POST['id_a_borrar'])) {
        $id_a_borrar = $_POST['id_a_borrar'];
        $consulta = "DELETE FROM Libros WHERE id_libro = $id_a_borrar";
        mysqli_query($conexion, $consulta);
    }
}

if (!$conexion) {
    $error_msg = mysqli_connect_error();
    if (strpos($error_msg, "undefined function") !== false || !function_exists('mysqli_connect')) {
        $error_detalle = "La extensión 'mysqli' no está habilitada en tu PHP. Revisa tu archivo php.ini.";
    } else {
        $error_detalle = "Error de conexión: " . $error_msg;
    }
} else {
    $consulta = "SELECT * FROM Libros";
    $resultado = mysqli_query($conexion, $consulta);
}


?>

<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biblioteca - Gestión de Libros</title>
    <link rel="icon" type="image/svg+xml"
        href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='%231abc9c'><path d='M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 9H9V9h10v2zm-4 4H9v-2h6v2zm4-8H9V5h10v2z'/></svg>">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/estilos.css">
</head>

<body>
    <div class="container">
        <header>
            <h1>📖 Gestión de Libros</h1>
            <nav class="main-menu">
                <a href="../index.html">Inicio</a>
                <a href="../libros/libros.html">Libros</a>
                <a href="../estudiantes/estudiantes.html">Estudiantes</a>
                <a href="../prestamos/prestamos.html">Préstamos</a>
            </nav>
        </header>

        <main>
            <nav class="submenu">
                <a href="libros.html">Inicio</a>
                <a href="libros_agregar.php">Añadir</a>
                <a href="libros_listar.php">Listar</a>
                <a href="libros_buscar.php">Buscar</a>
                <a href="libros_modificar.php">Modificar</a>
                <a href="libros_borrar.php">Borrar</a>
            </nav>

            <section class="content">
                <h2>Borrado de libros</h2>
                <div class="table-container">
                    <?php if (isset($error_detalle)): ?>
                        <div class="error-message"
                            style="background: rgba(224, 108, 117, 0.1); color: #e06c75; padding: 20px; border-radius: 8px; border: 1px solid #e06c75; margin-bottom: 20px; width: 100%;">
                            <strong style="display: block; margin-bottom: 10px;">⚠️ Error de Sistema</strong>
                            <?php echo $error_detalle; ?>
                            <p style="margin-top: 15px; font-size: 0.9em; color: #abb2bf;">
                                💡 <strong>Sugerencia:</strong> Si usas PHP de <code>C:\Program Files\PHP</code>,
                                renombra <code>php.ini-development</code> a <code>php.ini</code> y activa
                                <code>extension=mysqli</code>.
                            </p>
                        </div>
                    <?php elseif (isset($resultado) && mysqli_num_rows($resultado) > 0): ?>
                        <?php while ($fila = mysqli_fetch_assoc($resultado)): ?>
                            <div class="tarjeta">
                                <div class="portada">
                                    <?php if (!empty($fila['portada']) && file_exists("../portadas/" . $fila['portada'])): ?>
                                        <img src="../portadas/<?php echo $fila['portada']; ?>"
                                            alt="Portada de <?php echo $fila['titulo']; ?>">
                                    <?php else: ?>
                                        <div class="no-image" style="font-size: 4rem;">📚</div>
                                    <?php endif; ?>
                                </div>
                                <div class="info">
                                    <h3><?php echo $fila["titulo"]; ?></h3>
                                    <p><strong>Autor:</strong> <?php echo $fila["autor"]; ?></p>
                                    <p><strong>Editorial:</strong> <?php echo $fila["editorial"]; ?></p>
                                    <p><strong>ISBN:</strong> <?php echo $fila["isbn"]; ?></p>
                                    <p><strong>Año:</strong> <?php echo $fila["anio_publicacion"]; ?></p>
                                    <p><strong>Estado:</strong>
                                        <?php echo $fila["disponible"] ? '✅ Disponible' : '❌ No disponible'; ?></p>
                                </div>
                                <form action="libros_borrar.php" method="post">
                                    <input type="hidden" name="id_a_borrar" value="<?php echo $fila['id_libro']; ?>">
                                    <button type="submit" class="btn-borrar">Borrar</button>
                                </form>
                            </div>
                        <?php endwhile; ?>
                    <?php else: ?>
                        <p>No hay libros registrados en la biblioteca.</p>
                    <?php endif; ?>
                </div>
            </section>
        </main>

        <footer>
            <p>Sistema de Gestión de Biblioteca Escolar &copy; 2025</p>
        </footer>
    </div>
</body>

</html>
