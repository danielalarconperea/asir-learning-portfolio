# -*- coding: utf-8 -*-

"""
===================================================
 APUNTES COMPLETOS SOBRE CLASES EN PYTHON
===================================================

Este archivo contiene una explicación detallada y ejemplos de la mayoría de
los conceptos relacionados con la Programación Orientada a Objetos (POO) y
las clases en Python.
"""

# ===================================================
# 1. Definición Básica de una Clase y Objetos
# ===================================================

# Una clase es una plantilla o molde para crear objetos.
# Los objetos son instancias de una clase.
# La palabra clave 'class' se usa para definir una clase.
# Por convención, los nombres de las clases usan CamelCase (ej. MiClase).

print("\n--- 1. Definición Básica ---")

class Perro:
    """
    Esta es una clase simple que representa un perro.
    Esto es un 'docstring' que documenta la clase.
    """

    # --- Atributos de Clase ---
    # Son variables que pertenecen a la clase en sí, no a una instancia particular.
    # Se comparten entre todas las instancias de la clase.
    especie = "Canis lupus familiaris"
    patas = 4

    # --- Constructor (__init__) ---
    # Es un método especial que se llama automáticamente al crear una nueva instancia (objeto).
    # Se usa para inicializar los atributos del objeto.
    # 'self' es una referencia a la instancia actual del objeto. Es el primer parámetro
    # de cualquier método de instancia, aunque no se pasa explícitamente al llamar al método.
    def __init__(self, nombre, raza, edad):
        """Inicializa un nuevo objeto Perro."""
        print(f"Creando un nuevo perro llamado {nombre}")
        # --- Atributos de Instancia ---
        # Son variables que pertenecen a una instancia específica del objeto.
        # Cada objeto tiene su propia copia de estos atributos.
        self.nombre = nombre  # Atributo de instancia público
        self.raza = raza
        self.edad = edad
        self._energia = 100 # Atributo "protegido" (convención, ver Encapsulación)
        self.__secreto = "Este perro tiene un secreto" # Atributo "privado" (name mangling, ver Encapsulación)

    # --- Métodos de Instancia ---
    # Son funciones definidas dentro de una clase que operan sobre las instancias (objetos).
    # Siempre reciben 'self' como primer argumento.
    def ladrar(self):
        """Hace que el perro ladre."""
        print(f"{self.nombre} dice: Guau! Guau!")

    def describir(self):
        """Describe al perro."""
        return f"{self.nombre} es un {self.raza} de {self.edad} años. Especie: {self.especie}." # Accede a atributos de instancia y clase

    def jugar(self, tiempo_minutos):
        """Simula al perro jugando y gastando energía."""
        if self._energia >= tiempo_minutos * 0.5:
            print(f"{self.nombre} está jugando felizmente.")
            self._energia -= tiempo_minutos * 0.5
        else:
            print(f"{self.nombre} está demasiado cansado para jugar tanto.")

    def get_energia(self):
        """Método para obtener el valor de la energía (alternativa a acceso directo)."""
        return self._energia

    def revelar_secreto(self):
        """Método para acceder al atributo 'privado'."""
        # Dentro de la clase, se accede normalmente
        print(f"El secreto de {self.nombre} es: {self.__secreto}")


# --- Creación de Instancias (Objetos) ---
# Se llama a la clase como si fuera una función, pasando los argumentos requeridos por __init__ (excepto self).
mi_perro = Perro("Fido", "Labrador", 3)
otro_perro = Perro("Luna", "Beagle", 5)

# --- Acceso a Atributos ---
# Se usa la notación de punto (.)
print(f"Nombre del primer perro: {mi_perro.nombre}")
print(f"Raza del segundo perro: {otro_perro.raza}")

# Acceso a atributos de clase (se puede acceder desde la clase o desde la instancia)
print(f"Especie (desde la clase): {Perro.especie}")
print(f"Especie (desde la instancia 'mi_perro'): {mi_perro.especie}")

# --- Modificación de Atributos ---
mi_perro.edad = 4
print(f"Nueva edad de Fido: {mi_perro.edad}")

# Modificar un atributo de clase afecta a todas las instancias (a menos que la instancia lo haya sobrescrito)
# Perro.patas = 3 # ¡Pobres perros!
# print(f"Patas de Fido ahora (afectado por cambio en clase): {mi_perro.patas}")
# print(f"Patas de Luna ahora (afectado por cambio en clase): {otro_perro.patas}")
# Restauramos
# Perro.patas = 4

# Si una instancia modifica un atributo con el mismo nombre que uno de clase,
# crea un atributo de instancia que 'oculta' al de clase para esa instancia.
otro_perro.especie = "Canis lupus lunaris" # Luna ahora tiene su propia 'especie'
print(f"Especie de Luna (sobrescrita): {otro_perro.especie}")
print(f"Especie de Fido (sigue siendo la de clase): {mi_perro.especie}")
print(f"Especie (desde la clase, sin cambios): {Perro.especie}")


# --- Llamada a Métodos ---
mi_perro.ladrar()
descripcion_luna = otro_perro.describir()
print(descripcion_luna)

mi_perro.jugar(30)
print(f"Energía de Fido después de jugar: {mi_perro.get_energia()}")
otro_perro.jugar(250) # Demasiado tiempo

# ===================================================
# 2. Métodos Especiales (Dunder Methods / Magic Methods)
# ===================================================
# Son métodos con nombres rodeados por dobles guiones bajos (ej. `__init__`, `__str__`).
# Permiten definir cómo se comportan los objetos con operadores incorporados de Python.

print("\n--- 2. Métodos Especiales (Dunder Methods) ---")

class Libro:
    def __init__(self, titulo, autor, paginas):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas

    # --- __str__ ---
    # Define la representación "amigable" en formato string del objeto.
    # Se llama con print(objeto) o str(objeto).
    def __str__(self):
        return f'"{self.titulo}" por {self.autor}'

    # --- __repr__ ---
    # Define la representación "oficial" o "inequívoca" en formato string del objeto.
    # Idealmente, debería ser código Python válido para recrear el objeto.
    # Se llama con repr(objeto) o cuando se muestra el objeto en la consola interactiva.
    # Si __str__ no está definido, Python usa __repr__ en su lugar.
    def __repr__(self):
        return f'Libro(titulo="{self.titulo}", autor="{self.autor}", paginas={self.paginas})'

    # --- __len__ ---
    # Permite usar la función len() con el objeto.
    def __len__(self):
        return self.paginas

    # --- __eq__ ---
    # Define el comportamiento del operador de igualdad (==).
    def __eq__(self, other):
        if isinstance(other, Libro):
            return (self.titulo == other.titulo and
                    self.autor == other.autor)
        return NotImplemented # Importante para indicar que la comparación no está soportada con ese tipo

    # --- __add__ --- (Sobrecarga de Operadores - Ver Sección 11)
    # Define el comportamiento del operador de suma (+).
    def __add__(self, other):
        if isinstance(other, Libro):
            # Ejemplo: combinar dos libros en una "colección" (aquí solo sumamos páginas)
            nuevo_titulo = f"Colección: {self.titulo} y {other.titulo}"
            nuevo_autor = f"{self.autor} y {other.autor}"
            nuevas_paginas = self.paginas + other.paginas
            return Libro(nuevo_titulo, nuevo_autor, nuevas_paginas)
        return NotImplemented


libro1 = Libro("Cien Años de Soledad", "Gabriel García Márquez", 417)
libro2 = Libro("El Amor en los Tiempos del Cólera", "Gabriel García Márquez", 368)
libro3 = Libro("Cien Años de Soledad", "Gabriel García Márquez", 417) # Igual a libro1

print(libro1)          # Llama a __str__
print(str(libro1))     # Llama a __str__
print(repr(libro1))    # Llama a __repr__
print([libro1, libro2]) # Las colecciones suelen usar __repr__ para sus elementos

print(f"Número de páginas de libro1: {len(libro1)}") # Llama a __len__

print(f"¿libro1 == libro2? {libro1 == libro2}") # Llama a __eq__ -> False
print(f"¿libro1 == libro3? {libro1 == libro3}") # Llama a __eq__ -> True
print(f"¿libro1 == 'un string'? {libro1 == 'un string'}") # Llama a __eq__ -> False (devuelve NotImplemented, que Python interpreta como False)

libro_combinado = libro1 + libro2 # Llama a __add__
print(f"Libro combinado: {libro_combinado}")
print(f"Páginas del libro combinado: {len(libro_combinado)}")

# ===================================================
# 3. Herencia
# ===================================================
# Permite crear una nueva clase (clase hija o subclase) que hereda atributos
# y métodos de una clase existente (clase padre o superclase).
# Promueve la reutilización de código.

print("\n--- 3. Herencia ---")

# --- Clase Padre (Superclase) ---
class Animal:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad
        print(f"Ha nacido un animal: {self.nombre}")

    def comer(self):
        print(f"{self.nombre} está comiendo.")

    def sonido(self):
        print("El animal hace un sonido genérico.")

# --- Clase Hija (Subclase) ---
# Se especifica la clase padre entre paréntesis.
class Gato(Animal):
    # Puede tener su propio __init__
    def __init__(self, nombre, edad, color):
        print(f"Inicializando un Gato específico...")
        # --- Llamada al constructor de la clase padre ---
        # Es fundamental para inicializar los atributos heredados.
        super().__init__(nombre, edad) # 'super()' se refiere a la clase padre
        # Se añaden atributos específicos de la subclase
        self.color = color

    # --- Sobrescritura de Métodos ---
    # La subclase puede proporcionar su propia implementación de un método heredado.
    def sonido(self):
        print(f"{self.nombre} dice: Miau!")

    # --- Añadir Nuevos Métodos ---
    def ronronear(self):
        print(f"{self.nombre} está ronroneando... Prrrr...")

# --- Otra Subclase ---
class PerroDomestico(Animal): # Hereda de Animal
    def __init__(self, nombre, edad, raza):
        super().__init__(nombre, edad)
        self.raza = raza

    def sonido(self):
        # Se puede llamar al método de la clase padre si se desea
        # super().sonido()
        print(f"{self.nombre} (un {self.raza}) dice: Guau!")

    def buscar_pelota(self):
        print(f"{self.nombre} busca la pelota!")


# --- Uso de las clases heredadas ---
mi_gato = Gato("Misi", 2, "Naranja")
mi_perro_dom = PerroDomestico("Bobby", 5, "Golden Retriever")

mi_gato.comer()          # Método heredado de Animal
mi_gato.sonido()         # Método sobrescrito en Gato
mi_gato.ronronear()      # Método específico de Gato
print(f"Color de {mi_gato.nombre}: {mi_gato.color}")

mi_perro_dom.comer()     # Método heredado
mi_perro_dom.sonido()    # Método sobrescrito
mi_perro_dom.buscar_pelota() # Método específico

# --- isinstance() y issubclass() ---
# Funciones útiles para trabajar con herencia.
print(f"¿mi_gato es una instancia de Gato? {isinstance(mi_gato, Gato)}")       # True
print(f"¿mi_gato es una instancia de Animal? {isinstance(mi_gato, Animal)}")   # True (debido a la herencia)
print(f"¿mi_gato es una instancia de PerroDomestico? {isinstance(mi_gato, PerroDomestico)}") # False

print(f"¿Es Gato una subclase de Animal? {issubclass(Gato, Animal)}")         # True
print(f"¿Es Animal una subclase de Gato? {issubclass(Animal, Gato)}")         # False
print(f"¿Es Gato una subclase de object? {issubclass(Gato, object)}")       # True (todas las clases heredan de 'object' implícitamente)

# ===================================================
# 4. Encapsulación y Control de Acceso
# ===================================================
# Es el principio de ocultar los detalles internos de una clase y exponer
# solo lo necesario a través de una interfaz pública (métodos).
# Python no tiene modificadores de acceso estrictos como 'private' o 'public'
# en otros lenguajes, pero usa convenciones:

print("\n--- 4. Encapsulación ---")

class CuentaBancaria:
    def __init__(self, titular, saldo_inicial):
        self.titular = titular  # Atributo público: accesible desde cualquier lugar

        # Atributo protegido (convención): Un guion bajo `_` indica que el atributo
        # es para uso interno de la clase o subclases, pero técnicamente aún es accesible.
        self._tipo_cuenta = "Ahorro"

        # Atributo privado (Name Mangling): Doble guion bajo `__` al inicio (y no al final).
        # Python renombra internamente el atributo a `_NombreClase__nombreAtributo`.
        # Esto dificulta (pero no imposibilita) el acceso directo desde fuera.
        self.__saldo = saldo_inicial
        self.__numero_cuenta = "ES" + str(id(self))[-10:] # Ejemplo de atributo 'privado'

    # --- Métodos Públicos (Interfaz) ---
    def depositar(self, cantidad):
        if cantidad > 0:
            self.__saldo += cantidad
            print(f"Depósito exitoso. Saldo actual: {self.__obtener_saldo_formateado()}")
            self.__registrar_transaccion("Depósito", cantidad) # Llama a método privado interno
        else:
            print("La cantidad a depositar debe ser positiva.")

    def retirar(self, cantidad):
        if 0 < cantidad <= self.__saldo:
            self.__saldo -= cantidad
            print(f"Retiro exitoso. Saldo actual: {self.__obtener_saldo_formateado()}")
            self.__registrar_transaccion("Retiro", cantidad)
        elif cantidad > self.__saldo:
            print("Error: Saldo insuficiente.")
        else:
            print("La cantidad a retirar debe ser positiva.")

    def obtener_saldo(self):
        """Método público para consultar el saldo de forma controlada."""
        return self.__saldo

    def obtener_info_publica(self):
        """Devuelve información pública y 'protegida'."""
        # Accedemos al atributo 'protegido' desde dentro de la clase
        return f"Titular: {self.titular}, Tipo: {self._tipo_cuenta}"

    # --- Métodos "Privados" (Name Mangling) ---
    # Destinados a ser usados solo internamente por otros métodos de la clase.
    def __obtener_saldo_formateado(self):
        return f"{self.__saldo:.2f} EUR"

    def __registrar_transaccion(self, tipo, cantidad):
        # Simulación de registro interno
        print(f"--- Registro interno: {tipo} de {cantidad:.2f} EUR en cuenta {self.__numero_cuenta} ---")


cuenta = CuentaBancaria("Ana López", 1000.0)

# Acceso a atributos públicos
print(cuenta.titular)

# Acceso (y modificación) a atributos "protegidos" (posible, pero no recomendado desde fuera)
print(f"Tipo de cuenta (acceso 'protegido'): {cuenta._tipo_cuenta}")
cuenta._tipo_cuenta = "Corriente" # Técnicamente posible
print(f"Tipo de cuenta modificado: {cuenta._tipo_cuenta}")

# Intento de acceso directo a atributos "privados" (genera AttributeError)
# print(cuenta.__saldo) # Error!
# print(cuenta.__numero_cuenta) # Error!

# Acceso a través de métodos públicos (forma correcta)
cuenta.depositar(500.50)
cuenta.retirar(200)
print(f"Saldo obtenido con método público: {cuenta.obtener_saldo()}")
print(cuenta.obtener_info_publica())
cuenta.retirar(2000) # Saldo insuficiente

# --- Acceso a atributos "privados" usando Name Mangling (POSIBLE, pero EVITAR) ---
# Útil para depuración o casos muy específicos, pero rompe la encapsulación.
print(f"Accediendo al saldo 'privado' con name mangling: {cuenta._CuentaBancaria__saldo}")
cuenta._CuentaBancaria__saldo = 50000 # Modificación directa (mala práctica)
print(f"Saldo modificado directamente: {cuenta.obtener_saldo()}")

# Llamada a método 'privado' con name mangling (mala práctica)
formato_privado = cuenta._CuentaBancaria__obtener_saldo_formateado()
print(f"Formato obtenido con método 'privado' (vía mangling): {formato_privado}")


# ===================================================
# 5. Properties (Propiedades)
# ===================================================
# Permiten definir métodos que se comportan como atributos.
# Útil para añadir lógica (validación, cálculo) al obtener, establecer o eliminar un atributo.
# Se usan los decoradores @property, @<nombre_propiedad>.setter, @<nombre_propiedad>.deleter.

print("\n--- 5. Properties ---")

class Temperatura:
    def __init__(self, celsius):
        # Usamos el setter aquí para validar el valor inicial
        self.celsius = celsius # Llama al método setter 'celsius'

    # --- Getter (@property) ---
    # Define el método que se ejecuta al leer el atributo 'celsius'.
    @property
    def celsius(self):
        """Obtiene la temperatura en grados Celsius."""
        print("Ejecutando getter de Celsius")
        # El atributo real donde guardamos el valor suele ser "protegido"
        return self._celsius

    # --- Setter (@<propiedad>.setter) ---
    # Define el método que se ejecuta al asignar un valor a 'celsius'.
    @celsius.setter
    def celsius(self, valor):
        """Establece la temperatura en Celsius, con validación."""
        print(f"Ejecutando setter de Celsius con valor {valor}")
        if valor < -273.15:
            # Lanzamos una excepción si el valor no es válido
            raise ValueError("¡La temperatura no puede ser inferior al cero absoluto (-273.15 °C)!")
        self._celsius = float(valor) # Guardamos el valor en el atributo protegido

    # --- Deleter (@<propiedad>.deleter) ---
    # Define el método que se ejecuta al usar `del` sobre el atributo 'celsius'.
    @celsius.deleter
    def celsius(self):
        """Elimina el atributo de temperatura (ej. estableciéndolo a None)."""
        print("Ejecutando deleter de Celsius")
        # La acción puede variar: borrar el atributo, ponerlo a None, etc.
        # del self._celsius # Borraría el atributo _celsius
        self._celsius = None # O lo ponemos a None

    # --- Propiedad Calculada (Read-Only) ---
    # Se puede definir una property sin setter para crear atributos calculados.
    @property
    def fahrenheit(self):
        """Calcula y devuelve la temperatura en grados Fahrenheit."""
        print("Calculando Fahrenheit desde Celsius")
        if self._celsius is None:
            return None
        return (self._celsius * 9/5) + 32

    # También podríamos definir un setter para fahrenheit si quisiéramos
    # permitir establecer la temperatura en Fahrenheit y que se actualice Celsius.
    @fahrenheit.setter
    def fahrenheit(self, valor):
        """Establece la temperatura a partir de un valor Fahrenheit."""
        print(f"Ejecutando setter de Fahrenheit con valor {valor}")
        if valor is None:
            self.celsius = None # Usamos el setter de celsius
        else:
            temp_celsius = (float(valor) - 32) * 5/9
            self.celsius = temp_celsius # Llama al setter de celsius para validar y guardar


temp = Temperatura(25)   # Llama al setter al inicializar

# Acceso como atributo (llama al getter)
print(f"Temperatura en Celsius: {temp.celsius}")
print(f"Temperatura en Fahrenheit: {temp.fahrenheit}") # Llama al getter de fahrenheit

# Asignación como atributo (llama al setter)
temp.celsius = 30
print(f"Nueva temperatura en Celsius: {temp.celsius}")
print(f"Nueva temperatura en Fahrenheit: {temp.fahrenheit}")

# Intentar asignar valor inválido (llama al setter, lanza ValueError)
try:
    temp.celsius = -300
except ValueError as e:
    print(f"Error al asignar temperatura: {e}")

# Asignar usando el setter de Fahrenheit
temp.fahrenheit = 212
print(f"Temperatura Celsius después de setear Fahrenheit a 212: {temp.celsius}")
print(f"Temperatura Fahrenheit después de setear Fahrenheit a 212: {temp.fahrenheit}")

# Eliminar el atributo (llama al deleter)
del temp.celsius
print(f"Celsius después de 'del': {temp.celsius}")
print(f"Fahrenheit después de 'del celsius': {temp.fahrenheit}")

# Acceso directo al atributo "protegido" (sigue siendo posible, pero evita las properties)
# print(temp._celsius) # Accede al valor directamente

# ===================================================
# 6. Métodos de Clase (@classmethod) y Métodos Estáticos (@staticmethod)
# ===================================================

print("\n--- 6. Métodos de Clase y Estáticos ---")

class ContadorObjetos:
    # Atributo de clase para llevar la cuenta
    numero_instancias = 0

    def __init__(self, nombre):
        self.nombre = nombre
        # Incrementamos el contador de clase cada vez que se crea una instancia
        ContadorObjetos.numero_instancias += 1
        print(f"Creado objeto '{self.nombre}'. Total instancias: {ContadorObjetos.numero_instancias}")

    # --- Método de Instancia (normal) ---
    # Opera sobre la instancia específica (self).
    def quien_soy(self):
        print(f"Soy una instancia llamada {self.nombre}")

    # --- Método de Clase (@classmethod) ---
    # Opera sobre la clase misma, no sobre una instancia específica.
    # Recibe la clase (convencionalmente llamada 'cls') como primer argumento, en lugar de 'self'.
    # Puede acceder y modificar atributos de clase.
    # Se puede llamar desde la clase (NombreClase.metodo()) o desde una instancia (objeto.metodo()).
    @classmethod
    def obtener_contador(cls):
        """Devuelve el número total de instancias creadas de esta clase."""
        # 'cls' se refiere a la clase ContadorObjetos
        print(f"Accediendo al contador desde la clase: {cls.__name__}")
        return cls.numero_instancias

    @classmethod
    def crear_objeto_configurado(cls, config_str):
        """Factory method: Un método de clase usado para crear instancias de forma controlada."""
        # Ejemplo: crear un objeto a partir de un string de configuración
        # 'cls' aquí es ContadorObjetos, así que cls(nombre) llama a ContadorObjetos.__init__(nombre)
        nombre = f"Config-{config_str.upper()}"
        print(f"Usando factory method para crear '{nombre}'")
        return cls(nombre) # Crea y devuelve una instancia de la clase


    # --- Método Estático (@staticmethod) ---
    # No opera ni sobre la instancia (self) ni sobre la clase (cls).
    # Es básicamente una función normal que vive dentro del 'namespace' de la clase.
    # No puede acceder a atributos de instancia ni de clase directamente (a menos que se pasen como argumento).
    # Útil para funciones de utilidad relacionadas lógicamente con la clase, pero que no dependen de su estado.
    # Se puede llamar desde la clase o desde una instancia.
    @staticmethod
    def es_nombre_valido(nombre):
        """Verifica si un nombre es válido (ejemplo simple)."""
        # No necesita self ni cls
        return isinstance(nombre, str) and len(nombre) > 0

# Uso
print(f"Contador inicial (llamado desde la clase): {ContadorObjetos.obtener_contador()}")

obj1 = ContadorObjetos("Alfa")
obj2 = ContadorObjetos("Beta")

obj1.quien_soy() # Método de instancia

# Llamar a método de clase desde la clase y desde la instancia
print(f"Contador actual (llamado desde clase): {ContadorObjetos.obtener_contador()}")
print(f"Contador actual (llamado desde obj1): {obj1.obtener_contador()}") # Funciona igual

# Usar el factory method (método de clase)
obj_config = ContadorObjetos.crear_objeto_configurado("gamma")
obj_config.quien_soy()
print(f"Contador final: {ContadorObjetos.obtener_contador()}")

# Llamar a método estático desde la clase y desde la instancia
print(f"¿'Alfa' es nombre válido? (desde clase): {ContadorObjetos.es_nombre_valido('Alfa')}")
print(f"¿'' es nombre válido? (desde obj1): {obj1.es_nombre_valido('')}")


# --- Uso de @classmethod en Herencia ---
class SubContador(ContadorObjetos):
    # Hereda numero_instancias, __init__, etc.
    # El @classmethod también se hereda y 'cls' se referirá a SubContador
    pass

sub_obj1 = SubContador("SubAlfa")
# obtener_contador() llamado en SubContador devolverá el contador global (porque numero_instancias es de la clase padre)
# Si SubContador tuviera su propio 'numero_instancias', cls.numero_instancias se referiría a ese.
print(f"Contador desde SubContador (llamado desde clase hija): {SubContador.obtener_contador()}") # cls es SubContador, pero usa ContadorObjetos.numero_instancias
print(f"Total global sigue siendo: {ContadorObjetos.numero_instancias}")

# Si el factory method se llama desde la clase hija, crea una instancia de la clase hija
sub_obj_config = SubContador.crear_objeto_configurado("delta")
print(f"Tipo de objeto creado por factory en subclase: {type(sub_obj_config)}") # Es SubContador


# ===================================================
# 7. Herencia Múltiple
# ===================================================
# Una clase puede heredar de más de una clase padre.
# Python resuelve el orden de búsqueda de métodos y atributos usando el MRO (Method Resolution Order).
# El MRO sigue un algoritmo C3 linearization, que asegura un orden consistente y predecible.
# Puede ser potente, pero también compleja (problema del diamante). Usar con precaución.

print("\n--- 7. Herencia Múltiple ---")

class Volador:
    def __init__(self, **kwargs):
        print("Inicializando Volador")
        super().__init__(**kwargs) # Importante para la cooperación en MRO
        self.altitud_maxima = 1000

    def volar(self):
        print("Volando alto...")

class Nadador:
    def __init__(self, **kwargs):
        print("Inicializando Nadador")
        super().__init__(**kwargs) # Importante para la cooperación en MRO
        self.profundidad_maxima = 100

    def nadar(self):
        print("Nadando profundo...")

# Clase que hereda de ambas
class Pato(Volador, Nadador, Animal): # Hereda de Volador, Nadador y Animal (definida antes)
    def __init__(self, nombre, edad, color_pico):
        print("Inicializando Pato")
        # super().__init__ llamará a los __init__ de las clases padre en el orden MRO
        # Pasamos los argumentos necesarios para Animal
        super().__init__(nombre=nombre, edad=edad) # Se pasan como kwargs para que funcionen con **kwargs
        self.color_pico = color_pico

    # Puede sobrescribir métodos de cualquiera de las clases padre
    def sonido(self):
        print("Cuac! Cuac!")

# Instanciación
mi_pato = Pato("Donald", 1, "Naranja")

# Acceso a métodos de todas las clases padre
mi_pato.volar()
mi_pato.nadar()
mi_pato.comer() # Heredado de Animal
mi_pato.sonido() # Sobrescrito en Pato

# Acceso a atributos de las clases padre
print(f"Altitud máxima: {mi_pato.altitud_maxima}")
print(f"Profundidad máxima: {mi_pato.profundidad_maxima}")
print(f"Nombre: {mi_pato.nombre}") # Heredado de Animal vía super()
print(f"Color del pico: {mi_pato.color_pico}") # Propio de Pato

# --- MRO (Method Resolution Order) ---
# Muestra el orden en que Python buscará métodos y atributos.
print("\nMethod Resolution Order (MRO) para Pato:")
print(Pato.__mro__)
# El orden suele ser: Clase actual, Padres (de izquierda a derecha según definición), Abuelos, ..., object.

# --- Problema del Diamante ---
# Ocurre cuando una clase hereda de dos clases que tienen un ancestro común.
# El MRO de Python (C3) está diseñado para manejar esto de forma predecible.
# Ejemplo:
#      A
#     / \
#    B   C
#     \ /
#      D
# El MRO de D sería [D, B, C, A, object] (si D hereda de B, C).

class A:
    def ping(self): print("Ping desde A")
class B(A):
    def ping(self): print("Ping desde B")
class C(A):
    def ping(self): print("Ping desde C")
class D(B, C): # D hereda de B y C
    pass # No define ping

obj_d = D()
obj_d.ping() # Llama a B.ping() porque B está antes que C en el MRO de D.
print(f"MRO de D: {D.__mro__}")


# ===================================================
# 8. Clases Base Abstractas (ABCs - Abstract Base Classes)
# ===================================================
# Permiten definir "interfaces" o contratos que las subclases deben cumplir.
# Una ABC no puede ser instanciada directamente.
# Se definen métodos abstractos que las subclases concretas están obligadas a implementar.
# Útil para asegurar que ciertas clases tengan una estructura o comportamiento común.
# Se usa el módulo `abc` y los decoradores `@abstractmethod`.

print("\n--- 8. Clases Base Abstractas (ABCs) ---")

from abc import ABC, abstractmethod

# Definimos la Clase Base Abstracta heredando de ABC
class FormaGeometrica(ABC):

    def __init__(self, nombre):
        self.nombre = nombre

    @abstractmethod # Marca este método como abstracto
    def area(self):
        """Método abstracto: Calcula el área. Debe ser implementado por subclases."""
        pass # No tiene implementación aquí

    @abstractmethod
    def perimetro(self):
        """Método abstracto: Calcula el perímetro. Debe ser implementado por subclases."""
        pass

    # Las ABCs también pueden tener métodos concretos (no abstractos)
    def describir(self):
        print(f"Soy una forma geométrica llamada '{self.nombre}'.")


# --- Intento de instanciar la ABC (dará error) ---
try:
    forma_abstracta = FormaGeometrica("Abstracta")
except TypeError as e:
    print(f"Error esperado al instanciar ABC: {e}")


# --- Subclase Concreta que implementa los métodos abstractos ---
class Rectangulo(FormaGeometrica):
    def __init__(self, nombre, base, altura):
        super().__init__(nombre)
        self.base = base
        self.altura = altura

    # Implementación OBLIGATORIA de area
    def area(self):
        return self.base * self.altura

    # Implementación OBLIGATORIA de perimetro
    def perimetro(self):
        return 2 * (self.base + self.altura)

# --- Subclase que NO implementa todos los métodos abstractos ---
# Si intentamos instanciarla, también dará error.
class CirculoIncompleto(FormaGeometrica):
    def __init__(self, nombre, radio):
        super().__init__(nombre)
        self.radio = radio

    def area(self):
        import math
        return math.pi * (self.radio ** 2)

    # Falta implementar perimetro()

try:
    circulo_malo = CirculoIncompleto("Incompleto", 5)
except TypeError as e:
    print(f"Error esperado al instanciar clase que no implementa todo: {e}")


# --- Uso de la subclase concreta ---
mi_rectangulo = Rectangulo("Rect-1", 10, 5)
mi_rectangulo.describir() # Método concreto heredado de la ABC
print(f"Área de {mi_rectangulo.nombre}: {mi_rectangulo.area()}")       # Método implementado
print(f"Perímetro de {mi_rectangulo.nombre}: {mi_rectangulo.perimetro()}") # Método implementado


# ===================================================
# 9. Data Classes (@dataclass)
# ===================================================
# Introducidas en Python 3.7 (módulo `dataclasses`).
# Son un decorador que genera automáticamente métodos especiales comunes
# como `__init__`, `__repr__`, `__eq__`, y opcionalmente `__lt__`, `__le__`, etc.
# Muy útil para clases que principalmente almacenan datos.
# Reduce código repetitivo (boilerplate).

print("\n--- 9. Data Classes ---")

from dataclasses import dataclass, field

# El decorador @dataclass procesa la clase
@dataclass(order=True, frozen=False) # order=True genera __lt__, __le__, etc.
                                     # frozen=True haría las instancias inmutables (lanza error si intentas modificar atributos)
class Punto:
    # Los atributos se definen con type hints (anotaciones de tipo)
    x: float
    y: float
    z: float = 0.0 # Se pueden dar valores por defecto

    # field() permite personalizar campos
    # init=False: No incluir en el __init__ generado
    # repr=False: No incluir en el __repr__ generado
    # default_factory: Para valores por defecto mutables (como listas o dicts)
    distancia_origen: float = field(init=False, repr=True) # Calculado después de init
    metadatos: list = field(default_factory=list, repr=False) # Lista vacía por defecto

    # --- __post_init__ ---
    # Método opcional que se ejecuta después del __init__ generado automáticamente.
    # Útil para validaciones o cálculos que dependen de otros campos.
    def __post_init__(self):
        print("Ejecutando __post_init__")
        # Calculamos la distancia al origen
        self.distancia_origen = (self.x**2 + self.y**2 + self.z**2)**0.5
        # Ejemplo de validación
        if self.x < 0 or self.y < 0 or self.z < 0:
             print(f"Advertencia: El punto {self} tiene coordenadas negativas.")


# Creación de instancias (usa el __init__ generado)
p1 = Punto(1.0, 2.0) # z toma el valor por defecto 0.0
p2 = Punto(3.0, 4.0, 5.0, metadatos=['etiqueta1'])
p3 = Punto(1.0, 2.0) # Igual a p1 en valores
p4 = Punto(-1.0, -2.0) # Provocará advertencia en __post_init__

# __repr__ generado automáticamente
print(f"p1: {p1}") # Muestra distancia_origen porque repr=True
print(f"p2: {p2}") # No muestra metadatos porque repr=False

# __eq__ generado automáticamente (compara todos los campos)
print(f"¿p1 == p2? {p1 == p2}") # False
print(f"¿p1 == p3? {p1 == p3}") # True

# Métodos de comparación generados por order=True (comparan campo a campo en orden de definición)
print(f"¿p1 < p2? {p1 < p2}") # True (compara x: 1.0 < 3.0)

# Acceso a atributos
print(f"Coordenada x de p1: {p1.x}")
print(f"Distancia al origen de p2: {p2.distancia_origen}")
print(f"Metadatos de p2: {p2.metadatos}") # Accedemos aunque repr=False

# Modificación de atributos (posible porque frozen=False)
p1.x = 10.0
print(f"p1 modificado: {p1}")
# ¡OJO! La distancia_origen NO se recalcula automáticamente al modificar x, y, z
# Habría que llamar a __post_init__ manualmente o crear métodos que lo hagan.
# p1.__post_init__() # Para recalcular
# print(f"p1 recalculado: {p1}")

# Ejemplo con frozen=True (si estuviera activado)
# @dataclass(frozen=True)
# class PuntoInmutable:
#     x: float
#     y: float
# punto_f = PuntoInmutable(1, 1)
# try:
#      punto_f.x = 5 # Esto lanzaría dataclasses.FrozenInstanceError
# except Exception as e:
#      print(f"Error esperado al modificar instancia frozen: {e}")


# ===================================================
# 10. __slots__
# ===================================================
# Es un atributo de clase especial que permite restringir explícitamente
# los atributos que una instancia puede tener.
# Beneficios principales:
#   1. Ahorro de memoria: Python no crea el diccionario `__dict__` para cada instancia,
#      lo que puede ser significativo si se crean millones de objetos pequeños.
#   2. Previene la creación accidental de nuevos atributos en las instancias.
# Desventajas:
#   - No se pueden añadir nuevos atributos a la instancia dinámicamente.
#   - Complica la herencia (las subclases también deben definir __slots__ si quieren añadir atributos).
#   - No funciona bien con algunas herramientas de introspección o serialización que dependen de __dict__.

print("\n--- 10. __slots__ ---")

class PuntoLigero:
    # Definimos los únicos atributos permitidos para las instancias
    __slots__ = ('x', 'y', '_z') # Se usa una tupla (o lista) de strings

    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self._z = z # Podemos usar nombres "protegidos" en slots

    def __str__(self):
      return f"PuntoLigero(x={self.x}, y={self.y}, z={self._z})"


pt_ligero = PuntoLigero(10, 20)
print(pt_ligero)
print(f"pt_ligero.x = {pt_ligero.x}")

# Intento de añadir un nuevo atributo (fallará)
try:
    pt_ligero.nuevo_atributo = "Esto no funcionará"
except AttributeError as e:
    print(f"Error esperado al añadir atributo no en __slots__: {e}")

# La instancia no tiene __dict__
try:
    print(pt_ligero.__dict__)
except AttributeError as e:
    print(f"Error esperado al acceder a __dict__: {e}")

# Para saber qué atributos tiene, podemos inspeccionar __slots__
print(f"Atributos permitidos por __slots__: {PuntoLigero.__slots__}")

# --- Herencia con __slots__ ---
class Punto3DLigero(PuntoLigero):
    # Si la clase padre tiene __slots__, la hija DEBE definir __slots__
    # para añadir sus propios atributos controlados por slots.
    # Si la clase hija NO define __slots__, tendrá __dict__ y perderá el beneficio de memoria
    # para sus propios atributos (pero los heredados seguirán sin __dict__).
    # Para añadir atributos, se deben incluir los slots del padre si se quiere mantener todo ligero.
    # __slots__ = ('color',) # Solo permitiría 'color', perdería x, y, _z como slots
    # Si no se define __slots__ aquí, Punto3DLigero tendrá __dict__
     __slots__ = ('color',) # Añade 'color' a los atributos gestionados por slots

     def __init__(self, x, y, z, color):
         super().__init__(x, y, z)
         self.color = color

     def __str__(self):
         # Accedemos a los atributos heredados y al nuevo
         return f"Punto3DLigero(x={self.x}, y={self.y}, z={self._z}, color='{self.color}')"


pt3d = Punto3DLigero(1, 2, 3, 'rojo')
print(pt3d)
print(f"Color: {pt3d.color}")
print(f"X: {pt3d.x}") # Accede al atributo heredado

# Intento de añadir atributo no permitido (ni en padre ni en hijo)
try:
    pt3d.etiqueta = "prueba"
except AttributeError as e:
    print(f"Error esperado en subclase con __slots__: {e}")

# Si Punto3DLigero NO hubiera definido __slots__, lo siguiente funcionaría:
# pt3d.etiqueta = "prueba" # Funcionaría y se guardaría en pt3d.__dict__


# ===================================================
# 11. Sobrecarga de Operadores (Más Ejemplos)
# ===================================================
# Ya vimos `__str__`, `__repr__`, `__len__`, `__eq__`, `__add__`.
# Python permite sobrecargar la mayoría de los operadores definiendo
# los métodos especiales correspondientes.

print("\n--- 11. Sobrecarga de Operadores (Más Ejemplos) ---")

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    # --- Operadores Aritméticos ---
    def __add__(self, other): # self + other
        if isinstance(other, Vector2D):
            return Vector2D(self.x + other.x, self.y + other.y)
        return NotImplemented # Muy importante devolver esto si no se soporta

    def __sub__(self, other): # self - other
        if isinstance(other, Vector2D):
            return Vector2D(self.x - other.x, self.y - other.y)
        return NotImplemented

    def __mul__(self, scalar): # self * scalar
        if isinstance(scalar, (int, float)):
            return Vector2D(self.x * scalar, self.y * scalar)
        return NotImplemented

    # --- Operador Reflejado ---
    # Se usa cuando el objeto está a la DERECHA del operador (ej. 3 * vector)
    def __rmul__(self, scalar): # scalar * self
        print("Llamando a __rmul__")
        # A menudo, simplemente llama a la versión normal __mul__
        return self.__mul__(scalar)

    # --- Operador Aumentado (in-place) ---
    def __iadd__(self, other): # self += other
        if isinstance(other, Vector2D):
            print("Llamando a __iadd__ (modifica self)")
            self.x += other.x
            self.y += other.y
            return self # Debe retornar self
        return NotImplemented

    # --- Operadores de Comparación ---
    # __eq__ (==), __ne__ (!=), __lt__ (<), __le__ (<=), __gt__ (>), __ge__ (>=)
    # Si defines __eq__ y __lt__, Python puede inferir los otros (o puedes definirlos explícitamente)
    # Ejemplo: comparar por magnitud
    def __abs__(self): # abs(self) - Magnitud del vector
        return (self.x**2 + self.y**2)**0.5

    def __eq__(self, other): # self == other
        if isinstance(other, Vector2D):
            return self.x == other.x and self.y == other.y
        return NotImplemented

    def __lt__(self, other): # self < other (basado en magnitud)
        if isinstance(other, Vector2D):
            return abs(self) < abs(other)
        return NotImplemented

    # --- Acceso a Elementos (como secuencia o diccionario) ---
    def __len__(self): # len(self)
        return 2 # Un vector 2D tiene 2 componentes

    def __getitem__(self, index): # self[index]
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Índice de Vector2D fuera de rango (0 o 1)")

    def __setitem__(self, index, value): # self[index] = value
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        else:
            raise IndexError("Índice de Vector2D fuera de rango (0 o 1)")


# --- Uso de vectores con operadores sobrecargados ---
v1 = Vector2D(1, 2)
v2 = Vector2D(3, 4)
v3 = Vector2D(1, 2) # Igual a v1

print(f"v1: {v1}, v2: {v2}")

# Aritmética
suma = v1 + v2
print(f"v1 + v2 = {suma}")
resta = v2 - v1
print(f"v2 - v1 = {resta}")
prod_escalar = v1 * 3
print(f"v1 * 3 = {prod_escalar}")
prod_reflejado = 2 * v2 # Llama a v2.__rmul__(2)
print(f"2 * v2 = {prod_reflejado}")

# Aumentada (modifica v1)
print(f"v1 antes de += v2: {v1}")
v1 += v2 # Llama a v1.__iadd__(v2)
print(f"v1 después de += v2: {v1}")

# Comparación
print(f"Magnitud de v1: {abs(v1)}") # abs() llama a __abs__
print(f"Magnitud de v2: {abs(v2)}")
print(f"¿v1 == v2? {v1 == v2}") # False
print(f"¿v1 == v3? {v1 == v3}") # False (porque v1 fue modificado por +=)
v1_orig = Vector2D(1,2)
print(f"¿v1_orig == v3? {v1_orig == v3}") # True
print(f"¿v1 < v2? {v1 < v2}") # False (v1 tiene mayor magnitud ahora)
print(f"¿v1_orig < v2? {v1_orig < v2}") # True

# Acceso a elementos
print(f"Número de componentes de v2 (len): {len(v2)}")
print(f"Componente x de v2 (v2[0]): {v2[0]}")
print(f"Componente y de v2 (v2[1]): {v2[1]}")
# print(v2[2]) # Lanzaría IndexError

# Modificación de elementos
print(f"v2 antes de setitem: {v2}")
v2[0] = 10 # Llama a v2.__setitem__(0, 10)
v2[1] = 20
print(f"v2 después de setitem: {v2}")


# ===================================================
# 12. Context Managers (__enter__ y __exit__)
# ===================================================
# Permiten implementar objetos que pueden ser usados con la sentencia `with`.
# `with` garantiza que ciertos recursos (como archivos, conexiones de red, locks)
# se configuren y se liberen correctamente, incluso si ocurren errores.
# Se implementan los métodos `__enter__` y `__exit__`.

print("\n--- 12. Context Managers ---")

class GestorDeRecurso:
    def __init__(self, nombre_recurso):
        self.nombre = nombre_recurso
        self.recurso = None
        print(f"Inicializando Gestor para '{self.nombre}'")

    # --- __enter__ ---
    # Se ejecuta al entrar en el bloque `with`.
    # Debe devolver el objeto que será asignado a la variable después de `as` (si se usa).
    # Es donde se adquiere o configura el recurso.
    def __enter__(self):
        print(f"Entrando al contexto (__enter__): Adquiriendo recurso '{self.nombre}'...")
        # Simular adquisición de recurso (ej. abrir archivo, conectar a DB)
        self.recurso = f"Datos del recurso {self.nombre}"
        print("Recurso adquirido.")
        return self # Devolvemos la instancia del gestor

    # --- __exit__ ---
    # Se ejecuta al salir del bloque `with`, ya sea normalmente o por una excepción.
    # Recibe tres argumentos: tipo de excepción, valor de excepción, traceback.
    # Si no hubo excepción, los tres argumentos son None.
    # Es donde se libera o limpia el recurso.
    # Si __exit__ devuelve True, la excepción (si la hubo) se considera manejada y se suprime.
    # Si devuelve False o None (por defecto), la excepción se propaga fuera del bloque `with`.
    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"\nSaliendo del contexto (__exit__) para '{self.nombre}'...")
        # Simular liberación de recurso
        print(f"Liberando recurso '{self.nombre}'...")
        self.recurso = None # Marcar como liberado

        if exc_type:
            print(f"*** Ocurrió una excepción dentro del bloque 'with' ***")
            print(f"Tipo: {exc_type}")
            print(f"Valor: {exc_val}")
            # print(f"Traceback: {exc_tb}") # Suele ser largo
            print("El recurso se ha liberado igualmente.")
            # Decidimos si suprimir (True) o propagar (False) la excepción
            # return True # Suprimir la excepción
            return False # Propagar la excepción (comportamiento normal)
        else:
            print("Salida limpia del contexto (sin excepciones).")
            # No es necesario retornar nada (equivale a None/False), pero True también es válido si no hubo error.
            return True

# --- Uso del Context Manager ---
print("\n--- Ejemplo 1: Uso normal ---")
try:
    with GestorDeRecurso("Archivo Temporal") as gestor:
        print("\n--- Dentro del bloque 'with' ---")
        print(f"Usando el recurso gestionado: {gestor.recurso}")
        print(f"El nombre del gestor es: {gestor.nombre}")
        # Simulamos trabajo con el recurso...
        print("Trabajo completado.")
        # Al salir de aquí, se llamará a __exit__ automáticamente
    print("--- Fuera del bloque 'with' (ejecución normal) ---")
    # El recurso ya debería estar liberado
    # print(f"Intentando acceder al recurso fuera del with: {gestor.recurso}") # Sería None

except Exception as e:
    print(f"Se capturó una excepción fuera del with: {e}")


print("\n--- Ejemplo 2: Uso con excepción ---")
try:
    with GestorDeRecurso("Conexión DB") as gestor_db:
        print("\n--- Dentro del bloque 'with' (DB) ---")
        print(f"Recurso DB: {gestor_db.recurso}")
        # Simulamos un error
        resultado = 10 / 0
        print("Esta línea no se ejecutará.") # No llega aquí
    print("--- Fuera del bloque 'with' (DB) - No debería llegar aquí si hay error no suprimido ---")

except ZeroDivisionError as e:
    print(f"\n--- Excepción capturada FUERA del 'with' (DB) ---")
    print(f"Error capturado: {e}")
    # __exit__ se ejecutó igualmente para liberar el recurso, pero la excepción se propagó.

# También existe el módulo `contextlib` que ofrece utilidades para crear
# context managers de forma más concisa, por ejemplo, usando generadores
# con `@contextmanager`.

# ===================================================
# CONCLUSIÓN
# ===================================================
"""
Este recorrido cubre los aspectos fundamentales y muchos avanzados de las clases
en Python. La Programación Orientada a Objetos es un paradigma poderoso para
organizar y estructurar código complejo, promoviendo la reutilización,
mantenibilidad y escalabilidad.

Conceptos clave repasados:
- Definición de Clases, Atributos (de clase e instancia), Métodos (de instancia).
- Constructor `__init__` y `self`.
- Métodos Especiales (Dunder/Magic) para sobrecarga de operadores y comportamiento incorporado (`__str__`, `__repr__`, `__len__`, etc.).
- Herencia (Simple y Múltiple), `super()`, MRO, Sobrescritura de métodos.
- Encapsulación (convenciones `_` y `__` para protected/private).
- Properties (`@property`, `@setter`, `@deleter`) para control de acceso y lógica en atributos.
- Métodos de Clase (`@classmethod`) y Estáticos (`@staticmethod`).
- Clases Base Abstractas (ABCs) con `@abstractmethod` para definir interfaces.
- Data Classes (`@dataclass`) para reducir boilerplate en clases de datos.
- `__slots__` para optimización de memoria y restricción de atributos.
- Context Managers (`__enter__`, `__exit__`) para gestión de recursos con `with`.

Dominar estos conceptos te permitirá escribir código Python más robusto,
flexible y elegante. ¡La práctica constante es la clave!
"""
print("\n--- Fin de los apuntes sobre Clases en Python ---")