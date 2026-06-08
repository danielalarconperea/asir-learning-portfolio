<?php
// footer.php
?>
        </main>
        
        <footer>
            <div class="footer-content">
                <div class="footer-section">
                    <h3>Biblioteca Escolar</h3>
                    <p>Sistema de gestión de préstamos de libros</p>
                </div>
                
                <div class="footer-section">
                    <h3>Enlaces rápidos</h3>
                    <a href="index.php">Inicio</a>
                    <a href="catalogo.php">Catálogo</a>
                    <a href="contacto.php">Contacto</a>
                </div>
                
                <div class="footer-section">
                    <h3>Contacto</h3>
                    <p>📧 biblioteca@escuela.es</p>
                    <p>📞 912 34 56 78</p>
                </div>
            </div>
            
            <div class="footer-bottom">
                <p>Sistema de Gestión de Biblioteca Escolar &copy; 2024</p>
                <?php if (isset($_SESSION['rol'])): ?>
                    <small>Conectado como: <?php echo $_SESSION['rol']; ?></small>
                <?php endif; ?>
            </div>
        </footer>
    </div>
</body>
</html>