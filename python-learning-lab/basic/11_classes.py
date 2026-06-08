# Clase en vídeo: https://youtu.be/Kp4Mvapo5kc?t=29327

### Classes ###

# Definición de una clase vacía usando el keyword 'pass'
class MyEmptyPerson:
    pass  # Permite dejar la clase vacía sin errores

print(MyEmptyPerson)  # Muestra la referencia de la clase
print(MyEmptyPerson())  # Crea una instancia de la clase y la muestra

# Definición de la clase Person
class Person:
    # El método __init__ es el constructor de la clase, se ejecuta automáticamente al crear una nueva instancia.
    def __init__(self, name, surname, alias="Sin alias"):
        # self.full_name es una propiedad pública que combina el nombre, apellido y alias de la persona.
        self.full_name = f"{name} {surname} ({alias})"
        # self.__name es una propiedad privada que almacena solo el nombre de la persona.
        self.__name = name

    # Método para obtener el valor de la propiedad privada '__name'
    def get_name(self):
        # Este método devuelve el valor de la propiedad privada __name.
        return self.__name

    # Método para simular que la persona está caminando
    def walk(self):
        # Imprime un mensaje indicando que la persona está caminando.
        print(f"{self.full_name} está caminando")


# Creación de una instancia de la clase Person sin alias
my_person = Person("Brais", "Moure")
# Acceso a la propiedad pública full_name y muestra su valor.
print(my_person.full_name)  # Salida: "Brais Moure (Sin alias)"
# Uso del método get_name() para obtener el valor de la propiedad privada __name.
print(my_person.get_name())  # Salida: "Brais"
# Llamada al método walk() para mostrar que la persona está caminando.
my_person.walk()  # Salida: "Brais Moure (Sin alias) está caminando"

# Creación de una instancia de la clase Person con alias
my_other_person = Person("Brais", "Moure", "MoureDev")
# Muestra el valor de la propiedad pública full_name para la nueva instancia.
print(my_other_person.full_name)  # Salida: "Brais Moure (MoureDev)"
# Llamada al método walk() para mostrar que la persona está caminando.
my_other_person.walk()  # Salida: "Brais Moure (MoureDev) está caminando"

# Modificación de la propiedad pública full_name de la instancia my_other_person.
my_other_person.full_name = "Héctor de León (El loco de los perros)"
# Muestra el nuevo valor de la propiedad pública full_name.
print(my_other_person.full_name)  # Salida: "Héctor de León (El loco de los perros)"

# Asignación de un valor no esperado a la propiedad pública full_name.
my_other_person.full_name = 666
# Muestra el valor inesperado asignado a la propiedad pública full_name.
print(my_other_person.full_name)  # Salida: 666

# Definición de una clase Character con múltiples propiedades
class Character:
    def __init__(self, health, damage, speed):
        self.health = health  # Propiedad pública de salud
        self.damage = damage  # Propiedad pública de daño
        self.speed = speed  # Propiedad pública de velocidad

# Creación de instancias de la clase Character
warrior = Character(50, 30, 10)
ninja = Character(20, 20, 50)

# Muestra la propiedad 'speed' de cada instancia
print(f"warrior speed: {warrior.speed}")
print(f"ninja speed: {ninja.speed}")

# Clases adicionales para completar la información

# Herencia: Crear una clase que hereda de otra
class Student(Person):
    def __init__(self, name, surname, alias="Sin alias", student_id=None):
        super().__init__(name, surname, alias)  # Llama al constructor de la clase base
        self.student_id = student_id  # Nueva propiedad específica de Student

    # Método adicional específico de la clase Student
    def study(self):
        print(f"{self.full_name} está estudiando")

# Creación de una instancia de Student
student = Student("Juan", "Pérez", "Estudioso", "12345")
print(student.full_name)
print(student.student_id)
student.study()

# Polimorfismo: uso del mismo método en diferentes clases
class Dog:
    def speak(self):
        return "Woof!"

class Cat:
    def speak(self):
        return "Meow!"

# Uso de polimorfismo
animals = [Dog(), Cat()]
for animal in animals:
    print(animal.speak())  # Llama al método speak() de cada clase

# Encapsulamiento: protección de datos sensibles
class BankAccount:
    def __init__(self, account_number, balance):
        self.__account_number = account_number  # Propiedad privada
        self.__balance = balance  # Propiedad privada

    # Método público para obtener el balance
    def get_balance(self):
        return self.__balance

    # Método público para depositar dinero
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            return True
        return False

    # Método público para retirar dinero
    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
            return True
        return False

# Creación de una instancia de BankAccount
account = BankAccount("123-456-789", 1000)
print(account.get_balance())  # Muestra el balance actual
account.deposit(500)  # Deposita dinero
print(account.get_balance())  # Muestra el nuevo balance
account.withdraw(200)  # Retira dinero
print(account.get_balance())  # Muestra el balance después del retiro

'''
### Ejercicio 1: Sistema de Gestión de Libros

**Objetivo**: Crear un sistema simple para gestionar una colección de libros, incluyendo funcionalidades de herencia y encapsulamiento.

**Instrucciones**:

1. Define una clase `Book` con propiedades públicas y privadas, y métodos para acceder a ellas.
2. Crea una clase `Library` que contenga una lista de libros y tenga métodos para añadir, eliminar y buscar libros.
3. Utiliza herencia para crear una clase `EBook` que herede de `Book` y añada propiedades específicas de libros electrónicos, 
   como tamaño de archivo y formato.
4. Implementa polimorfismo en un método `display_info()` para que `Book` y `EBook` muestren su información de manera diferente.
'''

class Book:
    def __init__(self, title, author, publication_year):
        self.title = title  # Propiedad pública
        self.author = author  # Propiedad pública
        self.__publication_year = publication_year  # Propiedad privada

    def get_publication_year(self):
        return self.__publication_year

    def display_info(self):
        return f"Book: {self.title}, Author: {self.author}, Year: {self.get_publication_year()}"


class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def remove_book(self, title):
        self.books = [book for book in self.books if book.title != title]

    def find_book(self, title):
        for book in self.books:
            if book.title == title:
                return book
        return None

    def display_books(self):
        for book in self.books:
            print(book.display_info())


class EBook(Book):
    def __init__(self, title, author, publication_year, file_size, file_format):
        super().__init__(title, author, publication_year)
        self.file_size = file_size
        self.file_format = file_format

    def display_info(self):
        return f"EBook: {self.title}, Author: {self.author}, Year: {self.get_publication_year()}, Size: {self.file_size}MB, Format: {self.file_format}"


# Ejemplo de uso
library = Library()

book1 = Book("Don Quijote", "Miguel de Cervantes", 1605)
ebook1 = EBook("El Principito", "Antoine de Saint-Exupéry", 1943, 5, "PDF")

library.add_book(book1)
library.add_book(ebook1)

library.display_books()

library.remove_book("Don Quijote")

library.display_books()

'''
### Ejercicio 2: Sistema de Gestión de Tareas

**Objetivo**: Crear un sistema de gestión de tareas que utilice clases con propiedades públicas y privadas, y métodos, 
              además de herencia y polimorfismo.

**Instrucciones**:

1. Define una clase `Task` con propiedades como `title`, `description`, `status` y `priority`, algunas de las cuales deben ser privadas.
2. Crea métodos para acceder y modificar estas propiedades.
3. Define una clase `TaskManager` para manejar una lista de tareas, incluyendo métodos para añadir, eliminar y actualizar tareas.
4. Usa herencia para crear una clase `SubTask` que herede de `Task` y añada propiedades específicas.
5. Implementa polimorfismo para el método `display_info()` en `Task` y `SubTask`.
'''

class Task:
    def __init__(self, title, description, priority):
        self.title = title
        self.description = description
        self.__status = "Pending"  # Propiedad privada
        self.priority = priority

    def get_status(self):
        return self.__status

    def set_status(self, status):
        if status in ["Pending", "In Progress", "Completed"]:
            self.__status = status

    def display_info(self):
        return f"Task: {self.title}, Description: {self.description}, Status: {self.get_status()}, Priority: {self.priority}"


class TaskManager:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def remove_task(self, title):
        self.tasks = [task for task in self.tasks if task.title != title]

    def update_task_status(self, title, status):
        task = self.find_task(title)
        if task:
            task.set_status(status)

    def find_task(self, title):
        for task in self.tasks:
            if task.title == title:
                return task
        return None

    def display_tasks(self):
        for task in self.tasks:
            print(task.display_info())


class SubTask(Task):
    def __init__(self, title, description, priority, parent_task):
        super().__init__(title, description, priority)
        self.parent_task = parent_task

    def display_info(self):
        return f"SubTask: {self.title}, Description: {self.description}, Status: {self.get_status()}, Priority: {self.priority}, Parent Task: {self.parent_task.title}"


# Ejemplo de uso
task_manager = TaskManager()

task1 = Task("Learn Python", "Complete Python course on Udemy", "High")
subtask1 = SubTask("Learn OOP", "Finish OOP section", "High", task1)

task_manager.add_task(task1)
task_manager.add_task(subtask1)

task_manager.display_tasks()

task_manager.update_task_status("Learn Python", "In Progress")

task_manager.display_tasks()