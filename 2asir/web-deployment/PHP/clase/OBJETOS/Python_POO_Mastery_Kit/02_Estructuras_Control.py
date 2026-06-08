"""
02_Estructuras_Control.py

OBJETIVO:
Controlar el ciclo de vida y lógica interna.

CONCEPTOS CLAVE vs PHP:
- Constructor: `__construct` (PHP) -> `__init__` (Python)
- Destructor: `__destruct` (PHP) -> `__del__` (Python)
- Concatenación: `.` (PHP) -> `+` o f-strings (Python)
"""

class CuentaBancaria:
    
    # El CONSTRUCTOR (__init__)
    # 'self' es obligatorio ponerlo, pero no enviarlo al llamar.
    def __init__(self, nombre_titular, saldo_inicial=0):
        self.titular = nombre_titular
        self.saldo = saldo_inicial
        print(f"[INFO] Cuenta creada para {self.titular} con {self.saldo}€.")
    
    def depositar(self, cantidad):
        if cantidad > 0:
            self.saldo += cantidad
            print(f"Se han depositado {cantidad}€. Nuevo saldo: {self.saldo}€.")
        else:
            print("[ERROR] La cantidad a depositar debe ser positiva.")
    
    def retirar(self, cantidad):
        if cantidad > self.saldo:
            print(f"[ERROR] Fondos insuficientes. Tienes {self.saldo}€ y quieres sacar {cantidad}€.")
        elif cantidad <= 0:
            print("[ERROR] Debes retirar una cantidad válida.")
        else:
            self.saldo -= cantidad
            print(f"Se han retirado {cantidad}€. Nuevo saldo: {self.saldo}€.")
            
    # El DESTRUCTOR (__del__)
    # En Python es raro usarlo manualmente, el Garbage Collector se encarga.
    def __del__(self):
        print(f"[CIERRE] Cerrando sesión bancaria de {self.titular}.")

## -----------------------------------------
## SECCIÓN DE PRUEBAS
## -----------------------------------------

print("--- INICIO DEL PROGRAMA ---")

mi_cuenta = CuentaBancaria("Juan Pérez", 100)

mi_cuenta.depositar(50)
mi_cuenta.depositar(-20)
mi_cuenta.retirar(200)
mi_cuenta.retirar(30)

print("--- FIN DEL PROGRAMA ---")
# El destructor se llamará automáticamente cuando 'mi_cuenta' deje de ser útil
