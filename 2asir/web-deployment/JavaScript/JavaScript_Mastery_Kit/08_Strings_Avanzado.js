/**
 * 08_Strings_Avanzado.js
 * 
 * OBJETIVO:
 * Dominar la manipulación de cadenas de texto (strings) en JavaScript.
 * Los strings son inmutables: los métodos devuelven NUEVOS strings.
 * 
 * CONCEPTOS CUBIERTOS:
 * 1. Propiedades: .length
 * 2. Búsqueda: .indexOf(), .includes()
 * 3. Acceso: .charAt(), corchetes []
 * 4. Transformación: .toUpperCase(), .toLowerCase()
 * 5. Extracción: .slice(), .substring()
 * 6. Reemplazo: .replace()
 * 7. División: .split()
 */

console.log("-----------------------------------------");
console.log(" STRINGS: MANIPULACIÓN DE TEXTO ");
console.log("-----------------------------------------");

// -----------------------------------------------------------------------------
// 1. PROPIEDAD .length
// -----------------------------------------------------------------------------
console.log("\n--- Longitud de un String ---");

let mensaje = "Hola Mundo";
console.log(`Texto: "${mensaje}"`);
console.log(`Longitud (.length): ${mensaje.length}`);  // 10

// Útil para validaciones:
let password = "abc";
if (password.length < 8) {
    console.log("⚠️ La contraseña debe tener al menos 8 caracteres");
}

// -----------------------------------------------------------------------------
// 2. BÚSQUEDA: .indexOf() e .includes()
// -----------------------------------------------------------------------------
console.log("\n--- Buscar en un String ---");

let frase = "El perro se llama TOR";

// indexOf: Devuelve la POSICIÓN donde empieza la palabra, o -1 si no existe
let posCasa = frase.indexOf("casa");
let posPerro = frase.indexOf("perro");

console.log(`Frase: "${frase}"`);
console.log(`indexOf('casa') = ${posCasa} (no encontrado)`);
console.log(`indexOf('perro') = ${posPerro} (empieza en posición 3)`);

// includes: Devuelve true/false (más moderno y legible)
console.log(`includes('TOR') = ${frase.includes("TOR")}`);  // true
console.log(`includes('gato') = ${frase.includes("gato")}`);  // false

// -----------------------------------------------------------------------------
// 3. ACCESO: .charAt() y corchetes []
// -----------------------------------------------------------------------------
console.log("\n--- Acceder a Caracteres ---");

let palabra = "JavaScript";
console.log(`Palabra: "${palabra}"`);

// charAt(posición) - método clásico
console.log(`charAt(0) = '${palabra.charAt(0)}'`);  // J
console.log(`charAt(4) = '${palabra.charAt(4)}'`);  // S

// Corchetes [] - sintaxis moderna
console.log(`[0] = '${palabra[0]}'`);  // J
console.log(`[palabra.length - 1] = '${palabra[palabra.length - 1]}'`);  // t (último)

// Recorrer todos los caracteres:
console.log("\nRecorriendo carácter a carácter:");
for (let i = 0; i < palabra.length; i++) {
    console.log(`  Posición ${i}: ${palabra.charAt(i)}`);
}

// -----------------------------------------------------------------------------
// 4. TRANSFORMACIÓN: .toUpperCase() y .toLowerCase()
// -----------------------------------------------------------------------------
console.log("\n--- Mayúsculas y Minúsculas ---");

let texto = "HoLa MuNdO";
console.log(`Original: "${texto}"`);
console.log(`toUpperCase(): "${texto.toUpperCase()}"`);  // HOLA MUNDO
console.log(`toLowerCase(): "${texto.toLowerCase()}"`);  // hola mundo

// Útil para comparaciones sin importar mayúsculas:
let entrada = "ADMIN";
if (entrada.toLowerCase() === "admin") {
    console.log("✅ Usuario reconocido (ignorando mayúsculas)");
}

// -----------------------------------------------------------------------------
// 5. EXTRACCIÓN: .slice() y .substring()
// -----------------------------------------------------------------------------
console.log("\n--- Extraer Subcadenas ---");

let cadena = "Hola, ¡mundo!";
console.log(`Cadena: "${cadena}"`);

// slice(inicio, fin) - Extrae desde 'inicio' hasta 'fin' (sin incluir)
console.log(`slice(0, 4) = "${cadena.slice(0, 4)}"`);    // "Hola"
console.log(`slice(6, 12) = "${cadena.slice(6, 12)}"`);  // "¡mundo"
console.log(`slice(-6) = "${cadena.slice(-6)}"`);        // "mundo!" (desde el final)

// substring es similar pero no acepta negativos

// -----------------------------------------------------------------------------
// 6. REEMPLAZO: .replace()
// -----------------------------------------------------------------------------
console.log("\n--- Reemplazar Texto ---");

let saludo = "Hola, mundo";
console.log(`Original: "${saludo}"`);

// replace(buscar, reemplazo) - Solo reemplaza la PRIMERA ocurrencia
let nuevoSaludo = saludo.replace("mundo", "universo");
console.log(`replace('mundo', 'universo') = "${nuevoSaludo}"`);

// Para reemplazar TODAS las ocurrencias: replaceAll() o regex
let repetido = "la-la-la";
console.log(`Original: "${repetido}"`);
console.log(`replaceAll('-', ' ') = "${repetido.replaceAll("-", " ")}"`);

// -----------------------------------------------------------------------------
// 7. DIVISIÓN: .split()
// -----------------------------------------------------------------------------
console.log("\n--- Dividir en Array ---");

let listaCSV = "manzana,pera,naranja,plátano";
console.log(`CSV: "${listaCSV}"`);

// split(separador) - Divide el string en un array
let frutas = listaCSV.split(",");
console.log("Resultado de split(','):");
frutas.forEach((fruta, i) => console.log(`  [${i}] ${fruta}`));

// Ejemplo: Contar palabras
let oracion = "JavaScript es un lenguaje de programación";
let palabras = oracion.split(" ");
console.log(`\nLa oración tiene ${palabras.length} palabras`);

console.log("\n[!] Recuerda: Los strings son INMUTABLES. Los métodos devuelven NUEVOS strings.");
