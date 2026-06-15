<?php
// AJUSTA: pon tu email real aquí
define('EMAIL_DESTINO', 'tu@email.com');

$enviado = false;
$error   = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombre  = htmlspecialchars(trim($_POST['nombre']  ?? ''));
    $email   = filter_var(trim($_POST['email']   ?? ''), FILTER_VALIDATE_EMAIL);
    $asunto  = htmlspecialchars(trim($_POST['asunto']  ?? 'Contacto web'));
    $mensaje = htmlspecialchars(trim($_POST['mensaje'] ?? ''));

    if ($nombre && $email && $mensaje) {
        $headers  = "From: noreply@SentinelIT.com\r\n";
        $headers .= "Reply-To: $email\r\n";
        $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";

        $cuerpo = "Nombre: $nombre\nEmail: $email\n\n$mensaje";

        if (mail(EMAIL_DESTINO, "SentinelIT | $asunto", $cuerpo, $headers)) {
            $enviado = true;
        } else {
            $error = 'No se pudo enviar el mensaje. Inténtalo de nuevo o escríbenos directamente.';
        }
    } else {
        $error = 'Por favor rellena todos los campos correctamente.';
    }
}

$page_title = 'Contacto';
require 'includes/header.php';
require 'includes/navbar.php';
?>

<main class="container py-6">
    <div class="text-center mb-5">
        <span class="badge-cyber mb-3 d-inline-block"><i class="bi bi-broadcast-pin me-1"></i>Hablemos de tu perímetro</span>
        <h1 class="section-title">Pon en marcha tu SOC autónomo</h1>
        <div class="title-line"></div>
        <p class="section-subtitle mx-auto" style="max-width:640px">
            Despliegue piloto, integración con tu infraestructura o una demo técnica del agente sobre Raspberry Pi.
            Cuéntanos tu caso y un ingeniero de CyberGuard te responde con una propuesta concreta, no con un folleto.
        </p>
    </div>

    <div class="row justify-content-center g-4 g-lg-5">
        <div class="col-lg-7">

            <?php if ($enviado): ?>
                <div class="card-cyber text-center py-6">
                    <div class="icon-wrap mx-auto mb-2" style="background:rgba(var(--color-success-rgb,0,135,90),0.1);color:var(--color-success)">
                        <i class="bi bi-check2-circle"></i>
                    </div>
                    <h4 class="fw-bold mt-3 mb-2">Mensaje recibido</h4>
                    <p class="text-muted mb-1">Hemos registrado tu solicitud y te asignamos un ingeniero de turno.</p>
                    <p class="text-muted mb-4">Tiempo de respuesta objetivo: <strong class="text-dark">&lt; 24 h laborables</strong>.</p>
                    <div class="d-flex flex-wrap gap-2 justify-content-center">
                        <a href="index.php" class="btn-primary-cyber"><i class="bi bi-house me-2"></i>Volver al inicio</a>
                        <a href="como-funciona.php" class="btn-outline-cyber">Cómo funciona el sistema</a>
                    </div>
                </div>
            <?php else: ?>

                <?php if ($error): ?>
                    <div class="alert alert-danger rounded-3 mb-4 d-flex align-items-center">
                        <i class="bi bi-exclamation-triangle-fill me-2"></i><span><?= $error ?></span>
                    </div>
                <?php endif; ?>

                <div class="card-cyber">
                    <div class="d-flex align-items-center gap-3 mb-4">
                        <div class="icon-wrap mb-0"><i class="bi bi-chat-square-text"></i></div>
                        <div>
                            <h4 class="fw-bold mb-0">Cuéntanos tu caso</h4>
                            <p class="text-muted small mb-0">Respondemos a cada mensaje de forma manual. Nada de bots.</p>
                        </div>
                    </div>
                    <form method="POST" novalidate>
                        <div class="row g-3">
                            <div class="col-md-6">
                                <label class="form-label text-muted small fw-semibold">Nombre *</label>
                                <input type="text" name="nombre" class="form-control form-control-cyber"
                                       placeholder="Nombre y apellidos"
                                       value="<?= htmlspecialchars($_POST['nombre'] ?? '') ?>" required>
                            </div>
                            <div class="col-md-6">
                                <label class="form-label text-muted small fw-semibold">Email corporativo *</label>
                                <input type="email" name="email" class="form-control form-control-cyber"
                                       placeholder="nombre@tuempresa.com"
                                       value="<?= htmlspecialchars($_POST['email'] ?? '') ?>" required>
                            </div>
                        </div>
                        <div class="mb-3 mt-3">
                            <label class="form-label text-muted small fw-semibold">Asunto</label>
                            <input type="text" name="asunto" class="form-control form-control-cyber"
                                   placeholder="Ej.: Piloto en 3 sedes / Integración SIEM / Demo técnica"
                                   value="<?= htmlspecialchars($_POST['asunto'] ?? '') ?>">
                        </div>
                        <div class="mb-4">
                            <label class="form-label text-muted small fw-semibold">Mensaje *</label>
                            <textarea name="mensaje" class="form-control form-control-cyber" rows="6"
                                      placeholder="Cuéntanos el número de sedes, sistemas a proteger y qué te gustaría conseguir. Cuanto más concreto, mejor encajamos la propuesta." required><?= htmlspecialchars($_POST['mensaje'] ?? '') ?></textarea>
                        </div>
                        <button type="submit" class="btn-primary-cyber w-100">
                            <i class="bi bi-send me-2"></i>Enviar mensaje
                        </button>
                        <p class="text-muted small text-center mb-0 mt-3">
                            <i class="bi bi-shield-lock me-1"></i>Tus datos solo se usan para responderte. Sin spam, sin terceros.
                        </p>
                    </form>
                </div>

            <?php endif; ?>
        </div>

        <!-- Info lateral -->
        <div class="col-lg-4">
            <div class="card-cyber mb-3">
                <div class="d-flex align-items-start gap-3">
                    <i class="bi bi-envelope-at" style="color:var(--color-primary);font-size:1.5rem"></i>
                    <div>
                        <h6 class="fw-bold mb-1">Email directo</h6>
                        <p class="text-muted small mb-1">Soporte y nuevos proyectos:</p>
                        <a href="mailto:hola@cyberguard.io" class="footer-link small text-decoration-none">hola@cyberguard.io</a>
                    </div>
                </div>
            </div>
            <div class="card-cyber mb-3">
                <div class="d-flex align-items-start gap-3">
                    <i class="bi bi-clock-history" style="color:var(--color-primary);font-size:1.5rem"></i>
                    <div>
                        <h6 class="fw-bold mb-1">Tiempo de respuesta</h6>
                        <p class="text-muted small mb-0">Menos de 24 h en días laborables. Incidencias de clientes con SLA activo: respuesta en &lt; 1 h.</p>
                    </div>
                </div>
            </div>
            <div class="card-cyber mb-3">
                <div class="d-flex align-items-start gap-3">
                    <i class="bi bi-geo-alt" style="color:var(--color-primary);font-size:1.5rem"></i>
                    <div>
                        <h6 class="fw-bold mb-1">Dónde estamos</h6>
                        <p class="text-muted small mb-0">Ingeniería en Madrid, despliegues remotos en toda la península. El edge va a tu sede; el panel, a tu navegador.</p>
                    </div>
                </div>
            </div>
            <div class="card-cyber" style="background:var(--color-primary-soft, rgba(var(--color-primary-rgb),.06));border-color:rgba(var(--color-primary-rgb),.2)">
                <div class="d-flex align-items-center gap-2 mb-2">
                    <span class="badge-cyber badge-success"><i class="bi bi-circle-fill me-1" style="font-size:.5rem"></i>Operativo</span>
                    <span class="text-muted small">Estado de la plataforma</span>
                </div>
                <p class="text-muted small mb-0">Sensores y broker MQTT/mTLS sincronizados con AWS IoT Core. Monitorización 24/7, sin ventanas de mantenimiento programadas.</p>
            </div>
        </div>
    </div>

    <!-- Razones de contacto -->
    <div class="row g-4 mt-4 mt-lg-5">
        <div class="col-md-4">
            <div class="card-cyber h-100 text-center">
                <div class="icon-wrap mx-auto"><i class="bi bi-rocket-takeoff"></i></div>
                <h6 class="fw-bold mb-2">Piloto en tu red</h6>
                <p class="text-muted small mb-0">Desplegamos un sensor edge en una sede y medimos detecciones reales durante 14 días. Sin coste de instalación.</p>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card-cyber h-100 text-center">
                <div class="icon-wrap mx-auto" style="background:rgba(var(--color-success-rgb,0,135,90),0.1);color:var(--color-success)"><i class="bi bi-diagram-3"></i></div>
                <h6 class="fw-bold mb-2">Integración</h6>
                <p class="text-muted small mb-0">Conectamos los eventos del agente con tu SIEM, Slack o correo. El triage con IA (Gemini) llega ya enriquecido.</p>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card-cyber h-100 text-center">
                <div class="icon-wrap mx-auto" style="background:rgba(var(--color-warning-rgb,255,193,7),0.12);color:var(--color-warning)"><i class="bi bi-mortarboard"></i></div>
                <h6 class="fw-bold mb-2">Demo técnica</h6>
                <p class="text-muted small mb-0">¿Eres del equipo de seguridad? Te enseñamos el bucle HITL: detección, propuesta de mitigación y aprobación humana.</p>
            </div>
        </div>
    </div>
</main>

<?php require 'includes/footer.php'; ?>

