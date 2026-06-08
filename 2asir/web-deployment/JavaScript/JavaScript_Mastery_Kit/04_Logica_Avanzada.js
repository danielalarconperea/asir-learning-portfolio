/**
 * 04_Logica_Avanzada.js
 * 
 * OBJETIVO:
 * Manejar colecciones de datos (Arrays), estructurar información compleja (Objetos)
 * y manejar errores para que tu programa no se rompa.
 * 
 * CONCEPTOS CUBIERTOS:
 * 1. Arrays y métodos esenciales (.push, .map, .filter)
 * 2. Objetos (Propiedades y Métodos)
 * 3. Manejo de Errores (try / catch)
 * 4. JSON (Breve introducción)
 */

console.log("-----------------------------------------");
console.log(" LÓGICA AVANZADA: DATOS COMPLEJOS ");
console.log("-----------------------------------------");

// -----------------------------------------------------------------------------
// 1. ARRAYS (LISTAS)
// -----------------------------------------------------------------------------
// Colecciones ordenadas de datos.

let estudiantes = ["Ana", "Carlos", "Beatriz"];
console.log(`\n--- Array Inicial: ${estudiantes} ---`);

// Añadir al final
estudiantes.push("David");
console.log("Después de push('David'):", estudiantes);

// ITERAR (Recorrer)
console.log("\n--- Iterando con forEach ---");
estudiantes.forEach((nombre, indice) => {
    console.log(`${indice + 1}. ${nombre}`);
});

// TRANSFORMACIÓN (.MAP)
// Crea un NUEVO array transformando cada elemento.
console.log("\n--- Método .map() (Transformar) ---");
const correos = estudiantes.map(nombre => `${nombre.toLowerCase()}@escuela.com`);
console.log(correos);

// FILTRADO (.FILTER)
// Crea un NUEVO array con elementos que cumplan una condición.
console.log("\n--- Método .filter() (Filtrar) ---");
const nombresLargos = estudiantes.filter(nombre => nombre.length > 4);
console.log("Nombres con más de 4 letras:", nombresLargos);

// -----------------------------------------------------------------------------
// 2. OBJETOS
// -----------------------------------------------------------------------------
// Estructuras clave-valor para representar entidades reales.

const alumno = {
    // Propiedades
    nombre: "Ana",
    edad: 21,
    activo: true,
    notas: [8, 9, 7],

    // Métodos (Funciones dentro del objeto)
    saludar: function () {
        return `Hola, soy ${this.nombre} y tengo ${this.edad} años.`;
    },

    // Método para calcular promedio
    calcularPromedio: function () {
        let suma = 0;
        this.notas.forEach(nota => suma += nota);
        return suma / this.notas.length;
    }
};

console.log("\n--- Objetos ---");
console.log(alumno.saludar());
console.log(`Promedio de notas: ${alumno.calcularPromedio()}`);
console.log(`¿Está activo?: ${alumno.activo ? "SÍ" : "NO"}`);

// -----------------------------------------------------------------------------
// 3. MANEJO DE ERRORES (TRY / CATCH)
// -----------------------------------------------------------------------------
// Evita que el programa se detenga abruptamente si algo sale mal.

console.log("\n--- Manejo de Errores ---");

try {
    // Intentamos hacer algo peligroso
    let resultado = funcionQueNoExiste(); // Esto fallará
    console.log(resultado);
} catch (error) {
    // Si falla, entramos aquí
    console.error("¡ERROR CAPTURADO! 🛡️");
    console.error("Mensaje del error:", error.message);
} finally {
    // Esto se ejecuta SIEMPRE, haya error o no
    console.log("Bloque 'finally' ejecutado. Limpiando recursos...");
}

console.log("El programa continúa ejecutándose correctamente ✅");
