<?php session_start(); 
$nombre = $_REQUEST['nombre']; 
if ($nombre == "") { 
    echo "No ha escrito su nombre"; 
    header("Location:guardar_nombre.php"); //exit; 
} 
else { 
    $_SESSION["nombre"] = $nombre; 
    header("Location:guardar_nombre.php"); //exit; 
} ?>