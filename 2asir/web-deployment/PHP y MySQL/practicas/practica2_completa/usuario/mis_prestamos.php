<?php
require_once '../includes/session_config.php';
require_once '../includes/auth_check.php';
require_once '../conexion.php';

verificar_autenticacion();
$id_user = $_SESSION['user_id'];

$consulta = "SELECT P.id_prestamo, L.titulo, L.autor, P.fecha_prestamo, P.fecha_devolucion, P.devuelto 
             FROM Prestamos P 
             JOIN Libros L ON P.id_libro = L.id_libro 
             WHERE P.id_estudiante = '$id_user' 
             ORDER BY P.fecha_prestamo DESC";
$resultado = mysqli_query($conn, $consulta);
?>
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Mis Préstamos - Biblioteca</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/estilos.css">
</head>

<body>
    <?php include '../includes/header.php'; ?>
    <div class="container">
        <h2>Mis Préstamos e Historial</h2>
        <div class="table-container">
            <?php if (mysqli_num_rows($resultado) > 0): ?>
                <?php while ($fila = mysqli_fetch_assoc($resultado)): ?>
                    <div class="tarjeta loan-card" style="padding: 15px;">
                        <h3>
                            <?php echo htmlspecialchars($fila['titulo']); ?>
                        </h3>
                        <p style="font-size: 0.9em; color: gray;">
                            <?php echo htmlspecialchars($fila['autor']); ?>
                        </p>
                        <hr style="border: 0; border-top: 1px solid #eee; margin: 10px 0;">
                        <p><strong>Fecha:</strong>
                            <?php echo date('d/m/Y', strtotime($fila['fecha_prestamo'])); ?>
                        </p>
                        <p><strong>Estado:</strong>
                            <?php if ($fila['devuelto']): ?>
                                <span style="color: green;">Devuelto</span>
                            <?php else: ?>
                                <span style="color: orange;">En curso</span>
                            <?php endif; ?>
                        </p>
                    </div>
                <?php endwhile; ?>
            <?php else: ?>
                <p>No tienes préstamos registrados.</p>
            <?php endif; ?>
        </div>
        <a href="index.php" class="btn-editar"
            style="display:inline-block; margin-top:20px; max-width: 200px;">Volver</a>
    </div>
</body>

</html>