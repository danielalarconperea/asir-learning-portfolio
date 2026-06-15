<?php
$page_title = 'Tecnologías';
require 'includes/header.php';
require 'includes/navbar.php';

// El stack agrupado por capa de la arquitectura. Cada color usa variables del sistema de diseño.
$capas = [
    [
        'capa'     => 'Sensor / Edge',
        'subtitulo'=> 'Lo que corre dentro de cada Raspberry Pi, en el borde de la red.',
        'icono'    => 'bi-cpu',
        'color'    => 'primary',
        'items'    => [
            ['nombre'=>'Raspberry Pi 4 / 5', 'icono'=>'bi-motherboard', 'desc'=>'Sensor y coordinador en un mismo equipo. ARM64, 4–8 GB de RAM y consumo por debajo de 7 W: vigilancia 24/7 a coste de bombilla.'],
            ['nombre'=>'Python 3.11',         'icono'=>'bi-filetype-py', 'desc'=>'Núcleo del agente. Tailers concurrentes con threads, parseo por regex de los logs y cliente MQTT asíncrono hacia la nube.'],
            ['nombre'=>'systemd',             'icono'=>'bi-gear-wide-connected', 'desc'=>'El agente vive como daemon: arranque en boot, reinicio automático ante fallo y journald para diagnóstico.'],
            ['nombre'=>'Docker',              'icono'=>'bi-box-seam', 'desc'=>'Empaquetado opcional del agente para un despliegue reproducible e idéntico en cualquier host.'],
        ],
    ],
    [
        'capa'     => 'Respuesta y firewall',
        'subtitulo'=> 'Donde la decisión se convierte en acción sobre el sistema.',
        'icono'    => 'bi-fire',
        'color'    => 'danger',
        'items'    => [
            ['nombre'=>'iptables / nftables', 'icono'=>'bi-shield-lock', 'desc'=>'El Policy Engine traduce la decisión a reglas de firewall y banea la IP origen en segundos, con TTL para no envenenar la tabla.'],
            ['nombre'=>'Policy Engine',       'icono'=>'bi-sliders', 'desc'=>'Motor de reglas propio: evalúa umbrales por servicio, decide el verbo (alertar, bloquear, escalar) y deja una traza explicable.'],
        ],
    ],
    [
        'capa'     => 'Inteligencia (IA)',
        'subtitulo'=> 'El cerebro que da contexto a cada incidente.',
        'icono'    => 'bi-robot',
        'color'    => 'warning',
        'items'    => [
            ['nombre'=>'Google Gemini',       'icono'=>'bi-stars', 'desc'=>'LLM para el triaje: clasifica el ataque, estima severidad y redacta la mitigación en lenguaje natural para el analista.'],
            ['nombre'=>'Enriquecedor offline','icono'=>'bi-cpu-fill', 'desc'=>'Capa de heurísticas locales que contextualiza el evento aunque no haya nube ni cuota de API disponibles.'],
            ['nombre'=>'HITL',                'icono'=>'bi-person-check', 'desc'=>'Human-in-the-loop: cuando la confianza del modelo es baja, el sistema escala a una persona en vez de actuar a ciegas.'],
        ],
    ],
    [
        'capa'     => 'Transporte y nube',
        'subtitulo'=> 'Cómo viajan los eventos desde el borde hasta el centro.',
        'icono'    => 'bi-cloud',
        'color'    => 'success',
        'items'    => [
            ['nombre'=>'AWS IoT Core',        'icono'=>'bi-cloud-arrow-up', 'desc'=>'Broker MQTT gestionado: certificados X.509 por dispositivo, política por device y alta disponibilidad sin servidor propio.'],
            ['nombre'=>'MQTT + mTLS',         'icono'=>'bi-arrow-left-right', 'desc'=>'Mensajería ligera pensada para IoT, cifrada extremo a extremo. QoS 1 garantiza la entrega de los eventos críticos.'],
        ],
    ],
    [
        'capa'     => 'Panel y datos',
        'subtitulo'=> 'La cara visible: el SOC que ve el analista.',
        'icono'    => 'bi-bar-chart-line',
        'color'    => 'primary',
        'items'    => [
            ['nombre'=>'PHP 8',               'icono'=>'bi-filetype-php', 'desc'=>'Backend del panel. Consultas de agregación a MySQL y render dinámico de las vistas del SOC.'],
            ['nombre'=>'MySQL',               'icono'=>'bi-database', 'desc'=>'Persistencia de eventos, IPs y estadísticas. Vistas pre-agregadas que alimentan los KPIs del dashboard.'],
            ['nombre'=>'Bootstrap 5',         'icono'=>'bi-bootstrap', 'desc'=>'Sistema de rejilla y componentes responsive sobre el que se asienta la identidad visual de CyberGuard.'],
            ['nombre'=>'Chart.js',            'icono'=>'bi-graph-up', 'desc'=>'Gráficas en vivo del panel: actividad por servicio, top de atacantes y reparto de severidad.'],
        ],
    ],
    [
        'capa'     => 'Ingeniería y operación',
        'subtitulo'=> 'Lo que mantiene el proyecto trazable y reproducible.',
        'icono'    => 'bi-tools',
        'color'    => 'success',
        'items'    => [
            ['nombre'=>'Git / GitHub',        'icono'=>'bi-git', 'desc'=>'Control de versiones del código del sensor y del panel. Flujo por ramas y revisión de cambios.'],
            ['nombre'=>'Linux (Debian/RPiOS)','icono'=>'bi-ubuntu', 'desc'=>'Base del sistema en el edge. Permisos, servicios y firewall sobre un Linux endurecido.'],
        ],
    ],
];

// Mapeo de color -> variables del sistema de diseño (tema claro cyber).
$color_map = [
    'primary' => ['bg' => 'rgba(var(--color-primary-rgb),.10)', 'color' => 'var(--color-primary)'],
    'success' => ['bg' => 'rgba(var(--color-success-rgb),.10)', 'color' => 'var(--color-success)'],
    'warning' => ['bg' => 'rgba(var(--color-warning-rgb),.14)', 'color' => 'var(--color-warning)'],
    'danger'  => ['bg' => 'rgba(var(--color-danger-rgb),.10)',  'color' => 'var(--color-danger)'],
];
?>

<main>
<!-- HERO de página -->
<section class="section-pad">
    <div class="container">
        <div class="text-center mx-auto" style="max-width:780px">
            <span class="badge-cyber mb-3 d-inline-block">Stack tecnológico</span>
            <h1 class="section-title">La pila completa, del cable al dashboard</h1>
            <div class="title-line"></div>
            <p class="section-subtitle">
                CyberGuard combina <strong>hardware accesible, software libre y servicios cloud gestionados</strong>.
                Nada de cajas negras: cada pieza está elegida por una razón y se puede auditar.
            </p>
            <div class="d-flex flex-wrap gap-2 justify-content-center mt-4">
                <span class="badge-cyber">Edge-first</span>
                <span class="badge-cyber badge-success">Open source</span>
                <span class="badge-cyber badge-warning">IA explicable</span>
                <span class="badge-cyber badge-danger">Respuesta activa</span>
            </div>
        </div>
    </div>
</section>

<!-- DIAGRAMA DE FLUJO DEL DATO -->
<section class="section-pad section-alt">
    <div class="container">
        <div class="text-center mb-5">
            <span class="badge-cyber mb-3 d-inline-block">El recorrido del dato</span>
            <h2 class="section-title">De un intento de intrusión a una decisión</h2>
            <div class="title-line"></div>
        </div>
        <div class="row g-3 justify-content-center text-center align-items-stretch">
            <?php
            $flujo = [
                ['i'=>'bi-bug',            't'=>'Ataque',    'd'=>'SSH · FTP · HTTP'],
                ['i'=>'bi-cpu',           't'=>'Sensor Pi',  'd'=>'Tailer + regex'],
                ['i'=>'bi-robot',         't'=>'Triaje IA',  'd'=>'Gemini + HITL'],
                ['i'=>'bi-fire',          't'=>'Firewall',   'd'=>'iptables ban'],
                ['i'=>'bi-cloud-arrow-up','t'=>'AWS IoT',    'd'=>'MQTT · mTLS'],
                ['i'=>'bi-bar-chart-line','t'=>'Panel SOC',  'd'=>'PHP · Chart.js'],
            ];
            $ultimo = count($flujo) - 1;
            foreach ($flujo as $k => $f): ?>
            <div class="col-4 col-md-2">
                <div class="surface-cyber h-100 p-3 d-flex flex-column align-items-center justify-content-center">
                    <i class="bi <?= $f['i'] ?> fs-3 text-gradient-cyber"></i>
                    <div class="fw-bold small mt-2"><?= $f['t'] ?></div>
                    <div class="text-muted" style="font-size:.72rem;font-family:var(--font-mono)"><?= $f['d'] ?></div>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
        <p class="text-center text-muted small mt-4 mb-0">
            <i class="bi bi-info-circle me-1"></i>
            Todo el bucle <em>detectar &rarr; decidir &rarr; actuar</em> ocurre en el borde; la nube recibe la copia ya cifrada.
        </p>
    </div>
</section>

<!-- STACK POR CAPAS -->
<?php foreach ($capas as $idx => $capa):
    $cc = $color_map[$capa['color']];
    $alt = $idx % 2 === 1 ? ' section-alt' : ''; ?>
<section class="section-pad<?= $alt ?>">
    <div class="container">
        <div class="d-flex align-items-center gap-3 mb-4">
            <div class="icon-wrap flex-shrink-0 mb-0" style="background:<?= $cc['bg'] ?>;color:<?= $cc['color'] ?>">
                <i class="bi <?= $capa['icono'] ?>"></i>
            </div>
            <div>
                <h2 class="fw-bold mb-1" style="font-family:var(--font-display)"><?= $capa['capa'] ?></h2>
                <p class="text-muted small mb-0"><?= $capa['subtitulo'] ?></p>
            </div>
        </div>
        <div class="row g-4">
            <?php foreach ($capa['items'] as $t): ?>
            <div class="col-sm-6 col-lg-4 col-xl-3">
                <div class="card-cyber h-100 d-flex gap-3 align-items-start">
                    <div class="icon-wrap flex-shrink-0 mb-0" style="background:<?= $cc['bg'] ?>;color:<?= $cc['color'] ?>">
                        <i class="bi <?= $t['icono'] ?>"></i>
                    </div>
                    <div>
                        <h6 class="fw-bold mb-1"><?= $t['nombre'] ?></h6>
                        <p class="text-muted small mb-0"><?= $t['desc'] ?></p>
                    </div>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
    </div>
</section>
<?php endforeach; ?>

<!-- DECISIONES DE DISEÑO -->
<section class="section-pad section-alt">
    <div class="container">
        <div class="text-center mb-5">
            <span class="badge-cyber mb-3 d-inline-block">Por qué este stack</span>
            <h2 class="section-title">Tres decisiones que lo definen todo</h2>
            <div class="title-line"></div>
        </div>
        <div class="row g-4">
            <div class="col-md-4">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-primary-rgb),.10);color:var(--color-primary)"><i class="bi bi-pc-display-horizontal"></i></div>
                    <h5 class="fw-bold mb-2">Inteligencia en el borde</h5>
                    <p class="text-muted small mb-0">Una Raspberry Pi de menos de 100 € decide en local. Si cae la red, el sensor sigue defendiendo; la nube no es un punto único de fallo.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-success-rgb),.10);color:var(--color-success)"><i class="bi bi-unlock"></i></div>
                    <h5 class="fw-bold mb-2">Open source primero</h5>
                    <p class="text-muted small mb-0">Python, Linux, iptables, MySQL: tecnologías auditables y sin vendor lock-in. El único servicio gestionado es el broker MQTT.</p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-warning-rgb),.14);color:var(--color-warning)"><i class="bi bi-eye"></i></div>
                    <h5 class="fw-bold mb-2">IA explicable, no mágica</h5>
                    <p class="text-muted small mb-0">El LLM aporta contexto, no veredictos opacos. Cada decisión queda razonada y, si hay duda, la valida una persona.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CTA FINAL -->
<section class="section-pad">
    <div class="container">
        <div class="surface-cyber text-center p-5">
            <h2 class="section-title mb-3">¿Quieres ver el stack en acción?</h2>
            <p class="text-muted mb-4 mx-auto" style="max-width:560px">
                El panel está alimentado por estas mismas piezas, atacando y defendiendo en tiempo real.
            </p>
            <div class="d-flex flex-wrap gap-3 justify-content-center">
                <a href="panel.php" class="btn-primary-cyber"><i class="bi bi-speedometer2 me-2"></i>Abrir el panel</a>
                <a href="como-funciona.php" class="btn-outline-cyber"><i class="bi bi-diagram-3 me-2"></i>Ver la arquitectura</a>
            </div>
        </div>
    </div>
</section>
</main>

<?php require 'includes/footer.php'; ?>
