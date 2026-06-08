<?php
//iniciar sesión
session_start();

//Finalmente destruir la sesión
session_destroy();

//Redirigir a la página de inicio
header("Location: mostrar_sesion.php");
?>