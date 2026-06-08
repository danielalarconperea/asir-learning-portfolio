/**
 * 06_DOM_Basico.js
 * 
 * OBJETIVO:
 * Aprender a manipular elementos HTML desde JavaScript.
 * El DOM (Document Object Model) es la representación en memoria de la página.
 * 
 * CONCEPTOS CUBIERTOS:
 * 1. document.getElementById() - Seleccionar un elemento por su ID
 * 2. innerHTML vs textContent - Modificar contenido
 * 3. Modificar estilos (.style)
 * 4. getElementsByName() - Seleccionar varios elementos
 */

console.log("-----------------------------------------");
console.log(" DOM: MANIPULANDO LA PÁGINA WEB ");
console.log("-----------------------------------------");

// -----------------------------------------------------------------------------
// 1. SELECCIONAR ELEMENTOS (getElementById)
// -----------------------------------------------------------------------------
// Es la forma más común de "agarrar" un elemento HTML por su ID único.

console.log("\n--- Seleccionar Elementos ---");

// Simulamos que tenemos este HTML: <div id="miDiv">Hola</div>
// En JS, lo seleccionaríamos así:
// const miDiv = document.getElementById("miDiv");

// Ejemplo práctico (simulado para consola):
const elementoSimulado = { id: "miDiv", innerHTML: "Hola Mundo" };
console.log("Elemento seleccionado: " + elementoSimulado.id);
console.log("Contenido actual: " + elementoSimulado.innerHTML);

// -----------------------------------------------------------------------------
// 2. MODIFICAR CONTENIDO (innerHTML vs textContent)
// -----------------------------------------------------------------------------
console.log("\n--- Modificar Contenido ---");

// innerHTML: Interpreta etiquetas HTML
// textContent: Trata todo como texto plano (más seguro)

let contenidoOriginal = "Texto simple";
let contenidoConHTML = "<strong>Texto en negrita</strong>";

console.log("textContent mostraría: " + contenidoConHTML + " (literal)");
console.log("innerHTML interpretaría las etiquetas y mostraría: Texto en negrita");

// Ejemplo de uso real:
// document.getElementById("resultado").innerHTML = "<span style='color:red'>Error!</span>";
// document.getElementById("resultado").textContent = "Texto seguro sin HTML";

// -----------------------------------------------------------------------------
// 3. MODIFICAR ESTILOS (.style)
// -----------------------------------------------------------------------------
console.log("\n--- Modificar Estilos con .style ---");

// Cada propiedad CSS se convierte a camelCase en JS:
// CSS: background-color  →  JS: backgroundColor
// CSS: font-family       →  JS: fontFamily
// CSS: border-radius     →  JS: borderRadius

const estilosEjemplo = {
    backgroundColor: "blue",
    fontFamily: "Arial",
    color: "white",
    padding: "10px"
};

console.log("Estilos que aplicaríamos:");
for (let propiedad in estilosEjemplo) {
    console.log(`  .style.${propiedad} = "${estilosEjemplo[propiedad]}"`);
}

// Uso real:
// document.getElementById("miDiv").style.backgroundColor = "blue";
// document.getElementById("miDiv").style.fontFamily = "Arial";

// -----------------------------------------------------------------------------
// 4. SELECCIONAR VARIOS ELEMENTOS (getElementsByName)
// -----------------------------------------------------------------------------
console.log("\n--- Seleccionar Múltiples Elementos ---");

// getElementsByName devuelve una LISTA (HTMLCollection)
// Útil para grupos de radio buttons o checkboxes con el mismo "name"

// Simulación:
const radiosSimulados = [
    { name: "color", value: "rojo", checked: false },
    { name: "color", value: "verde", checked: true },
    { name: "color", value: "azul", checked: false }
];

console.log("Iterando sobre elementos con name='color':");
radiosSimulados.forEach((radio, i) => {
    const estado = radio.checked ? "✅ SELECCIONADO" : "⬜";
    console.log(`  [${i}] Valor: ${radio.value} ${estado}`);
});

// Uso real:
// const radios = document.getElementsByName("color");
// for (let i = 0; i < radios.length; i++) {
//     if (radios[i].checked) {
//         console.log("Seleccionado: " + radios[i].value);
//     }
// }

console.log("\n[!] Recuerda: getElementById devuelve UN elemento, getElementsByName devuelve VARIOS.");
