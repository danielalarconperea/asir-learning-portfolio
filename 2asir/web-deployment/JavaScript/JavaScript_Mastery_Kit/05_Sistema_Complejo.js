/**
 * 05_Sistema_Complejo.js
 * 
 * OBJETIVO: INTEGRACIÓN FINAL
 * Vamos a construir un pequeño sistema de gestión escolar.
 * Combinaremos: Clases, Arreglos, Métodos, Condicionales y Manejo de Errores.
 * 
 * PROYECTO: "Gestor de Notas Escolar"
 */

console.log("-----------------------------------------");
console.log(" SISTEMA DE GESTIÓN ESCOLAR v1.0 ");
console.log("-----------------------------------------");

class Estudiante {
    constructor(nombre, id) {
        this.nombre = nombre;
        this.id = id;
        this.notas = [];
    }

    agregarNota(nota) {
        if (nota < 0 || nota > 10) {
            console.error(`ERROR: La nota ${nota} no es válida (0-10).`);
            return;
        }
        this.notas.push(nota);
        console.log(`Nota ${nota} añadida a ${this.nombre}.`);
    }

    calcularPromedio() {
        if (this.notas.length === 0) return 0;

        // Usamos .reduce para sumar todas las notas
        const suma = this.notas.reduce((total, actual) => total + actual, 0);
        return (suma / this.notas.length).toFixed(2); // .toFixed(2) corta a 2 decimales
    }

    mostrarEstado() {
        const promedio = this.calcularPromedio();
        const estado = promedio >= 5 ? "APROBADO ✅" : "SUSPENDIDO ❌";
        return `${this.nombre} (ID: ${this.id}) - Promedio: ${promedio} - ${estado}`;
    }
}

class Escuela {
    constructor(nombre) {
        this.nombre = nombre;
        this.estudiantes = [];
    }

    matricular(estudiante) {
        this.estudiantes.push(estudiante);
        console.log(`Estudiante ${estudiante.nombre} matriculado en ${this.nombre}.`);
    }

    mostrarTodos() {
        console.log(`\n--- Listado de ${this.nombre} ---`);
        this.estudiantes.forEach(est => {
            console.log(est.mostrarEstado());
        });
    }

    obtenerMejorEstudiante() {
        if (this.estudiantes.length === 0) return null;

        // Ordenamos una copia del array de mayor a menor promedio
        // [...this.estudiantes] crea una copia para no alterar el original con .sort()
        const ordenados = [...this.estudiantes].sort((a, b) => b.calcularPromedio() - a.calcularPromedio());

        return ordenados[0]; // El primero es el mejor
    }
}

// --- EJECUCIÓN (Simulación) ---

const miEscuela = new Escuela("Instituto Tech");

// 1. Crear Estudiantes
const ana = new Estudiante("Ana García", 101);
const carlos = new Estudiante("Carlos Pérez", 102);
const beatriz = new Estudiante("Beatriz López", 103);

// 2. Matricular
miEscuela.matricular(ana);
miEscuela.matricular(carlos);
miEscuela.matricular(beatriz);

// 3. Poner Notas (Simulamos un semestre)
console.log("\n--- Añadiendo Notas ---");
ana.agregarNota(9.5);
ana.agregarNota(8.0);

carlos.agregarNota(4.5);
carlos.agregarNota(5.0); // Por los pelos...

beatriz.agregarNota(10);
beatriz.agregarNota(9.8); // ¡Casi perfecto!
beatriz.agregarNota(12);  // Error intencionado

// 4. Reportes
miEscuela.mostrarTodos();

console.log("\n--- Cuadro de Honor ---");
const mejor = miEscuela.obtenerMejorEstudiante();
if (mejor) {
    console.log(`🏆 El mejor estudiante es: ${mejor.nombre} con un promedio de ${mejor.calcularPromedio()}`);
}

console.log("\n[!] Sistema finalizado correctamente.");
