partidos = ['PSOE', 'PP', 'PODEMOS', 'CIUDADANOS', 'VOX']
votos = [0, 0, 0, 0, 0]

voto = int

while voto != 0:
    print('\nVOTOS ELECCIONES')
    print('----------------------')
    i = 0
    for partido in partidos:
        i+=1
        print(f'{i}.- {partido}')
    print('0.- SALIR DEL RECUENTO')
    print('----------------------')
    voto = int(input('Dime tu voto:\n--- '))

    if 1 <= voto <= 5:
        votos[voto - 1] += 1
    elif voto == 0:
        break
    else:
        print('\nIntroduce un valor correcto del 0 al 5')

max_votos = max(votos)

ganador = partidos[votos.index(max_votos)]

print('\nRESULTADOS FINALES:')
for i in range(len(partidos)):
    print(f'{partidos[i]}: {votos[i]} votos')


if votos.count(max_votos) > 1:
    print(f'\nLos partidos ganadores son: ')
    for i in range(votos.count(max_votos)):
        indice = votos.index(max_votos)
        maxVotos = votos.pop(indice)
        gan = partidos.pop(indice)
        print(f'{gan} con {maxVotos} votos. ')
    print()
else:
    print(f'\nEl partido ganador es {ganador} con {max_votos} votos.\n')
        
