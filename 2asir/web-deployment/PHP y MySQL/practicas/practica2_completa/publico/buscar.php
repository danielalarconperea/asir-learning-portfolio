<?php
require_once '../conexion.php';
require_once '../includes/session_config.php';
?>
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <title>Buscar Libros - Público</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../css/estilos.css">
</head>

<body>
    <?php include '../includes/header.php'; ?>
    <div class="container">
        <h2>Buscar en el Catálogo</h2>

        <form action="" method="GET" style="margin-bottom: 30px;">
            <div class="form-group">
                <input type="text" name="q" placeholder="Título, autor, ISBN..."
                    value="<?php echo isset($_GET['q']) ? htmlspecialchars($_GET['q']) : ''; ?>" required>
            </div>
            <button type="submit">Buscar</button>
        </form>

        <?php
        if (isset($_GET['q'])):
            $q = mysqli_real_escape_string($conn, $_GET['q']);
            $sql = "SELECT * FROM Libros WHERE disponible=1 AND (titulo LIKE '%$q%' OR autor LIKE '%$q%' OR isbn LIKE '%$q%')";
            $res = mysqli_query($conn, $sql);
            ?>
            <div class="table-container">
                <?php if (mysqli_num_rows($res) > 0): ?>
                    <?php while ($fila = mysqli_fetch_assoc($res)): ?>
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
                                    <?php echo htmlspecialchars($fila['titulo']); ?>
                                </h3>
                                <p>
                                    <?php echo htmlspecialchars($fila['autor']); ?>
                                </p>
                            </div>
                        </div>
                    <?php endwhile; ?>
                <?php else: ?>
                    <p>No se encontraron resultados.</p>
                <?php endif; ?>
            </div>
        <?php endif; ?>
    </div>
</body>

</html>