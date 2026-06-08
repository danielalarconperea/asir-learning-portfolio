**Ejercicio: Crear un Juego de Aventuras por Turnos con Clases en Python**

**Objetivo**: Desarrollar un juego de texto simple donde el jugador explore un mapa, encuentre enemigos y use habilidades. Debes implementar **clases** para estructurar el código.

---

### **Pasos a Seguir**:

1. **Definir las Clases Principales**:
   - **Clase `Jugador`**:
     - Atributos: `nombre` (str), `vida` (int), `posición` (tupla ej. (x, y)), `inventario` (lista de ítems).
     - Métodos: `moverse(dirección)`, `atacar(enemigo)`, `usar_ítem(ítem)`.
   - **Clase `Enemigo`**:
     - Atributos: `nombre`, `vida`, `daño` (int).
     - Métodos: `atacar(jugador)`.
   - **Clase `Mundo`**:
     - Atributos: `tamaño` (ej. 5x5), `jugador` (objeto de la clase `Jugador`), `enemigos` (lista de objetos `Enemigo` en posiciones aleatorias).
     - Métodos: `mostrar_mapa()`, `generar_enemigos()`.

2. **Crear la Lógica del Mapa**:
   - Usa una matriz o diccionario para representar posiciones (ej. `(0,0)` a `(4,4)`).
   - El jugador empieza en `(0,0)`. Los enemigos se generan aleatoriamente en otras coordenadas.

3. **Implementar Movimiento**:
   - El jugador ingresa direcciones (ej: "W", "A", "S", "D").
   - Validar que no salga de los límites del mapa.
   - Actualizar `posición` del jugador en cada movimiento.

4. **Sistema de Encuentros**:
   - Al moverse, verificar si la nueva posición del jugador coincide con la de un enemigo.
   - Si hay encuentro, iniciar un combate por turnos:
     - El jugador elige entre atacar, usar ítem o huir.
     - Los enemigos atacan automáticamente.

5. **Combate**:
   - En cada turno, el jugador y el enemigo pierden vida según el daño del oponente.
   - Si el jugador vence, el enemigo desaparece. Si huye, vuelve a la posición anterior.

6. **Condiciones de Victoria/Derrota**:
   - **Victoria**: Llegar a una posición específica (ej. `(4,4)`) o derrotar a todos los enemigos.
   - **Derrota**: Si `vida` del jugador llega a 0.

7. **Interfaz de Usuario**:
   - Mostrar mensajes descriptivos en cada acción (ej: "Te mueves al norte", "¡Un ogro te ataca!").
   - Actualizar el estado del juego después de cada acción (vida restante, posición).

8. **Flujo del Juego**:
   - Inicializar objetos: `jugador = Jugador(...)`, `mundo = Mundo(...)`.
   - Bucle principal (`while True`) que pregunte acciones al usuario y actualize el estado del juego.
   - Salir del bucle al cumplir condiciones de victoria/derrota.

---

**Recomendaciones**:
- Empieza codificando las clases y métodos básicos, luego añade funcionalidades paso a paso.
- Testea cada componente por separado (ej: movimiento, combate).