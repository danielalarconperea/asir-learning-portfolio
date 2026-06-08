# 🔐 PROMPT: Implementación Sistema de Autenticación y Roles - Biblioteca Escolar (Fase 2)

## 📋 CONTEXTO DEL PROYECTO

Tengo una práctica PHP/MySQL de gestión de biblioteca escolar **ya funcional** (Fase 1 completada) ubicada en:
```
c:\Users\2asir-01\OneDrive - Salesianos Atocha\Escritorio\PROGRAM\2ASIR\Implantacion aplicaciones web\PHP y MySQL\practicas\practica2_completa\
```

### Estado Actual (Fase 1 - Completada):
- ✅ CRUD completo de **Libros** (agregar, listar, modificar, borrar, buscar)
- ✅ CRUD completo de **Estudiantes**
- ✅ CRUD completo de **Préstamos** con lógica de disponibilidad
- ✅ Conexión centralizada en `conexion.php`
- ✅ Sanitización de entradas con `mysqli_real_escape_string`
- ✅ Estilos CSS profesionales en `css/estilos.css`

### Estructura Actual de Base de Datos:
```sql
-- Tablas existentes
Libros (id_libro, titulo, autor, editorial, isbn, anio_publicacion, disponible, portada)
Estudiantes (id_estudiante, password, nombre, apellidos, codigo_estudiante, curso, telefono)
Prestamos (id_prestamo, id_estudiante, id_libro, fecha_prestamo, fecha_devolucion, devuelto)
```

---

## 🎯 OBJETIVO DE LA FASE 2

Ampliar el sistema implementando:
1. **Sistema de autenticación** completo (registro, login, logout)
2. **Control de sesiones** con timeout y seguridad
3. **Sistema de roles** (administrador, profesor, estudiante, visitante)
4. **Separación Backend/Frontend** según permisos
5. **Seguridad avanzada** (hashing, prepared statements, protección CSRF)

---

## 📊 MODIFICACIONES A LA BASE DE DATOS

Ejecutar las siguientes modificaciones en `biblioteca_escolar`:

```sql
-- 1. Ampliar tabla Estudiantes con campos de autenticación y roles
ALTER TABLE Estudiantes
ADD COLUMN rol ENUM('estudiante', 'profesor', 'administrador') DEFAULT 'estudiante',
ADD COLUMN email VARCHAR(100) UNIQUE,
ADD COLUMN fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP;

-- 2. Crear tabla de auditoría de intentos de login
CREATE TABLE Intentos_Login (
    id_intento INTEGER UNSIGNED NOT NULL AUTO_INCREMENT,
    email VARCHAR(100),
    ip_address VARCHAR(45),
    intento DATETIME DEFAULT CURRENT_TIMESTAMP,
    exito BOOLEAN,
    PRIMARY KEY(id_intento)
);

-- 3. Índices para optimización
CREATE INDEX idx_email ON Estudiantes(email);
CREATE INDEX idx_rol ON Estudiantes(rol);
CREATE INDEX idx_disponible ON Libros(disponible);

-- 4. Insertar usuario administrador inicial (password: admin123)
INSERT INTO Estudiantes (nombre, apellidos, email, password, rol, codigo_estudiante)
VALUES ('Admin', 'Sistema', 'admin@biblioteca.local', '$2y$10$HASH_AQUI', 'administrador', 'ADMIN001');
```

---

## 🏗️ ESTRUCTURA DE ARCHIVOS

### ✅ Archivos EXISTENTES (Fase 1 - Completada):
```
practica2_completa/
├── conexion.php                   # Conexión centralizada a BD
├── index.php                      # Página principal con estadísticas
│
├── backups/
│   └── backup.sql                 # Script de creación de BD
│
├── css/
│   └── estilos.css                # Estilos profesionales del sistema
│
├── portadas/                      # Imágenes de portadas de libros
│
├── libros/                        # Módulo CRUD de Libros
│   ├── libros.html                # Menú del módulo
│   ├── libros_agregar.php
│   ├── libros_listar.php
│   ├── libros_buscar.php
│   ├── libros_modificar.php
│   └── libros_borrar.php
│
├── estudiantes/                   # Módulo CRUD de Estudiantes
│   ├── estudiantes.html           # Menú del módulo
│   ├── estudiantes_agregar.php
│   ├── estudiantes_listar.php
│   ├── estudiantes_buscar.php
│   ├── estudiantes_modificar.php
│   └── estudiantes_borrar.php
│
└── prestamos/                     # Módulo CRUD de Préstamos
    ├── prestamos.html             # Menú del módulo
    ├── prestamos_agregar.php
    ├── prestamos_listar.php
    ├── prestamos_buscar.php
    ├── prestamos_modificar.php
    └── prestamos_borrar.php
```

### 🆕 Archivos A CREAR (Fase 2 - Autenticación y Roles):
```
practica2_completa/
├── auth/                          # [NUEVO] Módulo de autenticación
│   ├── login.php                  # Formulario y lógica de login
│   ├── registro.php               # Formulario y lógica de registro
│   ├── logout.php                 # Destruir sesión
│   └── recuperar_password.php     # (Opcional) Recuperación
│
├── includes/                      # [NUEVO] Archivos comunes
│   ├── session_config.php         # Configuración de sesiones
│   ├── auth_check.php             # Verificación de autenticación
│   ├── role_check.php             # Verificación de roles
│   └── header.php                 # Header dinámico según rol
│
├── admin/                         # [NUEVO] Backend administrativo
│   ├── index.php                  # Dashboard admin
│   ├── usuarios.php               # Gestión de usuarios
│   ├── estadisticas.php           # Estadísticas del sistema
│   └── logs_acceso.php            # Visualización de intentos de login
│
├── usuario/                       # [NUEVO] Frontend usuarios registrados
│   ├── index.php                  # Dashboard usuario
│   ├── mi_perfil.php              # Editar perfil propio
│   ├── mis_prestamos.php          # Ver préstamos propios
│   └── reservar.php               # Realizar reservas
│
├── publico/                       # [NUEVO] Área pública (sin login)
│   ├── catalogo.php               # Catálogo público de libros
│   └── buscar.php                 # Búsqueda pública
│
├── error/                         # [NUEVO] Páginas de error
│   ├── 403.php                    # Acceso denegado
│   └── 404.php                    # No encontrado
│
└── index.php                      # [MODIFICAR] Redirigir según estado de sesión
```


---

## 🔒 REQUISITOS DE SEGURIDAD (OBLIGATORIOS)

### 1. Encriptación de Contraseñas
```php
// Al registrar
$password_hash = password_hash($_POST['password'], PASSWORD_DEFAULT);

// Al verificar
if (password_verify($_POST['password'], $hash_guardado)) {
    // Login correcto
}
```

### 2. Consultas Preparadas (Obligatorio en TODA la app)
```php
// ANTES (vulnerable):
$sql = "SELECT * FROM Estudiantes WHERE email = '$email'";

// DESPUÉS (seguro):
$stmt = $conexion->prepare("SELECT * FROM Estudiantes WHERE email = ?");
$stmt->bind_param("s", $email);
$stmt->execute();
```

### 3. Configuración de Sesiones Seguras
```php
// includes/session_config.php
ini_set('session.cookie_httponly', 1);
ini_set('session.cookie_secure', 0); // 1 si usas HTTPS
ini_set('session.use_strict_mode', 1);
session_set_cookie_params([
    'lifetime' => 1800, // 30 minutos
    'path' => '/',
    'httponly' => true,
    'samesite' => 'Strict'
]);
session_start();

// Regenerar ID periódicamente
if (!isset($_SESSION['last_regeneration']) || 
    time() - $_SESSION['last_regeneration'] > 300) {
    session_regenerate_id(true);
    $_SESSION['last_regeneration'] = time();
}
```

### 4. Control de Timeout
```php
// Verificar timeout en cada página protegida
$timeout = 1800; // 30 minutos
if (isset($_SESSION['ultimo_acceso']) && 
    (time() - $_SESSION['ultimo_acceso'] > $timeout)) {
    session_unset();
    session_destroy();
    header("Location: /auth/login.php?timeout=1");
    exit();
}
$_SESSION['ultimo_acceso'] = time();
```

### 5. Protección CSRF
```php
// Generar token
if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}

// En formularios
<input type="hidden" name="csrf_token" value="<?php echo $_SESSION['csrf_token']; ?>">

// Validar en servidor
if (!hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {
    die("Token CSRF inválido");
}
```

---

## 👥 LÓGICA DE ROLES

### Permisos por Rol:

| Funcionalidad | Visitante | Estudiante | Profesor | Admin |
|---------------|-----------|------------|----------|-------|
| Ver catálogo público | ✅ | ✅ | ✅ | ✅ |
| Login/Registro | ✅ | - | - | - |
| Reservar libros | ❌ | ✅ | ✅ | ✅ |
| Ver mis préstamos | ❌ | ✅ | ✅ | ✅ |
| Ver préstamos de estudiantes | ❌ | ❌ | ✅ | ✅ |
| CRUD Libros | ❌ | ❌ | ❌ | ✅ |
| CRUD Usuarios | ❌ | ❌ | ❌ | ✅ |
| Ver estadísticas | ❌ | ❌ | ❌ | ✅ |
| Ver logs de acceso | ❌ | ❌ | ❌ | ✅ |

### Verificación de Rol:
```php
// includes/role_check.php
function verificar_rol($roles_permitidos) {
    if (!isset($_SESSION['rol'])) {
        header("Location: /auth/login.php");
        exit();
    }
    
    if (!in_array($_SESSION['rol'], $roles_permitidos)) {
        header("Location: /error/403.php");
        exit();
    }
}

// Uso en páginas admin:
verificar_rol(['administrador']);

// Uso en páginas de profesores:
verificar_rol(['administrador', 'profesor']);
```

---

## 🎨 REQUISITOS DE DISEÑO

1. **Mantener coherencia** con los estilos existentes en `css/estilos.css`
2. **Header dinámico** que muestre:
   - Nombre del usuario logueado
   - Rol actual
   - Menú adaptado al rol
   - Botón de logout
3. **Formularios de login/registro** con validación JavaScript
4. **Mensajes de feedback** usando las clases `.success-message` y `.error-message` existentes
5. **Responsive design** para dispositivos móviles

---

## ✅ ENTREGABLES ESPERADOS

1. **Todos los archivos PHP** listados en la estructura
2. **SQL de migración** para actualizar la base de datos
3. **CSS adicional** si es necesario para los nuevos componentes
4. **JavaScript** para validaciones de cliente
5. **Documentación** de cómo probar el sistema (usuarios de prueba)

---

## 🚀 ORDEN DE IMPLEMENTACIÓN SUGERIDO

1. **Fase A**: Modificar BD y crear `includes/` (config sesiones, checks)
2. **Fase B**: Implementar `auth/` (login, registro, logout)
3. **Fase C**: Crear área `publico/` (catálogo sin login)
4. **Fase D**: Crear área `usuario/` (dashboard, reservas)
5. **Fase E**: Crear área `admin/` (dashboard, gestión, logs)
6. **Fase F**: Refactorizar archivos existentes para usar consultas preparadas
7. **Fase G**: Testing y pulido final

---

## 📝 NOTAS ADICIONALES

- La práctica debe funcionar en **AppServ** (localhost)
- Base de datos: `biblioteca_escolar`
- Credenciales en `conexion.php` (ya configurado)
- El sistema debe ser **funcional y profesional**, no un prototipo básico
- Priorizar **seguridad** sobre velocidad de desarrollo

---

**¡Procede a implementar esta ampliación del sistema de biblioteca escolar!**
