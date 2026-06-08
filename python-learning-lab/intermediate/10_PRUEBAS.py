posicion=(0, 0)

print(posicion)

x, y = posicion

print(posicion)

direccion = 'arriba'

if direccion == 'arriba':
    y += 1
elif direccion == 'abajo':
    y -= 1
elif direccion == 'izquierda':
    x -= 1
elif direccion == 'derecha':
    x += 1
posicion = (x, y)

print(type(posicion))

# Esto if ya no recoge bien la 'x' y la 'y'.

if direccion == 'arriba':
    y += 1
elif direccion == 'abajo':
    y -= 1
elif direccion == 'izquierda':
    x -= 1
elif direccion == 'derecha':
    x += 1

print(posicion)

tamaño = 10

mapa = [['.' for _ in range(tamaño)] for _ in range(tamaño)]
print(mapa,'\n')

for fila in reversed(mapa):  # Invertir para mejor visualización
    print(' '.join(fila))


import msvcrt

# print("Presiona una tecla: ")
# tecla = msvcrt.getch()  # Captura la tecla sin esperar Enter
# print("Tecla presionada:", tecla)
# print(type(tecla))
# for i in tecla:
#     print(i)
#     print(type(i))



# import pygame

# pygame.init()
# ventana = pygame.display.set_mode((400, 400))
# ejecutando = True

# while ejecutando:
#     for evento in pygame.event.get():
#         if evento.type == pygame.QUIT:
#             ejecutando = False
#         elif evento.type == pygame.KEYDOWN:
#             if evento.key == pygame.K_UP or evento.key == pygame.K_w:
#                 print("Mover arriba")
#             elif evento.key == pygame.K_DOWN or evento.key == pygame.K_s:
#                 print("Mover abajo")
#             elif evento.key == pygame.K_LEFT or evento.key == pygame.K_a:
#                 print("Mover izquierda")
#             elif evento.key == pygame.K_RIGHT or evento.key == pygame.K_d:
#                 print("Mover derecha")
#     # Aquí puedes actualizar la posición del jugador y redibujar el juego.
#     pygame.display.flip()

# pygame.quit()
print("\nDirección (w/s/a/d/s): ")
tecla = msvcrt.getch()
direccion = tecla.decode()
print(type(direccion))