<?php
/**
 * 04_Logica_Avanzada.php
 * 
 * OBJETIVO:
 * Jerarquías de clases y Polimorfismo. No repetir código usando herencia.
 * 
 * CONCEPTOS:
 * 1. Herencia (extends): Una clase hija hereda todo de la clase padre.
 * 2. Protected: Visible en la clase padre e hijas (pero no fuera).
 * 3. Clases Abstractas: Plantillas que no se pueden instanciar, obligan a las hijas a cumplir reglas.
 * 4. Interfaces: Contratos estrictos que definen QUÉ métodos debe haber.
 */

// INTERFAZ: Define un "contrato". Todo animal DEBE poder hacer sonido.
interface SerVivo
{
    public function hacerSonido();
}

// CLASE ABSTRACTA: Define la base. No existe un "Animal" genérico en la realidad.
abstract class Animal implements SerVivo
{
    protected $nombre; // Las hijas pueden acceder aquí

    public function __construct($nombre)
    {
        $this->nombre = $nombre;
    }

    // Método común para todos
    public function dormir()
    {
        return "{$this->nombre} está durmiendo: Zzz...";
    }

    // Método abstracto: Las hijas ESTÁN OBLIGADAS a definir cómo se mueven
    abstract public function moverse();
}

// CLASE HIJA 1
class Perro extends Animal
{
    public function hacerSonido()
    {
        return "¡Guau!";
    }

    public function moverse()
    {
        return "corriendo en 4 patas";
    }

    public function buscarPelota()
    {
        return "{$this->nombre} fue a buscar la pelota.";
    }
}

// CLASE HIJA 2
class Pajaro extends Animal
{
    public function hacerSonido()
    {
        return "¡Pío pío!";
    }

    public function moverse()
    {
        return "volando alto";
    }
}

## -----------------------------------------
## SECCIÓN DE POLIMORFISMO
## -----------------------------------------

// Función que acepta CUALQUIER Animal (Polimorfismo)
function presentarAnimal(Animal $animal)
{
    echo "Aquí tenemos a {$animal->dormir()}.\n";
    echo "Dice: " . $animal->hacerSonido() . "\n";
    echo "Se mueve: " . $animal->moverse() . "\n";
    echo "---------------------------\n";
}

$miPerro = new Perro("Firulais");
$miPajaro = new Pajaro("Tweety");

// $animalGen = new Animal("Test"); // ERROR: No se puede instanciar abstractas

presentarAnimal($miPerro);
presentarAnimal($miPajaro);

// Método exclusivo del perro
echo $miPerro->buscarPelota() . "\n";

/*
 * NOTA DOCENTE:
 * La herencia permite reutilizar el código de `dormir()`.
 * El polimorfismo permite tratar a Perros y Pájaros como "Animales" genéricos
 * en la función `presentarAnimal`, ahorrando código duplicado.
 */
?>