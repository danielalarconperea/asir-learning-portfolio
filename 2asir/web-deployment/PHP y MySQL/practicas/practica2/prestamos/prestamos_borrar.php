<?php
include '../conexion.php';

if ($conexion) {
    // La conexión ya establece el charset en conexion.php

    if (isset($_POST['id_a_borrar'])) {
        $id_a_borrar = intval($_POST['id_a_borrar']);

        // Antes de borrar el préstamo, obtenemos el ID del libro para restaurar su disponibilidad
        $res_loan = mysqli_query($conexion, "SELECT id_libro FROM Prestamos WHERE id_prestamo = $id_a_borrar");
        if ($loan_data = mysqli_fetch_assoc($res_loan)) {
            $id_lib = $loan_data['id_libro'];

            $consulta = "DELETE FROM Prestamos WHERE id_prestamo = $id_a_borrar";
            if (mysqli_query($conexion, $consulta)) {
                // Al eliminar un registro de préstamo, marcamos el libro como disponible de nuevo
                mysqli_query($conexion, "UPDATE Libros SET disponible = 1 WHERE id_libro = $id_lib");
                $msg_exito = "Préstamo eliminado correctamente.";
            } else {
                $msg_error = "Error al eliminar: " . mysqli_error($conexion);
            }
        }
    }
}

if ($conexion) {
    if (isset($_POST['buscar']) && !empty(trim($_POST['query']))) {
        $busqueda = mysqli_real_escape_string($conexion, trim(strtolower($_POST['query'])));
        $consulta = "SELECT P.id_prestamo, L.titulo AS titulo_libro, E.nombre, E.apellidos, P.fecha_prestamo 
                     FROM Prestamos P
                     JOIN Libros L ON P.id_libro = L.id_libro
                     JOIN Estudiantes E ON P.id_estudiante = E.id_estudiante
                     WHERE LOWER(L.titulo) LIKE '%$busqueda%' 
                        OR LOWER(E.nombre) LIKE '%$busqueda%' 
                        OR LOWER(E.apellidos) LIKE '%$busqueda%'";
    } else {
        $consulta = "SELECT P.id_prestamo, L.titulo AS titulo_libro, E.nombre, E.apellidos, P.fecha_prestamo 
                     FROM Prestamos P
                     JOIN Libros L ON P.id_libro = L.id_libro
                     JOIN Estudiantes E ON P.id_estudiante = E.id_estudiante";
    }
    $resultado = mysqli_query($conexion, $consulta);
}
?>

<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biblioteca - Borrar Préstamo</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/estilos.css">
</head>

<body>
    <div class="container">
        <header>
            <h1>📅 Gestión de Préstamos</h1>
            <nav class="main-menu">
                <a href="../index.php">Inicio</a>
                <a href="../libros/libros.html">Libros</a>
                <a href="../estudiantes/estudiantes.html">Estudiantes</a>
                <a href="../prestamos/prestamos.html">Préstamos</a>
            </nav>
        </header>

        <main>
            <nav class="submenu">
                <a href="prestamos.html">Inicio</a>
                <a href="prestamos_agregar.php">Añadir</a>
                <a href="prestamos_listar.php">Listar</a>
                <a href="prestamos_buscar.php">Buscar</a>
                <a href="prestamos_modificar.php">Modificar</a>
                <a href="prestamos_borrar.php">Borrar</a>
            </nav>

            <section class="content">
                <h2>Borrar Préstamos</h2>
                <form action="prestamos_borrar.php" method="post" style="margin-bottom: 30px;">
                    <div class="form-group">
                        <label for="query">Buscar:</label>
                        <input type="text" id="query" name="query" placeholder="Libro o estudiante...">
                    </div>
                    <button type="submit" name="buscar">Buscar</button>
                </form>
                <?php if (isset($msg_exito)) { ?>
                    <p class="success-message">
                        <?php echo $msg_exito; ?>
                    </p>
                <?php } ?>
                <?php if (isset($msg_error)) { ?>
                    <p class="error-message">
                        <?php echo $msg_error; ?>
                    </p>
                <?php } ?>

                <div class="table-container">
                    <?php if (isset($resultado) && mysqli_num_rows($resultado) > 0) { ?>
                        <?php while ($fila = mysqli_fetch_assoc($resultado)) { ?>
                            <div class="tarjeta loan-card">
                                <div class="info">
                                    <h3>
                                        <?php echo $fila["titulo_libro"]; ?>
                                    </h3>
                                    <p><strong>Estudiante:</strong>
                                        <?php echo $fila["nombre"] . " " . $fila["apellidos"]; ?>
                                    </p>
                                    <p><strong>Fecha:</strong>
                                        <?php echo date("d/m/Y", strtotime($fila["fecha_prestamo"])); ?>
                                    </p>
                                </div>
                                <form action="prestamos_borrar.php" method="post" style="margin-top: 15px;">
                                    <input type="hidden" name="id_a_borrar" value="<?php echo $fila['id_prestamo']; ?>">
                                    <button type="submit" class="btn-borrar">Eliminar</button>
                                </form>
                            </div>
                        <?php } ?>
                    <?php } else { ?>
                        <p>No hay préstamos registrados.</p>
                    <?php } ?>
                </div>
            </section>
        </main>

        <footer>
            <p>Sistema de Gestión de Biblioteca Escolar &copy; 2025</p>
        </footer>
    </div>
</body>

</html>