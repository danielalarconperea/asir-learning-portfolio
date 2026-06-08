# -*- coding: utf-8 -*-
"""
PYTHON 3.0: PROGRAMACIÓN ORIENTADA A OBJETOS (POO)
-------------------------------------------------
La POO permite organizar el código en "objetos" que combinan datos (atributos) 
y acciones (métodos). Imagina una clase como un plano de un coche y el objeto 
como el coche real que conduces.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass

# ==============================================================================
# NIVEL 1: BASES (PLANO Y REALIDAD)
# ==============================================================================

class Hero:
    """Clase base para nuestros héroes."""
    
    # Atributo de Clase (Compartido por todos los héroes)
    game_version = "v3.0.0"

    def __init__(self, name, health):
        """Constructor: Inicializa el estado del objeto."""
        self.name = name          # Atributo de instancia público
        self._health = health     # Atributo protegido (por convención)
        self.__secret_id = 999    # Atributo privado (name mangling)

    def speak(self):
        """Método de instancia."""
        print(f"[{self.name}] dice: ¡Listo para la batalla!")

# Crear objetos (instanciar)
my_hero = Hero("Aragon", 100)
my_hero.speak()

# ==============================================================================
# NIVEL 2: HERENCIA Y POLIMORFISMO
# ==============================================================================

class Warrior(Hero):
    """Subclase: Hereda de Hero."""
    
    def __init__(self, name, health, stamina):
        # super() llama al constructor del padre
        super().__init__(name, health)
        self.stamina = stamina

    def speak(self):
        """Sobrescritura: Cambia el comportamiento heredado."""
        print(f"[{self.name}] ruge: ¡Por la gloria!")

class Mage(Hero):
    def speak(self):
        print(f"[{self.name}] susurra: El saber es poder...")

# Polimorfismo: Una lista, diferentes comportamientos
party = [Warrior("Thorg", 150, 50), Mage("Gandalf", 80)]
for member in party:
    member.speak() # Cada uno usa su propia versión de 'speak'

# ==============================================================================
# NIVEL 3: ENCAPSULAMIENTO Y PROPERTIES
# ==============================================================================

class Item:
    def __init__(self, price):
        self._price = price

    @property
    def price(self):
        """Getter: controla cómo se lee el valor."""
        return f"{self._price} piezas de oro"

    @price.setter
    def price(self, value):
        """Setter: añade validación al modificar."""
        if value < 0:
            raise ValueError("El precio no puede ser negativo")
        self._price = value

sword = Item(100)
print(f"Precio: {sword.price}") # Usa el getter automáticamente
# sword.price = -5 # Lanzaría ValueError

# ==============================================================================
# NIVEL 4: MÉTODOS ESPECIALES (DUNDER)
# ==============================================================================

class Inventory:
    def __init__(self, items):
        self.items = items

    def __str__(self):
        """Define cómo se ve al imprimir string."""
        return f"Inventario con {len(self.items)} objetos: {', '.join(self.items)}"

    def __add__(self, other_item):
        """Sobrecarga del operador '+': permite sumar items directamente."""
        self.items.append(other_item)
        return self

inv = Inventory(["Espada", "Escudo"])
inv + "Poción" # Usa __add__
print(inv)

# ==============================================================================
# NIVEL 5: HERRAMIENTAS AVANZADAS
# ==============================================================================

# 5.1. ABC (Contratos obligatorios)
class Enemy(ABC):
    @abstractmethod
    def attack(self):
        pass

# 5.2. Data Classes (Estructuras rápidas)
@dataclass
class Loot:
    item_id: int
    name: str
    rarity: str = "común"

recompensa_final = Loot(1, "Corona de Oro", "Legendaria")
print(f"¡Has encontrado: {recompensa_final}!")

# 5.3. Métodos Dinámicos
class Utility:
    @staticmethod
    def is_valid_name(name):
        return len(name) > 3

    @classmethod
    def create_random(cls):
        # Lógica para crear un objeto de la propia clase
        return cls()

# ==============================================================================
# TIPS PRO PARA APRENDER MÁS
# ==============================================================================
# 1. __slots__: Úsalos para ahorrar memoria si creas miles de objetos pequeños.
# 2. MRO: Investiga 'Method Resolution Order' para herencia múltiple compleja.
# 3. Composicion: A veces es mejor que la herencia (un coche TIENE un motor, no ES un motor).
