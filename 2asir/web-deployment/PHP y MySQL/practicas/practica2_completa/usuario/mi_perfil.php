<?php
require_once '../includes/session_config.php';
require_once '../includes/auth_check.php';
require_once '../conexion.php';

verificar_autenticacion();
$id_user = $_SESSION['user_id'];
$msg = '';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $nombre = mysqli_real_escape_string($conn, trim($_POST['nombre']));
    $apellidos = mysqli_real_escape_string($conn, trim($_POST['apellidos']));
    $email = mysqli_real_escape_string($conn, trim($_POST['email']));
    $telefono = mysqli_real_escape_string($conn, trim($_POST['telefono']));

    // Validar email único (excluyendo el propio)
    $check = mysqli_query($conn, "SELECT id_estudiante FROM Estudiantes WHERE email='$email' AND id_estudiante != '$id_user'");
    if (mysqli_num_rows($check) > 0) {
        $msg = "Error: Ese email ya está en uso por otro usuario.";
    } else {
        $sql = "UPDATE Estudiantes SET nombre='$nombre', apellidos='$apellidos', email='$email', telefono='$telefono' WHERE id_estudiante='$id_user'";

        if (!empty($_POST['password'])) {
            $pass_hash = password_hash($_POST['password'], PASSWORD_DEFAULT);
            $sql = "UPDATE Estudiantes SET nombre='$nombre', apellidos='$apellidos', email='$email', telefono='$telefono', password='$pass_hash' WHERE id_estudiante='$id_user'";
        }

        if (mysqli_query($conn, $sql)) {
            $_SESSION['nombre'] = $nombre; // Actualizar sesión
            $msg = "Perfil actualizado correctamente.";
        } else {
            $msg = "Error al actualizar: " . mysqli_error($conn);
        }
    }
}

$datos = mysqli_fetch_assoc(mysqli_query($conn, "SELECT * FROM Estudiantes WHERE id_estudiante='$id_user'"));
?>
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Mi Perfil - Biblioteca</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/estilos.css">
    <style>
        .form-group {
            margin-bottom: 15px;
        }
    </style>
</head>

<body>
    <?php include '../includes/header.php'; ?>
    <div class="container">
        <h2>Editar Mi Perfil</h2>

        <?php if ($msg): ?>
            <div class="<?php echo strpos($msg, 'Error') !== false ? 'error-message' : 'success-message'; ?>">
                <?php echo $msg; ?>
            </div>
        <?php endif; ?>

        <form method="POST" action="mi_perfil.php"
            style="max-width: 500px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px;">
            <div class="form-group">
                <label>Nombre:</label>
                <input type="text" name="nombre" value="<?php echo htmlspecialchars($datos['nombre']); ?>" required>
            </div>
            <div class="form-group">
                <label>Apellidos:</label>
                <input type="text" name="apellidos" value="<?php echo htmlspecialchars($datos['apellidos']); ?>"
                    required>
            </div>
            <div class="form-group">
                <label>Email:</label>
                <input type="email" name="email" value="<?php echo htmlspecialchars($datos['email']); ?>" required>
            </div>
            <div class="form-group">
                <label>Teléfono:</label>
                <input type="text" name="telefono" value="<?php echo htmlspecialchars($datos['telefono']); ?>">
            </div>
            <div class="form-group">
                <label>Nueva Contraseña (dejar en blanco para no cambiar):</label>
                <input type="password" name="password" minlength="6">
            </div>
            <button type="submit" class="btn-editar" style="width: 100%; border:0; cursor:pointer;">Guardar
                Cambios</button>
        </form>
    </div>
</body>

</html>