/**
 * 02_Estructuras_Control.js
 * 
 * OBJETIVO:
 * Aprender a controlar el flujo del programa. Tomar decisiones (if/else)
 * y repetir acciones (bucles).
 * 
 * CONCEPTOS CUBIERTOS:
 * 1. Condicionales (if, else if, else, switch)
 * 2. Operadores de comparación (==, ===, !=, !==, >, <)
 * 3. Bucles (for, while)
 * 4. Control de flujo (break, continue)
 */

console.log("-----------------------------------------");
console.log(" CONTROLANDO EL FLUJO DEL PROGRAMA ");
console.log("-----------------------------------------");

// -----------------------------------------------------------------------------
// 1. CONDICIONALES (IF / ELSE)
// -----------------------------------------------------------------------------
// Permiten ejecutar código solo si se cumple una condición.

let notaExamen = 7.5;
let asistencia = 80; // Porcentaje

console.log(`\n--- Evaluando Alumno (Nota: ${notaExamen}, Asistencia: ${asistencia}%) ---`);

if (notaExamen >= 5 && asistencia >= 80) {
    console.log("Resultado: APROBADO ✅");
} else if (notaExamen >= 5 && asistencia < 80) {
    console.log("Resultado: SUSPENDIDO por Asistencia ❌");
} else {
    // Si no se cumple ninguna de las anteriores
    console.log("Resultado: SUSPENDIDO por Nota ❌");
}

// -----------------------------------------------------------------------------
// 2. OPERADORES DE COMPARACIÓN
// -----------------------------------------------------------------------------
// IMPORTANTE: En JS, siempre usa '===' (estricto) en lugar de '==' (laxo).
// '==' intenta convertir tipos, '===' verifica valor Y tipo.

let numero = 5;
let textoNumero = "5";

console.log("\n--- Comparación Estricta vs Laxa ---");
if (numero == textoNumero) {
    console.log("Con '==': Son iguales (JS convirtió el texto a número).");
}

if (numero === textoNumero) {
    console.log("Con '===': Son iguales.");
} else {
    console.log("Con '===': NO son iguales (Diferente tipo). ¡MEJOR PRÁCTICA!");
}

// -----------------------------------------------------------------------------
// 3. SWITCH (Múltiples casos)
// -----------------------------------------------------------------------------
// Útil cuando tienes muchas condiciones sobre la misma variable.

let diaSemana = 3; // 1 = Lunes, 2 = Martes...

console.log("\n--- Switch Case ---");
switch (diaSemana) {
    case 1:
        console.log("Es Lunes, ánimo.");
        break; // Importante: 'break' evita que siga ejecutando los siguientes casos
    case 2:
    case 3:
    case 4:
        console.log("Es día laborable (Martes-Jueves).");
        break;
    case 5:
        console.log("¡Es Viernes!");
        break;
    default:
        console.log("Es fin de semana 🎉");
}

// -----------------------------------------------------------------------------
// 4. BUCLES (LOOPS) - FOR
// -----------------------------------------------------------------------------
// Repetir un bloque de código un número determinado de veces.
// Estructura: for (inicialización; condición; actualización)

console.log("\n--- Bucle For (Contando hasta 5) ---");
for (let i = 1; i <= 5; i++) {
    // 'i' es la variable contadora típica
    console.log(`Iteración número: ${i}`);
}

// -----------------------------------------------------------------------------
// 5. BUCLES (LOOPS) - WHILE
// -----------------------------------------------------------------------------
// Repetir MIENTRAS se cumpla una condición. Útil cuando no sabes cuántas veces repetirás.

console.log("\n--- Bucle While (Cuenta regresiva) ---");
let contador = 3;

while (contador > 0) {
    console.log(`Despegue en T-minus: ${contador}...`);
    contador--; // Disminuimos el contador
}
console.log("¡DESPEGUE! 🚀");

// -----------------------------------------------------------------------------
// 6. BREAK y CONTINUE
// -----------------------------------------------------------------------------

console.log("\n--- Break y Continue ---");
// Buscamos el primer número par mayor que 0
for (let i = 1; i <= 10; i++) {
    if (i % 2 !== 0) {
        continue; // Salta esta iteración si es impar
    }
    console.log(`Encontrado par: ${i}`);
    if (i === 6) {
        console.log("Paramos en 6 (break).");
        break; // Detiene el bucle completamente
    }
}
