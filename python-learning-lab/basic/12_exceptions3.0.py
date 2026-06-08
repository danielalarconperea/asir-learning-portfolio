# -*- coding: utf-8 -*-
"""
PYTHON 3.0: MANEJO DE EXCEPCIONES (ERRORES BAJO CONTROL)
-------------------------------------------------------
Las excepciones son eventos que interrumpen el flujo normal de un programa. 
Manejarlas es la diferencia entre un programa que "crashea" y uno que informa 
al usuario y sigue funcionando.
"""

# ==============================================================================
# NIVEL 1: CAPTURA BÁSICA (EL PARACAÍDAS)
# ==============================================================================

def basic_division(a, b):
    try:
        # Aquí va el código que puede fallar
        res = a / b
        print(f"Resultado: {res}")
    except ZeroDivisionError:
        # Aquí manejamos el error específico
        print("Error: No puedes dividir por cero.")

basic_division(10, 0)

# ==============================================================================
# NIVEL 2: ESPECIFICIDAD Y EL OBJETO DE ERROR
# ==============================================================================

def robust_conversion(data):
    try:
        return int(data)
    except ValueError as e:
        # Capturamos el objeto del error 'e' para más detalle
        print(f"Error de valor: '{data}' no es un número. Detalles: {e}")
    except Exception as e:
        # Captura genérica (úsalo al final como red de seguridad)
        print(f"Error inesperado: {type(e).__name__}")

robust_conversion("hola")

# ==============================================================================
# NIVEL 3: EL FLUJO COMPLETO (TRY-EXCEPT-ELSE-FINALLY)
# ==============================================================================

def process_file(filename):
    f = None
    try:
        print(f"Abriendo {filename}...")
        f = open(filename, "r")
    except FileNotFoundError:
        print("¡El archivo no existe!")
    else:
        # Se ejecuta SOLO si NO hubo error en el try
        print("Archivo leído con éxito.")
        print(f.read())
    finally:
        # Se ejecuta SIEMPRE (haya error o no). Ideal para cerrar recursos.
        if f:
            f.close()
            print("Recurso cerrado correctamente.")

# ==============================================================================
# NIVEL 4: LANZAR TUS PROPIOS ERRORES (RAISE)
# ==============================================================================

def validate_age(age):
    if age < 0:
        # Lanzamos un error manualmente con un mensaje claro
        raise ValueError(f"Edad inválida: {age}. No puede ser negativa.")
    if age < 18:
        print("Acceso denegado (Menor de edad).")
    else:
        print("Acceso concedido.")

# ==============================================================================
# NIVEL 5: EXCEPCIONES PERSONALIZADAS (SISTEMA ATM)
# ==============================================================================

class InsufficientFundsError(Exception):
    """Excepción propia para el banco."""
    def __init__(self, balance, amount):
        self.msg = f"Saldo insuficiente. Tienes {balance}€ e intentas sacar {amount}€."
        super().__init__(self.msg)

class ATM:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFundsError(self.balance, amount)
        self.balance -= amount
        print(f"Retirada éxito. Nuevo saldo: {self.balance}€")

my_atm = ATM(500)
try:
    my_atm.withdraw(1000)
except InsufficientFundsError as e:
    print(f"ALERTA BANCARIA: {e.msg}")

# ==============================================================================
# TIPS PRO PARA APRENDER MÁS
# ==============================================================================
# 1. 'raise from': Úsalo para encadenar errores (ej. un error de red causó un error de App).
# 2. 'contextlib': Investiga cómo crear gestores de contexto para evitar tantos try/finally.
# 3. 'AssertionError': Usa 'assert' para depuración (comprobar que algo DEBE ser cierto).
