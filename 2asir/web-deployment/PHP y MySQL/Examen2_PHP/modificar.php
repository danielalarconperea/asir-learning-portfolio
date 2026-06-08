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

    if (isset($_POST["modificar"])) {
        $id = mysqli_real_escape_string($conexion, $_POST["id"]);
        $username = mysqli_real_escape_string($conexion, $_POST["username"]);
        $nombre = mysqli_real_escape_string($conexion, $_POST["nombre"]);
        $email = mysqli_real_escape_string($conexion, $_POST["email"]);
        $fecha_nacimiento = mysqli_real_escape_string($conexion, $_POST["fecha_nacimiento"]);
        $pais = mysqli_real_escape_string($conexion, $_POST["pais"]);

        $consulta_upd = "UPDATE usuarios SET username = '$username', nombre = '$nombre', email = '$email', fecha_nacimiento = '$fecha_nacimiento', pais = '$pais' WHERE id = '$id'";
        if (mysqli_query($conexion, $consulta_upd)) {
            $msg_exito = "Libro actualizado correctamente.";
        } else {
            $msg_error = "Error al actualizar: " . mysqli_error($conexion);
        }
    }

    if (isset($_POST['buscar']) && !empty(trim($_POST['busqueda']))) {
        $busqueda = mysqli_real_escape_string($conexion, trim(strtolower($_POST['busqueda'])));
        $consulta = "SELECT * FROM usuarios WHERE LOWER(username) LIKE '%$busqueda%' OR id LIKE '%$busqueda%'";
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
    <title>Modificar Usuario</title>
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
            max-width: 800px;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
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
            background: #fff8e1;
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
            border: 2px solid #ffe082;
            border-radius: 10px;
            font-size: 1rem;
        }
        
        .search-input:focus {
            outline: none;
            border-color: #FF9800;
        }
        
        .btn-search {
            padding: 14px 25px;
            background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
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
        
        .user-found {
            background: #e8f5e9;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        
        .user-avatar {
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.2rem;
            font-weight: bold;
        }
        
        .user-found-info h3 {
            color: #333;
            margin-bottom: 5px;
        }
        
        .form-section {
            display: none;
        }
        
        .form-group {
            margin-bottom: 25px;
        }
        
        label {
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: 600;
            font-size: 0.95rem;
        }
        
        input, select {
            width: 100%;
            padding: 14px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1rem;
            transition: border 0.3s;
        }
        
        input:focus, select:focus {
            outline: none;
            border-color: #FF9800;
        }
        
        .btn-submit {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.1rem;
            font-weight: 600;
            cursor: pointer;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .btn-submit:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(255, 152, 0, 0.3);
        }
        
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
        }





        .success-message{
            color: rgba(5, 255, 14, 1);
            margin-top: 10px;
        }
        .error-message{
            color: rgba(255, 5, 5, 1);
            margin-top: 10px;
        }


        
        .btn-modificar {
            background: linear-gradient(135deg, #1abc9c 0%, #16a085 100%);
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
            .form-row {
                grid-template-columns: 1fr;
            }
            
            .content {
                padding: 20px;
            }
            
            .search-form {
                flex-direction: column;
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
            <h1>✏️ Modificar Usuario</h1>
            <p>Actualiza la información de los usuarios registrados</p>
        </div>
        
        <div class="content">
            <div class="search-section">
                <form action="modificar.php" method="POST" class="search-form">
                    <input type="text" name="busqueda" class="search-input" 
                           placeholder="Ingresa el ID o username del usuario...">
                    <button type="submit" name="buscar" class="btn-search">Buscar Usuario</button>
                </form>
            </div>
            
            
            <?php if (isset($resultado)): ?>
            <div class="table-container" style="margin-top: 30px;">
                <?php if (mysqli_num_rows($resultado) > 0): ?>
                    <?php while ($fila = mysqli_fetch_assoc($resultado)): ?>
                        <div class="tarjeta">
                            <div class="info">
                                <form action="modificar.php" method="post">
                                    <p><strong>ID Usuario:</strong> <?php echo $fila["id"]; ?></p>
                                    <input type="hidden" name="id" value="<?php echo $fila['id']; ?>">
                                    <p><strong>Nombre de usuario:</strong>              
                                        <input type="text" id="username" name="username" required 
                                            value="<?php echo $fila["username"]; ?>">
                                    </p>
                                    <p><strong>nombre:</strong>
                                        <input type="text" id="nombre" name="nombre" required 
                                            value="<?php echo $fila["nombre"]; ?>">
                                    </p>
                                    <p><strong>email:</strong>
                                        <input type="email" id="email" name="email" required 
                                            value="<?php echo $fila["email"]; ?>">
                                    </p>
                                    <div class="form-row">
                                        <div class="form-group">
                                            <label for="fecha_nacimiento">Fecha de nacimiento</label>
                                            <input type="date" id="fecha_nacimiento" name="fecha_nacimiento" value="<?php echo $fila["fecha_nacimiento"]; ?>">
                                        </div>
                                        <div class="form-group">
                                            <label for="pais">País</label>
                                            <select id="pais" name="pais" value="<?php echo $fila["pais"]; ?>">
                                                <option value=""><?php echo $fila["pais"]; ?></option>
                                                <option value="España">España</option>
                                                <option value="México">México</option>
                                                <option value="Colombia">Colombia</option>
                                                <option value="Argentina">Argentina</option>
                                                <option value="Chile">Chile</option>
                                                <option value="Perú">Perú</option>
                                                <option value="Venezuela">Venezuela</option>
                                                <option value="Estados Unidos">Estados Unidos</option>
                                            </select>
                                        </div>
                                    </div>
                                    <button type="submit" class="btn-modificar" name="modificar">Modificar</button>
                                    <?php if($msg_exito != ''): ?>
                                        <p class="success-message"><?php echo $msg_exito ?></p>
                                    <?php endif; ?>
                                    <?php if($msg_error != ''): ?>
                                        <p class="error-message"><?php echo $msg_error ?></p>
                                    <?php endif; ?>
                                </form>
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