import random
import os
import time

# Lista de 15 opciones (una de ellas es 'BONUS')
opciones = [
    # 'OPCIÓN 1',
    # 'OPCIÓN 2',
    # 'OPCIÓN 3',
    # 'OPCIÓN 4',
    # 'OPCIÓN 5',
    # 'OPCIÓN 6',
    # 'OPCIÓN 7',
    # 'OPCIÓN 8',
    # 'OPCIÓN 9',
    # 'OPCIÓN 10',
    # 'OPCIÓN 11',
    # 'OPCIÓN 12',
    # 'OPCIÓN 13',
    # 'OPCIÓN 14',
    'BONUS'
]

print('Girando la ruleta...')
time.sleep(2)  # Simula el giro

# Selección aleatoria
resultado = random.choice(opciones)
print('La ruleta se detuvo en:', resultado)

# Si el resultado es BONUS, se ejecutan las acciones especiales
if resultado == 'BONUS':
    print('¡Felicidades! Has obtenido BONUS.')
    
    numero=0
    while(numero!=5):
        numero = random.randint(0, 10)
        print(numero)
        num = random.randint(1, 15)
        commands = {
            1: 'start calc',
            2: 'start notepad',
            3: 'start mspaint',
            4: 'start write',
            5: 'start explorer',
            6: 'start https://www.google.com',
            7: 'dir',
            8: 'start control',
            9: 'start ms-settings:display',
            10:  'start ms-settings:network',
            11:  'start taskmgr',
            12:  'start eventvwr',
            13:  'start devmgmt.msc',
            14:  'start powershell',
            15:  'start wsl'
        }
        os.system(commands.get(num, ''))
