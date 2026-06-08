"""
05_Sistema_Complejo.py

OBJETIVO:
El "Factor WOW". Un minijuego RPG de consola.

DIFERENCIAS INTERESANTES:
- rand(min, max): En Python es `random.randint(min, max)`
- echo: `print()`
- Herencia y super(): `super().__init__(...)` para llamar al constructor padre.
"""

import random
from abc import ABC, abstractmethod

# 1. CLASE BASE (ABSTRACTA)
class Personaje(ABC):
    
    def __init__(self, nombre, hp, ataque):
        # En Python, 'protected' es solo convención _variable
        self._nombre = nombre
        self._hp = hp
        self._max_hp = hp
        self._ataque = ataque
        
    def esta_vivo(self):
        return self._hp > 0
    
    def get_nombre(self):
        return self._nombre
    
    def recibir_dano(self, cantidad):
        self._hp -= cantidad
        if self._hp < 0:
            self._hp = 0
        print(f" > {self._nombre} recibe {cantidad} de daño. (HP: {self._hp}/{self._max_hp})")
        
    @abstractmethod
    def atacar(self, objetivo):
        pass

# 2. CLASES HIJAS
class Guerrero(Personaje):
    
    def atacar(self, objetivo):
        min_dmg = self._ataque - 5
        max_dmg = self._ataque + 5
        dano = random.randint(min_dmg, max_dmg)
        
        # Posibilidad de crítico
        if random.randint(1, 10) > 8:
            dano *= 2
            print("¡CRÍTICO BRUTAL!", end=" ")
            
        print(f"⚔️ {self._nombre} golpea con su espada a {objetivo.get_nombre()}!")
        objetivo.recibir_dano(dano)

class Mago(Personaje):
    
    def __init__(self, nombre, hp, ataque):
        # Llamamos al constructor del padre obligatoriamente
        super().__init__(nombre, hp, ataque)
        self.__mana = 50 # Privado real (__)
        
    def atacar(self, objetivo):
        if self.__mana >= 10:
            dano = int(self._ataque * 1.5)
            self.__mana -= 10
            print(f"🔥 {self._nombre} lanza una bola de fuego a {objetivo.get_nombre()}! (Maná: {self.__mana})")
            objetivo.recibir_dano(dano)
        else:
            print(f"💨 {self._nombre} no tiene maná y golpea con su bastón...")
            objetivo.recibir_dano(5)

# 3. MOTOR DEL JUEGO (ESTÁTICO)
class Arena:
    
    @staticmethod
    def combatir(p1, p2):
        print("\n======================================")
        print(f"   COMIENZA EL DUELO: {p1.get_nombre()} vs {p2.get_nombre()}")
        print("======================================\n")
        
        turno = 1
        while p1.esta_vivo() and p2.esta_vivo():
            print(f"\n--- TURNO {turno} ---")
            
            # P1 ataca
            p1.atacar(p2)
            if not p2.esta_vivo(): break
            
            # P2 ataca
            p2.atacar(p1)
            
            turno += 1
            
        Arena.declarar_ganador(p1, p2)
        
    @staticmethod
    def declarar_ganador(p1, p2):
        print("\n======================================")
        if p1.esta_vivo():
            print(f"🏆 ¡VICTORIA PARA {p1.get_nombre()}!")
        else:
            print(f"🏆 ¡VICTORIA PARA {p2.get_nombre()}!")
        print("======================================\n")

## -----------------------------------------
## EJECUCIÓN
## -----------------------------------------

if __name__ == "__main__":
    heroe = Guerrero("Conan", 150, 20)
    villano = Mago("Saruman", 90, 35)
    
    Arena.combatir(heroe, villano)
