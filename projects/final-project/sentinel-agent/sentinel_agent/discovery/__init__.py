"""
Subpaquete de descubrimiento: probes independientes y degradables.

Cada probe expone:
  * funciones `parse_*` PURAS (sin I/O) — testables con fixtures de salida real.
  * una función `collect()` que ejecuta los comandos del sistema y delega en
    las `parse_*`, devolviendo (seccion: dict, degraded: list[str]).

Un fallo en un probe degrada SU sección (a unknown/[]) y añade un motivo a
`degraded`, sin tumbar el snapshot completo.
"""
