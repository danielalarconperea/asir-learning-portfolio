def palabraVeces(palabra,num):
    print()
    for i in range(num):
        print(palabra)
    print()

palabra = str(input('Dime una palabra\n--- '))
num = int(input('Dime un número\n--- '))
palabraVeces(palabra,num)