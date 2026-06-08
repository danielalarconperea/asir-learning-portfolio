<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biblioteca - Añadir Estudiante</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/estilos.css">
</head>

<body>
    <div class="container">
        <header>
            <h1>👨‍🎓 Gestión de Estudiantes</h1>
            <nav class="main-menu">
                <a href="../index.php">Inicio</a>
                <a href="../libros/libros.html">Libros</a>
                <a href="../estudiantes/estudiantes.html">Estudiantes</a>
                <a href="../prestamos/prestamos.html">Préstamos</a>
            </nav>
        </header>

        <main>
            <nav class="submenu">
                <a href="estudiantes.html">Inicio</a>
                <a href="estudiantes_agregar.php">Añadir</a>
                <a href="estudiantes_listar.php">Listar</a>
                <a href="estudiantes_buscar.php">Buscar</a>
                <a href="estudiantes_modificar.php">Modificar</a>
                <a href="estudiantes_borrar.php">Borrar</a>
            </nav>

            <section class="content">
                <h2>Añadir Estudiante</h2>
                <form action="estudiantes_agregar.php" method="post">
                    <div class="form-group">
                        <label for="nombre">Nombre:</label>
                        <input type="text" id="nombre" name="nombre" placeholder="Ej: Juan" required>
                    </div>

                    <div class="form-group">
                        <label for="apellidos">Apellidos:</label>
                        <input type="text" id="apellidos" name="apellidos" placeholder="Ej: García López" required>
                    </div>

                    <div class="form-group">
                        <label for="codigo_estudiante">Código de Estudiante:</label>
                        <input type="text" id="codigo_estudiante" name="codigo_estudiante" placeholder="Ej: EST2024001"
                            required>
                    </div>

                    <div class="form-group">
                        <label for="curso">Curso:</label>
                        <input type="text" id="curso" name="curso" placeholder="Ej: 2º ASIR" required>
                    </div>

                    <div class="form-group">
                        <label for="telefono">Teléfono:</label>
                        <input type="text" id="telefono" name="telefono" placeholder="Ej: 600000000" required>
                    </div>

                    <div class="form-group">
                        <label for="password">Contraseña:</label>
                        <input type="password" id="password" name="password" required>
                    </div>

                    <button type="submit" name="enviar">Agregar Estudiante</button>
                </form>

                <?php
                if (isset($_POST["enviar"])) {
                    require_once '../conexion.php';
                    $conexion = $conn;

                    $nombre = mysqli_real_escape_string($conexion, $_POST["nombre"]);
                    $apellidos = mysqli_real_escape_string($conexion, $_POST["apellidos"]);
                    $codigo = mysqli_real_escape_string($conexion, $_POST["codigo_estudiante"]);
                    $curso = mysqli_real_escape_string($conexion, $_POST["curso"]);
                    $telefono = mysqli_real_escape_string($conexion, $_POST["telefono"]);
                    $password = mysqli_real_escape_string($conexion, $_POST["password"]);

                    // Verificar si el código ya existe
                    $check_query = "SELECT id_estudiante FROM Estudiantes WHERE codigo_estudiante = '$codigo'";
                    $check_result = mysqli_query($conexion, $check_query);

                    if (mysqli_num_rows($check_result) > 0) {
                        echo "<div class='error-message'>Error: El código de estudiante '$codigo' ya está registrado.</div>";
                    } else {
                        $consulta = "INSERT INTO Estudiantes (nombre, apellidos, codigo_estudiante, curso, telefono, password) 
                                     VALUES ('$nombre', '$apellidos', '$codigo', '$curso', '$telefono', '$password')";

                        if (mysqli_query($conexion, $consulta)) {
                            echo "<div class='success-message'>Estudiante '$nombre' agregado correctamente.</div>";
                        } else {
                            echo "<div class='error-message'>Error al agregar: " . mysqli_error($conexion) . "</div>";
                        }
                    }
                    mysqli_close($conexion);
                }
                ?>
            </section>
        </main>

        <footer>
            <p>Sistema de Gestión de Biblioteca Escolar &copy; 2025</p>
        </footer>
    </div>
</body>

</html>