/**
 * 07_Formularios_Eventos.js
 * 
 * OBJETIVO:
 * Aprender a leer datos de formularios HTML y responder a eventos del usuario.
 * 
 * CONCEPTOS CUBIERTOS:
 * 1. Acceder a valores de inputs (.value)
 * 2. Conversión de tipos (parseInt, parseFloat)
 * 3. Eventos básicos (onclick, onchange)
 * 4. prompt() y alert() para entrada/salida rápida
 */

console.log("-----------------------------------------");
console.log(" FORMULARIOS Y EVENTOS ");
console.log("-----------------------------------------");

// -----------------------------------------------------------------------------
// 1. ACCEDER A VALORES DE INPUTS (.value)
// -----------------------------------------------------------------------------
console.log("\n--- Acceder a Valores de Formulario ---");

// Método 1: Por nombre del formulario y campo
// document.nombreFormulario.nombreCampo.value

// Método 2: Por getElementById (más moderno y recomendado)
// document.getElementById("miInput").value

// Simulación:
const formularioSimulado = {
    nombre: { value: "Juan" },
    edad: { value: "25" },
    telefono: { value: "612345678" }
};

console.log("Valores del formulario:");
console.log("  Nombre: " + formularioSimulado.nombre.value);
console.log("  Edad: " + formularioSimulado.edad.value);
console.log("  Teléfono: " + formularioSimulado.telefono.value);

// -----------------------------------------------------------------------------
// 2. CONVERSIÓN DE TIPOS (parseInt, parseFloat)
// -----------------------------------------------------------------------------
console.log("\n--- Conversión de Tipos ---");

// ¡IMPORTANTE! Los valores de los inputs SIEMPRE son STRINGS.
// Si necesitas hacer cálculos, debes convertirlos.

let edadTexto = "25";       // String
let edadNumero = parseInt(edadTexto);  // Number entero

let precioTexto = "19.99";
let precioNumero = parseFloat(precioTexto); // Number decimal

console.log("Tipo de '25': " + typeof edadTexto);
console.log("Tipo de parseInt('25'): " + typeof edadNumero);
console.log("Tipo de parseFloat('19.99'): " + typeof precioNumero);

// Ejemplo: Calcular área de triángulo
let base = parseFloat("10");
let altura = parseFloat("5");
let area = (base * altura) / 2;
console.log(`\nÁrea del triángulo (base=${base}, altura=${altura}): ${area}`);

// -----------------------------------------------------------------------------
// 3. EVENTOS BÁSICOS
// -----------------------------------------------------------------------------
console.log("\n--- Eventos Comunes ---");

// Los eventos se definen en el HTML o con addEventListener en JS.

const eventosComunes = {
    onclick: "Se dispara al hacer CLIC (botones)",
    onchange: "Se dispara al CAMBIAR un valor (selects, inputs)",
    onsubmit: "Se dispara al ENVIAR un formulario",
    onmouseover: "Se dispara al pasar el ratón por encima",
    onkeyup: "Se dispara al SOLTAR una tecla"
};

console.log("Eventos más usados:");
for (let evento in eventosComunes) {
    console.log(`  ${evento}: ${eventosComunes[evento]}`);
}

// Ejemplo en HTML:
// <button onclick="miFuncion()">Pulsa aquí</button>
// <select onchange="cambiarColor()">...</select>

// -----------------------------------------------------------------------------
// 4. prompt() y alert()
// -----------------------------------------------------------------------------
console.log("\n--- Entrada/Salida Rápida ---");

// prompt() muestra un cuadro de diálogo para que el usuario escriba algo.
// Devuelve el texto escrito o null si cancela.

// alert() muestra un mensaje emergente.

// Simulación (no ejecutamos prompt real en consola):
console.log("prompt('¿Cuál es tu nombre?') → Abre un cuadro de texto");
console.log("alert('¡Hola!') → Muestra un mensaje emergente");

// Ejemplo de uso:
// let nombre = prompt("¿Cómo te llamas?");
// if (nombre !== null) {
//     alert("Hola, " + nombre);
// }

// -----------------------------------------------------------------------------
// 5. EJEMPLO PRÁCTICO COMPLETO
// -----------------------------------------------------------------------------
console.log("\n--- Ejemplo: Calculadora Simple ---");

function calcularSuma(a, b) {
    let num1 = parseFloat(a);
    let num2 = parseFloat(b);

    if (isNaN(num1) || isNaN(num2)) {
        return "Error: Introduce números válidos";
    }

    return num1 + num2;
}

console.log("calcularSuma('10', '5') = " + calcularSuma("10", "5"));
console.log("calcularSuma('abc', '5') = " + calcularSuma("abc", "5"));

console.log("\n[!] Recuerda: SIEMPRE convierte con parseInt/parseFloat antes de calcular.");
