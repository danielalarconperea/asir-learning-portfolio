<?php
require_once '../includes/session_config.php';
require_once '../conexion.php';
?>

<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Catálogo Público - Biblioteca Escolar</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/estilos.css">
</head>

<body>
    <?php include '../includes/header.php'; ?>

    <div class="container">
        <h2>Catálogo de Libros</h2>

        <?php
        $consulta = "SELECT * FROM Libros WHERE disponible = 1";
        $resultado = mysqli_query($conn, $consulta);
        ?>

        <div class="table-container">
            <?php if (mysqli_num_rows($resultado) > 0): ?>
                <?php while ($fila = mysqli_fetch_assoc($resultado)): ?>
                    <div class="tarjeta">
                        <div class="portada">
                            <?php if (!empty($fila['portada']) && file_exists("../portadas/" . $fila['portada'])): ?>
                                <img src="../portadas/<?php echo $fila['portada']; ?>" alt="<?php echo $fila['titulo']; ?>">
                            <?php else: ?>
                                <div class="no-image">📖</div>
                            <?php endif; ?>
                        </div>
                        <div class="info">
                            <h3>
                                <?php echo htmlspecialchars($fila["titulo"]); ?>
                            </h3>
                            <p><strong>Autor:</strong>
                                <?php echo htmlspecialchars($fila["autor"]); ?>
                            </p>
                            <p><strong>Editorial:</strong>
                                <?php echo htmlspecialchars($fila["editorial"]); ?>
                            </p>
                        </div>
                    </div>
                <?php endwhile; ?>
            <?php else: ?>
                <p>No hay libros disponibles en este momento.</p>
            <?php endif; ?>
        </div>
    </div>
</body>

</html>