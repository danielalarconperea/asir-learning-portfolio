/**
 * 10_Radio_Checkbox.js
 * 
 * OBJETIVO:
 * Dominar el trabajo con radio buttons y checkboxes en formularios.
 * Son fundamentales para configuradores, encuestas y formularios complejos.
 * 
 * CONCEPTOS CUBIERTOS:
 * 1. Acceder a grupos de radios con elements['name']
 * 2. Propiedad .checked - ¿Está marcado?
 * 3. Propiedad .disabled - Deshabilitar opciones
 * 4. Iterar sobre checkboxes para sumar valores
 * 5. Ejemplo completo: Configurador con precios
 */

console.log("-----------------------------------------");
console.log(" RADIO BUTTONS Y CHECKBOXES ");
console.log("-----------------------------------------");

// -----------------------------------------------------------------------------
// DIFERENCIA CLAVE
// -----------------------------------------------------------------------------
console.log("\n--- Radio vs Checkbox ---");
console.log("RADIO: Solo UNA opción puede estar seleccionada (mismo 'name')");
console.log("CHECKBOX: Múltiples opciones pueden estar marcadas\n");

// -----------------------------------------------------------------------------
// 1. SIMULACIÓN DE RADIO BUTTONS
// -----------------------------------------------------------------------------
// HTML de ejemplo:
// <input type="radio" name="motor" value="0"> Gasolina
// <input type="radio" name="motor" value="1500" checked> Diesel
// <input type="radio" name="motor" value="3000"> Híbrido

const radiosMotor = [
    { name: "motor", value: "0", checked: false, text: "Gasolina" },
    { name: "motor", value: "1500", checked: true, text: "Diésel (+1500€)" },
    { name: "motor", value: "3000", checked: false, text: "Híbrido (+3000€)" }
];

console.log("--- Radio Buttons (Tipo de Motor) ---");
radiosMotor.forEach((radio, i) => {
    let estado = radio.checked ? "🔘" : "⚪";
    console.log(`  ${estado} ${radio.text}`);
});

// Obtener el valor del radio seleccionado:
function obtenerRadioSeleccionado(radios) {
    for (let i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            return radios[i];
        }
    }
    return null;
}

let motorSeleccionado = obtenerRadioSeleccionado(radiosMotor);
console.log(`\nMotor seleccionado: ${motorSeleccionado.text}`);
console.log(`Valor (precio extra): ${motorSeleccionado.value}€`);

// -----------------------------------------------------------------------------
// 2. SIMULACIÓN DE CHECKBOXES
// -----------------------------------------------------------------------------
// HTML de ejemplo:
// <input type="checkbox" name="extra" value="750"> Metalizada
// <input type="checkbox" name="extra" value="200" checked> Llantas
// <input type="checkbox" name="extra" value="800" checked> Climatizador

const checkboxesExtras = [
    { name: "extra", value: "750", checked: false, text: "Metalizada (+750€)" },
    { name: "extra", value: "200", checked: true, text: "Llantas (+200€)" },
    { name: "extra", value: "800", checked: true, text: "Climatizador (+800€)" },
    { name: "extra", value: "340", checked: false, text: "GPS (+340€)" }
];

console.log("\n--- Checkboxes (Extras) ---");
checkboxesExtras.forEach(cb => {
    let estado = cb.checked ? "☑️" : "⬜";
    console.log(`  ${estado} ${cb.text}`);
});

// Sumar los valores de los checkboxes marcados:
function sumarCheckboxes(checkboxes) {
    let total = 0;
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked) {
            total += parseInt(checkboxes[i].value);
        }
    }
    return total;
}

let totalExtras = sumarCheckboxes(checkboxesExtras);
console.log(`\nTotal extras seleccionados: ${totalExtras}€`);

// -----------------------------------------------------------------------------
// 3. PROPIEDAD .disabled
// -----------------------------------------------------------------------------
console.log("\n--- Deshabilitar Opciones (.disabled) ---");

// A veces necesitamos deshabilitar opciones según otras selecciones.
// Ejemplo: "DVD solo disponible en modelo Familiar"

let opcionDVD = { text: "DVD", value: "800", disabled: false };

// Si el modelo NO es familiar, deshabilitamos:
let modeloFamiliar = false;

if (!modeloFamiliar) {
    opcionDVD.disabled = true;
    console.log("❌ DVD deshabilitado (solo disponible en Familiar)");
} else {
    console.log("✅ DVD disponible");
}

// En código real:
// document.getElementById("dvd").disabled = true;

// -----------------------------------------------------------------------------
// 4. EJEMPLO COMPLETO: CONFIGURADOR DE PC
// -----------------------------------------------------------------------------
console.log("\n--- Ejemplo: Configurador de PC ---");

const PRECIO_BASE = 500;

const configuracion = {
    procesador: [
        { value: 0, checked: true, text: "i3 (base)" },
        { value: 100, checked: false, text: "i5 (+100€)" },
        { value: 250, checked: false, text: "i7 (+250€)" }
    ],
    extras: [
        { value: 50, checked: true, text: "SSD 256GB (+50€)" },
        { value: 80, checked: false, text: "RAM 16GB (+80€)" },
        { value: 30, checked: true, text: "Teclado mecánico (+30€)" }
    ]
};

function calcularPrecioTotal(config) {
    let total = PRECIO_BASE;

    // Sumar procesador seleccionado
    let proc = obtenerRadioSeleccionado(config.procesador);
    total += parseInt(proc.value);

    // Sumar extras marcados
    total += sumarCheckboxes(config.extras);

    return total;
}

console.log("Configuración actual:");
console.log("  Procesador: " + obtenerRadioSeleccionado(configuracion.procesador).text);
console.log("  Extras: ");
configuracion.extras.filter(e => e.checked).forEach(e => console.log("    - " + e.text));
console.log(`\n💰 PRECIO TOTAL: ${calcularPrecioTotal(configuracion)}€`);

// -----------------------------------------------------------------------------
// 5. CÓDIGO REAL PARA COPIAR
// -----------------------------------------------------------------------------
console.log("\n--- Código Real (para usar en HTML) ---");
console.log(`
function calcularTotal() {
    var PRECIO_BASE = 500;
    var total = PRECIO_BASE;
    
    // Obtener valor del radio seleccionado
    var form = document.getElementById("miFormulario");
    total += parseInt(form.elements["procesador"].value);
    
    // Sumar checkboxes marcados
    var extras = form.elements["extra"];
    for (var i = 0; i < extras.length; i++) {
        if (extras[i].checked) {
            total += parseInt(extras[i].value);
        }
    }
    
    // Mostrar resultado
    document.getElementById("precioTotal").textContent = total + "€";
}
`);

console.log("\n[!] Recuerda: Los radios con el mismo 'name' forman un grupo exclusivo.");
