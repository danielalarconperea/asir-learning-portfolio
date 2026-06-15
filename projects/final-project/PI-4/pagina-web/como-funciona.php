<?php
$page_title = 'Cómo funciona';
require 'includes/header.php';
require 'includes/navbar.php';
?>

<main>

<!-- HERO DE SECCIÓN -->
<section class="container py-6">
    <div class="row justify-content-center text-center">
        <div class="col-lg-9">
            <span class="badge-cyber mb-3 d-inline-block">Arquitectura del sistema</span>
            <h1 class="section-title">Un SOC autónomo que cabe en la palma de la mano</h1>
            <div class="title-line"></div>
            <p class="section-subtitle" style="max-width:640px;">
                SentinelIT distribuye la inteligencia entre el <strong>borde</strong> y la <strong>nube</strong>:
                sensores sobre Raspberry Pi vigilan la red del cliente, mientras un coordinador con IA
                correlaciona, decide y ordena la respuesta. Detección y bloqueo en segundos, sin operadores de guardia.
            </p>
        </div>
    </div>

    <!-- KPIs de rendimiento del pipeline -->
    <div class="row g-4 justify-content-center mt-2">
        <div class="col-6 col-md-3">
            <div class="kpi-card h-100">
                <div class="kpi-value text-gradient-cyber">&lt;1<span style="font-size:1.3rem">s</span></div>
                <div class="kpi-label">Captura → nube</div>
            </div>
        </div>
        <div class="col-6 col-md-3">
            <div class="kpi-card h-100">
                <div class="kpi-value text-gradient-cyber">~8<span style="font-size:1.3rem">s</span></div>
                <div class="kpi-label">Decisión de la IA</div>
            </div>
        </div>
        <div class="col-6 col-md-3">
            <div class="kpi-card h-100">
                <div class="kpi-value text-gradient-cyber">mTLS</div>
                <div class="kpi-label">Cifrado extremo a extremo</div>
            </div>
        </div>
        <div class="col-6 col-md-3">
            <div class="kpi-card h-100">
                <div class="kpi-value text-gradient-cyber">24/7</div>
                <div class="kpi-label">Sin intervención</div>
            </div>
        </div>
    </div>
</section>

<!-- LOS CUATRO COMPONENTES -->
<section class="section-alt section-pad">
    <div class="container">
        <div class="text-center mb-5">
            <span class="badge-cyber mb-3 d-inline-block">Las cuatro piezas</span>
            <h2 class="section-title">De la línea de log al bloqueo</h2>
            <div class="title-line"></div>
            <p class="section-subtitle">
                Cuatro componentes especializados, conectados por un único canal MQTT cifrado.
                Cada uno hace una cosa y la hace bien.
            </p>
        </div>

        <div class="row g-4">
            <!-- Sensor -->
            <div class="col-md-6 col-lg-3">
                <div class="card-cyber h-100">
                    <div class="icon-wrap"><i class="bi bi-cpu"></i></div>
                    <span class="badge-cyber badge-success mb-2 d-inline-block">Borde · Cliente</span>
                    <h6 class="fw-bold">Sensor (Raspberry Pi 4)</h6>
                    <p class="text-muted small">
                        Se despliega dentro de la red a proteger. Lee en streaming los logs de
                        <strong>SSH, FTP y Apache</strong>, extrae los indicadores con expresiones
                        regulares y firma cada evento antes de enviarlo. Sin tráfico de logs hacia
                        afuera: solo viajan eventos estructurados.
                    </p>
                    <div class="d-flex flex-wrap gap-1 mt-2">
                        <span class="badge-cyber">agente_monitor.py</span>
                        <span class="badge-cyber">journalctl</span>
                    </div>
                </div>
            </div>

            <!-- AWS IoT Core -->
            <div class="col-md-6 col-lg-3">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-success-rgb),0.10);color:var(--color-success)"><i class="bi bi-cloud-arrow-up"></i></div>
                    <span class="badge-cyber mb-2 d-inline-block">Transporte · Nube</span>
                    <h6 class="fw-bold">AWS IoT Core</h6>
                    <p class="text-muted small">
                        Broker MQTT gestionado que actúa de columna vertebral. Multiplexa los eventos
                        de todos los sensores con autenticación <strong>mTLS por certificado X.509</strong>,
                        de modo que cada Raspberry Pi tiene una identidad única y revocable.
                    </p>
                    <div class="d-flex flex-wrap gap-1 mt-2">
                        <span class="badge-cyber">MQTT</span>
                        <span class="badge-cyber">TLS 1.2</span>
                        <span class="badge-cyber">X.509</span>
                    </div>
                </div>
            </div>

            <!-- Coordinador -->
            <div class="col-md-6 col-lg-3">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-warning-rgb),0.15);color:#9A7400"><i class="bi bi-diagram-3"></i></div>
                    <span class="badge-cyber badge-warning mb-2 d-inline-block">Cerebro · Nube/Edge</span>
                    <h6 class="fw-bold">Coordinador (Raspberry Pi 5)</h6>
                    <p class="text-muted small">
                        El cerebro del SOC. Se suscribe a todos los eventos, mantiene el historial de
                        cada IP y consulta a la <strong>IA (Gemini)</strong> para clasificar la amenaza,
                        razonar la mitigación y emitir la orden de bloqueo de vuelta al sensor.
                    </p>
                    <div class="d-flex flex-wrap gap-1 mt-2">
                        <span class="badge-cyber">coordinador.py</span>
                        <span class="badge-cyber">Gemini</span>
                    </div>
                </div>
            </div>

            <!-- Panel web -->
            <div class="col-md-6 col-lg-3">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-danger-rgb),0.10);color:var(--color-danger)"><i class="bi bi-bar-chart"></i></div>
                    <span class="badge-cyber badge-danger mb-2 d-inline-block">Visibilidad · Operador</span>
                    <h6 class="fw-bold">Panel web</h6>
                    <p class="text-muted small">
                        La ventana del analista. Muestra en vivo ataques, IPs bloqueadas, mapas de
                        origen y series temporales, y permite la <strong>supervisión humana (HITL)</strong>
                        para validar o revertir las decisiones automáticas cuando hace falta.
                    </p>
                    <div class="d-flex flex-wrap gap-1 mt-2">
                        <span class="badge-cyber">PHP</span>
                        <span class="badge-cyber">Chart.js</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- FLUJO DE UN ATAQUE (TIMELINE) -->
<section class="container section-pad">
    <div class="row justify-content-center">
        <div class="col-lg-9 text-center mb-5">
            <span class="badge-cyber mb-3 d-inline-block">Anatomía de una detección</span>
            <h2 class="section-title">Qué ocurre cuando alguien ataca</h2>
            <div class="title-line"></div>
            <p class="section-subtitle">
                Seguimos un intento real de fuerza bruta por SSH desde que se escribe en el log
                hasta que el atacante queda fuera. Tiempo total típico: menos de quince segundos.
            </p>
        </div>
    </div>

    <div class="row justify-content-center">
        <div class="col-lg-8">
            <div class="timeline-step">
                <div class="timeline-num">1</div>
                <div>
                    <div class="d-flex flex-wrap align-items-center gap-2 mb-1">
                        <h6 class="fw-bold mb-0">Intento de acceso</h6>
                        <span class="badge-cyber badge-danger">t = 0,0 s</span>
                    </div>
                    <p class="text-muted small mb-2">
                        Una IP desconocida intenta autenticarse por SSH con credenciales inválidas.
                        El sistema operativo del activo protegido deja constancia en el journal.
                    </p>
                    <pre class="surface-cyber p-2 mb-0" style="overflow-x:auto;"><code style="color:var(--color-text);font-size:.78rem;">Failed password for invalid user admin from 203.0.113.45 port 51224 ssh2</code></pre>
                </div>
            </div>

            <div class="timeline-step">
                <div class="timeline-num">2</div>
                <div>
                    <div class="d-flex flex-wrap align-items-center gap-2 mb-1">
                        <h6 class="fw-bold mb-0">Captura en el borde</h6>
                        <span class="badge-cyber badge-success">+0,1 s</span>
                    </div>
                    <p class="text-muted small mb-0">
                        El agente de la Pi 4 sigue el log con <code style="color:var(--color-primary)">journalctl -f</code>,
                        detecta la línea al instante y extrae IP, servicio y tipo de evento mediante
                        expresiones regulares. Ningún log abandona la red del cliente.
                    </p>
                </div>
            </div>

            <div class="timeline-step">
                <div class="timeline-num">3</div>
                <div>
                    <div class="d-flex flex-wrap align-items-center gap-2 mb-1">
                        <h6 class="fw-bold mb-0">Publicación cifrada</h6>
                        <span class="badge-cyber">+0,8 s</span>
                    </div>
                    <p class="text-muted small mb-0">
                        El evento se serializa a JSON, se firma y se publica en
                        <code style="color:var(--color-primary)">sentinel/eventos</code> sobre AWS IoT Core
                        vía MQTT con mTLS. El payload pesa pocos cientos de bytes: viaja en menos de un segundo
                        incluso con conexiones modestas.
                    </p>
                </div>
            </div>

            <div class="timeline-step">
                <div class="timeline-num">4</div>
                <div>
                    <div class="d-flex flex-wrap align-items-center gap-2 mb-1">
                        <h6 class="fw-bold mb-0">Triaje con IA</h6>
                        <span class="badge-cyber badge-warning">+8 s</span>
                    </div>
                    <p class="text-muted small mb-0">
                        El coordinador recibe el evento, recupera el historial de
                        <code style="color:var(--color-primary)">203.0.113.45</code> y consulta a Gemini con
                        el contexto del activo. La IA clasifica el patrón como fuerza bruta sostenida,
                        asigna severidad <strong>alta</strong> y propone bloqueo inmediato.
                    </p>
                </div>
            </div>

            <div class="timeline-step">
                <div class="timeline-num">5</div>
                <div>
                    <div class="d-flex flex-wrap align-items-center gap-2 mb-1">
                        <h6 class="fw-bold mb-0">Respuesta automática</h6>
                        <span class="badge-cyber badge-danger">+9 s</span>
                    </div>
                    <p class="text-muted small mb-2">
                        El coordinador publica la orden en <code style="color:var(--color-primary)">sentinel/ordenes</code>.
                        El agente la recibe y aplica la regla en el cortafuegos del propio activo.
                        La IP queda aislada antes de poder probar la siguiente contraseña.
                    </p>
                    <pre class="surface-cyber p-2 mb-0" style="overflow-x:auto;"><code style="color:var(--color-text);font-size:.78rem;">iptables -A INPUT -s 203.0.113.45 -j DROP</code></pre>
                </div>
            </div>

            <div class="timeline-step">
                <div class="timeline-num"><i class="bi bi-eye"></i></div>
                <div>
                    <div class="d-flex flex-wrap align-items-center gap-2 mb-1">
                        <h6 class="fw-bold mb-0">Supervisión humana (HITL)</h6>
                        <span class="badge-cyber">posterior</span>
                    </div>
                    <p class="text-muted small mb-0">
                        Todo queda registrado en el panel con su justificación. El analista puede
                        confirmar el bloqueo, revertirlo o ajustar la política. La máquina actúa en
                        milisegundos; la persona conserva siempre la última palabra.
                    </p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- POR QUÉ ESTE DISEÑO -->
<section class="section-alt section-pad">
    <div class="container">
        <div class="text-center mb-5">
            <span class="badge-cyber mb-3 d-inline-block">Decisiones de diseño</span>
            <h2 class="section-title">Por qué edge + nube, y no solo nube</h2>
            <div class="title-line"></div>
        </div>
        <div class="row g-4">
            <div class="col-md-6 col-lg-4">
                <div class="card-cyber h-100">
                    <div class="icon-wrap"><i class="bi bi-shield-lock"></i></div>
                    <h5 class="fw-bold mb-2">Tus logs no salen</h5>
                    <p class="text-muted small mb-0">
                        El análisis bruto ocurre en el borde. A la nube solo viajan eventos
                        estructurados y firmados, nunca el contenido completo de los logs.
                        Menos superficie expuesta y menos coste de transferencia.
                    </p>
                </div>
            </div>
            <div class="col-md-6 col-lg-4">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-success-rgb),0.10);color:var(--color-success)"><i class="bi bi-lightning-charge"></i></div>
                    <h5 class="fw-bold mb-2">Respuesta local</h5>
                    <p class="text-muted small mb-0">
                        El bloqueo se aplica en el propio activo atacado. Aunque la conexión a la nube
                        se degrade, las reglas ya desplegadas siguen protegiendo la red.
                    </p>
                </div>
            </div>
            <div class="col-md-6 col-lg-4">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-warning-rgb),0.15);color:#9A7400"><i class="bi bi-diagram-2"></i></div>
                    <h5 class="fw-bold mb-2">Escala horizontal</h5>
                    <p class="text-muted small mb-0">
                        Añadir un sensor es enchufar otra Raspberry Pi y darle su certificado.
                        El coordinador y el panel absorben el nuevo nodo sin reconfigurar nada.
                    </p>
                </div>
            </div>
            <div class="col-md-6 col-lg-4">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-danger-rgb),0.10);color:var(--color-danger)"><i class="bi bi-cpu-fill"></i></div>
                    <h5 class="fw-bold mb-2">Hardware accesible</h5>
                    <p class="text-muted small mb-0">
                        Sin appliances propietarios de cinco cifras. Todo corre sobre Raspberry Pi y
                        servicios gestionados de pago por uso: capacidades de SOC al alcance de una pyme.
                    </p>
                </div>
            </div>
            <div class="col-md-6 col-lg-4">
                <div class="card-cyber h-100">
                    <div class="icon-wrap"><i class="bi bi-robot"></i></div>
                    <h5 class="fw-bold mb-2">IA con contexto</h5>
                    <p class="text-muted small mb-0">
                        La IA no clasifica a ciegas: recibe el perfil del activo y el historial de la IP,
                        así que distingue un escaneo aislado de una campaña dirigida.
                    </p>
                </div>
            </div>
            <div class="col-md-6 col-lg-4">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-success-rgb),0.10);color:var(--color-success)"><i class="bi bi-person-check"></i></div>
                    <h5 class="fw-bold mb-2">Humano al mando</h5>
                    <p class="text-muted small mb-0">
                        Cada acción automática queda trazada y es reversible desde el panel.
                        La automatización gana velocidad sin renunciar al control del analista.
                    </p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- STACK TECNOLÓGICO -->
<section class="container section-pad">
    <div class="text-center mb-5">
        <span class="badge-cyber mb-3 d-inline-block">Bajo el capó</span>
        <h2 class="section-title">El stack, sin humo</h2>
        <div class="title-line"></div>
        <p class="section-subtitle">Tecnologías estándar y probadas. Sin cajas negras.</p>
    </div>
    <div class="row g-4 justify-content-center">
        <div class="col-md-4">
            <div class="surface-cyber p-4 h-100">
                <h6 class="fw-bold d-flex align-items-center gap-2 mb-3">
                    <i class="bi bi-hdd-network" style="color:var(--color-primary)"></i> Borde
                </h6>
                <ul class="list-unstyled text-muted small mb-0 d-grid gap-2">
                    <li><i class="bi bi-check2 me-1" style="color:var(--color-success)"></i> Raspberry Pi 4 / 5</li>
                    <li><i class="bi bi-check2 me-1" style="color:var(--color-success)"></i> Python 3 · paho-mqtt</li>
                    <li><i class="bi bi-check2 me-1" style="color:var(--color-success)"></i> systemd · journalctl</li>
                    <li><i class="bi bi-check2 me-1" style="color:var(--color-success)"></i> iptables / nftables</li>
                </ul>
            </div>
        </div>
        <div class="col-md-4">
            <div class="surface-cyber p-4 h-100">
                <h6 class="fw-bold d-flex align-items-center gap-2 mb-3">
                    <i class="bi bi-cloud" style="color:var(--color-primary)"></i> Nube e IA
                </h6>
                <ul class="list-unstyled text-muted small mb-0 d-grid gap-2">
                    <li><i class="bi bi-check2 me-1" style="color:var(--color-success)"></i> AWS IoT Core (MQTT)</li>
                    <li><i class="bi bi-check2 me-1" style="color:var(--color-success)"></i> mTLS · certificados X.509</li>
                    <li><i class="bi bi-check2 me-1" style="color:var(--color-success)"></i> Google Gemini (triaje)</li>
                    <li><i class="bi bi-check2 me-1" style="color:var(--color-success)"></i> Políticas de mitigación</li>
                </ul>
            </div>
        </div>
        <div class="col-md-4">
            <div class="surface-cyber p-4 h-100">
                <h6 class="fw-bold d-flex align-items-center gap-2 mb-3">
                    <i class="bi bi-window-stack" style="color:var(--color-primary)"></i> Visibilidad
                </h6>
                <ul class="list-unstyled text-muted small mb-0 d-grid gap-2">
                    <li><i class="bi bi-check2 me-1" style="color:var(--color-success)"></i> Panel web en PHP</li>
                    <li><i class="bi bi-check2 me-1" style="color:var(--color-success)"></i> Gráficas con Chart.js</li>
                    <li><i class="bi bi-check2 me-1" style="color:var(--color-success)"></i> Histórico de eventos</li>
                    <li><i class="bi bi-check2 me-1" style="color:var(--color-success)"></i> Validación humana (HITL)</li>
                </ul>
            </div>
        </div>
    </div>
</section>

<!-- CTA FINAL -->
<section class="section-alt section-pad">
    <div class="container text-center">
        <h2 class="section-title mb-3">¿Quieres verlo sobre tu red?</h2>
        <p class="text-muted mb-4" style="max-width:540px;margin-inline:auto;">
            Te montamos una demostración con un sensor real y te enseñamos el flujo completo,
            desde el primer intento de acceso hasta el bloqueo en el panel.
        </p>
        <div class="d-flex flex-wrap justify-content-center gap-3">
            <a href="contacto.php" class="btn-primary-cyber">Solicitar una demo</a>
            <a href="servicios.php" class="btn-outline-cyber">Ver servicios</a>
        </div>
    </div>
</section>

</main>

<?php require 'includes/footer.php'; ?>
