<?php
$page_title = 'Servicios';
require 'includes/header.php';
require 'includes/navbar.php';

// Catálogo de servicios. Cada color usa las variables del sistema de diseño (tema claro cyber).
$servicios = [
    [
        'icono'  => 'bi-shield-lock',
        'color'  => 'primary',
        'titulo' => 'Defensa SSH activa',
        'desc'   => 'Inspección continua del puerto 22. Correlamos intentos fallidos por IP, usuario y huella temporal para distinguir un fallo legítimo de un ataque de fuerza bruta.',
        'tags'   => ['Brute-force', 'Credential stuffing', 'Fail2ban-like'],
    ],
    [
        'icono'  => 'bi-hdd-network',
        'color'  => 'success',
        'titulo' => 'Protección FTP / SFTP',
        'desc'   => 'Detección de ataques de diccionario contra el servicio de transferencia. El agente corta la sesión y publica el evento antes de que el atacante complete la enumeración de credenciales.',
        'tags'   => ['Dictionary attack', 'Anon login', 'Exfil temprana'],
    ],
    [
        'icono'  => 'bi-globe2',
        'color'  => 'warning',
        'titulo' => 'Análisis de tráfico web',
        'desc'   => 'Parseo de los logs de Apache en streaming. Identificamos escaneo de directorios, fuzzing de rutas, user-agents de herramientas (sqlmap, nikto) y patrones de exploits conocidos.',
        'tags'   => ['Path scanning', 'CVE probing', 'Bot fingerprinting'],
    ],
    [
        'icono'  => 'bi-cpu',
        'color'  => 'danger',
        'titulo' => 'Sensores edge autónomos',
        'desc'   => 'Cada Raspberry Pi opera como nodo independiente: detecta, decide y actúa en local aunque pierda conexión con la nube. El cerebro va en el borde, no en un servidor remoto.',
        'tags'   => ['Edge computing', 'Offline-first', 'Bajo consumo'],
    ],
    [
        'icono'  => 'bi-robot',
        'color'  => 'primary',
        'titulo' => 'Triaje con IA (Gemini)',
        'desc'   => 'Un modelo de lenguaje clasifica cada incidente, estima severidad y propone mitigación en lenguaje natural. Cuando la confianza es baja, escala a un humano en lugar de actuar a ciegas (HITL).',
        'tags'   => ['LLM triage', 'Severity scoring', 'Human-in-the-loop'],
    ],
    [
        'icono'  => 'bi-cloud-arrow-up',
        'color'  => 'success',
        'titulo' => 'Telemetría a AWS IoT Core',
        'desc'   => 'Cada evento viaja por MQTT con mTLS y QoS 1 hasta AWS IoT Core. Política por dispositivo, certificados X.509 rotables y trazabilidad íntegra desde el sensor hasta el panel.',
        'tags'   => ['MQTT + mTLS', 'QoS 1', 'X.509 por device'],
    ],
    [
        'icono'  => 'bi-bar-chart-line',
        'color'  => 'warning',
        'titulo' => 'Panel SOC en tiempo real',
        'desc'   => 'Dashboard web con KPIs vivos: ataques por servicio, top de IPs hostiles, mapa de severidad y tasa de bloqueo. Las gráficas se alimentan de la base de datos sin recargar la página.',
        'tags'   => ['KPIs en vivo', 'Top atacantes', 'Chart.js'],
    ],
    [
        'icono'  => 'bi-fire',
        'color'  => 'danger',
        'titulo' => 'Respuesta automática (firewall)',
        'desc'   => 'Cuando se supera el umbral, el Policy Engine traduce la decisión a reglas de iptables y banea la IP origen en segundos. Bloqueos con TTL para no envenenar la tabla de forma permanente.',
        'tags'   => ['iptables', 'Auto-ban', 'TTL configurable'],
    ],
    [
        'icono'  => 'bi-diagram-3',
        'color'  => 'primary',
        'titulo' => 'Discovery del entorno',
        'desc'   => 'El sensor se autoconfigura: descubre los servicios expuestos del host, genera su System Profile y adapta el triaje al contexto real de la máquina, sin tocar la configuración a mano.',
        'tags'   => ['Auto-config', 'System Profile', 'Cero fricción'],
    ],
];

// Mapeo de color -> variables del sistema de diseño. Usamos rgba(var(--*-rgb)) para los tintes.
$color_map = [
    'primary' => ['bg' => 'rgba(var(--color-primary-rgb),.10)', 'color' => 'var(--color-primary)'],
    'success' => ['bg' => 'rgba(var(--color-success-rgb),.10)', 'color' => 'var(--color-success)'],
    'warning' => ['bg' => 'rgba(var(--color-warning-rgb),.14)', 'color' => 'var(--color-warning)'],
    'danger'  => ['bg' => 'rgba(var(--color-danger-rgb),.10)',  'color' => 'var(--color-danger)'],
];

// Pilares del flujo "detectar -> decidir -> actuar".
$pilares = [
    ['icono' => 'bi-radar',          'titulo' => 'Detectar', 'desc' => 'Tailers en streaming sobre los logs de SSH, FTP y Apache. Latencia de detección por debajo de los 30 s.'],
    ['icono' => 'bi-cpu-fill',       'titulo' => 'Decidir',  'desc' => 'El Policy Engine evalúa umbrales y la IA aporta contexto. Decisión explicable, nunca una caja negra.'],
    ['icono' => 'bi-lightning-charge','titulo'=> 'Actuar',   'desc' => 'Bloqueo en el firewall local y publicación del incidente a la nube, todo de forma autónoma.'],
];
?>

<!-- HERO de página -->
<main>
<section class="section-pad">
    <div class="container">
        <div class="text-center mx-auto" style="max-width:780px">
            <span class="badge-cyber mb-3 d-inline-block">Lo que ofrecemos</span>
            <h1 class="section-title">Un SOC autónomo en cada borde de tu red</h1>
            <div class="title-line"></div>
            <p class="section-subtitle">
                CyberGuard despliega sensores que <strong>detectan, deciden y responden</strong> a las amenazas
                en segundos &mdash; con IA en el triaje y supervisión humana cuando importa. Esto es lo que cubre la plataforma.
            </p>
            <div class="d-flex flex-wrap gap-3 justify-content-center mt-4">
                <a href="como-funciona.php" class="btn-primary-cyber"><i class="bi bi-play-circle me-2"></i>Ver cómo funciona</a>
                <a href="panel.php" class="btn-outline-cyber"><i class="bi bi-speedometer2 me-2"></i>Abrir el panel</a>
            </div>
        </div>

        <!-- Mini-KPIs de cabecera -->
        <div class="row g-3 justify-content-center mt-5">
            <div class="col-6 col-md-3">
                <div class="surface-cyber text-center p-3 h-100">
                    <div class="fw-bold fs-4 text-gradient-cyber" style="font-variant-numeric:tabular-nums">&lt;30 s</div>
                    <div class="text-muted small">de detección a bloqueo</div>
                </div>
            </div>
            <div class="col-6 col-md-3">
                <div class="surface-cyber text-center p-3 h-100">
                    <div class="fw-bold fs-4 text-gradient-cyber" style="font-variant-numeric:tabular-nums">3</div>
                    <div class="text-muted small">servicios vigilados</div>
                </div>
            </div>
            <div class="col-6 col-md-3">
                <div class="surface-cyber text-center p-3 h-100">
                    <div class="fw-bold fs-4 text-gradient-cyber" style="font-variant-numeric:tabular-nums">100%</div>
                    <div class="text-muted small">tráfico cifrado mTLS</div>
                </div>
            </div>
            <div class="col-6 col-md-3">
                <div class="surface-cyber text-center p-3 h-100">
                    <div class="fw-bold fs-4 text-gradient-cyber" style="font-variant-numeric:tabular-nums">24/7</div>
                    <div class="text-muted small">sin operador de guardia</div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- GRID DE SERVICIOS -->
<section class="section-pad section-alt">
    <div class="container">
        <div class="text-center mb-5">
            <span class="badge-cyber mb-3 d-inline-block">Capacidades</span>
            <h2 class="section-title">Cobertura de extremo a extremo</h2>
            <div class="title-line"></div>
            <p class="section-subtitle">Del paquete que entra por el cable a la decisión que llega al panel del analista.</p>
        </div>

        <div class="row g-4">
            <?php foreach ($servicios as $s):
                $c = $color_map[$s['color']]; ?>
            <div class="col-md-6 col-lg-4">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:<?= $c['bg'] ?>;color:<?= $c['color'] ?>">
                        <i class="bi <?= $s['icono'] ?>"></i>
                    </div>
                    <h5 class="fw-bold mb-2"><?= $s['titulo'] ?></h5>
                    <p class="text-muted small"><?= $s['desc'] ?></p>
                    <div class="d-flex flex-wrap gap-2 mt-auto pt-2">
                        <?php foreach ($s['tags'] as $tag): ?>
                            <span class="badge-cyber small"><?= $tag ?></span>
                        <?php endforeach; ?>
                    </div>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
    </div>
</section>

<!-- FLUJO: DETECTAR -> DECIDIR -> ACTUAR -->
<section class="section-pad">
    <div class="container">
        <div class="text-center mb-5">
            <span class="badge-cyber mb-3 d-inline-block">Cómo trabaja</span>
            <h2 class="section-title">Detectar &middot; Decidir &middot; Actuar</h2>
            <div class="title-line"></div>
            <p class="section-subtitle">Un único bucle de respuesta que se ejecuta entero dentro de la Raspberry Pi.</p>
        </div>
        <div class="row g-4">
            <?php foreach ($pilares as $i => $p): ?>
            <div class="col-md-4">
                <div class="card-cyber h-100 text-center">
                    <div class="timeline-num mx-auto mb-3"><?= $i + 1 ?></div>
                    <div class="icon-wrap mx-auto" style="background:rgba(var(--color-primary-rgb),.10);color:var(--color-primary)">
                        <i class="bi <?= $p['icono'] ?>"></i>
                    </div>
                    <h5 class="fw-bold mb-2"><?= $p['titulo'] ?></h5>
                    <p class="text-muted small mb-0"><?= $p['desc'] ?></p>
                </div>
            </div>
            <?php endforeach; ?>
        </div>
    </div>
</section>

<!-- DIFERENCIADORES -->
<section class="section-pad section-alt">
    <div class="container">
        <div class="row g-5 align-items-center">
            <div class="col-lg-5">
                <span class="badge-cyber mb-3 d-inline-block">Por qué CyberGuard</span>
                <h2 class="section-title text-start">Seguridad que decide sola, pero rinde cuentas</h2>
                <p class="text-muted">
                    La mayoría de honeypots solo registran. CyberGuard <strong>actúa</strong>: corta la conexión,
                    banea la IP y deja una traza explicable de por qué lo hizo. Y cuando la IA no lo tiene claro,
                    para y te pregunta.
                </p>
                <a href="contacto.php" class="btn-primary-cyber mt-2"><i class="bi bi-chat-dots me-2"></i>Hablar con el equipo</a>
            </div>
            <div class="col-lg-7">
                <div class="row g-3">
                    <div class="col-sm-6">
                        <div class="surface-cyber p-3 h-100">
                            <i class="bi bi-cpu fs-4 text-gradient-cyber"></i>
                            <h6 class="fw-bold mt-2 mb-1">Inteligencia en el borde</h6>
                            <p class="text-muted small mb-0">Decide en local en milisegundos; la nube es para auditar, no para reaccionar.</p>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="surface-cyber p-3 h-100">
                            <i class="bi bi-people fs-4 text-gradient-cyber"></i>
                            <h6 class="fw-bold mt-2 mb-1">Humano en el bucle</h6>
                            <p class="text-muted small mb-0">Las acciones de alto impacto requieren validación. Cero falsos baneos a ciegas.</p>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="surface-cyber p-3 h-100">
                            <i class="bi bi-shield-check fs-4 text-gradient-cyber"></i>
                            <h6 class="fw-bold mt-2 mb-1">Trazabilidad total</h6>
                            <p class="text-muted small mb-0">Cada evento queda firmado y replicado en AWS IoT Core con su cadena de decisión.</p>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="surface-cyber p-3 h-100">
                            <i class="bi bi-arrows-angle-expand fs-4 text-gradient-cyber"></i>
                            <h6 class="fw-bold mt-2 mb-1">Escala sumando nodos</h6>
                            <p class="text-muted small mb-0">Añades una Raspberry Pi y se autoconfigura. La infraestructura central no se toca.</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CTA FINAL -->
<section class="section-pad">
    <div class="container">
        <div class="surface-cyber text-center p-5">
            <h2 class="section-title mb-3">¿Lo desplegamos en tu entorno?</h2>
            <p class="text-muted mb-4 mx-auto" style="max-width:560px">
                Te montamos un sensor de demostración en menos de una tarde y te enseñamos
                el panel con tráfico real atacando el honeypot.
            </p>
            <div class="d-flex flex-wrap gap-3 justify-content-center">
                <a href="como-funciona.php" class="btn-primary-cyber"><i class="bi bi-diagram-3 me-2"></i>Ver la arquitectura</a>
                <a href="contacto.php" class="btn-outline-cyber"><i class="bi bi-envelope me-2"></i>Contactar</a>
            </div>
        </div>
    </div>
</section>
</main>

<?php require 'includes/footer.php'; ?>
