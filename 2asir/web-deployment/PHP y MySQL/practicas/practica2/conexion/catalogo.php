<?php
// catalogo.php - Catálogo accesible para todos
include 'header.php';

// TODO: Lógica para mostrar libros según filtros
// TODO: Para usuarios logueados, mostrar opción de reserva
// TODO: Para administradores, mostrar opciones de edición
?>

<section class="catalogo">
    <h2>Catálogo de Libros</h2>
    
    <div class="filtros">
        <form method="GET" class="filtro-form">
            <input type="text" name="busqueda" placeholder="Buscar por título o autor..." 
                   value="<?php echo isset($_GET['busqueda']) ? htmlspecialchars($_GET['busqueda']) : ''; ?>">
            
            <select name="disponible">
                <option value="">Todos los libros</option>
                <option value="1" <?php echo (isset($_GET['disponible']) && $_GET['disponible'] == '1') ? 'selected' : ''; ?>>Disponibles</option>
                <option value="0" <?php echo (isset($_GET['disponible']) && $_GET['disponible'] == '0') ? 'selected' : ''; ?>>Prestados</option>
            </select>
            
            <button type="submit">🔍 Filtrar</button>
            
            <?php if (tieneRol('administrador')): ?>
                <a href="admin_libros_agregar.php" class="btn-agregar">+ Añadir Libro</a>
            <?php endif; ?>
        </form>
    </div>
    
    <div class="libros-grid">
        <!-- TODO: Generar dinámicamente tarjetas de libros -->
        <div class="libro-card">
            <div class="libro-portada">
                <img src="portadas/default.jpg" alt="Portada">
            </div>
            <div class="libro-info">
                <h3>Título del Libro</h3>
                <p class="libro-autor">Autor del Libro</p>
                <p class="libro-editorial">Editorial</p>
                <p class="libro-disponibilidad disponible">✅ Disponible</p>
                
                <div class="libro-acciones">
                    <?php if (estaLogueado() && !tieneRol('administrador')): ?>
                        <button class="btn-reservar">Reservar</button>
                    <?php endif; ?>
                    
                    <?php if (tieneRol('administrador')): ?>
                        <a href="admin_libros_editar.php?id=1" class="btn-editar">Editar</a>
                        <button class="btn-eliminar">Eliminar</button>
                    <?php endif; ?>
                </div>
            </div>
        </div>
    </div>
</section>

<?php include 'footer.php'; ?>