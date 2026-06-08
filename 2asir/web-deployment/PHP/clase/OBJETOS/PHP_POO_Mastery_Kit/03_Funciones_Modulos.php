<?php
/**
 * 03_Funciones_Modulos.php
 * 
 * OBJETIVO:
 * Encapsulamiento y miembros estáticos. Proteger los datos y compartir recursos.
 * 
 * CONCEPTOS:
 * 1. Visibilidad:
 *    - public: Accesible desde cualquier lugar.
 *    - private: Solo accesible DESDE LA PROPIA CLASE.
 *    - protected: Solo clase y herencia (lo veremos luego).
 * 2. Getters y Setters: Métodos públicos para controlar propiedades privadas.
 * 3. Static: Propiedades/Métodos que pertenecen a la CLASE, no al objeto.
 */

class Usuario
{
    // PRIVATE: Nadie puede tocar esto directamente desde fuera
    private $password;
    public $username;

    // STATIC: Contador compartido por TODOS los usuarios
    public static $totalUsuarios = 0;

    public function __construct($nombre, $pass)
    {
        $this->username = $nombre;
        $this->setPassword($pass); // Usamos el setter interno

        // Aumentamos el contador de la CLASE (self::, no $this->)
        self::$totalUsuarios++;
    }

    // SETTER: Validamos antes de guardar
    public function setPassword($passNueva)
    {
        if (strlen($passNueva) < 6) {
            echo "[ERROR] La contraseña para {$this->username} es muy corta.\n";
        } else {
            // Simulamos encriptación
            $this->password = hash('sha256', $passNueva);
            echo "[OK] Contraseña actualizada correctamente.\n";
        }
    }

    // GETTER: Devuelve un dato (pero nunca la contraseña real)
    public function getPasswordHash()
    {
        return $this->password;
    }

    // MÉTODO ESTÁTICO: Se puede llamar sin crear objetos
    public static function verContador()
    {
        return "Actualmente hay " . self::$totalUsuarios . " usuarios registrados.";
    }
}

## -----------------------------------------
## SECCIÓN DE PRUEBAS DE ENCAPSULAMIENTO
## -----------------------------------------

echo "Usuarios iniciales: " . Usuario::verContador() . "\n\n";

$user1 = new Usuario("Ana", "123"); // Error, corta
$user1->setPassword("secreto123");   // OK

// Intentar acceder directamente a privado da error fatal:
// echo $user1->password; // ESTO FALLARÍA

echo "Hash guardado: " . $user1->getPasswordHash() . "\n";

## -----------------------------------------
## SECCIÓN DE PRUEBAS ESTÁTICAS
## -----------------------------------------

$user2 = new Usuario("Carlos", "passwordSegura");
$user3 = new Usuario("Eva", "claveMaestra");

// El contador ha subido solo
echo "\n" . Usuario::verContador() . "\n";

/*
 * NOTA DOCENTE:
 * La encapsulación (private/getters/setters) es el pilar de la seguridad en POO.
 * "Static" es útil para contadores globales o utilidades que no dependen de un objeto específico.
 */
?>