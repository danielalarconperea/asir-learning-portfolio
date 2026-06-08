# from datetime import datetime
# fecha_de_ahora = datetime.now()

from datetime import date
fecha_de_ahora = date.today()

def nacimiento(dia, mes, año):
    if fecha_de_ahora.month > mes or (fecha_de_ahora.month == mes and fecha_de_ahora.day >= dia):
        return fecha_de_ahora.year - año
    else: 
        return fecha_de_ahora.year - año - 1


edad = nacimiento(24, 5, 2006)
print('Tienes',edad,'años.')



# def nacimiento(dia, mes, año):
#     if 3 > mes or (3 == mes and 17 >= dia):
#         return 2025 - año
#     else: 
#         return 2025 - año - 1

# edad = nacimiento(24, 5, 2006)
# print('Tienes',edad,'años.')