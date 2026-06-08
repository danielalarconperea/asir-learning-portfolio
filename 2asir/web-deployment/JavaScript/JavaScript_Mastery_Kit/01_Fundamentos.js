/**
 * 01_Fundamentos.js
 * 
 * OBJETIVO:
 * Entender los bloques de construcción básicos de JavaScript: variables, tipos de datos
 * y cómo mostrar información por consola.
 * 
 * CONCEPTOS CUBIERTOS:
 * 1. Declaración de variables (let vs const vs var)
 * 2. Tipos de datos primitivos (String, Number, Boolean, Null, Undefined)
 * 3. Operadores básicos
 * 4. Template Literals (Interpolación de cadenas)
 */

console.log("-----------------------------------------");
console.log(" BIENVENIDO A LOS FUNDAMENTOS DE JS ");
console.log("-----------------------------------------");

// -----------------------------------------------------------------------------
// 1. DECLARACIÓN DE VARIABLES
// -----------------------------------------------------------------------------
// En JS moderno, evitamos 'var'. Usamos 'let' para valores que cambian
// y 'const' para valores que no deberían cambiar.

const nombreCurso = "1ASIR / 2ASIR JavaScript"; // No cambiará
let estudianteActual = "Estudiante Iniciado";      // Puede cambiar
let nivelProgreso = 0;                           // Puede cambiar

console.log("Curso:", nombreCurso);
console.log("Estudiante:", estudianteActual);

// Intentar cambiar una constante daría error:
// nombreCurso = "Otro Curso"; // ERROR!

// Cambiar una variable let es válido:
estudianteActual = "Estudiante Avanzando";
nivelProgreso = 10;
console.log("Nuevo estado:", estudianteActual, "- Nivel:", nivelProgreso);

// -----------------------------------------------------------------------------
// 2. TIPOS DE DATOS
// -----------------------------------------------------------------------------
// JS es de tipado dinámico, no necesitas declarar el tipo (int, string, etc.)

let texto = "Hola Mundo";       // String
let numeroEntero = 42;          // Number
let numeroDecimal = 3.14;       // Number (en JS todos son 'number')
let esDivertido = true;         // Boolean
let valorDesconocido;           // Undefined (declarada pero no asignada)
let valorVacio = null;          // Null (intencionalmente vacío)

console.log("\n--- Tipos de Datos ---");
console.log("Tipo de 'texto':", typeof texto);
console.log("Tipo de 'numeroEntero':", typeof numeroEntero);
console.log("Tipo de 'esDivertido':", typeof esDivertido);
console.log("Tipo de 'valorDesconocido':", typeof valorDesconocido);

// -----------------------------------------------------------------------------
// 3. OPERADORES BÁSICOS
// -----------------------------------------------------------------------------
console.log("\n--- Operaciones Matemáticas ---");
let suma = 10 + 5;
let resta = 10 - 5;
let multiplicacion = 10 * 5;
let division = 10 / 2;
let modulo = 10 % 3; // Resto de la división (10 / 3 = 3 y sobra 1)

console.log("10 + 5 =", suma);
console.log("10 % 3 =", modulo, "(Resto)");

// Operadores de asignación compuesta
let puntos = 100;
puntos += 50; // Equivalente a: puntos = puntos + 50
console.log("Puntos acumulados:", puntos);

// -----------------------------------------------------------------------------
// 4. TEMPLATE LITERALS (Interpolación)
// -----------------------------------------------------------------------------
// Usamos comillas invertidas (backticks ` `) para insertar variables dentro de texto
// sin tener que usar el operador '+' para concatenar.

console.log("\n--- Mensaje Final ---");
// Forma antigua (concatenación):
console.log("El usuario " + estudianteActual + " tiene " + puntos + " puntos.");

// Forma moderna (Template Literal):
const mensajeFinal = `El usuario ${estudianteActual} tiene ${puntos} puntos y promedia ${puntos / 10} por nivel.`;
console.log(mensajeFinal);

console.log("\n[!] Has completado el Nivel 01. ¡Pasa al siguiente script!");
