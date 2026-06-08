<?php
require_once '../includes/session_config.php';
require_once '../includes/role_check.php';
require_once '../conexion.php';

verificar_rol(['administrador']);

$consulta = "SELECT * FROM Intentos_Login ORDER BY intento DESC LIMIT 50";
$resultado = mysqli_query($conn, $consulta);
?>
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Logs de Acceso - Admin</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/estilos.css">
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
        }

        th,
        td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }

        th {
            background: #2c3e50;
            color: white;
        }

        .success {
            color: #27ae60;
            font-weight: bold;
        }

        .fail {
            color: #c0392b;
            font-weight: bold;
        }
    </style>
</head>

<body>
    <?php include '../includes/header.php'; ?>
    <div class="container">
        <h2>Auditoría de Accesos (Últimos 50)</h2>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Fecha/Hora</th>
                        <th>Email Intentado</th>
                        <th>IP</th>
                        <th>Resultado</th>
                    </tr>
                </thead>
                <tbody>
                    <?php while ($fila = mysqli_fetch_assoc($resultado)): ?>
                        <tr>
                            <td>
                                <?php echo $fila['intento']; ?>
                            </td>
                            <td>
                                <?php echo htmlspecialchars($fila['email']); ?>
                            </td>
                            <td>
                                <?php echo htmlspecialchars($fila['ip_address']); ?>
                            </td>
                            <td>
                                <?php if ($fila['exito']): ?>
                                    <span class="success">ÉXITO</span>
                                <?php else: ?>
                                    <span class="fail">FALLIDO</span>
                                <?php endif; ?>
                            </td>
                        </tr>
                    <?php endwhile; ?>
                </tbody>
            </table>
        </div>
    </div>
</body>

</html>