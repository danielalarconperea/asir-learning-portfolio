# 📔 Apuntes de PHP y MySQL

Este documento resume los conceptos, funciones y estructuras utilizadas en el desarrollo de aplicaciones web con PHP y MySQL, basándose en los ejercicios de la carpeta.

---

## 🗄️ 1. Fundamentos de MySQL (SQL)

### Crear Base de Datos y Tablas
```sql
-- Crear base de datos
CREATE DATABASE IF NOT EXISTS biblioteca_escolar;
USE biblioteca_escolar;

-- Ejemplo de creación de tabla con claves primarias y foráneas
CREATE TABLE Libros (
    id_libro INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    titulo VARCHAR(100),
    autor VARCHAR(100),
    disponible BOOLEAN DEFAULT true,
    PRIMARY KEY(id_libro)
);

CREATE TABLE Prestamos (
    id_prestamo INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    id_estudiante INTEGER UNSIGNED,
    id_libro INTEGER UNSIGNED,
    fecha_prestamo DATETIME,
    PRIMARY KEY(id_prestamo),
    -- Claves foráneas con borrado en cascada
    FOREIGN KEY (id_estudiante) REFERENCES Estudiantes(id_estudiante) ON DELETE CASCADE,
    FOREIGN KEY (id_libro) REFERENCES Libros(id_libro) ON DELETE CASCADE
);
```

### Consultas Básicas
- **Insertar**: `INSERT INTO Tabla (col1, col2) VALUES ('val1', 'val2');`
- **Seleccionar**: `SELECT * FROM Tabla WHERE condicion;`
- **Actualizar**: `UPDATE Tabla SET col1 = 'nuevo_val' WHERE id = 1;`
- **Borrar**: `DELETE FROM Tabla WHERE id = 1;`
- **Búsqueda parcial**: `SELECT * FROM Tabla WHERE nombre LIKE '%texto%';`

---

## 🐘 2. Conexión PHP a MySQL (mysqli)

Para conectar PHP con MySQL se utiliza la extensión `mysqli`.

### Establecer Conexión
```php
<?php
$host = "localhost";
$user = "root";
$pass = "asdf";
$db   = "biblioteca_escolar";

// Crear conexión
$conexion = mysqli_connect($host, $user, $pass, $db);

// Comprobar conexión
if (!$conexion) {
    die("Error de conexión: " . mysqli_connect_error());
}

// Configurar charset para evitar problemas con tildes y ñ
mysqli_set_charset($conexion, "utf8mb4");
?>
```

---

## 📝 3. Operaciones CRUD en PHP

### A. Listar Datos (Read)
```php
$consulta = "SELECT * FROM Estudiantes";
$resultado = mysqli_query($conexion, $consulta);

if (mysqli_num_rows($resultado) > 0) {
    while ($fila = mysqli_fetch_assoc($resultado)) {
        echo "Nombre: " . $fila['nombre'] . "<br>";
        echo "Email: " . $fila['email'] . "<hr>";
    }
} else {
    echo "No hay registros.";
}
```

### B. Insertar Datos (Create)
Desde un formulario con `method="post"`:
```php
if (isset($_POST["enviar"])) {
    // Escapar datos para seguridad
    $nombre = mysqli_real_escape_string($conexion, $_POST["nombre"]);
    $curso  = mysqli_real_escape_string($conexion, $_POST["curso"]);

    $sql = "INSERT INTO Estudiantes (nombre, curso) VALUES ('$nombre', '$curso')";

    if (mysqli_query($conexion, $sql)) {
        echo "Registro guardado con éxito.";
    } else {
        echo "Error: " . mysqli_error($conexion);
    }
}
```

### C. Modificar Datos (Update)
```php
$id = $_POST['id_estudiante'];
$nuevo_nombre = mysqli_real_escape_string($conexion, $_POST['nombre']);

$sql = "UPDATE Estudiantes SET nombre = '$nuevo_nombre' WHERE id_estudiante = '$id'";

if (mysqli_query($conexion, $sql)) {
    echo "Actualizado correctamente.";
}
```

### D. Borrar Datos (Delete)
```php
$id = $_GET['id'];
$sql = "DELETE FROM Estudiantes WHERE id_estudiante = '$id'";

if (mysqli_query($conexion, $sql)) {
    echo "Registro eliminado.";
}
```

---

## 🔐 4. Seguridad y Buenas Prácticas

### Evitar Inyección SQL
Utilizar siempre `mysqli_real_escape_string()` antes de insertar variables en una consulta SQL.
```php
$limpio = mysqli_real_escape_string($conexion, $_POST['sucio']);
```

### Gestión de Errores
- `mysqli_error($conexion)`: Devuelve la descripción del último error.
- `die()`: Detiene la ejecución del script mostrando un mensaje.

---

## 🚀 5. Sesiones en PHP

Las sesiones permiten mantener datos del usuario a través de diferentes páginas.

```php
// 1. Iniciar sesión (debe ser lo primero en el archivo)
session_start();

// 2. Guardar datos en la sesión
$_SESSION['usuario'] = "Juan";
$_SESSION['rol'] = "admin";

// 3. Acceder a datos
if (isset($_SESSION['usuario'])) {
    echo "Bienvenido, " . $_SESSION['usuario'];
}

// 4. Cerrar sesión
session_unset(); // Libera las variables
session_destroy(); // Destruye la sesión
```

---

## 🛠️ 6. Funciones Imprescindibles

| Función | Descripción |
|---------|-------------|
| `mysqli_connect()` | Abre una conexión al servidor MySQL. |
| `mysqli_query()` | Realiza una consulta a la base de datos. |
| `mysqli_fetch_assoc()` | Devuelve una fila de resultado como array asociativo. |
| `mysqli_num_rows()` | Devuelve el número de filas de un resultado. |
| `mysqli_real_escape_string()` | Escapa caracteres especiales en una cadena para SQL. |
| `mysqli_close()` | Cierra una conexión previamente abierta. |
| `isset()` | Comprueba si una variable está definida y no es null. |
| `header("Location: url")` | Redirecciona a otra página. |

---

*Apuntes generados automáticamente basados en el contenido de la carpeta PHP y MySQL.*
