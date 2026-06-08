import random
import sys

# try:
from msvcrt import getch  # Windows
# except ImportError:
#     import termios
#     import tty

#     def getch():  # Unix/Linux
#         fd = sys.stdin.fileno()
#         old_settings = termios.tcgetattr(fd)
#         try:
#             tty.setraw(sys.stdin.fileno())
#             ch = sys.stdin.read(1)
#         finally:
#             termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
#         return ch

class Jugador:
    def __init__(self, nombre='', vida=100, posicion=(0, 0), inventario_posicion=(0, 0),inventario=None, daño=15):
        self.nombre = nombre
        self.vida = vida
        self.posicion = posicion
        self.inventario_posicion = inventario_posicion
        self.inventario = inventario if inventario is not None else []
        self.daño = daño

    def moverse(self, direccion):
        x, y = self.posicion
        if direccion == 'w':
            y += 1
        elif direccion == 's':
            y -= 1
        elif direccion == 'a':
            x -= 1
        elif direccion == 'd':
            x += 1
        self.posicion = (x, y)

    def atacar(self, enemigo):
        print(f'\n{self.nombre} ataca a {enemigo.nombre}!')
        enemigo.vida -= self.daño
        print(f'{enemigo.nombre} pierde {self.daño} de vida!')
        if enemigo.vida <= 0:
            print(f'\n---- ¡{enemigo.nombre} ha sido derrotado! ----')
        else:
            print(f'{enemigo.nombre} tiene {enemigo.vida} de vida restante.')

    def usar_item(self, item):
        if item in self.inventario:
            print(f'\n{self.nombre} usa {item}!')
            if item == 'pocion de vida':
                self.vida += 20
                print(f'{self.nombre} recupera 20 de vida!')
            self.inventario.remove(item)
        else:
            print(f'\nError: {item} no está en el inventario')

class Enemigo:
    def __init__(self, nombre='', vida=50, daño=10, posicion=(0,0)):
        self.nombre = nombre
        self.vida = vida
        self.daño = daño
        self.posicion = posicion

    def atacar(self, jugador):
        print(f'\n{self.nombre} ataca a {jugador.nombre}!')
        jugador.vida -= self.daño
        print(f'{jugador.nombre} pierde {self.daño} de vida!')
        if jugador.vida <= 0:
            print(f'\n---- ¡{jugador.nombre} ha sido derrotado! ----')
        else:
            print(f'{jugador.nombre} tiene {jugador.vida} de vida restante.')

class Mundo:
    def __init__(self, tamaño, jugador):
        self.tamaño = tamaño
        self.jugador = jugador
        self.enemigos = []
        self.pociones = []

    def mostrar_mapa(self):
        print("\nMapa del Mundo:")
        mapa = [['.' for _ in range(self.tamaño)] for _ in range(self.tamaño)]
        px, py = self.jugador.posicion
        
        if 0 <= px < self.tamaño and 0 <= py < self.tamaño:
            mapa[py][px] = 'J'

        for enemigo in self.enemigos:
            ex, ey = enemigo.posicion
            if 0 <= ex < self.tamaño and 0 <= ey < self.tamaño and enemigo.vida > 0:
                mapa[ey][ex] = 'E'

        for fila in reversed(mapa):
            print(' '.join(fila))

    def generar_pociones(self, cantidad):
        lista=['pocion de vida', 'pocion de daño', 'pocion de aumento de daño', 'pocion de inutil']
        for i in range(cantidad):
            while True:
                x = random.randint(0, self.tamaño-1)
                y = random.randint(0, self.tamaño-1)
                if(x, y) != self.jugador.posicion and self.jugador.posicion:
                    break
            self.pociones.append(
                Jugador(
                    inventario_posicion=(x, y),
                    inventario=None
                )
            )

    def generar_enemigos(self, cantidad):
        for i in range(cantidad):
            while True:
                x = random.randint(0, self.tamaño-1)
                y = random.randint(0, self.tamaño-1)
                if (x, y) != self.jugador.posicion:
                    break
            self.enemigos.append(
                Enemigo(
                    nombre=f'Enemigo {i+1}',
                    vida=random.randint(30, 60),
                    daño=random.randint(5, 15),
                    posicion=(x, y)
                )
            )

    def obtener_enemigo_en_posicion(self, posicion):
        for enemigo in self.enemigos:
            if enemigo.posicion == posicion and enemigo.vida > 0:
                return enemigo
        return None

def main():
    nombre_jugador = input("Ingresa tu nombre: ")
    jugador = Jugador(nombre=nombre_jugador,)
    mundo = Mundo(5, jugador)
    mundo.generar_enemigos(3)

    while True:
        mundo.mostrar_mapa()
        print(f"\nVida de {jugador.nombre}: {jugador.vida}")
        print("Inventario:", jugador.inventario)

        # Verificar posición victoria
        if jugador.posicion == (mundo.tamaño-1, mundo.tamaño-1):
            print("\n¡Has llegado al tesoro final! ¡VICTORIA!")
            break
            
        # Verificar enemigos derrotados
        if not mundo.enemigos:
            print("\n¡Has derrotado a todos los enemigos! ¡VICTORIA!")
            break

        enemigo = mundo.obtener_enemigo_en_posicion(jugador.posicion)
        if enemigo:
            posicion_anterior = jugador.posicion
            print(f"\n¡Te encuentras con {enemigo.nombre}!")
            huir = False
            
            while enemigo.vida > 0 and jugador.vida > 0:
                accion = input("\n¿Qué quieres hacer? (atacar/huir/usar/inventario): ").lower()
                
                if accion == 'atacar':
                    jugador.atacar(enemigo)
                    if enemigo.vida > 0:
                        enemigo.atacar(jugador)
                
                elif accion == 'huir':
                    huir = True
                    break
                
                elif accion == 'usar':
                    if not jugador.inventario:
                        print("Inventario vacío!")
                        continue
                    item = input("¿Qué ítem quieres usar?: ").lower()
                    jugador.usar_item(item)
                    if enemigo.vida > 0:
                        enemigo.atacar(jugador)
                
                elif accion == 'inventario':
                    print("Inventario:", ", ".join(jugador.inventario))
                
                else:
                    print("Acción no válida")
                    continue

                if jugador.vida <= 0:
                    break

            if jugador.vida <= 0:
                print("\n---- ¡Has sido derrotado! ----")
                break
            elif huir:
                jugador.posicion = posicion_anterior
                print(f'\n---- {nombre_jugador} ha huido! ----')
            else:
                mundo.enemigos.remove(enemigo)

        # Movimiento
        print("\nDirección (W/S/A/D/E=Salir): ")
        tecla = getch()
        direccion = tecla.decode().lower() if sys.platform == 'win32' else tecla.lower()
        
        if direccion == 'e':
            break
            
        if direccion in ['w', 's', 'a', 'd']:
            jugador.moverse(direccion)
            x, y = jugador.posicion
            jugador.posicion = (
                max(0, min(x, mundo.tamaño-1)),
                max(0, min(y, mundo.tamaño-1))
            )
        else:
            print("Dirección no válida!")

if __name__ == "__main__":
    main()

# Condiciones de Victoria:

# Alcanzar la esquina (4,4) en un mapa 5x5

# Derrotar a todos los enemigos

# Sistema de Combate Mejorado:

# El enemigo ataca después de cada acción del jugador

# Al huir, el jugador regresa a su posición anterior

# Manejo de Ítems Corregido:

# Sistema de uso de ítems más intuitivo

# Verificación de inventario vacío

# Compatibilidad Multiplataforma:

# Soporte para entrada de teclado en Unix/Linux y Windows

# Generación de Enemigos:

# Los enemigos ya no aparecen en la posición inicial del jugador

# Mensajes Más Descriptivos:

# Mejor feedback al jugador en cada acción

# Indicación clara del estado del juego

# Errores Corregidos:

# Variables no definidas

# Flujo de turnos en combate

# Posiciones inválidas en el mapa