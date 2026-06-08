<?php
require_once '../conexion.php';
$conexion = $conn;

if (!$conexion) {
    $error_detalle = "Error de conexión: " . mysqli_connect_error();
} else {
    mysqli_set_charset($conexion, "utf8mb4");
    if (isset($_POST['buscar']) && !empty(trim($_POST['titulo_buscar']))) {
        $busqueda = mysqli_real_escape_string($conexion, trim(strtolower($_POST['titulo_buscar'])));
        $consulta = "SELECT * FROM Libros WHERE LOWER(titulo) LIKE '%$busqueda%' OR LOWER(autor) LIKE '%$busqueda%' OR LOWER(editorial) LIKE '%$busqueda%' OR LOWER(isbn) LIKE '%$busqueda%' OR LOWER(anio_publicacion) LIKE '%$busqueda%'";
        $resultado = mysqli_query($conexion, $consulta);
    }
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
                <a href="../index.php">Inicio</a>
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
                <h2>Buscar Libros</h2>
                <form action="libros_buscar.php" method="post" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="titulo_buscar">Buscar:</label>
                        <input type="text" id="titulo_buscar" name="titulo_buscar"
                            placeholder="Ej: El Quijote, Miguel de Cervantes, 1605"
                            value="<?php echo isset($_POST['titulo_buscar']) ? $_POST['titulo_buscar'] : ''; ?>">
                    </div>
                    <button type="submit" name="buscar">Buscar</button>
                </form>

                <?php if (isset($resultado)) { ?>
                    <div class="table-container" style="margin-top: 30px;">
                        <?php if (mysqli_num_rows($resultado) > 0) { ?>
                            <?php while ($fila = mysqli_fetch_assoc($resultado)) { ?>
                                <div class="tarjeta">
                                    <div class="portada">
                                        <?php if (!empty($fila['portada']) && file_exists("../portadas/" . $fila['portada'])) { ?>
                                            <img src="../portadas/<?php echo $fila['portada']; ?>"
                                                alt="Portada de <?php echo $fila['titulo']; ?>">
                                        <?php } else { ?>
                                            <div class="no-image" style="font-size: 4rem;"></div>
                                        <?php } ?>
                                    </div>
                                    <div class="info">
                                        <h3><?php echo $fila["titulo"]; ?></h3>
                                        <p><strong>Autor:</strong> <?php echo $fila["autor"]; ?></p>
                                        <p><strong>Editorial:</strong> <?php echo $fila["editorial"]; ?></p>
                                        <p><strong>ISBN:</strong> <?php echo $fila["isbn"]; ?></p>
                                        <p><strong>Año:</strong> <?php echo $fila["anio_publicacion"]; ?></p>
                                        <p><strong>Estado:</strong>
                                            <?php echo $fila["disponible"] ? 'Disponible' : 'No disponible'; ?></p>
                                    </div>
                                </div>
                            <?php } ?>
                        <?php } else { ?>
                            <p style="text-align: center; color: #e06c75;">No se encontraron resultados para la búsqueda.</p>
                        <?php } ?>
                    </div>
                <?php } ?>
            </section>
        </main>

        <footer>
            <p>Sistema de Gestión de Biblioteca Escolar &copy; 2025</p>
        </footer>
    </div>
</body>

</html>