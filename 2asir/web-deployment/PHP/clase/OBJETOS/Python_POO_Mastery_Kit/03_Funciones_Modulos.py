"""
03_Funciones_Modulos.py

OBJETIVO:
Encapsulamiento y estáticos.

DIFERENCIAS ENORME CON PHP:
1. Python NO tiene 'private' o 'protected' reales. Todo es público por defecto.
2. Convención: Si una variable empieza por `_` (ej. `_password`), SE RESPETA como privada, aunque técnicamente podrías tocarla.
3. Estáticos: Se usan decoradores `@staticmethod` o `@classmethod`.
"""

import hashlib # Necesario para simular el hash

class Usuario:
    # Atributo DE CLASE (Estático en concepto)
    total_usuarios = 0
    
    def __init__(self, nombre, password):
        self.username = nombre
        # El guion bajo `_` indica "NO TOQUES ESTO DESDE FUERA"
        self._password = "" 
        
        self.set_password(password)
        
        # Aumentamos el contador de la CLASE
        Usuario.total_usuarios += 1
        
    def set_password(self, pass_nueva):
        if len(pass_nueva) < 6:
            print(f"[ERROR] La contraseña para {self.username} es muy corta.")
        else:
            # En Python usamos hashlib para sha256
            self._password = hashlib.sha256(pass_nueva.encode()).hexdigest()
            print("[OK] Contraseña actualizada correctamente.")
            
    def get_password_hash(self):
        return self._password
    
    # MÉTODO ESTÁTICO (Decorador @staticmethod)
    # No recibe 'self' porque no depende de un objeto concreto
    @staticmethod
    def ver_contador():
        return f"Actualmente hay {Usuario.total_usuarios} usuarios registrados."

## -----------------------------------------
## PRUEBAS
## -----------------------------------------

print(f"Usuarios iniciales: {Usuario.ver_contador()}\n")

user1 = Usuario("Ana", "123")        # Error
user1.set_password("secreto123")     # OK

# En Python PODRÍAS hacer print(user1._password) y funcionaría,
# pero un buen programador Python NUNCA lo haría.
print(f"Hash guardado: {user1.get_password_hash()}")

## ESTÁTICOS
user2 = Usuario("Carlos", "passwordSegura")
user3 = Usuario("Eva", "claveMaestra")

print(f"\n{Usuario.ver_contador()}")
