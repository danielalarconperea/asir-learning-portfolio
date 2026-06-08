<?php
/**
 * 05_Sistema_Complejo.php
 * 
 * OBJETIVO:
 * El "Factor WOW". Un minijuego RPG de consola que combina todo lo aprendido.
 * 
 * USA:
 * - Clases, Objetos, Constructores.
 * - Herencia (Personaje -> Guerrero/Mago).
 * - Encapsulamiento (puntos de vida privados).
 * - Lógica de control aleatoria y bucles de juego.
 * - Reporte de estado estático y visual.
 */

// 1. CLASE BASE
abstract class Personaje
{
    protected $nombre;
    protected $hp;       // Puntos de vida
    protected $maxHp;
    protected $ataque;

    public function __construct($nombre, $hp, $ataque)
    {
        $this->nombre = $nombre;
        $this->hp = $hp;
        $this->maxHp = $hp;
        $this->ataque = $ataque;
    }

    public function estaVivo()
    {
        return $this->hp > 0;
    }

    public function getNombre()
    {
        return $this->nombre;
    }

    // Método para recibir daño
    public function recibirDano($cantidad)
    {
        $this->hp -= $cantidad;
        if ($this->hp < 0)
            $this->hp = 0;
        echo " > {$this->nombre} recibe $cantidad de daño. (HP: {$this->hp}/{$this->maxHp})\n";
    }

    // Método abstracto para atacar (cada uno ataca distinto)
    abstract public function atacar(Personaje $objetivo);
}

// 2. CLASES HIJAS (Guerrero y Mago)
class Guerrero extends Personaje
{
    public function atacar(Personaje $objetivo)
    {
        $dano = rand($this->ataque - 5, $this->ataque + 5);
        // Posibilidad de crítico
        if (rand(1, 10) > 8) {
            $dano *= 2;
            echo "¡CRÍTICO BRUTAL! ";
        }
        echo "⚔️ {$this->nombre} golpea con su espada a {$objetivo->getNombre()}!\n";
        $objetivo->recibirDano($dano);
    }
}

class Mago extends Personaje
{
    private $mana = 50;

    public function atacar(Personaje $objetivo)
    {
        if ($this->mana >= 10) {
            $dano = $this->ataque * 1.5; // La magia duele más
            $this->mana -= 10;
            echo "🔥 {$this->nombre} lanza una bola de fuego a {$objetivo->getNombre()}! (Maná: {$this->mana})\n";
            $objetivo->recibirDano($dano);
        } else {
            echo "💨 {$this->nombre} no tiene maná y golpea con su bastón...\n";
            $objetivo->recibirDano(5); // Daño ridículo físico
        }
    }
}

// 3. MOTOR DEL JUEGO (CLASE ESTATICA)
class Arena
{
    public static function combatir(Personaje $p1, Personaje $p2)
    {
        echo "\n======================================\n";
        echo "   COMIENZA EL DUELO: {$p1->getNombre()} vs {$p2->getNombre()}";
        echo "\n======================================\n";

        $turno = 1;
        while ($p1->estaVivo() && $p2->estaVivo()) {
            echo "\n--- TURNO $turno ---\n";

            // Ataca P1
            $p1->atacar($p2);
            if (!$p2->estaVivo())
                break; // Si muere, para

            // Pausa dramática simulada (opcional, quitada por velocidad)

            // Ataca P2
            $p2->atacar($p1);

            $turno++;
        }

        self::declararGanador($p1, $p2);
    }

    private static function declararGanador($p1, $p2)
    {
        echo "\n======================================\n";
        if ($p1->estaVivo()) {
            echo "🏆 ¡VICTORIA PARA {$p1->getNombre()}!";
        } else {
            echo "🏆 ¡VICTORIA PARA {$p2->getNombre()}!";
        }
        echo "\n======================================\n";
    }
}

## -----------------------------------------
## SECCIÓN DE EJECUCIÓN
## -----------------------------------------

$heroe = new Guerrero("Conan", 150, 20); // Mucha vida, ataque medio
$villano = new Mago("Saruman", 90, 35);  // Poca vida, mucho daño

Arena::combatir($heroe, $villano);

/*
 * REFLEXIÓN FINAL:
 * Hemos creado un sistema complejo donde:
 * 1. El motor (Arena) no sabe qué tipos de personajes luchan, solo sabe que son "Personajes".
 * 2. Cada clase gestiona su propia lógica interna (el mago su maná, el guerrero sus críticos).
 * 3. Todo está encapsulado y ordenado. ¡Esto es POO!
 */
?>