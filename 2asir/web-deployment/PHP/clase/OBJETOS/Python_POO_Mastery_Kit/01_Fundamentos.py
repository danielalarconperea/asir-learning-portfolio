"""
01_Fundamentos.py

OBJETIVO:
Entender los bloques básicos de la Programación Orientada a Objetos (POO) en Python
(equivalente al PHP anterior).

CONCEPTOS:
1. Clase (class): La plantilla. En Python se definen con `class Nombre:`.
2. Objeto: La instancia.
3. Atributos (Propiedades): Variables ligadas a `self`.
4. Métodos: Funciones dentro de la clase que SIEMPRE reciben `self` como primer parámetro.
5. __init__: El constructor (equivalente a __construct de PHP).
"""

## -----------------------------------------
## SECCIÓN 1: DEFINICIÓN DE LA CLASE
## -----------------------------------------

class Libro:
    # En Python no se suelen declarar las propiedades fuera del constructor
    # se inicializan dinámicamente, aunque es buena práctica anotarlas.

    def __init__(self):
        # Inicializamos atributos vacíos
        self.titulo = ""
        self.autor = ""
        self.paginas = 0

    # MÉTODOS
    # OJO: En Python, 'this' se llama 'self' y hay que ponerlo EXPLICITAMENTE
    # como primer argumento.
    def mostrar_info(self):
        return f"El libro '{self.titulo}' escrito por {self.autor} tiene {self.paginas} páginas."

## -----------------------------------------
## SECCIÓN 2: INSTANCIACIÓN
## -----------------------------------------

print("--- CREANDO OBJETOS ---")

# En Python NO se usa 'new'. Se llama a la clase como si fuera una función.
libro1 = Libro()
# Accedemos con punto (.) en vez de flecha (->)
libro1.titulo = "El Principito"
libro1.autor = "Antoine de Saint-Exupéry"
libro1.paginas = 96

libro2 = Libro()
libro2.titulo = "1984"
libro2.autor = "George Orwell"
libro2.paginas = 328

## -----------------------------------------
## SECCIÓN 3: USANDO LOS OBJETOS
## -----------------------------------------

print(f"Libro 1: {libro1.titulo}")
print(f"Libro 2: {libro2.titulo}")

print("\n--- INFORMACIÓN DETALLADA ---")
print(libro1.mostrar_info())
print(libro2.mostrar_info())

"""
REFLEXIÓN DOCENTE COMPARATIVA:
- PHP: $this->variable
- Python: self.variable
- PHP: function nombre()
- Python: def nombre(self):
"""
