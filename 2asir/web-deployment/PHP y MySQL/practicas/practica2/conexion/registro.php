<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Biblioteca - Registrarse</title>
    <link rel="stylesheet" href="css/estilos.css">
    <link rel="stylesheet" href="css/auth.css">
</head>
<body>
    <div class="auth-container">
        <div class="auth-box">
            <div class="auth-header">
                <h1>📚 Biblioteca Escolar</h1>
                <p>Crear Nueva Cuenta</p>
            </div>
            
            <form action="procesar_registro.php" method="POST" class="auth-form" id="formRegistro">
                <div class="form-row">
                    <div class="form-group">
                        <label for="nombre">Nombre:</label>
                        <input type="text" id="nombre" name="nombre" required 
                               placeholder="María">
                    </div>
                    
                    <div class="form-group">
                        <label for="apellidos">Apellidos:</label>
                        <input type="text" id="apellidos" name="apellidos" required 
                               placeholder="González Pérez">
                    </div>
                </div>
                
                <div class="form-group">
                    <label for="email">Email institucional:</label>
                    <input type="email" id="email" name="email" required 
                           placeholder="usuario@escuela.es">
                    <small>Debe ser un email de la escuela</small>
                </div>
                
                <div class="form-group">
                    <label for="codigo">Código de estudiante/profesor:</label>
                    <input type="text" id="codigo_estudiante" name="codigo_estudiante" required 
                           placeholder="EST2024001" pattern="[A-Z]{3}\d{7}">
                    <small>Formato: 3 letras + 7 números (ej: EST2024001)</small>
                </div>
                
                <div class="form-group">
                    <label for="curso">Curso:</label>
                    <select id="curso" name="curso" required>
                        <option value="">Seleccione un curso</option>
                        <option value="1º ESO">1º ESO</option>
                        <option value="2º ESO">2º ESO</option>
                        <option value="3º ESO">3º ESO</option>
                        <option value="4º ESO">4º ESO</option>
                        <option value="1º Bachillerato">1º Bachillerato</option>
                        <option value="2º Bachillerato">2º Bachillerato</option>
                        <option value="Profesor">Profesor</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="password">Contraseña:</label>
                    <input type="password" id="password" name="password" required 
                           placeholder="••••••••" minlength="6">
                    <small>Mínimo 6 caracteres</small>
                </div>
                
                <div class="form-group">
                    <label for="confirm_password">Confirmar contraseña:</label>
                    <input type="password" id="confirm_password" name="confirm_password" required 
                           placeholder="••••••••">
                </div>
                
                <div class="form-group">
                    <label for="telefono">Teléfono:</label>
                    <input type="tel" id="telefono" name="telefono" 
                           placeholder="611223344" pattern="[0-9]{9}">
                </div>
                
                <div class="form-group">
                    <div class="checkbox-group">
                        <input type="checkbox" id="terminos" name="terminos" required>
                        <label for="terminos">Acepto los términos y condiciones</label>
                    </div>
                </div>
                
                <div class="form-group">
                    <button type="submit" class="btn btn-primary">Registrarse</button>
                </div>
                
                <div class="auth-links">
                    <a href="index.php">Volver al inicio</a>
                    <a href="login.php">Ya tengo cuenta</a>
                </div>
            </form>
        </div>
    </div>
    
    <script>
    // Validación de contraseñas coincidentes
    document.getElementById('formRegistro').addEventListener('submit', function(e) {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        
        if (password !== confirmPassword) {
            e.preventDefault();
            alert('Las contraseñas no coinciden');
        }
    });
    </script>
</body>
</html>