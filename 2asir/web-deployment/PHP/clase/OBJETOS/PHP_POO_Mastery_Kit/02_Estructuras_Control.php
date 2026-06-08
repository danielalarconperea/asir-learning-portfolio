<?php
/**
 * 02_Estructuras_Control.php
 * 
 * OBJETIVO:
 * Controlar el ciclo de vida de un objeto y aplicar lógica dentro de las clases.
 * 
 * CONCEPTOS:
 * 1. Constructor (__construct): Método mágico que se ejecuta AUTOMÁTICAMENTE al hacer `new`.
 * 2. Destructor (__destruct): Se ejecuta cuando el objeto se elimina o acaba el script.
 * 3. Lógica interna: Usar if/else dentro de los métodos para validar datos.
 */

class CuentaBancaria
{
    public $titular;
    public $saldo;

    // El CONSTRUCTOR inicializa el objeto con datos obligatorios
    public function __construct($nombreTitular, $saldoInicial = 0)
    {
        $this->titular = $nombreTitular;
        $this->saldo = $saldoInicial;
        echo "[INFO] Cuenta creada para {$this->titular} con {$this->saldo}€.\n";
    }

    public function depositar($cantidad)
    {
        // Estructura de control para validar
        if ($cantidad > 0) {
            $this->saldo += $cantidad;
            echo "Se han depositado {$cantidad}€. Nuevo saldo: {$this->saldo}€.\n";
        } else {
            echo "[ERROR] La cantidad a depositar debe ser positiva.\n";
        }
    }

    public function retirar($cantidad)
    {
        // Lógica para evitar saldo negativo
        if ($cantidad > $this->saldo) {
            echo "[ERROR] Fondos insuficientes. Tienes {$this->saldo}€ y quieres sacar {$cantidad}€.\n";
        } elseif ($cantidad <= 0) {
            echo "[ERROR] Debes retirar una cantidad válida.\n";
        } else {
            $this->saldo -= $cantidad;
            echo "Se han retirado {$cantidad}€. Nuevo saldo: {$this->saldo}€.\n";
        }
    }

    // El DESTRUCTOR se llama al final útiles para cerrar conexiones o guardar logs
    public function __destruct()
    {
        echo "[CIERRE] Cerrando sesión bancaria de {$this->titular}.\n";
    }
}

## -----------------------------------------
## SECCIÓN DE PRUEBAS
## -----------------------------------------

echo "--- INICIO DEL PROGRAMA ---\n";

// Al hacer new, se ejecuta __construct solo
$miCuenta = new CuentaBancaria("Juan Pérez", 100);

// Probamos la lógica de control
$miCuenta->depositar(50);   // Funciona
$miCuenta->depositar(-20);  // Error validado
$miCuenta->retirar(200);    // Error fondos insuficientes
$miCuenta->retirar(30);     // Funciona

echo "--- FIN DEL PROGRAMA (El destructor se ejecutará ahora) ---\n";

/*
 * NOTA DOCENTE:
 * El constructor es vital para asegurar que un objeto nunca exista "vacío" o en un estado inválido.
 * Obliga al programador a dar los datos mínimos necesarios al crear el objeto.
 */
?>