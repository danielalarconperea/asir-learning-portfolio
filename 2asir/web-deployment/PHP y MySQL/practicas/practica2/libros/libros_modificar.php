<?php
include '../conexion.php';

if ($conexion) {
    // La conexión ya establece el charset en conexion.php


    if (isset($_POST["modificar"])) {
        $id_libro = mysqli_real_escape_string($conexion, $_POST['id_libro']);
        $titulo = mysqli_real_escape_string($conexion, trim($_POST['titulo']));
        $autor = mysqli_real_escape_string($conexion, trim($_POST['autor']));
        $editorial = mysqli_real_escape_string($conexion, trim($_POST['editorial']));
        $isbn = mysqli_real_escape_string($conexion, trim($_POST['isbn']));
        $anio_publicacion = mysqli_real_escape_string($conexion, trim($_POST['anio_publicacion']));
        $disponible = mysqli_real_escape_string($conexion, $_POST['disponible']);

        $consulta_upd = "UPDATE Libros SET titulo = '$titulo', autor = '$autor', editorial = '$editorial', isbn = '$isbn', anio_publicacion = '$anio_publicacion', disponible = $disponible WHERE id_libro = '$id_libro'";
        if (mysqli_query($conexion, $consulta_upd)) {
            $msg_exito = "Libro actualizado correctamente.";
        } else {
            $msg_error = "Error al actualizar: " . mysqli_error($conexion);
        }
    }

    if (isset($_POST['buscar'])) {
        $busqueda = mysqli_real_escape_string($conexion, trim(strtolower($_POST['titulo_buscar'])));
        $consulta = "SELECT * FROM Libros WHERE LOWER(titulo) LIKE '%$busqueda%' OR LOWER(autor) LIKE '%$busqueda%' OR LOWER(editorial) LIKE '%$busqueda%' OR LOWER(isbn) LIKE '%$busqueda%' OR LOWER(anio_publicacion) LIKE '%$busqueda%'";
        $resultado_busqueda = mysqli_query($conexion, $consulta);
    } else {
        $consulta = "SELECT * FROM Libros";
        $resultado_busqueda = mysqli_query($conexion, $consulta);
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
                <h2>Modificar Libros</h2>
                <form action="libros_modificar.php" method="post" enctype="multipart/form-data">
                    <div class="form-group">
                        <label for="titulo_buscar">Buscar:</label>
                        <input type="text" id="titulo_buscar" name="titulo_buscar"
                            placeholder="Ej: El Quijote, Miguel de Cervantes, 1605" required>
                    </div>
                    <button type="submit" name="buscar">Buscar</button>
                </form>

                <?php if (isset($msg_exito)) { ?>
                    <p class="success-message"><?php echo $msg_exito; ?></p>
                <?php } ?>

                <?php if (isset($msg_error)) { ?>
                    <p class="error-message"><?php echo $msg_error; ?></p>
                <?php } ?>

                <?php if (isset($resultado_busqueda)) { ?>
                    <div class="table-container" style="margin-top: 30px;">
                        <?php if (mysqli_num_rows($resultado_busqueda) > 0) { ?>
                            <?php while ($fila = mysqli_fetch_assoc($resultado_busqueda)) { ?>
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
                                        <form action="libros_modificar.php" method="post">
                                            <p><strong>ID Libro:</strong> <?php echo $fila["id_libro"]; ?>
                                            </p>
                                            <input type="hidden" name="id_libro" value="<?php echo $fila['id_libro']; ?>">
                                            <h3><input type="text" class="input-modificar" name="titulo"
                                                    value="<?php echo $fila["titulo"]; ?>"></h3>
                                            <p><strong>Autor:</strong>
                                                <input type="text" class="input-modificar" name="autor"
                                                    value="<?php echo $fila["autor"]; ?>">
                                            </p>
                                            <p><strong>Editorial:</strong>
                                                <input type="text" class="input-modificar" name="editorial"
                                                    value="<?php echo $fila["editorial"]; ?>">
                                            </p>
                                            <p><strong>ISBN:</strong>
                                                <input type="text" class="input-modificar" name="isbn" pattern="^(97[89])-\d{1,10}$"
                                                    title="Por favor, introduce un ISBN válido (Formato: 978-0000000000)"
                                                    value="<?php echo $fila["isbn"]; ?>">
                                            </p>
                                            <p><strong>Año:</strong>
                                                <input type="number" class="input-modificar" name="anio_publicacion"
                                                    value="<?php echo $fila["anio_publicacion"]; ?>">
                                            </p>
                                            <p><strong>Estado:</strong>
                                                <select name="disponible" class="input-modificar">
                                                    <option value="1" <?php echo $fila["disponible"] ? 'selected' : ''; ?>>
                                                        Disponible</option>
                                                    <option value="0" <?php echo !$fila["disponible"] ? 'selected' : ''; ?>>No
                                                        disponible</option>
                                                </select>
                                            </p>
                                            <button type="submit" class="btn-modificar" name="modificar">Modificar</button>
                                        </form>
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