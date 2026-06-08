<?php  

// Iniciar o mantener la sesión  
session_start();  

// Guardar una variable en la sesión  
$_SESSION['usuario'] = 'Juan Pérez';  
$_SESSION['email'] = 'juan@ejemplo.com';  
$_SESSION['ultimo_acceso'] = date('Y-m-d H:i:s');  

// También puedes guardar arrays y otros tipos de datos  
$_SESSION['preferencias'] = [  
    'tema' => 'oscuro',  
    'idioma' => 'español',  
    'notificaciones' => true  
];  

// Redirigir a otra página para mostrar la información  
header('Location: mostrar_sesion.php');  
exit();  

?>