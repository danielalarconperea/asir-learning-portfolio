/**
 * 03_Funciones_Modulos.js
 * 
 * OBJETIVO:
 * Entender cómo organizar el código en bloques reutilizables (funciones)
 * y cómo funciona el alcance (scope) de las variables.
 * 
 * CONCEPTOS CUBIERTOS:
 * 1. Declaración de funciones
 * 2. Funciones Flecha (Arrow Functions)
 * 3. Parámetros y Retorno
 * 4. Scope (Alcance Global vs Local)
 */

console.log("-----------------------------------------");
console.log(" FUNCIONES Y MODULARIDAD ");
console.log("-----------------------------------------");

// -----------------------------------------------------------------------------
// 1. DECLARACIÓN DE FUNCIONES (TRADICIONAL)
// -----------------------------------------------------------------------------
// Una función es un bloque de código que realiza una tarea específica.

function saludar(nombre) {
    // 'nombre' es un parámetro (variable local de la función)
    console.log(`Hola, ${nombre}! Bienvenido al curso.`);
}

console.log("\n--- Función Simple ---");
saludar("Estudiante"); // Llamada a la función
saludar("Profesor");

// -----------------------------------------------------------------------------
// 2. RETORNO DE VALORES
// -----------------------------------------------------------------------------
// Las funciones pueden devolver un resultado para usarlo después.

function sumar(a, b) {
    return a + b; // Devuelve la suma
    // El código después de 'return' NUNCA se ejecuta
    console.log("Esto nunca se verá");
}

console.log("\n--- Función con Return ---");
let resultado = sumar(10, 5);
console.log(`La suma de 10 + 5 es: ${resultado}`);

// Podemos usar el resultado directamente:
console.log(`El doble de la suma es: ${sumar(10, 5) * 2}`);

// -----------------------------------------------------------------------------
// 3. FUNCIONES FLECHA (MODERNO - ES6)
// -----------------------------------------------------------------------------
// Sintaxis más corta, muy común en React, Vue, etc.

const multiplicar = (a, b) => {
    return a * b;
};

// Si es una sola línea, podemos omitir llaves y return:
const dividir = (a, b) => a / b;

console.log("\n--- Funciones Flecha ---");
console.log("Multiplicar 5 * 5:", multiplicar(5, 5));
console.log("Dividir 10 / 2:", dividir(10, 2));

// -----------------------------------------------------------------------------
// 4. SCOPE (ALCANCE)
// -----------------------------------------------------------------------------
// Dónde "viven" tus variables.

let variableGlobal = "Soy visible en todo el archivo";

function pruebaScope() {
    let variableLocal = "Solo soy visible DENTRO de esta función";

    console.log("\n--- Dentro de la función ---");
    console.log(variableGlobal); // Funciona
    console.log(variableLocal);  // Funciona
}

pruebaScope();

console.log("\n--- Fuera de la función ---");
console.log(variableGlobal); // Funciona
// console.log(variableLocal); // ERROR: variableLocal is not defined

// -----------------------------------------------------------------------------
// 5. CALLBACKS (Introducción)
// -----------------------------------------------------------------------------
// Pasar funciones como argumentos a otras funciones.

function procesarUsuario(nombre, callback) {
    console.log(`Procesando a ${nombre}...`);
    // Ejecutamos la función que nos pasaron
    callback();
}

console.log("\n--- Callbacks ---");
procesarUsuario("Ana", () => {
    console.log("¡Callback ejecutado! El usuario ha sido procesado.");
});
