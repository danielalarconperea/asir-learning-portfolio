# Proyecto Sugerido: Sistema de Gestión Bibliotecaria POO

Después de estudiar los scripts de este kit, estás listo para construir algo real.
Aquí tienes una propuesta de proyecto para consolidar tus conocimientos de PHP Orientado a Objetos.

## La Idea: "BiblioTech Core"
Un sistema de gestión de backend para bibliotecas escolares, diseñado 100% con clases, abandonando el código espagueti procedural.

## ¿Por qué mola?
Es el siguiente paso natural en tu aprendizaje. La mayoría de frameworks modernos (Laravel, Symfony) funcionan así. Si construyes esto, entenderás cómo funcionan las "piezas de lego" del software profesional.

## Características a Implementar (Roadmap)

### Fase 1: Clases Base (Modelos)
- Crear una clase abstracta `Recurso` (propiedades: id, título, fecha).
- Crear clases hijas `Libro` (añade ISBN, autor) y `Revista` (añade número de edición).
- Usar **Traits** para funcionalidades compartidas como `Logueable` (poder guardar acciones en un archivo de texto).

### Fase 2: Gestión (Controladores)
- Clase `Biblioteca`:
    - Propiedad privada `$catalogo` (array de objetos).
    - Método `agregarRecurso(Recurso $r)`.
    - Método `buscarPorTitulo($string)`.
    - Método `prestar($id)`.

### Fase 3: Persistencia (Simulada o Real)
- Crear una interfaz `Almacenable` con métodos `guardar()` y `cargar()`.
- Implementar una clase `GestorJSON` que implemente esa interfaz para guardar tus objetos en un archivo `.json`.

## Reto Extra (Nivel Dios)
Implementa un sistema de **Excepciones Personalizadas**.
- Crea una clase `RecursoNoEncontradoException`.
- Lanza esta excepción cuando busques un libro que no existe y captúrala con `try/catch` para mostrar un mensaje amigable.

---
¡Ánimo! La POO cambia tu forma de pensar, pero una vez haces "clic", no querrás programar de otra forma.
