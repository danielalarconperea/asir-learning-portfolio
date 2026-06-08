<?php
/**
 * 01_Fundamentos.php
 * 
 * OBJETIVO:
 * Entender los bloques básicos de la Programación Orientada a Objetos (POO) en PHP.
 * La POO nos permite organizar el código modelando cosas del mundo real.
 * 
 * CONCEPTOS:
 * 1. Clase (Class): El plano o plantilla (ej. "Coche").
 * 2. Objeto (Object): Una instancia concreta (ej. "Mi Ferrari Rojo").
 * 3. Propiedades: Variables dentro de una clase (características).
 * 4. Métodos: Funciones dentro de una clase (comportamientos).
 * 5. Instanciación: Crear un objeto con `new`.
 */

## -----------------------------------------
## SECCIÓN 1: DEFINICIÓN DE LA CLASE
## -----------------------------------------

// Definimos la plantilla "Libro"
class Libro
{
    // PROPIEDADES (Características del libro)
    // 'public' significa que se pueden acceder desde fuera de la clase
    public $titulo;
    public $autor;
    public $paginas;

    // MÉTODOS (Acciones que puede hacer el libro o que se hacen con él)
    public function mostrarInfo()
    {
        // $this hace referencia a "este" objeto específico que estamos usando
        return "El libro '{$this->titulo}' escrito por {$this->autor} tiene {$this->paginas} páginas.";
    }
}

## -----------------------------------------
## SECCIÓN 2: INSTANCIACIÓN (CREAR OBJETOS)
## -----------------------------------------

echo "--- CREANDO OBJETOS ---\n";

// Creamos el primer objeto (una copia de la plantilla Libro)
$libro1 = new Libro();
$libro1->titulo = "El Principito";
$libro1->autor = "Antoine de Saint-Exupéry";
$libro1->paginas = 96;

// Creamos un segundo objeto totalmente independiente
$libro2 = new Libro();
$libro2->titulo = "1984";
$libro2->autor = "George Orwell";
$libro2->paginas = 328;

## -----------------------------------------
## SECCIÓN 3: USANDO LOS OBJETOS
## -----------------------------------------

// Accedemos a sus propiedades
echo "Libro 1: " . $libro1->titulo . "\n";
echo "Libro 2: " . $libro2->titulo . "\n";

// Llamamos a sus métodos
echo "\n--- INFORMACIÓN DETALLADA ---\n";
echo $libro1->mostrarInfo() . "\n";
echo $libro2->mostrarInfo() . "\n";

/* 
 * REFLEXIÓN DOCENTE:
 * Fíjate cómo usamos la MISMA función `mostrarInfo()` para los dos objetos,
 * pero cada uno imprime sus PROPIOS datos. Esa es la magia de $this.
 * $this es un camaleón que se adapta al objeto que lo llama.
 */
?>