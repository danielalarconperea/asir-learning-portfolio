<?php
if (isset($_POST["enviar"])) {
    $host = "localhost";
    $user = "root";
    $pass = "rootroot";
    $db = "red_social_db";

    $conexion = mysqli_connect($host, $user, $pass, $db)
        or die("Error de conexión: " . mysqli_connect_error());

    mysqli_set_charset($conexion, "utf8mb4");

    $username = mysqli_real_escape_string($conexion, $_POST["username"]);
    $nombre = mysqli_real_escape_string($conexion, $_POST["nombre"]);
    $email = mysqli_real_escape_string($conexion, $_POST["email"]);
    $fecha_nacimiento = mysqli_real_escape_string($conexion, $_POST["fecha_nacimiento"]);
    $pais = mysqli_real_escape_string($conexion, $_POST["pais"]);

    $consulta = "INSERT INTO usuarios (username, nombre, email, fecha_nacimiento, pais) 
                 VALUES ('$username', '$nombre', '$email', '$fecha_nacimiento', '$pais')";

    if (mysqli_query($conexion, $consulta)) {
        $bien = "Usuario '$username' agregado correctamente.";
    } else {
        $mal = "Error al agregar el usuario: " . mysqli_error($conexion);
    }

    mysqli_close($conexion);
}

?>

<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Registrar Usuario</title>
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
            max-width: 600px;
            overflow: hidden;
        }
        
        .header {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
            color: white;
            padding: 30px;
            text-align: center;
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
            font-size: 0.9rem;
            display: flex;
            align-items: center;
            gap: 5px;
            transition: background 0.3s;
        }
        
        .back-btn:hover {
            background: rgba(255,255,255,0.3);
        }
        
        .form-container {
            padding: 40px;
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
            border-color: #4CAF50;
        }
        
        .btn-submit {
            width: 100%;
            padding: 16px;
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
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
            box-shadow: 0 10px 20px rgba(76, 175, 80, 0.3);
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
        
        @media (max-width: 768px) {
            .form-row {
                grid-template-columns: 1fr;
                gap: 0;
            }
            
            .form-container {
                padding: 30px 20px;
            }
            
            .header {
                padding: 25px 20px;
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
            <h1>👤 Registrar Nuevo Usuario</h1>
            <p>Completa los datos para unirse a la red social</p>
        </div>
        
        <div class="form-container">
            <form action="insertar.php" method="POST">
                <div class="form-group">
                    <label for="username">Nombre de usuario *</label>
                    <input type="text" id="username" name="username" required 
                           placeholder="Ej: maria_g">
                </div>
                
                <div class="form-group">
                    <label for="nombre">Nombre completo *</label>
                    <input type="text" id="nombre" name="nombre" required 
                           placeholder="Ej: María González">
                </div>
                
                <div class="form-group">
                    <label for="email">Correo electrónico *</label>
                    <input type="email" id="email" name="email" required 
                           placeholder="usuario@email.com">
                </div>
                
                <div class="form-row">
                    <div class="form-group">
                        <label for="fecha_nacimiento">Fecha de nacimiento</label>
                        <input type="date" id="fecha_nacimiento" name="fecha_nacimiento">
                    </div>
                    
                    <div class="form-group">
                        <label for="pais">País</label>
                        <select id="pais" name="pais">
                            <option value="">Seleccionar país...</option>
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
                
                <button type="submit" name="enviar" class="btn-submit">Registrar Usuario</button>
                <?php if($bien != ''): ?>
                    <p class="success-message"><?php echo $bien ?></p>
                <?php endif; ?>
                <?php if($mal != ''): ?>
                    <p class="error-message"><?php echo $mal ?></p>
                <?php endif; ?>
            </form>
        </div>
    </div>
</body>
</html>