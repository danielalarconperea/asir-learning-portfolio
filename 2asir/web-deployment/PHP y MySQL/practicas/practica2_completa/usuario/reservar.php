<?php
require_once '../includes/session_config.php';
require_once '../includes/auth_check.php';
require_once '../conexion.php';

verificar_autenticacion();
$id_user = $_SESSION['user_id'];
$msg = '';

// Procesar Reserva
if (isset($_POST['reservar_libro'])) {
    $id_libro = mysqli_real_escape_string($conn, $_POST['id_libro']);

    // Verificar que sigue disponible
    $check = mysqli_query($conn, "SELECT disponible FROM Libros WHERE id_libro = '$id_libro'");
    $book = mysqli_fetch_assoc($check);

    if ($book && $book['disponible'] == 1) {
        $fecha = date('Y-m-d H:i:s');
        $insert = "INSERT INTO Prestamos (id_estudiante, id_libro, fecha_prestamo) VALUES ('$id_user', '$id_libro', '$fecha')";

        if (mysqli_query($conn, $insert)) {
            // Marcar como no disponible
            mysqli_query($conn, "UPDATE Libros SET disponible = 0 WHERE id_libro = '$id_libro'");
            $msg = "¡Libro reservado con éxito! Pasa por recepción a recogerlo.";
        } else {
            $msg = "Error al reservar: " . mysqli_error($conn);
        }
    } else {
        $msg = "Lo sentimos, este libro ya no está disponible.";
    }
}

// Listar disponibles
$consulta = "SELECT * FROM Libros WHERE disponible = 1";
$resultado = mysqli_query($conn, $consulta);
?>
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Reservar Libros - Biblioteca</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/estilos.css">
</head>

<body>
    <?php include '../includes/header.php'; ?>
    <div class="container">
        <h2>Reservar Libros</h2>

        <?php if ($msg): ?>
            <div class="success-message">
                <?php echo $msg; ?>
            </div>
        <?php endif; ?>

        <div class="table-container">
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
                        <p>
                            <?php echo htmlspecialchars($fila["autor"]); ?>
                        </p>
                        <form method="POST" action="reservar.php">
                            <input type="hidden" name="id_libro" value="<?php echo $fila['id_libro']; ?>">
                            <button type="submit" name="reservar_libro" class="btn-editar"
                                style="background: #27ae60; border:none; width:100%; margin-top:10px; cursor:pointer;">Reservar
                                Ahora</button>
                        </form>
                    </div>
                </div>
            <?php endwhile; ?>
        </div>
    </div>
</body>

</html>