<?php
require_once 'db.php';
require_once 'includes/logger.php';
require_once 'includes/session_control.php';
$page_title = 'Sugerencias de Mejora';
require 'includes/header.php';
 
if (!validar_sesion_activa($pdo)) {
    header('Location: login.php');
    exit;
}
 
// Asegurarse de que la tabla sugerencias exista por si no han importado el schema.sql editado
$pdo->exec("CREATE TABLE IF NOT EXISTS sugerencias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    comentario TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;");
 
$mensaje = '';
$error = '';
 
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['accion']) && $_POST['accion'] === 'crear_sugerencia') {
    $comentario = trim($_POST['comentario'] ?? '');
    if ($comentario) {
        $stmt = $pdo->prepare("INSERT INTO sugerencias (usuario_id, comentario) VALUES (?, ?)");
        $stmt->execute([$_SESSION['usuario_id'], $comentario]);
        $mensaje = '¡Gracias por tu sugerencia! Lo tendremos muy en cuenta.';
        log_activity('nueva_sugerencia', [
            'longitud'   => strlen($comentario),
            'comentario' => $comentario,
        ]);
    } else {
        $error = 'El comentario no puede estar vacío.';
    }
}
?>
<?php require 'includes/navbar.php'; ?>
 
<main class="container-fluid my-5 px-lg-5">
    <div class="mb-5">
        <span class="badge-cyber mb-3 d-inline-block"><i class="bi bi-lightbulb me-1"></i>Tu voz mueve el roadmap</span>
        <h2 class="section-title m-0">Sugerencias y mejoras</h2>
        <div class="title-line"></div>
        <p class="section-subtitle mt-2 mb-0" style="max-width:720px">
            CyberGuard se construye sobre lo que detectan los analistas que lo usan a diario. Si echas algo en falta
            en el panel, en las reglas del Policy Engine o en el flujo de aprobación HITL, cuéntanoslo: cada idea
            entra en la cola de priorización del equipo de producto.
        </p>
    </div>

    <div class="row g-4">
        <!-- Columna de formulario -->
        <div class="col-lg-5">
            <div class="card-cyber h-100">
                <div class="d-flex align-items-center gap-3 mb-3">
                    <div class="icon-wrap mb-0"><i class="bi bi-send-plus"></i></div>
                    <div>
                        <h5 class="fw-bold mb-0">Envíanos tu idea</h5>
                        <p class="text-muted small mb-0">Una sugerencia clara vale más que diez genéricas.</p>
                    </div>
                </div>
                <?php if ($mensaje): ?>
                    <div class="alert alert-success d-flex align-items-center">
                        <i class="bi bi-check-circle-fill me-2"></i><span><?= htmlspecialchars($mensaje) ?></span>
                    </div>
                <?php endif; ?>
                <?php if ($error): ?>
                    <div class="alert alert-danger d-flex align-items-center">
                        <i class="bi bi-exclamation-triangle-fill me-2"></i><span><?= htmlspecialchars($error) ?></span>
                    </div>
                <?php endif; ?>
                <form method="POST" action="sugerencias.php">
                    <input type="hidden" name="accion" value="crear_sugerencia">
                    <div class="mb-3">
                        <label class="form-label text-muted small fw-semibold">¿Qué podemos mejorar del sistema?</label>
                        <textarea name="comentario" class="form-control form-control-cyber" rows="6" required placeholder="Ej.: «Me gustaría poder filtrar el panel de eventos por sensor», «Añadid una regla del Policy Engine para escaneos de puertos lentos», «Un resumen diario por correo del triage de Gemini»..."></textarea>
                    </div>
                    <button type="submit" class="btn-primary-cyber border-0 px-4 w-100"><i class="bi bi-send me-2"></i>Enviar sugerencia</button>
                </form>
                <hr class="divider-cyber my-4">
                <p class="text-muted small mb-2 fw-semibold text-uppercase" style="letter-spacing:.04em">Qué nos ayuda más</p>
                <ul class="list-unstyled small text-muted mb-0">
                    <li class="mb-2"><i class="bi bi-bullseye text-primary me-2"></i>Describe el caso concreto donde te falta algo.</li>
                    <li class="mb-2"><i class="bi bi-graph-up-arrow text-primary me-2"></i>Cuéntanos qué te haría ganar tiempo en el día a día.</li>
                    <li class="mb-0"><i class="bi bi-shield-check text-primary me-2"></i>Si es un riesgo de seguridad, márcalo en el texto.</li>
                </ul>
            </div>
        </div>

        <!-- Columna de comentarios (solo admin) -->
        <?php if ($_SESSION['rol'] === 'admin'): ?>
        <div class="col-lg-7">
            <div class="card-cyber h-100">
                <div class="d-flex flex-wrap align-items-center justify-content-between gap-2 mb-3">
                    <h5 class="fw-bold mb-0"><i class="bi bi-inbox me-2 text-primary"></i>Bandeja de sugerencias</h5>
                    <span class="badge-cyber"><i class="bi bi-shield-lock me-1"></i>Vista de administrador</span>
                </div>
                <div class="table-responsive">
                    <table class="table table-hover align-middle">
                        <thead style="background-color: var(--color-bg); color: var(--color-text);">
                            <tr>
                                <th style="width: 25%">Usuario</th>
                                <th style="width: 55%">Sugerencia</th>
                                <th style="width: 20%">Fecha</th>
                            </tr>
                        </thead>
                        <tbody>
                            <?php
                            $stmt_sug = $pdo->query("SELECT s.*, u.nombre, u.email FROM sugerencias s JOIN usuarios u ON s.usuario_id = u.id ORDER BY s.id DESC");
                            if ($stmt_sug->rowCount() > 0):
                                while ($s = $stmt_sug->fetch(PDO::FETCH_ASSOC)):
                            ?>
                            <tr>
                                <td>
                                    <strong><?= htmlspecialchars($s['nombre']) ?></strong><br>
                                    <small class="text-muted"><?= htmlspecialchars($s['email']) ?></small>
                                </td>
                                <td><?= nl2br($s['comentario']) ?></td>
                                <td class="text-muted small"><i class="bi bi-calendar3 me-1"></i><?= htmlspecialchars($s['created_at']) ?></td>
                            </tr>
                            <?php
                                endwhile;
                            else:
                            ?>
                            <tr>
                                <td colspan="3" class="text-center text-muted py-5">
                                    <i class="bi bi-inbox d-block mb-2" style="font-size:2.5rem;opacity:.3"></i>
                                    Todavía no hay sugerencias. En cuanto el equipo envíe la primera, aparecerá aquí.
                                </td>
                            </tr>
                            <?php endif; ?>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        <?php else: ?>
        <div class="col-lg-7">
            <div class="card-cyber h-100 d-flex flex-column justify-content-center">
                <div class="text-center mb-4">
                    <div class="icon-wrap mx-auto" style="background:rgba(var(--color-warning-rgb,255,193,7),0.12);color:var(--color-warning)"><i class="bi bi-lightbulb"></i></div>
                    <h5 class="fw-bold mt-3 mb-2">De la idea al cambio en producción</h5>
                    <p class="text-muted small mb-0 mx-auto" style="max-width:480px">Así viaja tu sugerencia dentro de CyberGuard. Cada propuesta queda registrada y se revisa en el ciclo de mejora del producto.</p>
                </div>
                <div class="row g-3 text-center">
                    <div class="col-4">
                        <div class="surface-cyber py-3 h-100">
                            <i class="bi bi-pencil-square d-block mb-2 text-primary" style="font-size:1.4rem"></i>
                            <div class="fw-semibold small">La envías</div>
                            <div class="text-muted" style="font-size:.78rem">Queda registrada al instante</div>
                        </div>
                    </div>
                    <div class="col-4">
                        <div class="surface-cyber py-3 h-100">
                            <i class="bi bi-list-check d-block mb-2 text-primary" style="font-size:1.4rem"></i>
                            <div class="fw-semibold small">Se prioriza</div>
                            <div class="text-muted" style="font-size:.78rem">Entra en el roadmap</div>
                        </div>
                    </div>
                    <div class="col-4">
                        <div class="surface-cyber py-3 h-100">
                            <i class="bi bi-rocket-takeoff d-block mb-2 text-primary" style="font-size:1.4rem"></i>
                            <div class="fw-semibold small">Se despliega</div>
                            <div class="text-muted" style="font-size:.78rem">Llega a tu panel</div>
                        </div>
                    </div>
                </div>
                <p class="text-muted small text-center mb-0 mt-4"><i class="bi bi-heart-fill text-danger me-1"></i>Gracias por ayudarnos a hacer SentinelIT mejor.</p>
            </div>
        </div>
        <?php endif; ?>
    </div>
</main>
 
<?php require 'includes/footer.php'; ?>

