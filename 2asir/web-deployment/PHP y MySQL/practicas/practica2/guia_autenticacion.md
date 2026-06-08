# Guía Paso a Paso: Sistema de Autenticación y Roles

Esta guía detalla cómo implementar un sistema de seguridad completo para tu práctica de Biblioteca Escolar, aprovechando la estructura que ya tienes en la carpeta `conexion/`.

---

## Paso 1: Preparación de la Base de Datos

Actualmente, tu tabla `Estudiantes` no tiene una columna para distinguir entre administradores (profesores) y alumnos.

Ejecuta esta sentencia SQL en tu gestor de base de datos (phpMyAdmin o MySQL Workbench):

```sql
ALTER TABLE Estudiantes ADD COLUMN rol ENUM('usuario', 'admin') DEFAULT 'usuario' AFTER password;

-- Opcional: Convertir a un usuario existente en administrador para pruebas
UPDATE Estudiantes SET rol = 'admin' WHERE id_estudiante = 1; 
```

---

## Paso 2: Corrección y Configuración (database_config.php)

He notado que tu archivo de configuración tiene una extensión duplicada: `database_config.php.php`. 

1. **Renombra** el archivo a `database_config.php`.
2. **Asegúrate** de que los datos de conexión sean correctos (especialmente la contraseña, que en `conexion.php` es `rootroot` pero en el config está vacía).

```php
// database_config.php
define('DB_HOST', 'localhost');
define('DB_USER', 'root');
define('DB_PASS', 'rootroot'); // Cambia según tu configuración
define('DB_NAME', 'biblioteca_escolar');
```

---

## Paso 3: Completar el Registro de Usuarios (`procesar_registro.php`)

Debes capturar los datos del formulario de `registro.php` y guardarlos cifrando la contraseña.

**Lógica sugerida:**
- Si el "Curso" seleccionado es "Profesor", asígnale `rol = 'admin'`.
- De lo contrario, `rol = 'usuario'`.

```php
// Ejemplo de lógica en procesar_registro.php
$pass_cifrada = password_hash($_POST['password'], PASSWORD_DEFAULT);
$rol = ($_POST['curso'] == 'Profesor') ? 'admin' : 'usuario';

$sql = "INSERT INTO Estudiantes (nombre, apellidos, codigo_estudiante, curso, telefono, password, rol) 
        VALUES ('$nombre', '$apellidos', '$codigo', '$curso', '$telefono', '$pass_cifrada', '$rol')";
```

---

## Paso 4: Completar el Inicio de Sesión (`procesar_login.php`)

En este archivo debes verificar que el usuario exista y que la contraseña coincida.

```php
// Ejemplo de lógica en procesar_login.php
$email = $_POST['email']; // O código_estudiante
$password = $_POST['password'];

// 1. SELECT * FROM Estudiantes WHERE email = ...
// 2. Verificar contraseña:
if (password_verify($password, $user_db['password'])) {
    session_start();
    $_SESSION['id_usuario'] = $user_db['id_estudiante'];
    $_SESSION['nombre'] = $user_db['nombre'];
    $_SESSION['rol'] = $user_db['rol'];
    header("Location: ../index.php");
}
```

---

## Paso 5: Protección de Rutas (Control de Roles)

Utiliza las funciones que ya tienes en `database_config.php` al principio de cada página que quieras proteger.

### Para páginas que solo puede ver el Administrador:
(Ejemplo: `libros_borrar.php`, gestión de estudiantes, etc.)

```php
<?php
require_once '../conexion/database_config.php';
requerirRol('admin'); // Si no es admin, redirige al index
?>
```

### Para páginas que requieren estar logueado (Cualquier rol):
```php
<?php
require_once '../conexion/database_config.php';
if (!estaLogueado()) {
    header("Location: ../conexion/login.html");
    exit();
}
?>
```

---

## Paso 6: Actualización de la Interfaz (`header.php` o `index.php`)

Modifica tu menú de navegación para mostrar opciones según el rol.

```php
<nav class="main-menu">
    <a href="index.php">Inicio</a>
    <a href="libros/libros.html">Libros</a>
    
    <?php if (isset($_SESSION['rol']) && $_SESSION['rol'] === 'admin'): ?>
        <!-- Solo admins ven esto -->
        <a href="estudiantes/estudiantes.html">Gestionar Estudiantes</a>
    <?php endif; ?>

    <?php if (isset($_SESSION['id_usuario'])): ?>
        <a href="conexion/logout.php">Cerrar Sesión (<?php echo $_SESSION['nombre']; ?>)</a>
    <?php else: ?>
        <a href="conexion/login.html">Iniciar Sesión</a>
    <?php endif; ?>
</nav>
```

---

## Paso 7: Implementar el Cierre de Sesión (`logout.php`)

Simplemente destruye la sesión y redirige.

```php
<?php
session_start();
session_destroy();
header("Location: ../index.php");
exit();
?>
```

---

### Consejos de Seguridad:
1. **Sanitización**: Usa la función `sanear()` que tienes definida en `database_config.php` para evitar Inyecciones SQL.
2. **Password Hashing**: Nunca guardes contraseñas en texto plano. Usa siempre `password_hash()` y `password_verify()`.
3. **Prepared Statements**: Para mayor seguridad, considera usar `mysqli_prepare` en lugar de concatenar variables en los strings de SQL.
