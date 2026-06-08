# **Ejercicio: Crear un Juego de Aventuras por Turnos con Clases en Python**

# **Objetivo**: Desarrollar un juego de texto simple donde el jugador explore un mapa, encuentre enemigos y use habilidades. Debes implementar **clases** para estructurar el código.

# 1. **Definir las Clases Principales**:
#    - **Clase Jugador**:
#      - Atributos: nombre (str), vida (int), posición (tupla ej. (x, y)), inventario (lista de ítems).
#      - Métodos: moverse(dirección), atacar(enemigo), usar_ítem(ítem).

import random
import msvcrt

class Jugador:
    def __init__(self, nombre='', vida=100, posicion=(0, 0), inventario=None, daño=15):
        self.nombre = nombre
        self.vida = vida
        self.posicion = posicion
        self.inventario = inventario if inventario is not None else []
        self.daño = daño  # Atributo de daño añadido

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
            # Ejemplo de efecto de ítem: poción de vida
            if item == 'pocion de vida':
                self.vida += 20
                print(f'{self.nombre} recupera 20 de vida!')
            self.inventario.remove(item)
        else:
            print(f'\nError: {item} no está en el inventario')


#    - **Clase Enemigo**:
#      - Atributos: nombre, vida, daño (int).
#      - Métodos: atacar(jugador).

class Enemigo:
    def __init__(self, nombre='', vida=50, daño=10, posicion=(0,0)):
        self.nombre = nombre
        self.vida = vida
        self.daño = daño
        self.posicion = posicion  # Atributo posición añadido

    def atacar(self, jugador):
        print(f'\n{self.nombre} ataca a {jugador.nombre}!')
        jugador.vida -= self.daño
        print(f'{jugador.nombre} pierde {self.daño} de vida!')
        if jugador.vida <= 0:
            print(f'\n---- ¡{jugador.nombre} ha sido derrotado! ----')
        else:
            print(f'{jugador.nombre} tiene {jugador.vida} de vida restante.')


#    - **Clase Mundo**:
#      - Atributos: tamaño (ej. 5x5), jugador (objeto de la clase Jugador), enemigos (lista de objetos Enemigo en posiciones aleatorias).
#      - Métodos: mostrar_mapa(), generar_enemigos().

class Mundo:
    def __init__(self, tamaño, jugador):
        self.tamaño = tamaño
        self.jugador = jugador
        self.enemigos = []

    def mostrar_mapa(self):
        print("\nMapa del Mundo:")
        mapa = [['.' for _ in range(self.tamaño)] for _ in range(self.tamaño)]
        px, py = self.jugador.posicion
        
        # Dibujar jugador si está dentro del mapa
        if 0 <= px < self.tamaño and 0 <= py < self.tamaño:
            mapa[py][px] = 'J'

        # Dibujar enemigos
        for enemigo in self.enemigos:
            ex, ey = enemigo.posicion
            if 0 <= ex < self.tamaño and 0 <= ey < self.tamaño:
                mapa[ey][ex] = 'E'

        # Mostrar mapa
        for fila in reversed(mapa):  # Invertir para mejor visualización
            print(' '.join(fila))

    def generar_enemigos(self, cantidad):
        for i in range(cantidad):
            x = random.randint(0, self.tamaño-1)
            y = random.randint(0, self.tamaño-1)
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

# **Función principal del juego**
def main():
    # Configuración inicial
    nombre_jugador = input("Ingresa tu nombre: ")
    jugador = Jugador(nombre=nombre_jugador, inventario=['pocion de vida'])
    mundo = Mundo(5, jugador)
    mundo.generar_enemigos(3)

    while True:
        mundo.mostrar_mapa()
        print(f"\nVida de {jugador.nombre}: {jugador.vida}")
        print("Inventario:", jugador.inventario)

        # Verificar combate
        enemigo = mundo.obtener_enemigo_en_posicion(jugador.posicion)
        if enemigo:
            print(f"\n¡Te encuentras con {enemigo.nombre}!")
            while enemigo.vida > 0 and jugador.vida > 0:
                accion = input("\n¿Qué quieres hacer? (atacar/huir/usar item/ver inventario): ").lower()
                if accion == 'atacar':
                    jugador.atacar(enemigo)
                    if enemigo.vida > 0:
                        enemigo.atacar(jugador)
                elif accion == 'huir':
                    huir = True
                    break
                elif accion == 'ver inventario':
                    for item in jugador.inventario: print(item)
                elif accion == 'usar':
                    item = input("¿Qué ítem quieres usar?: ")
                    jugador.usar_item(item.lower())
                else:
                    print("Acción no válida")
            if jugador.vida <= 0:
                print("\n---- ¡Has sido derrotado! ----")
                break
            elif huir == True:
                print(f'\n---- {nombre_jugador} ha salido corriendo ----')
                huir = False
            else:
                mundo.enemigos.remove(enemigo)

        # Movimiento
        print("\nDirección (W/S/A/D/E=EXIT): ")
        tecla = msvcrt.getch()
        direccion = tecla.decode().lower()
        if direccion == 'e':
            break
        if direccion in ['w', 's', 'a', 'd']:
            jugador.moverse(direccion)
            # Limitar posición dentro del mapa
            x, y = jugador.posicion
            jugador.posicion = (
                max(0, min(x, mundo.tamaño-1)),
                max(0, min(y, mundo.tamaño-1)))
        else:
            print("Dirección no válida!")

if __name__ == "__main__":
    main()


# ⚱︎⚱︎⚱︎
# ☠︎☠︎☠︎
# ☢︎☢︎☢︎
# ❤︎❤︎❤︎
# ⚔︎⚔︎⚔︎


# 2. **Crear la Lógica del Mapa**:
#    - Usa una matriz o diccionario para representar posiciones (ej. (0,0) a (4,4)).
#    - El jugador empieza en (0,0). Los enemigos se generan aleatoriamente en otras coordenadas.

# 3. **Implementar Movimiento**:
#    - El jugador ingresa direcciones (ej: "W", "A", "S", "D").
#    - Validar que no salga de los límites del mapa.
#    - Actualizar posición del jugador en cada movimiento.

# 4. **Sistema de Encuentros**:
#    - Al moverse, verificar si la nueva posición del jugador coincide con la de un enemigo.
#    - Si hay encuentro, iniciar un combate por turnos:
#      - El jugador elige entre atacar, usar ítem o huir.
#      - Los enemigos atacan automáticamente.

# 5. **Combate**:
#    - En cada turno, el jugador y el enemigo pierden vida según el daño del oponente.
#    - Si el jugador vence, el enemigo desaparece. Si huye, vuelve a la posición anterior.

# 6. **Condiciones de Victoria/Derrota**:
#    - **Victoria**: Llegar a una posición específica (ej. (4,4)) o derrotar a todos los enemigos.
#    - **Derrota**: Si vida del jugador llega a 0.

# 7. **Interfaz de Usuario**:
#    - Mostrar mensajes descriptivos en cada acción (ej: "Te mueves al norte", "¡Un ogro te ataca!").
#    - Actualizar el estado del juego después de cada acción (vida restante, posición).

# 8. **Flujo del Juego**:
#    - Inicializar objetos: jugador = Jugador(...), mundo = Mundo(...).
#    - Bucle principal (while True) que pregunte acciones al usuario y actualize el estado del juego.
#    - salir del bucle al cumplir condiciones de victoria/derrota.

# ---

# **Recomendaciones**:
# - Empieza codificando las clases y métodos básicos, luego añade funcionalidades paso a paso.
# - Testea cada componente por separado (ej: movimiento, combate).