<?php
require_once '../includes/session_config.php';
require_once '../includes/role_check.php';
require_once '../conexion.php';

verificar_rol(['administrador']);

$consulta = "SELECT * FROM Estudiantes ORDER BY rol, apellidos";
$resultado = mysqli_query($conn, $consulta);
?>
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Gestión de Usuarios - Admin</title>
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
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }

        th {
            background: #34495e;
            color: white;
        }

        tr:hover {
            background: #f9f9f9;
        }

        .rol-badge {
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.85em;
            font-weight: bold;
        }

        .rol-admin {
            background: #e74c3c;
            color: white;
        }

        .rol-profesor {
            background: #f1c40f;
            color: #333;
        }

        .rol-estudiante {
            background: #3498db;
            color: white;
        }
    </style>
</head>

<body>
    <?php include '../includes/header.php'; ?>
    <div class="container">
        <h2>Gestión de Usuarios</h2>
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nombre</th>
                        <th>Email</th>
                        <th>Rol</th>
                        <th>Acciones</th>
                    </tr>
                </thead>
                <tbody>
                    <?php while ($fila = mysqli_fetch_assoc($resultado)): ?>
                        <tr>
                            <td>
                                <?php echo $fila['id_estudiante']; ?>
                            </td>
                            <td>
                                <?php echo htmlspecialchars($fila['nombre'] . ' ' . $fila['apellidos']); ?>
                            </td>
                            <td>
                                <?php echo htmlspecialchars($fila['email']); ?>
                            </td>
                            <td>
                                <?php
                                $class = 'rol-estudiante';
                                if ($fila['rol'] == 'administrador')
                                    $class = 'rol-admin';
                                if ($fila['rol'] == 'profesor')
                                    $class = 'rol-profesor';
                                ?>
                                <span class="rol-badge <?php echo $class; ?>">
                                    <?php echo ucfirst($fila['rol']); ?>
                                </span>
                            </td>
                            <td>
                                <a href="../estudiantes/estudiantes_modificar.php?id=<?php echo $fila['id_estudiante']; ?>"
                                    class="btn-editar" style="font-size: 0.8em;">Editar</a>
                            </td>
                        </tr>
                    <?php endwhile; ?>
                </tbody>
            </table>
        </div>
    </div>
</body>

</html>