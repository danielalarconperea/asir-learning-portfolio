<?php
session_start();
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    <form action="" method="post">
        <label for="nombre">Nombre:</label>
        <input type="text" name="nombre" id="nombre">
        <br>
        <label for="apellido1">Apellido 1:</label>
        <input type="text" name="apellido1" id="apellido1">
        <br>
        <label for="apellido2">Apellido 2:</label>
        <input type="text" name="apellido2" id="apellido2">
        <br>
        <input type="submit" value="Enviar">
    </form>
</body>
</html>
<?php
$_SESSION['nombre'] = $_POST['nombre'];
$_SESSION['apellido1'] = $_POST['apellido1'];
$_SESSION['apellido2'] = $_POST['apellido2'];
?>
<br>
<a href="index.php">Volver al inicio</a>