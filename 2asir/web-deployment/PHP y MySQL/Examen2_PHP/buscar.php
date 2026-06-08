<?php
if (isset($_POST["buscar"]) && $_SERVER["REQUEST_METHOD"] == "POST") {
    $host = "localhost";
    $user = "root";
    $pass = "rootroot";
    $db = "red_social_db";

    $conexion = mysqli_connect($host, $user, $pass, $db)
        or die("Error de conexión: " . mysqli_connect_error());
}
if ($conexion){
    mysqli_set_charset($conexion, "utf8mb4");
    if (isset($_POST['buscar']) && !empty(trim($_POST['busqueda']))) {
        $busqueda = mysqli_real_escape_string($conexion, trim(strtolower($_POST['busqueda'])));
        $consulta = "SELECT * FROM usuarios WHERE LOWER(username) LIKE '%$busqueda%'";
        $resultado = mysqli_query($conexion, $consulta);
    }
    else if(isset($_POST['buscar']) && empty(trim($_POST['busqueda']))){
        $consulta = "SELECT * FROM usuarios";
        $resultado = mysqli_query($conexion, $consulta);
    }
}
?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Buscar Usuarios</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
        }
        
        .header {
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            color: white;
            padding: 30px;
            border-radius: 20px 20px 0 0;
            text-align: center;
            margin-bottom: 30px;
        }
        
        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        
        .back-btn {
            position: absolute;
            top: 30px;
            left: 30px;
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 50px;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: background 0.3s;
        }
        
        .back-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        
        .search-container {
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
        
        .search-form {
            display: flex;
            gap: 15px;
        }
        
        .search-input {
            flex: 1;
            padding: 16px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1rem;
        }
        
        .search-input:focus {
            outline: none;
            border-color: #2196F3;
        }
        
        .btn-search {
            padding: 16px 30px;
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s;
        }
        
        .btn-search:hover {
            transform: translateY(-2px);
        }
        
        .results-container {
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            overflow: hidden;
        }
        
        .user-card {
            padding: 25px;
            border-bottom: 1px solid #eee;
            transition: background 0.3s;
        }
        
        .user-card:hover {
            background: #f8f9fa;
        }
        
        .user-header {
            display: flex;
            align-items: center;
            gap: 15px;
            margin-bottom: 20px;
        }
        
        .user-avatar {
            width: 60px;
            height: 60px;
            background: linear-gradient(135deg, #2196F3 0%, #1976D2 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.5rem;
            font-weight: bold;
        }
        
        .user-info h3 {
            font-size: 1.4rem;
            color: #333;
            margin-bottom: 5px;
        }
        
        .user-meta {
            color: #666;
            font-size: 0.9rem;
        }
        
        .user-stats {
            display: flex;
            gap: 20px;
            margin-bottom: 15px;
        }
        
        .stat {
            background: #f0f7ff;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9rem;
            color: #2196F3;
        }
        
        .posts-section {
            background: #f8f9fa;
            border-radius: 10px;
            padding: 20px;
            margin-top: 15px;
        }
        
        .post {
            padding: 15px;
            border-bottom: 1px solid #e0e0e0;
        }
        
        .post:last-child {
            border-bottom: none;
        }
        
        .post-content {
            color: #333;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        
        .post-meta {
            display: flex;
            justify-content: space-between;
            color: #666;
            font-size: 0.85rem;
        }
        
        .no-results {
            text-align: center;
            padding: 50px;
            color: #666;
            font-style: italic;
        }
        






        .table-container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }

        .tarjeta {
            display: flex;
            flex-direction: column;
            background-color: white;
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: 1px solid #edf2f7;
            padding-bottom: 20px;
        }

        .tarjeta:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
        }

        .tarjeta .info {
            padding: 20px 20px 0px 20px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .tarjeta .info h3 {
            margin: 0;
        }

        .tarjeta .info p {
            margin: 0;
        }

        
        @media (max-width: 768px) {
            .search-form {
                flex-direction: column;
            }
            
            .user-header {
                flex-direction: column;
                text-align: center;
            }
            
            .user-stats {
                justify-content: center;
            }
            
            h1 {
                font-size: 2rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="index.html" class="back-btn">← Volver</a>
            <h1>🔍 Buscar Usuarios</h1>
            <p>Encuentra usuarios y sus publicaciones</p>
        </div>
        
        <div class="search-container">
            <form action="buscar.php" method="POST" class="search-form">
                <input type="text" name="busqueda" class="search-input" 
                       placeholder="Buscar por username">
                <button type="submit" name="buscar" class="btn-search">Buscar</button>
            </form>
        </div>
        
        <?php if (isset($resultado)): ?>
            <div class="table-container" style="margin-top: 30px;">
                <?php if (mysqli_num_rows($resultado) > 0): ?>
                    <?php while ($fila = mysqli_fetch_assoc($resultado)): 
                        $user_id = $fila["id"];?>
                        <div class="tarjeta">
                            <div class="info">
                                <h2><?php echo $fila["username"]; ?></h2>
                                <p><strong>Nombre Completo:</strong> <?php echo $fila["nombre"]; ?></p>
                                <p><strong>Email:</strong> <?php echo $fila["email"]; ?></p>
                                <p><strong>Fecha de nacimiento:</strong> <?php echo $fila["fecha_nacimiento"]; ?></p>
                                <p><strong>País:</strong> <?php echo $fila["pais"]; ?></p>
                            </div>
                            <?php $consulta2 = "SELECT * FROM publicaciones WHERE usuario_id='$user_id'"; 
                                  $resultado2 = mysqli_query($conexion, $consulta2);?>
                            <div class="info">
                                <h3>Publicaciones</h3>
                                <?php if (mysqli_num_rows($resultado2) > 0): ?>
                                    <?php while ($fila2 = mysqli_fetch_assoc($resultado2)): ?>
                                        <h4>Publicación - <?php echo $fila2["id"]; ?></h4>
                                        <p><?php echo $fila2["contenido"]; ?></p>
                                        <p><strong>Fecha de publicación:</strong> <?php echo $fila2["fecha_publicacion"]; ?></p>
                                        <p><strong>LIKES:</strong> <?php echo $fila2["likes"]; ?></p>
                                    <?php endwhile; ?>
                                <?php else: ?>
                                    <p>No tiene publicaciones.</p>
                                <?php endif; ?>
                            </div>
                        </div>
                    <?php endwhile; ?>
                <?php else: ?>
                    <p style="text-align: center; color: #e06c75;">No se encontraron resultados para la búsqueda.</p>
                <?php endif; ?>
            </div>
        <?php endif; ?>
    
        </div>
    </div>
</body>
</html>