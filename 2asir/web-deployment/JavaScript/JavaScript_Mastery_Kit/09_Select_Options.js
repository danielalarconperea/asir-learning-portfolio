/**
 * 09_Select_Options.js
 * 
 * OBJETIVO:
 * Aprender a trabajar con elementos <select> (desplegables) en formularios.
 * 
 * CONCEPTOS CUBIERTOS:
 * 1. selectedIndex - Índice de la opción seleccionada
 * 2. options[] - Array de opciones disponibles
 * 3. .text y .value - Texto visible y valor interno
 * 4. Evento onchange - Detectar cambios de selección
 */

console.log("-----------------------------------------");
console.log(" SELECT Y OPTIONS ");
console.log("-----------------------------------------");

// -----------------------------------------------------------------------------
// ESTRUCTURA HTML DE UN SELECT
// -----------------------------------------------------------------------------
console.log("\n--- Estructura de un <select> ---");
console.log(`
HTML de ejemplo:
<select name="producto" id="miSelect" onchange="cambiarProducto()">
    <option value="1000">Móvil</option>
    <option value="1200">PC</option>
    <option value="100">Pantalla</option>
    <option value="50">Teclado</option>
</select>
`);

// -----------------------------------------------------------------------------
// 1. SIMULACIÓN DE UN SELECT
// -----------------------------------------------------------------------------
// Creamos un objeto que simula el comportamiento de un <select>

const selectSimulado = {
    name: "producto",
    selectedIndex: 1,  // PC está seleccionado (índice 1)
    options: [
        { text: "Móvil", value: "1000" },
        { text: "PC", value: "1200" },
        { text: "Pantalla", value: "100" },
        { text: "Teclado", value: "50" }
    ]
};

// -----------------------------------------------------------------------------
// 2. OBTENER EL ÍNDICE SELECCIONADO
// -----------------------------------------------------------------------------
console.log("\n--- selectedIndex ---");

let indice = selectSimulado.selectedIndex;
console.log("Índice seleccionado: " + indice);

// En código real sería:
// let indice = document.getElementById("miSelect").selectedIndex;

// -----------------------------------------------------------------------------
// 3. ACCEDER A LA OPCIÓN SELECCIONADA
// -----------------------------------------------------------------------------
console.log("\n--- Acceder a options[indice] ---");

let opcionActual = selectSimulado.options[indice];
console.log("Texto visible (.text): " + opcionActual.text);
console.log("Valor interno (.value): " + opcionActual.value);

// El .text es lo que ve el usuario
// El .value es lo que usamos en JS (puede ser un ID, precio, código, etc.)

// -----------------------------------------------------------------------------
// 4. RECORRER TODAS LAS OPCIONES
// -----------------------------------------------------------------------------
console.log("\n--- Listar Todas las Opciones ---");

console.log("Opciones disponibles:");
for (let i = 0; i < selectSimulado.options.length; i++) {
    let opt = selectSimulado.options[i];
    let marcador = (i === selectSimulado.selectedIndex) ? " ✅" : "";
    console.log(`  [${i}] ${opt.text} (valor: ${opt.value})${marcador}`);
}

// -----------------------------------------------------------------------------
// 5. EJEMPLO PRÁCTICO: CALCULADORA DE PRECIOS
// -----------------------------------------------------------------------------
console.log("\n--- Ejemplo: Selector de Productos ---");

function obtenerPrecioProducto(select) {
    let idx = select.selectedIndex;
    let precio = parseFloat(select.options[idx].value);
    let nombre = select.options[idx].text;
    return { nombre, precio };
}

let resultado = obtenerPrecioProducto(selectSimulado);
console.log(`Producto: ${resultado.nombre}`);
console.log(`Precio: ${resultado.precio}€`);

// -----------------------------------------------------------------------------
// 6. CÓDIGO REAL PARA COPIAR
// -----------------------------------------------------------------------------
console.log("\n--- Código Real (para usar en HTML) ---");
console.log(`
function cambiarProducto() {
    // Obtener el select
    var select = document.getElementById("miSelect");
    
    // Obtener índice seleccionado
    var indice = select.selectedIndex;
    
    // Obtener texto y valor
    var texto = select.options[indice].text;
    var valor = select.options[indice].value;
    
    // Mostrar en otros campos
    document.getElementById("textoProducto").value = texto;
    document.getElementById("precioProducto").value = valor + "€";
}
`);

console.log("\n[!] El evento 'onchange' se dispara cada vez que el usuario cambia la selección.");
