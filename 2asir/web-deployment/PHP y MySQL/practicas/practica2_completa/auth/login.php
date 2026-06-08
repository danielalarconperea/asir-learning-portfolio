<?php
require_once '../includes/session_config.php';
require_once '../conexion.php';

$error = '';

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    // Protección básica y obtención de datos
    $email = filter_var(trim($_POST['email']), FILTER_SANITIZE_EMAIL);
    $password = $_POST['password'];
    $ip = $_SERVER['REMOTE_ADDR'];

    // Usar sentencias preparadas para prevenir SQL Injection
    // Nota: El campo 'email' debe existir en la BD. Si usas 'codigo_estudiante' para login, cambia la query.
    $stmt = $conn->prepare("SELECT id_estudiante, nombre, password, rol FROM Estudiantes WHERE email = ?");

    if ($stmt) {
        $stmt->bind_param("s", $email);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($row = $result->fetch_assoc()) {
            // Verificar contraseña
            if (password_verify($password, $row['password'])) {
                // Login EXITOSO
                session_regenerate_id(true); // Prevenir fijación de sesión
                $_SESSION['user_id'] = $row['id_estudiante'];
                $_SESSION['nombre'] = $row['nombre'];
                $_SESSION['rol'] = $row['rol'];
                $_SESSION['ultimo_acceso'] = time();

                // Registrar log de éxito
                $log_stmt = $conn->prepare("INSERT INTO Intentos_Login (email, ip_address, exito) VALUES (?, ?, 1)");
                $log_stmt->bind_param("ss", $email, $ip);
                $log_stmt->execute();

                // Redirección según rol
                if ($row['rol'] == 'administrador') {
                    header("Location: ../admin/index.php");
                } else {
                    header("Location: ../usuario/index.php"); // Profesores y estudiantes van aquí
                }
                exit();
            } else {
                $error = "Contraseña incorrecta.";
                // Registrar log de fallo
                $conn->query("INSERT INTO Intentos_Login (email, ip_address, exito) VALUES ('$email', '$ip', 0)");
            }
        } else {
            $error = "No existe una cuenta con ese email.";
            // Registrar log de fallo
            $conn->query("INSERT INTO Intentos_Login (email, ip_address, exito) VALUES ('$email', '$ip', 0)");
        }
        $stmt->close();
    } else {
        $error = "Error del sistema: " . $conn->error;
    }
}
?>

<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Biblioteca Escolar</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/estilos.css">
    <style>
        .login-container {
            max-width: 400px;
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
            <h2 style="text-align:center; color:#2c3e50; margin-bottom:20px;">Iniciar Sesión</h2>

            <?php if (!empty($error)): ?>
                <div class="error-message">
                    <?php echo $error; ?>
                </div>
            <?php endif; ?>

            <?php if (isset($_GET['timeout'])): ?>
                <div class="error-message">Tu sesión ha expirado por inactividad.</div>
            <?php endif; ?>

            <form action="login.php" method="POST">
                <div class="form-group">
                    <label for="email">Email:</label>
                    <input type="email" id="email" name="email" required placeholder="tu@email.com">
                </div>

                <div class="form-group">
                    <label for="password">Contraseña:</label>
                    <input type="password" id="password" name="password" required>
                </div>

                <button type="submit" style="width:100%; margin-top:20px;">Entrar</button>
            </form>

            <p style="text-align:center; margin-top:15px; font-size:0.9em;">
                ¿No tienes cuenta? <a href="registro.php">Regístrate aquí</a>
            </p>
        </div>
    </div>
</body>

</html>