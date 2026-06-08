tri_o_cir=input('Quieres calcular el área de un tríangulo o la de un círculo [C/T]: ')

if tri_o_cir == 'C' or tri_o_cir == 'c':
    radio=float(input('Dime el radio del círculo: '))
    area_c=(radio**2)*3.141592
    print('El área del círculo es:',area_c)
elif tri_o_cir == 'T' or tri_o_cir == 't':
    base=float(input('Dime la base del triángulo: '))
    altura=float(input('Dime la altura del triángulo: '))
    area_t=(base*altura)/2
    print('El área del triángulo es:',area_t)