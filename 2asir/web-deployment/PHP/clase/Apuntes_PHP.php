<?php
/**
 * ============================================================================
 *               🐘 APUNTES DE PHP BÁSICO - GUÍA DE ESTUDIO
 * ============================================================================
 * 
 * Este archivo resume las funciones y conceptos clave de PHP vistos en clase.
 * Ideal para estudiar sintaxis y funciones integradas.
 * 
 * ÍNDICE:
 * 1. VARIABLES Y TIPOS
 * 2. ESTRUCTURAS DE CONTROL (IF, FOR, WHILE)
 * 3. FUNCIONES DE CADENAS (STRINGS)
 * 4. ARRAYS Y SUS FUNCIONES
 * 5. MATEMÁTICAS Y FECHAS
 * 6. MANEJO DE ARCHIVOS (FECHEROS)
 * 7. FORMULARIOS Y SUPERGLOBALES
 */

/* ----------------------------------------------------------------------------
 * 1. VARIABLES Y TIPOS
 * ----------------------------------------------------------------------------
 */
$nombre = "Juan";          // String
$edad = 20;               // Integer
$precio = 19.99;          // Float
$es_valido = true;         // Boolean

// Concatenación
echo "Hola " . $nombre;    // Con el punto .
echo "Edad: $edad";        // Las comillas dobles interpretan variables


/* ----------------------------------------------------------------------------
 * 2. ESTRUCTURAS DE CONTROL
 * ----------------------------------------------------------------------------
 */

// Condicionales
if ($edad >= 18) {
    // Código si es verdadero
} else {
    // Código si es falso
}

// Bucle FOR (Saber cuántas veces repite)
for ($i = 0; $i < 10; $i++) {
    // echo $i;
}

// Bucle WHILE (Repite mientras se cumpla la condición)
while ($condicion) {
    // ...
}

// Bucle FOREACH (Específico para recorrer ARRAYS)
foreach ($mi_array as $valor) {
    // echo $valor;
}


/* ----------------------------------------------------------------------------
 * 3. FUNCIONES DE CADENAS (STRINGS)
 * ----------------------------------------------------------------------------
 */

$texto = "  Hola Mundo  ";

strlen($texto);             // Devuelve la longitud del string.
trim($texto);               // Quita espacios en blanco al principio y al final.
strtolower($texto);         // Pasa todo a minúsculas.
strtoupper($texto);         // Pasa todo a MAYÚSCULAS.
str_replace("Mundo", "PHP", $texto); // Reemplaza un texto por otro.
substr($texto, 0, 4);       // Extrae una parte del string (inicio, longitud).
strip_tags("<p>Hola</p>");  // Elimina etiquetas HTML del string (Seguridad).
strcmp($str1, $str2);       // Compara dos strings (devuelve 0 si son iguales).


/* ----------------------------------------------------------------------------
 * 4. ARRAYS Y SUS FUNCIONES
 * ----------------------------------------------------------------------------
 */

// Crear Array
$frutas = ["Manzana", "Pera", "Plátano"];

count($frutas);             // Cuenta cuántos elementos tiene el array.
array_push($frutas, "Uva"); // Añade un elemento al final.
array_pop($frutas);         // Elimina el último elemento.

// Conversión Array <-> String
$lista = implode(", ", $frutas);   // Array a String: "Manzana, Pera..."
$nuevo_array = explode(", ", $lista); // String a Array (usa un delimitador).


/* ----------------------------------------------------------------------------
 * 5. MATEMÁTICAS Y FECHAS
 * ----------------------------------------------------------------------------
 */

rand(1, 100);               // Genera un número aleatorio entre 1 y 100.
abs(-5);                    // Valor absoluto: 5.
round(3.6);                 // Redondea al entero más cercano: 4.

date("d/m/Y");              // Fecha actual: 14/01/2026.
date("H:i:s");              // Hora actual: 11:05:00.
time();                     // Timestamp actual (segundos desde 1970).


/* ----------------------------------------------------------------------------
 * 6. MANEJO DE ARCHIVOS (FICHEROS TXT)
 * ----------------------------------------------------------------------------
 */

$archivo = "datos.txt";

// Abrir para lectura ('r') o escritura ('w' o 'a')
$fd = fopen($archivo, "r"); 

while (!feof($fd)) {            // Mientras no sea el fin del archivo (End Of File)
    $linea = fgets($fd);        // Lee una línea
    echo trim($linea);          // Limpia y muestra
}

fclose($fd);                    // ¡SIEMPRE cerrar el archivo!

// Forma rápida de leer/escribir
file_get_contents($archivo);    // Lee todo el archivo en un string.
file_put_contents($archivo, "texto", FILE_APPEND); // Escribe al final del archivo.


/* ----------------------------------------------------------------------------
 * 7. FORMULARIOS Y SUPERGLOBALES
 * ----------------------------------------------------------------------------
 */

$_POST['campo'];            // Datos enviados por método POST (ocultos).
$_GET['id'];                // Datos enviados por la URL (ej: ?id=5).
$_FILES['foto'];            // Información de archivos subidos.

// Comprobar si se ha pulsado el botón de enviar
if (isset($_POST['enviar'])) {
    // Procesar formulario
}

// Redireccionar a otra página
header("Location: index.php");

// Fin de los apuntes para estudio.
?>
