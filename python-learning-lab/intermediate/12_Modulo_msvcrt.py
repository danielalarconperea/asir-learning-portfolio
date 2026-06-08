# Módulo msvcrt - Solo disponible en Windows para operaciones de consola
# Este código debe ejecutarse en terminal/CMD de Windows

import msvcrt
import sys
import os

# Verificar si estamos en Windows
if os.name != 'nt':
    print("Este módulo solo funciona en Windows!")
    sys.exit(1)

# ----------------------------------------------------------------------------------
# 1. DETECCIÓN DE TECLAS (SIMPLE)
# ----------------------------------------------------------------------------------
print("\n--- 1. Detección de teclas simples ---\n")

# getch() - Lee un solo carácter sin mostrarlo (echo)
print("Presiona cualquier tecla (getch)...")
tecla = msvcrt.getch()  # Retorna un byte (ej: b'a')
print(f"Tecla presionada: {tecla} -> Decodificado: {tecla.decode()}")

# getche() - Lee un carácter y lo muestra en consola (con echo)
print("\nPresiona una tecla (getche)...")
tecla = msvcrt.getche()  # Se ve el carácter presionado
print(f"\nTecla: {tecla.decode()}")

# getwch() y getwche() - Versiones unicode (para caracteres especiales)
print("\nPresiona una tecla especial (getwch)...")
tecla = msvcrt.getwch()  # Retorna un string en vez de bytes
print(f"\nTecla especial: {tecla}")

# ----------------------------------------------------------------------------------
# 2. DETECCIÓN DE TECLAS (AVANZADO)
# ----------------------------------------------------------------------------------
print("\n--- 2. Detección avanzada y combinaciones ---\n")

# kbhit() - Verifica si se presionó una tecla (no bloqueante)
print("Presiona cualquier tecla (tienes 5 segundos)...")
timeout = 5  # segundos
start = os.times().elapsed

while (os.times().elapsed - start) < timeout:
    if msvcrt.kbhit():  # True si hay tecla presionada
        tecla = msvcrt.getch()
        print(f"\nTecla detectada: {tecla.decode()}")
        break
else:
    print("\nTiempo agotado!")

# Detectar flechas y teclas especiales (retornan dos códigos)
print("\nPresiona una flecha direccional...")
primera_tecla = msvcrt.getch()
if primera_tecla == b'\xe0':  # Código inicial de teclas especiales
    segunda_tecla = msvcrt.getch()
    flechas = {
        b'H': 'Arriba',
        b'P': 'Abajo',
        b'K': 'Izquierda',
        b'M': 'Derecha'
    }
    print(f"Dirección: {flechas.get(segunda_tecla, 'Desconocida')}")

# ----------------------------------------------------------------------------------
# 3. MANEJO DE LA CONSOLA
# ----------------------------------------------------------------------------------
print("\n--- 3. Manejo de la consola ---\n")

# putch() - Imprime un carácter (bytes)
print("Imprimiendo caracteres con putch:")
msvcrt.putch(b'A')  # Debe ser bytes
msvcrt.putch(b'\n')

# putwch() - Versión unicode
msvcrt.putwch('ñ')  # Acepta caracteres especiales
msvcrt.putwch('\n')

# setmode() - Cambiar modo de un archivo (ej: stdin a binario)
# Útil para leer datos binarios desde consola
fd = sys.stdin.fileno()
msvcrt.setmode(fd, os.O_BINARY)  # Modo binario

# ----------------------------------------------------------------------------------
# 4. EJEMPLOS PRÁCTICOS
# ----------------------------------------------------------------------------------
print("\n--- 4. Ejemplos prácticos ---\n")

# a) Lectura de contraseña sin mostrar caracteres
print("Ingresa contraseña (no se verán los caracteres): ")
password = []
while True:
    tecla = msvcrt.getch()
    if tecla == b'\r':  # Enter
        break
    elif tecla == b'\x08':  # Backspace
        if password:
            password.pop()
            msvcrt.putch(b'\x08')  # Retrocede
            msvcrt.putch(b' ')     # Borra
            msvcrt.putch(b'\x08')
    else:
        password.append(tecla.decode())
        msvcrt.putch(b'*')  # Muestra asterisco
print(f"\nContraseña ingresada: {''.join(password)}")

# b) Menú interactivo con flechas
def menu_interactivo():
    opciones = ["Opción 1", "Opción 2", "Opción 3", "Salir"]
    seleccion = 0
    
    print("\nSelecciona con flechas (Arriba/Abajo):")
    while True:
        for i, op in enumerate(opciones):
            prefix = ">" if i == seleccion else " "
            print(f"{prefix} {op}")
        
        tecla = msvcrt.getch()
        if tecla == b'\xe0':
            tecla = msvcrt.getch()
            if tecla == b'H':  # Arriba
                seleccion = max(0, seleccion-1)
            elif tecla == b'P':  # Abajo
                seleccion = min(len(opciones)-1, seleccion+1)
        elif tecla == b'\r':  # Enter
            return seleccion
        
        # Mueve el cursor arriba
        sys.stdout.write('\033[{}A'.format(len(opciones)))

# Llamar al menú (descomentar para probar)
seleccion = menu_interactivo()
print(f"\nSeleccionaste: {seleccion+1}")

# ----------------------------------------------------------------------------------
# POSIBLES RESULTADOS/COMENTARIOS
# ----------------------------------------------------------------------------------
"""
--- Ejemplo de ejecución ---

--- 1. Detección de teclas simples ---

Presiona cualquier tecla (getch)...
Tecla presionada: b'a' -> Decodificado: a

Presiona una tecla (getche)...
k
Tecla: k

Presiona una tecla especial (getwch)...
�
Tecla especial: ñ

--- 2. Detección avanzada y combinaciones ---

Presiona cualquier tecla (tienes 5 segundos)...
Tecla detectada: s

Presiona una flecha direccional...
Dirección: Arriba

--- 3. Manejo de la consola ---

Imprimiendo caracteres con putch:
A
ñ

--- 4. Ejemplos prácticos ---

Ingresa contraseña (no se verán los caracteres): 
*****
Contraseña ingresada: hola5

Selecciona con flechas (Arriba/Abajo):
> Opción 1
  Opción 2
  Opción 3
  Salir
Seleccionaste: 2
"""

# Notas finales:
# - Algunos caracteres pueden variar según sistema
# - Las flechas requieren dos lecturas de teclado
# - Funciones bloqueantes (getch) detienen la ejecución hasta recibir entrada
# - Ideal para crear interfaces CLI interactivas en Windows