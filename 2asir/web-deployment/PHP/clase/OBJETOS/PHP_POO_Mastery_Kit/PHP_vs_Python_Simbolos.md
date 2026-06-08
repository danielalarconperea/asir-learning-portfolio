# Guía de Símbolos: PHP vs Python

Aquí tienes una tabla comparativa y explicación detallada de los símbolos "raros" de PHP y su equivalente en Python. ¡Verás que no son tan distintos una vez entiendes la lógica!

## Tabla Rápida

| Símbolo PHP | Qué hace en PHP | Equivalente Python | Ejemplo |
| :--- | :--- | :--- | :--- |
| **`$`** | Inicio de variable | *(Nada)* | `$x = 1` vs `x = 1` |
| **`->`** | Acceder a propiedad/método de **OBJETO** | **`.`** | `$obj->met()` vs `obj.met()` |
| **`=>`** | Asignar valor en Array Asociativo (Diccionario) | **`:`** | `['a' => 1]` vs `{'a': 1}` |
| **`::`** | Acceder a elemento **ESTÁTICO** de Clase | **`.`** | `Clase::met()` vs `Clase.met()` |
| **`.`** | Concatenar (unir) textos | **`+`** | `'a' . 'b'` vs `'a' + 'b'` |

---

## Explicación Detallada

### 1. El Operador de Objeto (`->` vs `.`)
En PHP, el punto `.` ya estaba ocupado para unir textos (historia antigua), así que tuvieron que inventarse una flecha `->` para acceder a las cosas de dentro de un objeto.

*   **PHP:** "Oye objeto, ve hacia (`->`) tu método ejecutar".
*   **Python:** "Del objeto, dame el punto (`.`) método ejecutar".

```php
// PHP
$usuario->guardar();
$usuario->nombre;
```
```python
# Python
usuario.guardar()
usuario.nombre
```

### 2. El Operador de Asociación (`=>` vs `:`)
Se usa EXCLUSIVAMENTE al definir **Arrays Asociativos** (lo que en Python son Diccionarios). Es la flecha que dice "esta clave APUNTA A este valor".

*   **PHP:** `Array(Clave => Valor)`
*   **Python:** `Dict{Clave : Valor}`

```php
// PHP
$datos = [
    "nombre" => "Juan",
    "edad" => 25
];
```
```python
# Python
datos = {
    "nombre": "Juan",
    "edad": 25
}
```

### 3. El Operador de Resolución de Ámbito (`::`)
Este asusta, pero fácil. Se usa cuando quieres llamar a algo que pertenece a la **CLASE** y no a un objeto concreto (cosas estáticas o constantes). En Python no existe distinción, se usa el punto `.` para todo.

*   **PHP:** Usa `::` para cosas estáticas (Static) o constantes (Const).
*   **Python:** Usa `.` para todo.

```php
// PHP
User::encontrar(1); // Método estático
echo User::ROL_ADMIN; // Constante
```
```python
# Python
User.encontrar(1) # Método estático (@staticmethod)
print(User.ROL_ADMIN) # Variable de clase
```

### 4. El Dólar (`$`)
PHP necesita el `$` para saber que algo es una variable. Si no lo pones, PHP cree que es una constante o una función. Python es más "listo" (o mágico) y lo deduce solo.

---

### Resumen Mental
*   Si unes texto: `.`
*   Si tocas un objeto: `->`
*   Si defines un array clave-valor: `=>`
*   Si tocas algo estático de una clase: `::`
