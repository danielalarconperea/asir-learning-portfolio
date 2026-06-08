<?php
require_once '../includes/session_config.php';
require_once '../conexion.php';

$msg = '';
$error = '';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Sanitización
    $nombre = trim($_POST['nombre']);
    $apellidos = trim($_POST['apellidos']);
    $email = trim($_POST['email']);
    $password = $_POST['password'];
    $confirm_password = $_POST['confirm_password'];
    $rol = 'estudiante'; // Rol por defecto

    // Generación automática de código (ejemplo simple)
    $codigo_estudiante = 'EST' . time(); // En producción usar algo más robusto

    // Validaciones
    if ($password !== $confirm_password) {
        $error = "Las contraseñas no coinciden.";
    } elseif (strlen($password) < 6) {
        $error = "La contraseña debe tener al menos 6 caracteres.";
    } else {
        // Verificar si email ya existe
        $stmt = $conn->prepare("SELECT id_estudiante FROM Estudiantes WHERE email = ?");
        $stmt->bind_param("s", $email);
        $stmt->execute();
        $stmt->store_result();

        if ($stmt->num_rows > 0) {
            $error = "Este email ya está registrado.";
        } else {
            // Hash password
            $password_hash = password_hash($password, PASSWORD_DEFAULT);
            $curso = '1º ASIR'; // Valor por defecto o añadir campo al form
            $telefono = '';

            // Insertar
            $insert = $conn->prepare("INSERT INTO Estudiantes (nombre, apellidos, email, password, rol, codigo_estudiante, curso, telefono) VALUES (?, ?, ?, ?, ?, ?, ?, ?)");
            $insert->bind_param("ssssssss", $nombre, $apellidos, $email, $password_hash, $rol, $codigo_estudiante, $curso, $telefono);

            if ($insert->execute()) {
                header("Location: login.php?msg=registro_exitoso");
                exit();
            } else {
                $error = "Error al registrar: " . $conn->error;
            }
        }
        $stmt->close();
    }
}
?>

<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Registro - Biblioteca Escolar</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/estilos.css">
    <style>
        .login-container {
            max-width: 500px;
            margin: 50px auto;
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>

<body>
    <?php include '../includes/header.php'; ?>

    <div class="container">
        <div class="login-container">
            <h2 style="text-align:center; color:#2c3e50;">Registro de Estudiante</h2>

            <?php if (!empty($error)): ?>
                <div class="error-message">
                    <?php echo $error; ?>
                </div>
            <?php endif; ?>

            <form action="registro.php" method="POST">
                <div class="form-group">
                    <label>Nombre:</label>
                    <input type="text" name="nombre" required
                        value="<?php echo isset($nombre) ? htmlspecialchars($nombre) : ''; ?>">
                </div>
                <div class="form-group">
                    <label>Apellidos:</label>
                    <input type="text" name="apellidos" required
                        value="<?php echo isset($apellidos) ? htmlspecialchars($apellidos) : ''; ?>">
                </div>
                <div class="form-group">
                    <label>Email:</label>
                    <input type="email" name="email" required
                        value="<?php echo isset($email) ? htmlspecialchars($email) : ''; ?>">
                </div>
                <div class="form-group">
                    <label>Contraseña:</label>
                    <input type="password" name="password" required minlength="6">
                </div>
                <div class="form-group">
                    <label>Confirmar Contraseña:</label>
                    <input type="password" name="confirm_password" required minlength="6">
                </div>

                <button type="submit" style="width:100%; margin-top:20px;">Registrarse</button>
            </form>
            <p style="text-align:center; margin-top:10px;">
                <a href="login.php">Ya tengo cuenta</a>
            </p>
        </div>
    </div>
</body>

</html>