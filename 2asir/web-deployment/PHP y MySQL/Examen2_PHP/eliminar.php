<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $host = "localhost";
    $user = "root";
    $pass = "rootroot";
    $db = "red_social_db";

    $conexion = mysqli_connect($host, $user, $pass, $db)
        or die("Error de conexión: " . mysqli_connect_error());
}
if ($conexion){
    mysqli_set_charset($conexion, "utf8mb4");
    if (isset($_POST['id_a_borrar'])) {
        $id_a_borrar = $_POST['id_a_borrar'];
        $consulta = "DELETE FROM usuarios WHERE id = $id_a_borrar";
        mysqli_query($conexion, $consulta);
    }


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
    <title>Eliminar Usuario</title>
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
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.1);
            width: 100%;
            max-width: 700px;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
            color: white;
            padding: 30px;
            text-align: center;
            position: relative;
        }
        
        h1 {
            font-size: 2.2rem;
            margin-bottom: 10px;
        }
        
        .back-btn {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255,255,255,0.2);
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 50px;
            text-decoration: none;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: background 0.3s;
        }
        
        .back-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        
        .content {
            padding: 40px;
        }
        
        .search-section {
            background: #ffebee;
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
        }
        
        .search-form {
            display: flex;
            gap: 15px;
        }
        
        .search-input {
            flex: 1;
            padding: 14px;
            border: 2px solid #ffcdd2;
            border-radius: 10px;
            font-size: 1rem;
        }
        
        .search-input:focus {
            outline: none;
            border-color: #f44336;
        }
        
        .btn-search {
            padding: 14px 25px;
            background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
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
        
        .user-details {
            background: #fff3e0;
            border-radius: 15px;
            padding: 30px;
            margin-bottom: 30px;
            display: none;
        }
        
        .user-header {
            display: flex;
            align-items: center;
            gap: 20px;
            margin-bottom: 25px;
        }
        
        .user-avatar {
            width: 70px;
            height: 70px;
            background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.8rem;
            font-weight: bold;
        }
        
        .user-info h3 {
            font-size: 1.5rem;
            color: #333;
            margin-bottom: 5px;
        }
        
        .user-meta {
            color: #666;
        }
        
        .user-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        
        .stat-card {
            background: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            border: 1px solid #ffcdd2;
        }
        
        .stat-number {
            font-size: 1.8rem;
            font-weight: bold;
            color: #f44336;
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: #666;
            font-size: 0.9rem;
        }
        
        .warning {
            background: #ffebee;
            border: 2px solid #f44336;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
            margin-bottom: 25px;
        }
        
        .warning-icon {
            font-size: 2rem;
            margin-bottom: 15px;
        }
        
        .warning h4 {
            color: #d32f2f;
            margin-bottom: 10px;
            font-size: 1.3rem;
        }
        
        .warning p {
            color: #666;
            line-height: 1.5;
        }
        
        .btn-danger {
            width: 100%;
            padding: 18px;
            background: linear-gradient(135deg, #f44336 0%, #d32f2f 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .btn-danger:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(244, 67, 54, 0.3);
        }



        
        .btn-borrar {
            background: linear-gradient(135deg, #e74c3c 0%, #c0392b 100%) !important;
            color: white;
            padding: 14px 28px;
            border: none;
            border-radius: 8px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 10px;
            box-shadow: 0 4px 6px rgba(22, 160, 133, 0.2);
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
            
            .user-stats {
                grid-template-columns: 1fr;
            }
            
            .user-header {
                flex-direction: column;
                text-align: center;
            }
            
            .content {
                padding: 20px;
            }
            
            h1 {
                font-size: 1.8rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <a href="index.html" class="back-btn">← Volver</a>
            <h1>🗑️ Eliminar Usuario</h1>
            <p>Borrar usuarios del sistema de red social</p>
        </div>
        
        <div class="content">
            <div class="search-section">
                <form action="eliminar.php" method="POST" class="search-form">
                    <input type="text" name="id" class="search-input" 
                           placeholder="Ingresa username del usuario...">
                    <button type="submit" name="buscar" class="btn-search">Buscar Usuario</button>
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
                                <form action="eliminar.php" method="post">
                                    <input type="hidden" name="id_a_borrar" value="<?php echo $fila['id']; ?>">
                                    <button type="submit" class="btn-borrar">Borrar</button>
                                </form>
                            </div>
                        <?php endwhile; ?>
                    <?php else: ?>
                        <p style="text-align: center; color: #e06c75;">No se encontraron resultados para la búsqueda.</p>
                    <?php endif; ?>
                </div>
            <?php endif; ?>
                
                
            </div>
        </div>
    </div>
</body>
</html>