import random
# X | 0 | X
# ----------
# 0 | X | 0
# ----------
# X | 0 | X

print('7|8|9\n4|5|6\n1|2|3')
pos1,pos2,pos3,pos4,pos5,pos6,pos7,pos8,pos9='   ','   ','   ','   ','   ','   ','   ','   ','   '
fila1 = [pos7,pos8,pos9]
fila2 = [pos4,pos5,pos6]
fila3 = [pos1,pos2,pos3]
print('------------------------')
print('OPCIONES')
print('1.Ver tablero')
print('2.Posicionar la X')
print('------------------------')

def Ubicacion_ficha_yo():
    siguiente_turno = False
    while siguiente_turno == False:
        option=int(input('Dime la posición donde quieres colocar la ficha: '))
        print('☣☣☣☣☣☣☣☣☣☣☣☣☣☣☣☣☣')
        if option == 1:
            if fila3[0] == '   ':
                if ficha==True:
                    fila3[0] = ' X '
                else:
                    fila3[0] = ' 0 '
                siguiente_turno = True
            elif fila3[0] != '   ':
                print('Esta casilla esta marcada')
            else:
                print('Marque una posición valida')
            print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 2:
            if fila3[1] == '   ':
                if ficha==True:
                    fila3[1] = ' X '
                else:
                    fila3[1] = ' 0 '
                siguiente_turno = True
            elif fila3[1] != '   ':
                print('Esta casilla esta marcada')
            else:
                print('Marque una posición valida')
            print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 3:
            if fila3[2] == '   ':
                if ficha==True:
                    fila3[2] = ' X '
                else:
                    fila3[2] = ' 0 '
                siguiente_turno = True
            elif fila3[2] != '   ':
                print('Esta casilla esta marcada')
            else:
                print('Marque una posición valida')
            print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 4:
            if fila2[0] == '   ':
                if ficha==True:
                    fila2[0] = ' X '
                else:
                    fila2[0] = ' 0 '
                siguiente_turno = True
            elif fila2[0] != '   ':
                print('Esta casilla esta marcada')
            else:
                print('Marque una posición valida')
            print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 5:
            if fila2[1] == '   ':
                if ficha==True:
                    fila2[1] = ' X '
                else:
                    fila2[1] = ' 0 '
                siguiente_turno = True
            elif fila2[1] != '   ':
                print('Esta casilla esta marcada')
            else:
                print('Marque una posición valida')
            print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 6:
            if fila2[2] == '   ':
                if ficha==True:
                    fila2[2] = ' X '
                else:
                    fila2[2] = ' 0 '
                siguiente_turno = True
            elif fila2[2] != '   ':
                print('Esta casilla esta marcada')
            else:
                print('Marque una posición valida')
            print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 7:
            if fila1[0] == '   ':
                if ficha==True:
                    fila1[0] = ' X '
                else:
                    fila1[0] = ' 0 '
                siguiente_turno = True
            elif fila1[0] != '   ':
                print('Esta casilla esta marcada')
            else:
                print('Marque una posición valida')
            print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 8:
            if fila1[1] == '   ':
                if ficha==True:
                    fila1[1] = ' X '
                else:
                    fila1[1] = ' 0 '
                siguiente_turno = True
            elif fila1[1] != '   ':
                print('Esta casilla esta marcada')
            else:
                print('Marque una posición valida')
            print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 9:
            if fila1[2] == '   ':
                if ficha==True:
                    fila1[2] = ' X '
                else:
                    fila1[2] = ' 0 '
                siguiente_turno = True
            elif fila1[2] != '   ':
                print('Esta casilla esta marcada')
            else:
                print('Marque una posición valida')
            print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        else:
            print("Opción no válida")


# def Ubicacion_ficha_bot():
#     # Verificar si hay casillas vacías
    
    
#     siguiente_turno = False
#     print('❆❆❆❆❆❆❆❆❆❆❆❆❆❆❆❆❆')
#     while siguiente_turno == False:
#         option = random.randint(1, 9)


def Ubicacion_ficha_bot():
    if all(cell != '   ' for row in [fila1, fila2, fila3] for cell in row):
        print("❆❆❆❆❆❆❆❆❆❆❆❆❆❆❆❆❆")
        return

    siguiente_turno = False
    print('❆❆❆❆❆❆❆❆❆❆❆❆❆❆❆❆❆')
    while siguiente_turno == False:
        option=random.randint(1, 9)    
        if option == 1:
            if fila3[0] == '   ':
                if ficha==True:
                    fila3[0] = ' 0 '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
                else:
                    fila3[0] = ' X '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 2:
            if fila3[1] == '   ':
                if ficha==True:
                    fila3[1] = ' 0 '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
                else:
                    fila3[1] = ' X '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 3:
            if fila3[2] == '   ':
                if ficha==True:
                    fila3[2] = ' 0 '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
                else:
                    fila3[2] = ' X '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 4:
            if fila2[0] == '   ':
                if ficha==True:
                    fila2[0] = ' 0 '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
                else:
                    fila2[0] = ' X '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 5:
            if fila2[1] == '   ':
                if ficha==True:
                    fila2[1] = ' 0 '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
                else:
                    fila2[1] = ' X '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 6:
            if fila2[2] == '   ':
                if ficha==True:
                    fila2[2] = ' 0 '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
                else:
                    fila2[2] = ' X '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 7:
            if fila1[0] == '   ':
                if ficha==True:
                    fila1[0] = ' 0 '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
                else:
                    fila1[0] = ' X '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 8:
            if fila1[1] == '   ':
                if ficha==True:
                    fila1[1] = ' 0 '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
                else:
                    fila1[1] = ' X '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        elif option == 9:
            if fila1[2] == '   ':
                if ficha==True:
                    fila1[2] = ' 0 '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
                else:
                    fila1[2] = ' X '
                    siguiente_turno = True
                    print('',fila1[0],'|',fila1[1],'|',fila1[2],'\n','---------------','\n',fila2[0],'|',fila2[1],'|',fila2[2],'\n','---------------','\n',fila3[0],'|',fila3[1],'|',fila3[2],)
        else:
            print("Opción no válida")
            break
    print('❆❆❆❆❆❆❆❆❆❆❆❆❆❆❆❆❆')


# Aqui empieza la acción:
try:
    bot=str(input('¿Quieres jugar contra la Maquina u otro Jugador? [J/M]: '))
    if bot=='J' or bot=='j':
        print('Buena suerte en la partida!!')
        bot=False
    elif bot=='M' or bot=='m':
        print('Buena suerte!!')
        bot=True
    else:
        print('no marcaste una opción válida así que:')
        print('Juegas contra el bot!!')
        bot=True
    ficha=str(input('Dime con que ficha quieres empezar [X/0]: '))
    if ficha=='X' or ficha=='x':
        print('EMPIZAS TU con -X-!!')
        ficha=True
    elif ficha=='0':
        print('EMPIZAS TU con -0-!!')
        ficha=False
    else:
        print('no marcaste una opción válida así que:')
        print('EMPIZAS TU con -X-!!')
        ficha=True
    ganador=False
    while ganador==False:
        if ((fila1[0]==' X ' and fila2[0]==' X ' and fila3[0]==' X ') 
            or (fila1[1]==' X ' and fila2[1]==' X ' and fila3[1]==' X ') 
            or (fila1[2]==' X ' and fila2[2]==' X ' and fila3[2]==' X ')
            or (fila1[0]==' X ' and fila1[1]==' X ' and fila1[2]==' X ')
            or (fila2[0]==' X ' and fila2[1]==' X ' and fila2[2]==' X ')
            or (fila3[0]==' X ' and fila3[1]==' X ' and fila3[2]==' X ')
            or (fila1[0]==' X ' and fila2[1]==' X ' and fila3[2]==' X ')
            or (fila1[2]==' X ' and fila2[1]==' X ' and fila3[0]==' X ')
        ):
            print('HAN GANADO LAS -X-!!!')
            resultado=input('Quieres echarte otra partida??[S/N]: ')
            if resultado=='S' or resultado=='s':
                fila1[0],fila1[1],fila1[2],fila2[0],fila2[1],fila2[2],fila3[0],fila3[1],fila3[2]='   ','   ','   ','   ','   ','   ','   ','   ','   '
                print('---------------------------------------------------------Siguiente Partida:')
                bot=str(input('¿Quieres jugar contra la Maquina u otro Jugador? [J/M]: '))
                if bot=='J' or bot=='j':
                    print('Buena suerte en la partida!!')
                    bot=False
                elif bot=='M' or bot=='m':
                    print('Buena suerte!!')
                    bot=True
                else:
                    print('no marcaste una opción válida así que:')
                    print('Juegas contra el bot!!')
                    bot=True
                ficha=str(input('Dime con que ficha quieres empezar [X/0]: '))
                if ficha=='X' or ficha=='x':
                    print('EMPIZAS TU con -X-!!')
                    ficha=True
                elif ficha=='0':
                    print('EMPIZAS TU con -0-!!')
                    ficha=False
                else:
                    print('no marcaste una opción válida así que:')
                    print('EMPIZAS TU con -X-!!')
                    ficha=True
            elif resultado=='N' or resultado=='n':
                ganador=True

        elif ((fila1[0]==' 0 ' and fila2[0]==' 0 ' and fila3[0]==' 0 ') 
            or (fila1[1]==' 0 ' and fila2[1]==' 0 ' and fila3[1]==' 0 ') 
            or (fila1[2]==' 0 ' and fila2[2]==' 0 ' and fila3[2]==' 0 ')
            or (fila1[0]==' 0 ' and fila1[1]==' 0 ' and fila1[2]==' 0 ')
            or (fila2[0]==' 0 ' and fila2[1]==' 0 ' and fila2[2]==' 0 ')
            or (fila3[0]==' 0 ' and fila3[1]==' 0 ' and fila3[2]==' 0 ')
            or (fila1[0]==' 0 ' and fila2[1]==' 0 ' and fila3[2]==' 0 ')
            or (fila1[2]==' 0 ' and fila2[1]==' 0 ' and fila3[0]==' 0 ')
        ):
            print('HAN GANADO LOS -0-!!!')
            resultado=input('Quieres echarte otra partida??[S/N]: ')
            if resultado=='S' or resultado=='s':
                fila1[0],fila1[1],fila1[2],fila2[0],fila2[1],fila2[2],fila3[0],fila3[1],fila3[2]='   ','   ','   ','   ','   ','   ','   ','   ','   '
                bot=str(input('¿Quieres jugar contra la Maquina u otro Jugador? [J/M]: '))
                if bot=='J' or bot=='j':
                    print('Buena suerte en la partida!!')
                    bot=False
                elif bot=='M' or bot=='m':
                    print('Buena suerte!!')
                    bot=True
                else:
                    print('no marcaste una opción válida así que:')
                    print('Juegas contra el bot!!')
                    bot=True
                ficha=str(input('Dime con que ficha quieres empezar [X/0]: '))
                if ficha=='X' or ficha=='x':
                    print('EMPIZAS TU con -X-!!')
                    ficha=True
                elif ficha=='0':
                    print('EMPIZAS TU con -0-!!')
                    ficha=False
                else:
                    print('no marcaste una opción válida así que:')
                    print('EMPIZAS TU con -X-!!')
                    ficha=True  
            elif resultado=='N' or resultado=='n':
                ganador=True
        elif (fila1[0]!='   ' and fila2[0]!='   ' and fila3[0]!='   '
                and fila1[1]!='   ' and fila2[1]!='   ' and fila3[1]!='   ' 
                and fila1[2]!='   ' and fila2[2]!='   ' and fila3[2]!='   '
        ):
            print('HABEIS QUEDADO EMPATE!?!')
            resultado=input('Quieres echarte otra partida??[S/N]: ')
            if resultado=='S' or resultado=='s':
                fila1[0],fila1[1],fila1[2],fila2[0],fila2[1],fila2[2],fila3[0],fila3[1],fila3[2]='   ','   ','   ','   ','   ','   ','   ','   ','   '
                ficha=str(input('Dime con que ficha quieres empezar [X/0]: '))
                bot=str(input('¿Quieres jugar contra la Maquina u otro Jugador? [J/M]: '))
                if bot=='J' or bot=='j':
                    print('Buena suerte en la partida!!')
                    bot=False
                elif bot=='M' or bot=='m':
                    print('Buena suerte!!')
                    bot=True
                else:
                    print('no marcaste una opción válida así que:')
                    print('Juegas contra el bot!!')
                    bot=True
                if ficha=='X' or ficha=='x':
                    print('EMPIZAS TU con -X-!!')
                    ficha=True
                elif ficha=='0':
                    print('EMPIZAS TU con -0-!!')
                    ficha=False
                else:
                    print('no marcaste una opción válida así que:')
                    print('EMPIZAS TU con -X-!!')
                    ficha=True  
            elif resultado=='N' or resultado=='n':
                ganador=True
        else:
            if bot==False:
                if ficha==True:
                    Ubicacion_ficha_yo()
                    ficha=False
                else:
                    Ubicacion_ficha_yo()
                    ficha=True
            else:
                Ubicacion_ficha_yo()
                Ubicacion_ficha_bot()
except:
    print("Se ha producido un error")
else:  
    
    print("La partida ha terminado correctamente")
finally:  # Opcional
    # Se ejecuta siempre
    print("Hasta pronto")
