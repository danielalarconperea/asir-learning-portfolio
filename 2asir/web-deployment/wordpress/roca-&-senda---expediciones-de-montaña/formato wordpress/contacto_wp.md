# Guía de Bloques WordPress: Contacto

Pasos para crear la página de contacto usando bloques estándar.

### 1. CABECERA
*   Bloque **Grupo** (Fondo Oscuro `#1F2937`, Texto Blanco).
*   **Encabezado (H1)**: "Hablemos de tu reto".
*   **Párrafo**: "Nuestro equipo de guías está listo para asesorarte personalmente."

---

### 2. CONTENIDO PRINCIPAL (2 Columnas)
*   Agrega un bloque **Columnas (50/50)**.
*   **COLUMNA IZQUIERDA (Info)**:
    *   **Encabezado (H2)**: "Información de Contacto"
    *   **Párrafo**: "Estamos ubicados en las faldas de la Sierra de Madrid..."
    *   **Grupo (Ubicación)**: Emoji 📍 + Texto: "Puerto de Navacerrada, Madrid".
    *   **Grupo (Teléfono)**: Emoji 📞 + Texto: "+34 600 000 000".
    *   **Grupo (Email)**: Emoji ✉️ + Texto: "info@rocaysenda.com".
    *   **Imagen (Mapa)**: `https://images.unsplash.com/photo-1544198365-f5d60b6d8190?w=800` (Recórtala como un rectángulo y redondea los bordes).

*   **COLUMNA DERECHA (Formulario)**:
    *   Crea un bloque **Grupo** con fondo blanco y una sombra suave (Sombra exterior).
    *   **Encabezado (H3)**: "Envíanos un mensaje".
    *   **Opción A (Sencilla)**: Si tienes un plugin de formularios (como WPForms o Contact Form 7), inserta su bloque aquí.
    *   **Opción B (Bloques nativos)**: WordPress tiene un bloque llamado **Formulario** (si el tema lo soporta). Añadir campos:
        *   Nombre (Campo de texto).
        *   Email (Campo de correo).
        *   Actividad (Desplegable).
        *   Mensaje (Área de texto).
        *   Botón de envío (Fondo Naranja).
