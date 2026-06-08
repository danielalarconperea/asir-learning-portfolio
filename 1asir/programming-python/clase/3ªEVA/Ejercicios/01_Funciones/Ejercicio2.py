def par(a):
    if a % 2 == 0:
        return 0
    else:
        return 1

lista = [1,6,30,215,22]

for i in lista:
    num = par(i)
    print(f'El número {i}, ¿es par[0] o impar[1]?: {num}')