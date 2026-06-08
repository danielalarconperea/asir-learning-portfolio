<?php session_start(); ?> 
<!DOCTYPE html> 
<html lang="es"> 
<body> 
<h1>Nombre (1)</h1> 
<?php if (isset($_SESSION["nombre"])) 
    { print "<p>Usted ya ha escrito que su nombre es: 
        <strong>$_SESSION[nombre]</strong></p>\n"; } ?> 
<form action="guardar_nombre.php" method="get"> 
    <p>Escriba su nombre:</p> 
    <p><strong>Nombre:</strong> 
    <input type="text" name="nombre"> 
    <input type="submit" value="Guardar"> 
    <input type="reset" value="Borrar"> 
    </p> 
</form> 
<p><a href="mostrar_nombre.php">Volver al inicio.</a></p> 
</body> 
</html> 
