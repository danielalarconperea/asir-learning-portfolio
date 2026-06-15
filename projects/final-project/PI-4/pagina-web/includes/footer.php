<!-- includes/footer.php -->
<?php $site_footer = htmlspecialchars($site_title_global ?? 'SentinelIT');
      $email_footer = htmlspecialchars($contact_email_global ?? 'info@SentinelIT.com'); ?>
<footer class="mt-5 pt-5 pb-4 section-alt">
    <div class="container">
        <div class="row gy-4">
            <div class="col-lg-4 col-md-6">
                <h5 class="fw-bold mb-3">
                    <i class="bi bi-shield-fill-check me-2" style="color:var(--color-primary)"></i><?= $site_footer ?>
                </h5>
                <p class="text-muted small mb-3">Protección inteligente basada en Raspberry Pi y AWS IoT Core. Detección en tiempo real, respuesta automatizada.</p>
                <span class="badge-cyber badge-success">
                    <i class="bi bi-circle-fill me-1" style="font-size:.55em;vertical-align:middle"></i>Sistemas operativos
                </span>
            </div>
            <div class="col-lg-2 col-md-6">
                <h6 class="fw-bold mb-3">Navegación</h6>
                <ul class="list-unstyled small mb-0">
                    <li class="mb-1"><a href="servicios.php"     class="text-muted text-decoration-none footer-link">Servicios</a></li>
                    <li class="mb-1"><a href="como-funciona.php" class="text-muted text-decoration-none footer-link">Cómo funciona</a></li>
                    <li class="mb-1"><a href="tecnologias.php"   class="text-muted text-decoration-none footer-link">Tecnologías</a></li>
                    <li class="mb-1"><a href="equipo.php"        class="text-muted text-decoration-none footer-link">Equipo</a></li>
                    <li class="mb-1"><a href="contacto.php"      class="text-muted text-decoration-none footer-link">Contacto</a></li>
                </ul>
            </div>
            <div class="col-lg-3 col-md-6">
                <h6 class="fw-bold mb-3">Plataforma</h6>
                <ul class="list-unstyled small mb-0">
                    <li class="mb-1"><span class="text-muted"><i class="bi bi-cpu me-2"></i>Sensores Raspberry Pi</span></li>
                    <li class="mb-1"><span class="text-muted"><i class="bi bi-cloud me-2"></i>AWS IoT Core (mTLS)</span></li>
                    <li class="mb-1"><span class="text-muted"><i class="bi bi-lightning-charge me-2"></i>Respuesta automatizada</span></li>
                    <li class="mb-1"><span class="text-muted"><i class="bi bi-graph-up-arrow me-2"></i>Panel en tiempo real</span></li>
                </ul>
            </div>
            <div class="col-lg-3 col-md-6">
                <h6 class="fw-bold mb-3">Contacto</h6>
                <p class="text-muted small mb-2"><i class="bi bi-envelope me-2"></i><a href="mailto:<?= $email_footer ?>" class="text-muted text-decoration-none footer-link"><?= $email_footer ?></a></p>
                <p class="text-muted small mb-2"><i class="bi bi-telephone me-2"></i>+34 900 000 000</p>
                <p class="text-muted small mb-0"><i class="bi bi-geo-alt me-2"></i>España</p>
            </div>
        </div>
        <hr class="divider-cyber my-4">
        <div class="d-flex flex-column flex-md-row justify-content-between align-items-center gap-2">
            <p class="text-muted small mb-0">© <?= date('Y') ?> <?= $site_footer ?> — Todos los derechos reservados</p>
            <p class="text-muted small mb-0">
                <span class="d-inline-flex align-items-center"><i class="bi bi-shield-lock me-1"></i>Plataforma de demostración</span>
            </p>
        </div>
    </div>
</footer>

<!-- Bootstrap JS -->
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<!-- JS propio -->
<script src="js/main.js"></script>

<?php if (basename($_SERVER['PHP_SELF']) === 'panel.php'): ?>
    <!-- Chart.js solo en el panel -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <script src="js/charts.js"></script>
<?php endif; ?>

</body>
</html>

