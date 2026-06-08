# Guía de Colores - Roca & Senda

Esta es la configuración de colores recomendada para el tema WordPress (Astra) basada en el código fuente del proyecto.

## 🎨 Colores de Identidad
| Elemento | Código Hex | Color | Uso principal |
| :--- | :--- | :--- | :--- |
| **Primario** | `#F97316` | Naranja | Botones, Enlaces, Icono Logo |
| **Secundario** | `#374151` | Gris Carbón | Títulos, Menú, Texto destacado |
| **Texto Cuerpo** | `#4B5563` | Gris Medio | Párrafos y descripciones |

---

## 🛠️ Configuración en el Personalizador (WordPress)

### Sección: Colores del Tema
*   **Énfasis:** `#F97316`
*   **Enlaces:** `#F97316`
*   **Encabezados (H1-H6):** `#374151`
*   **Texto del cuerpo:** `#4B5563`

### Sección: Paleta Global
Si configuras los círculos de la paleta de izquierda a derecha:
1.  **Color 1 (Marca):** `#F97316`
2.  **Color 2 (Marca Alt):** `#EA580C`
3.  **Color 3 (Encabezado):** `#374151`
4.  **Color 4 (Texto):** `#4B5563`
5.  **Color 5 (Fondo):** `#FFFFFF`
6.  **Color 6 (Fondo Sutil):** `#F9FAFB`
7.  **Color 7 (Bordes):** `#E5E7EB`
8.  **Color 8 (Extra):** `#F3F4F6`

---

## 🔘 Botones
*   **Botón Principal:**
    *   Fondo: `#F97316`
    *   Texto: `#FFFFFF` 
    *   Hover: `#EA580C`
*   **Botón Secundario:**
    *   Fondo: `#374151`
    *   Texto: `#FFFFFF`
    *   Hover: `#1F2937`

---

## 🔡 Tipografía
Basado en el archivo `index.html`, estas son las fuentes configuradas:

1.  **Encabezados (Títulos H1-H6):** `Montserrat`
    *   **Estilo sugerido:** Bold o ExtraBold (700 u 800).
    *   **Uso:** Títulos principales para dar un aspecto robusto y de montaña.

2.  **Texto del Cuerpo (Párrafos y Menú):** `Inter`
    *   **Estilo sugerido:** Regular (400) o Medium (500).
    *   **Uso:** Lectura general, es una fuente muy limpia y moderna.

### Cómo configurarlo en Astra:
*   Ve a **Global** > **Tipografía**.
*   En **Fuente del cuerpo**, selecciona `Inter`.
*   En **Fuentes de los encabezados**, selecciona `Montserrat`.

---

## 📋 Configuración del Menú
Basado en el componente `Navbar.tsx`, el menú debe tener la siguiente estructura y estilo:

### Estructura de Páginas
1.  **Inicio**
2.  **Nosotros**
3.  **Servicios**
4.  **Blog**
5.  **Contacto**
6.  **Botón RESERVAR** (Apunta a la página de Servicios)

### Estilo del Menú (Astra)
*   **Diseño:** Menú principal a la derecha del logo.
*   **Tipografía del menú:** `Inter`, Peso: `600 (Semibold)`, Transformación: `Mayúsculas (UPPERCASE)`.
*   **Colores del menú:**
    *   Color normal: `#4B5563` (Gris).
    *   Color al pasar el ratón (Hover): `#F97316` (Naranja).
    *   Color del elemento activo: `#F97316` (Naranja).

### Botón de Llamada a la Acción (RESERVAR)
Para replicar el diseño exacto del código, el botón del menú debe configurarse en **Astra > Maquetador de cabeceras**:
*   **Fondo:** `#F97316` (Naranja).
*   **Color texto:** `#FFFFFF` (Blanco).
*   **Borde:** Redondeado al máximo (40px o más para efecto píldora).
*   **Hover:** Fondo `#1F2937` (Gris oscuro/negro).

---

## 📄 Diseño de Páginas
A continuación se detalla el contenido y la estructura de las páginas principales según el código fuente:

### 1. Página de Inicio (Home)
*   **Sección Hero:**
    *   Fondo: Imagen de montaña con superposición (overlay) gris oscuro al 40%.
    *   Título: "Tu próxima aventura comienza en la **cima**." (Cima en naranja `#F97316`).
    *   Botón Principal: "Ver Rutas" (Naranja).
    *   Botón Secundario: "Contactar Ahora" (Transparente con borde blanco).
*   **Sección de Pilares (Seguridad, Niveles, Ecoturismo):**
    *   Iconos en cajas con bordes muy redondeados (`3xl`).
    *   Efecto hover: Fondo cambia a naranja muy suave (`orange-50`).

### 2. Página de Servicios (Catálogo)
*   **Cabecera:** Fondo `#1F2937` (Gris oscuro) con el título "Catálogo de Aventuras" en blanco.
*   **Filtros:** Botones tipo "píldora" para filtrar entre 'Todos', 'Trekking' y 'Escalada'.
*   **Tarjetas de Ruta (Cards):**
    *   Bordes muy redondeados y sombra suave.
    *   Imagen con efecto zoom al pasar el ratón.
    *   Etiquetas de categoría (naranja) y dificultad (blanco translúcido) sobre la imagen.
    *   Información inferior: Iconos de reloj (duración) y euro (precio).

### 3. Página de Contacto
*   **Estructura:** Dos columnas.
    *   **Izquierda:** Información de contacto (Email, Teléfono) con iconos naranja.
    *   **Derecha:** Formulario de contacto con campos limpios y botón enviar en naranja.

### 4. Página de Nosotros
*   Presentación de los guías (Dani & Nacho) con enfoque en seguridad y experiencia profesional.
*   Uso de bloques de texto grandes y limpios con tipografía `Inter`.
