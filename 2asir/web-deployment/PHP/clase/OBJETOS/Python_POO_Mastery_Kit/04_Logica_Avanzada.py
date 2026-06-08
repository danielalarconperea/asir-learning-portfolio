"""
04_Logica_Avanzada.py

OBJETIVO:
Herencia, Clases Abstractas y Polimorfismo.

DIFERENCIAS:
- Herencia: `class Hija(Padre):` en vez de `extends`.
- Abstractas: Python necesita importar `ABC` y `abstractmethod`.
- Interfaces: En Python no existe `interface`. Se usan clases abstractas puras.
"""

from abc import ABC, abstractmethod

# CLASE ABSTRACTA (Equivalente a abstract class Animal)
class Animal(ABC):
    
    def __init__(self, nombre):
        self.nombre = nombre
        
    def dormir(self):
        return f"{self.nombre} está durmiendo: Zzz..."
    
    # Método abstracto (obliga a definirlo en hijos)
    @abstractmethod
    def moverse(self):
        pass
    
    @abstractmethod
    def hacer_sonido(self):
        pass

# CLASE HIJA 1
class Perro(Animal):
    def hacer_sonido(self):
        return "¡Guau!"
    
    def moverse(self):
        return "corriendo en 4 patas"
    
    def buscar_pelota(self):
        return f"{self.nombre} fue a buscar la pelota."

# CLASE HIJA 2
class Pajaro(Animal):
    def hacer_sonido(self):
        return "¡Pío pío!"
    
    def moverse(self):
        return "volando alto"

## -----------------------------------------
## POLIMORFISMO
## -----------------------------------------

# Python no requiere declarar el tipo de datos (type hinting opcional)
# def presentar_animal(animal: Animal): funcionaría para documentar
def presentar_animal(animal):
    print(f"Aquí tenemos a {animal.dormir()}.")
    print(f"Dice: {animal.hacer_sonido()}")
    print(f"Se mueve: {animal.moverse()}")
    print("---------------------------")

mi_perro = Perro("Firulais")
mi_pajaro = Pajaro("Tweety")

# abstract = Animal("Test") # DARÍA ERROR

presentar_animal(mi_perro)
presentar_animal(mi_pajaro)

print(mi_perro.buscar_pelota())
