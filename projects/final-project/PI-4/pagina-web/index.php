<?php
$page_title = 'Inicio';
require 'includes/header.php';
require 'includes/navbar.php';
?>

<!-- HERO -->
<section class="hero px-3">
    <div class="container">
        <div class="row align-items-center g-5">
            <div class="col-lg-7">
                <span class="badge-cyber badge-success mb-4 d-inline-flex align-items-center gap-2">
                    <i class="bi bi-broadcast"></i> SOC operativo &middot; 24/7/365
                </span>
                <h1 class="hero-title mb-4">
                    Tu SOC autónomo<br>
                    <span>en el borde</span><br>
                    de la red
                </h1>
                <p class="hero-subtitle mb-4">
                    SentinelIT convierte una Raspberry Pi en un sensor de seguridad gestionado:
                    detecta, prioriza con IA y mitiga amenazas en el propio dispositivo, en
                    segundos y sin reglas que mantener. La nube solo orquesta; la decisión
                    ocurre donde está el ataque.
                </p>
                <ul class="list-unstyled hero-points mb-5">
                    <li class="d-flex align-items-start gap-2 mb-2">
                        <i class="bi bi-check-circle-fill text-success mt-1"></i>
                        <span>Respuesta automática en <strong>&lt; 30&nbsp;s</strong> desde la detección al bloqueo</span>
                    </li>
                    <li class="d-flex align-items-start gap-2 mb-2">
                        <i class="bi bi-check-circle-fill text-success mt-1"></i>
                        <span>Triaje con IA (Gemini) y <strong>humano en el bucle</strong> para acciones críticas</span>
                    </li>
                    <li class="d-flex align-items-start gap-2">
                        <i class="bi bi-check-circle-fill text-success mt-1"></i>
                        <span>Telemetría cifrada de extremo a extremo sobre <strong>MQTT&nbsp;+&nbsp;mTLS</strong></span>
                    </li>
                </ul>
                <div class="d-flex flex-wrap gap-3">
                    <a href="servicios.php"     class="btn-primary-cyber"><i class="bi bi-grid-1x2 me-2"></i>Ver servicios</a>
                    <a href="como-funciona.php" class="btn-outline-cyber"><i class="bi bi-diagram-3 me-2"></i>Cómo funciona</a>
                </div>
            </div>
            <div class="col-lg-5 d-none d-lg-flex justify-content-center mt-5 mt-lg-0">
                <!-- Diagrama decorativo SVG (tema claro: SOC edge → nube) -->
                <svg viewBox="0 0 320 320" width="320" height="320" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Diagrama de la arquitectura: sensores en el borde conectados a un SOC central y a la nube">
                    <circle cx="160" cy="160" r="140" fill="none" stroke="rgba(0,86,210,0.10)" stroke-width="1"/>
                    <circle cx="160" cy="160" r="100" fill="none" stroke="rgba(0,86,210,0.14)" stroke-width="1"/>
                    <circle cx="160" cy="160" r="60"  fill="none" stroke="rgba(0,86,210,0.20)" stroke-width="1"/>
                    <circle cx="160" cy="160" r="30"  fill="rgba(0,86,210,0.10)" stroke="#0056D2" stroke-width="1.5"/>
                    <text x="160" y="165" text-anchor="middle" fill="#0056D2" font-size="14" font-family="JetBrains Mono" font-weight="600">SOC</text>
                    <!-- Conexiones -->
                    <line x1="160" y1="44"  x2="160" y2="130" stroke="rgba(0,86,210,0.30)" stroke-width="1" stroke-dasharray="4"/>
                    <line x1="276" y1="160" x2="190" y2="160" stroke="rgba(0,86,210,0.30)" stroke-width="1" stroke-dasharray="4"/>
                    <line x1="160" y1="276" x2="160" y2="190" stroke="rgba(0,86,210,0.30)" stroke-width="1" stroke-dasharray="4"/>
                    <line x1="44"  y1="160" x2="130" y2="160" stroke="rgba(0,86,210,0.30)" stroke-width="1" stroke-dasharray="4"/>
                    <!-- Nodos -->
                    <circle cx="160" cy="30"  r="14" fill="#FFFFFF" stroke="#00875A" stroke-width="1.5"/>
                    <circle cx="290" cy="160" r="14" fill="#FFFFFF" stroke="#0056D2" stroke-width="1.5"/>
                    <circle cx="160" cy="290" r="14" fill="#FFFFFF" stroke="#00875A" stroke-width="1.5"/>
                    <circle cx="30"  cy="160" r="14" fill="#FFFFFF" stroke="#DC3545" stroke-width="1.5"/>
                    <text x="160" y="34"  text-anchor="middle" fill="#00875A" font-size="9" font-family="JetBrains Mono">Pi</text>
                    <text x="290" y="164" text-anchor="middle" fill="#0056D2" font-size="9" font-family="JetBrains Mono">AWS</text>
                    <text x="160" y="294" text-anchor="middle" fill="#00875A" font-size="9" font-family="JetBrains Mono">Pi</text>
                    <text x="30"  y="164" text-anchor="middle" fill="#DC3545" font-size="9" font-family="JetBrains Mono">!</text>
                    <text x="160" y="20"  text-anchor="middle" fill="#6C757D" font-size="8" font-family="JetBrains Mono">sensor</text>
                    <text x="290" y="186" text-anchor="middle" fill="#6C757D" font-size="8" font-family="JetBrains Mono">IoT Core</text>
                    <text x="160" y="312" text-anchor="middle" fill="#6C757D" font-size="8" font-family="JetBrains Mono">sensor</text>
                    <text x="30"  y="186" text-anchor="middle" fill="#6C757D" font-size="8" font-family="JetBrains Mono">amenaza</text>
                </svg>
            </div>
        </div>
    </div>
</section>

<!-- TIRA DE CONFIANZA / STACK -->
<section class="py-4 section-alt">
    <div class="container">
        <p class="text-center text-muted small text-uppercase mb-3" style="letter-spacing:.08em">
            Construido sobre tecnología probada
        </p>
        <div class="row row-cols-2 row-cols-md-3 row-cols-lg-6 g-3 text-center align-items-center justify-content-center">
            <div class="col"><span class="badge-cyber"><i class="bi bi-cpu me-1"></i>Raspberry Pi</span></div>
            <div class="col"><span class="badge-cyber"><i class="bi bi-stars me-1"></i>Gemini AI</span></div>
            <div class="col"><span class="badge-cyber"><i class="bi bi-cloud me-1"></i>AWS IoT Core</span></div>
            <div class="col"><span class="badge-cyber"><i class="bi bi-diagram-2 me-1"></i>MQTT</span></div>
            <div class="col"><span class="badge-cyber"><i class="bi bi-shield-lock me-1"></i>mTLS</span></div>
            <div class="col"><span class="badge-cyber"><i class="bi bi-bricks me-1"></i>nftables</span></div>
        </div>
    </div>
</section>

<!-- PROPUESTA DE VALOR -->
<section class="py-6">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="section-title">Seguridad que decide sola, donde importa</h2>
            <div class="title-line"></div>
            <p class="section-subtitle">
                No es otro panel que avisa cuando ya es tarde. SentinelIT actúa en el
                dispositivo, recorta el tiempo de exposición y deja el control en tus manos.
            </p>
        </div>
        <div class="row g-4">
            <div class="col-md-6 col-lg-3">
                <div class="card-cyber h-100">
                    <div class="icon-wrap"><i class="bi bi-lightning-charge"></i></div>
                    <h5 class="fw-bold mb-2">Respuesta en segundos</h5>
                    <p class="text-muted small mb-0">
                        Del primer paquete malicioso al bloqueo en menos de 30&nbsp;s. La
                        decisión se toma en el borde, sin esperar a un analista ni a la nube.
                    </p>
                </div>
            </div>
            <div class="col-md-6 col-lg-3">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-success-rgb),0.1);color:var(--color-success)"><i class="bi bi-robot"></i></div>
                    <h5 class="fw-bold mb-2">Triaje con IA</h5>
                    <p class="text-muted small mb-0">
                        El motor de políticas y el LLM (Gemini) clasifican cada evento,
                        descartan el ruido y proponen la mitigación: bloquear IP, cerrar
                        puerto o aislar servicio.
                    </p>
                </div>
            </div>
            <div class="col-md-6 col-lg-3">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-warning-rgb),0.15);color:#9A7400"><i class="bi bi-person-check"></i></div>
                    <h5 class="fw-bold mb-2">Humano en el bucle</h5>
                    <p class="text-muted small mb-0">
                        Las acciones reversibles se aplican solas; las críticas esperan tu
                        visto bueno desde el panel. Control total, cero piloto automático ciego.
                    </p>
                </div>
            </div>
            <div class="col-md-6 col-lg-3">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-danger-rgb),0.1);color:var(--color-danger)"><i class="bi bi-shield-lock"></i></div>
                    <h5 class="fw-bold mb-2">Cifrado de extremo a extremo</h5>
                    <p class="text-muted small mb-0">
                        Cada sensor se autentica con certificado propio y habla por
                        MQTT&nbsp;sobre&nbsp;mTLS contra AWS IoT Core. Nada viaja en claro.
                    </p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CÓMO ENCAJA / FLUJO -->
<section class="py-6 section-alt">
    <div class="container">
        <div class="row align-items-center g-5">
            <div class="col-lg-5">
                <span class="badge-cyber mb-3 d-inline-block">Detectar &rarr; Decidir &rarr; Mitigar</span>
                <h2 class="section-title mb-3">Del paquete sospechoso a la regla de firewall, sin pasar por ti</h2>
                <p class="text-muted mb-4">
                    El sensor observa el tráfico y el comportamiento del dispositivo, levanta
                    una alerta y la enriquece con el perfil del sistema. El SOC la puntúa, y si
                    la política lo permite, el agente aplica la contramedida en local y reporta
                    de vuelta. Todo queda registrado y es auditable.
                </p>
                <a href="como-funciona.php" class="btn-outline-cyber">
                    Ver el flujo completo <i class="bi bi-arrow-right ms-1"></i>
                </a>
            </div>
            <div class="col-lg-7">
                <div class="row g-4">
                    <div class="col-sm-6">
                        <div class="surface-cyber h-100 p-4">
                            <div class="d-flex align-items-center gap-2 mb-2">
                                <span class="badge-cyber">01</span>
                                <h6 class="fw-bold mb-0">Detección en el borde</h6>
                            </div>
                            <p class="text-muted small mb-0">
                                Sondas en la Raspberry Pi vigilan conexiones, escaneos y
                                fuerza bruta sobre SSH y servicios expuestos.
                            </p>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="surface-cyber h-100 p-4">
                            <div class="d-flex align-items-center gap-2 mb-2">
                                <span class="badge-cyber">02</span>
                                <h6 class="fw-bold mb-0">Enriquecimiento</h6>
                            </div>
                            <p class="text-muted small mb-0">
                                El evento se acompaña del System Profile del dispositivo para
                                dar contexto real al triaje, no una alerta a ciegas.
                            </p>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="surface-cyber h-100 p-4">
                            <div class="d-flex align-items-center gap-2 mb-2">
                                <span class="badge-cyber">03</span>
                                <h6 class="fw-bold mb-0">Decisión (IA + política)</h6>
                            </div>
                            <p class="text-muted small mb-0">
                                El Policy Engine y Gemini deciden la severidad y la acción:
                                automática si es segura, o a revisión humana si es crítica.
                            </p>
                        </div>
                    </div>
                    <div class="col-sm-6">
                        <div class="surface-cyber h-100 p-4">
                            <div class="d-flex align-items-center gap-2 mb-2">
                                <span class="badge-cyber badge-success">04</span>
                                <h6 class="fw-bold mb-0">Mitigación</h6>
                            </div>
                            <p class="text-muted small mb-0">
                                El agente aplica la regla (drop de IP, cierre de puerto) con
                                nftables en local y confirma el resultado al SOC.
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- ESTADÍSTICAS -->
<section class="py-6">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="section-title">La plataforma en cifras</h2>
            <div class="title-line"></div>
            <p class="section-subtitle">
                Datos agregados de la flota de sensores en demostración durante las últimas 24&nbsp;horas.
            </p>
        </div>
        <div class="row g-4 text-center">
            <div class="col-6 col-md-3">
                <div class="stat-counter" data-target="12847">0</div>
                <div class="stat-label">Eventos analizados</div>
            </div>
            <div class="col-6 col-md-3">
                <div class="stat-counter" data-target="11203">0</div>
                <div class="stat-label">Amenazas mitigadas</div>
            </div>
            <div class="col-6 col-md-3">
                <div class="stat-counter" data-target="98">0</div>
                <div class="stat-label">% precisión del triaje</div>
            </div>
            <div class="col-6 col-md-3">
                <div class="stat-counter" data-target="24">0</div>
                <div class="stat-label">Horas de monitorización continua</div>
            </div>
        </div>
        <p class="text-center text-muted small mt-4 mb-0">
            <i class="bi bi-info-circle me-1"></i>
            Cifras de demostración. La latencia media de respuesta medida es de <strong>18&nbsp;s</strong> con un tiempo de actividad del <strong>99,9&nbsp;%</strong>.
        </p>
    </div>
</section>

<!-- PARA QUIÉN -->
<section class="py-6 section-alt">
    <div class="container">
        <div class="text-center mb-5">
            <h2 class="section-title">Pensado para entornos sin SOC propio</h2>
            <div class="title-line"></div>
            <p class="section-subtitle">
                Si tienes dispositivos expuestos y nadie mirando los logs a las 3 de la mañana,
                este es tu sitio.
            </p>
        </div>
        <div class="row g-4">
            <div class="col-md-4">
                <div class="card-cyber h-100">
                    <div class="icon-wrap"><i class="bi bi-shop"></i></div>
                    <h5 class="fw-bold mb-2">Pymes y comercios</h5>
                    <p class="text-muted small mb-0">
                        Protección de nivel empresarial sin contratar un equipo de seguridad
                        ni desplegar appliances caros. Se instala y trabaja solo.
                    </p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-success-rgb),0.1);color:var(--color-success)"><i class="bi bi-hdd-network"></i></div>
                    <h5 class="fw-bold mb-2">IoT y entornos OT</h5>
                    <p class="text-muted small mb-0">
                        Sensores ligeros junto a la maquinaria o las cámaras, donde un agente
                        pesado no cabe. Vigilancia distribuida sin tocar la red central.
                    </p>
                </div>
            </div>
            <div class="col-md-4">
                <div class="card-cyber h-100">
                    <div class="icon-wrap" style="background:rgba(var(--color-warning-rgb),0.15);color:#9A7400"><i class="bi bi-buildings"></i></div>
                    <h5 class="fw-bold mb-2">Sedes y delegaciones</h5>
                    <p class="text-muted small mb-0">
                        Despliega un sensor por ubicación y gobiérnalos todos desde un único
                        panel. Escalar es añadir hardware, no reescribir la arquitectura.
                    </p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CTA FINAL -->
<section class="py-6">
    <div class="container">
        <div class="surface-cyber text-center shadow-cyber px-4 py-5 px-md-5">
            <span class="badge-cyber badge-success mb-3 d-inline-block">
                <i class="bi bi-broadcast me-1"></i>Listo para desplegar
            </span>
            <h2 class="section-title mb-3">Pon un SOC autónomo a vigilar tu infraestructura</h2>
            <p class="text-muted mb-4 mx-auto" style="max-width:620px">
                Cuéntanos qué quieres proteger y te montamos una demo con un sensor real:
                verás la detección, el triaje con IA y la mitigación en directo desde el panel.
            </p>
            <div class="d-flex flex-wrap gap-3 justify-content-center">
                <a href="contacto.php" class="btn-primary-cyber"><i class="bi bi-chat-dots me-2"></i>Hablar con el equipo</a>
                <a href="tecnologias.php" class="btn-outline-cyber"><i class="bi bi-cpu me-2"></i>Ver la arquitectura</a>
            </div>
        </div>
    </div>
</section>

<?php require 'includes/footer.php'; ?>
