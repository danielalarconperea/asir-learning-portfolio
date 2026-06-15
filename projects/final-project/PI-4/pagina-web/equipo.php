<?php
$page_title = 'Equipo';
require 'includes/header.php';
require 'includes/navbar.php';

// AJUSTA: cambia los datos del equipo con los reales
$equipo = [
    [
        'nombre'   => 'Felix Tejedor Zapatero',
        'rol'      => 'Arquitectura cloud y monitorización',
        'desc'     => 'Diseña la malla de sensores distribuidos y la integración con AWS IoT Core. Responsable del transporte mTLS, la identidad por certificado y la fiabilidad del pipeline edge-a-nube.',
        'iniciales'=> 'FT',
        'focos'    => ['AWS IoT', 'mTLS', 'Infra edge'],
    ],
    [
        'nombre'   => 'Daniel Alarcón Perea',
        'rol'      => 'Detección y respuesta',
        'desc'     => 'Desarrolla los agentes de monitorización y la lógica de detección en tiempo real. Lleva el triaje con IA, las políticas de mitigación y la respuesta automática en el cortafuegos.',
        'iniciales'=> 'DA',
        'focos'    => ['Agentes', 'IA / Triaje', 'Respuesta'],
    ],
];
?>

<main>

<!-- HERO -->
<section class="container py-6">
    <div class="row justify-content-center text-center">
        <div class="col-lg-8">
            <span class="badge-cyber mb-3 d-inline-block">Las personas detrás del sistema</span>
            <h1 class="section-title">Un equipo pequeño con una idea grande</h1>
            <div class="title-line"></div>
            <p class="section-subtitle" style="max-width:620px;">
                Somos ingenieros obsesionados con una pregunta: ¿por qué la ciberseguridad activa
                sigue reservada a quien puede pagar un SOC de seis cifras? SentinelIT es nuestra respuesta.
            </p>
        </div>
    </div>
</section>

<!-- TARJETAS DEL EQUIPO -->
<section class="container pb-5">
    <div class="row g-4 justify-content-center">
        <?php foreach ($equipo as $persona): ?>
        <div class="col-md-6 col-lg-5">
            <div class="card-cyber h-100 text-center">
                <!-- Avatar con iniciales. Para foto real: sustituir por <img> en img/team/ -->
                <div class="mx-auto mb-3 d-flex align-items-center justify-content-center"
                     style="width:88px;height:88px;border-radius:50%;
                            background:var(--color-primary-soft);
                            border:2px solid rgba(var(--color-primary-rgb),0.35);">
                    <span style="font-family:var(--font-mono);font-weight:700;font-size:1.6rem;color:var(--color-primary);letter-spacing:.04em;">
                        <?= htmlspecialchars($persona['iniciales']) ?>
                    </span>
                </div>
                <h5 class="fw-bold mb-1"><?= htmlspecialchars($persona['nombre']) ?></h5>
                <p class="mb-3" style="color:var(--color-primary);font-size:0.9rem;font-weight:600;">
                    <?= htmlspecialchars($persona['rol']) ?>
                </p>
                <p class="text-muted small mb-3"><?= htmlspecialchars($persona['desc']) ?></p>
                <div class="d-flex flex-wrap justify-content-center gap-1">
                    <?php foreach ($persona['focos'] as $foco): ?>
                        <span class="badge-cyber"><?= htmlspecialchars($foco) ?></span>
                    <?php endforeach; ?>
                </div>
            </div>
        </div>
        <?php endforeach; ?>
    </div>
</section>

<!-- SOBRE SENTINELIT -->
<section class="section-alt section-pad">
    <div class="container">
        <div class="row align-items-center g-5">
            <div class="col-lg-6">
                <span class="badge-cyber mb-3 d-inline-block">Nuestra historia</span>
                <h2 class="section-title mb-3">Nacimos de un proyecto de fin de grado</h2>
                <div class="title-line" style="margin-inline:0;"></div>
                <p class="text-muted">
                    SentinelIT empezó como un experimento: demostrar que un SOC autónomo —detección,
                    análisis con IA y respuesta automática— podía construirse con un par de
                    Raspberry Pi y servicios cloud de pago por uso, en lugar de appliances que
                    cuestan más que el negocio que protegen.
                </p>
                <p class="text-muted mb-0">
                    Lo que era una prueba de concepto se convirtió en una plataforma que vigila redes
                    reales 24/7. Seguimos fieles a la idea original: <strong>democratizar la
                    ciberseguridad activa</strong> con hardware accesible, tecnología estándar y una
                    persona siempre con la última palabra.
                </p>
            </div>
            <div class="col-lg-6">
                <div class="row g-3">
                    <div class="col-6">
                        <div class="kpi-card h-100">
                            <div class="kpi-value text-gradient-cyber">2</div>
                            <div class="kpi-label">Ingenieros</div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="kpi-card h-100">
                            <div class="kpi-value text-gradient-cyber">&lt;15<span style="font-size:1.2rem">s</span></div>
                            <div class="kpi-label">Del ataque al bloqueo</div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="kpi-card h-100">
                            <div class="kpi-value text-gradient-cyber">100%</div>
                            <div class="kpi-label">Stack abierto</div>
                        </div>
                    </div>
                    <div class="col-6">
                        <div class="kpi-card h-100">
                            <div class="kpi-value text-gradient-cyber">24/7</div>
                            <div class="kpi-label">En guardia</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- NUESTROS PRINCIPIOS -->
<section class="container section-pad">
    <div class="text-center mb-5">
        <span class="badge-cyber mb-3 d-inline-block">Cómo trabajamos</span>
        <h2 class="section-title">Tres principios que no negociamos</h2>
        <div class="title-line"></div>
    </div>
    <div class="row g-4 justify-content-center">
        <div class="col-md-4">
            <div class="card-cyber h-100 text-center">
                <div class="icon-wrap mx-auto"><i class="bi bi-unlock"></i></div>
                <h5 class="fw-bold mb-2">Sin cajas negras</h5>
                <p class="text-muted small mb-0">
                    Tecnología estándar y verificable: MQTT, TLS, iptables, Python. Si no podemos
                    explicar por qué el sistema tomó una decisión, no la dejamos tomarla sola.
                </p>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card-cyber h-100 text-center">
                <div class="icon-wrap mx-auto" style="background:rgba(var(--color-success-rgb),0.10);color:var(--color-success)"><i class="bi bi-person-check"></i></div>
                <h5 class="fw-bold mb-2">La persona, al mando</h5>
                <p class="text-muted small mb-0">
                    La automatización gana tiempo; el analista conserva el control. Cada acción
                    queda trazada, justificada y es reversible desde el panel (HITL).
                </p>
            </div>
        </div>
        <div class="col-md-4">
            <div class="card-cyber h-100 text-center">
                <div class="icon-wrap mx-auto" style="background:rgba(var(--color-warning-rgb),0.15);color:#9A7400"><i class="bi bi-piggy-bank"></i></div>
                <h5 class="fw-bold mb-2">Accesible de verdad</h5>
                <p class="text-muted small mb-0">
                    Capacidades de SOC sobre Raspberry Pi y cloud de pago por uso. Protección seria
                    sin presupuesto de gran corporación.
                </p>
            </div>
        </div>
    </div>
</section>

<!-- CTA FINAL -->
<section class="section-alt section-pad">
    <div class="container text-center">
        <h2 class="section-title mb-3">¿Hablamos?</h2>
        <p class="text-muted mb-4" style="max-width:520px;margin-inline:auto;">
            Tanto si quieres ver una demo como si te interesa cómo está construido por dentro,
            nos encanta enseñar el sistema.
        </p>
        <div class="d-flex flex-wrap justify-content-center gap-3">
            <a href="contacto.php" class="btn-primary-cyber">Contactar con el equipo</a>
            <a href="como-funciona.php" class="btn-outline-cyber">Cómo funciona</a>
        </div>
    </div>
</section>

</main>

<?php require 'includes/footer.php'; ?>
