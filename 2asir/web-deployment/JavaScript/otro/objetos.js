/* =========================================================================
   GUÍA MAESTRA DE PROGRAMACIÓN ORIENTADA A OBJETOS (POO) EN JAVASCRIPT
=========================================================================
   Instrucciones:
   1. Copia este código en un archivo (ej: poo_master.js).
   2. Ejecútalo con Node.js (node poo_master.js) o en la consola del navegador.
   3. Lee los comentarios paso a paso.
*/

console.log("🟦 --- 1. OBJETOS LITERALES (La base) ---");

// DEFINICIÓN: La forma más básica. Agrupa datos (propiedades) y comportamientos (métodos).
const ironMan = {
    nombre: "Tony Stark",    // Propiedad
    equipo: "Avengers",      // Propiedad
    energia: 100,
    
    // Método: Función dentro de un objeto
    atacar: function() {
        console.log(`${this.nombre} dispara un rayo repulsor.`);
        // 'this' hace referencia al propio objeto
    },

    // Sintaxis moderna de métodos (ES6)
    recargar() {
        this.energia = 100;
        console.log("Energía al máximo.");
    }
};

ironMan.atacar(); 
// PROBLEMA: Si queremos crear 100 superhéroes, tendríamos que copiar y pegar este código 100 veces.

console.log("\n🟦 --- 2. EL CAMINO ANTIGUO: FUNCIÓN CONSTRUCTORA Y PROTOTIPOS ---");

// Antes de ES6 (2015), no existía la palabra 'class'. Usábamos funciones.
// Esto es importante para entender qué pasa "bajo el capó".

function HeroeAntiguo(nombre, alias) {
    // 'this' se refiere a la nueva instancia que se crea
    this.nombre = nombre;
    this.alias = alias;
}

// PROTOTYPE:
// Para no copiar la función 'saludar' en CADA objeto (gastando memoria),
// la adjuntamos al prototipo. Todos los objetos heredarán de aquí.
HeroeAntiguo.prototype.saludar = function() {
    console.log(`Hola, soy ${this.alias} (Versión antigua).`);
};

const batman = new HeroeAntiguo("Bruce Wayne", "Batman");
batman.saludar();


console.log("\n🟦 --- 3. SINTAXIS MODERNA: CLASES (ES6) ---");

// Esto es "Azúcar Sintáctico". Por debajo sigue usando prototipos, pero es más limpio.

class Heroe {
    // 1. Constructor: Se ejecuta automáticamente al hacer 'new'
    constructor(nombre, poder) {
        this.nombre = nombre;
        this._poder = poder; // Convención: guion bajo implica "tratar como privado" (aunque es público)
        this.nivel = 1;
    }

    // 2. Métodos: Se agregan automáticamente al prototipo
    entrenar() {
        this.nivel++;
        console.log(`${this.nombre} ha subido al nivel ${this.nivel}.`);
    }

    // 3. Getters y Setters: Para controlar el acceso a propiedades
    get info() {
        return `${this.nombre} usa ${this._poder}`;
    }

    set cambiarPoder(nuevoPoder) {
        if (nuevoPoder.length < 3) {
            console.log("Error: El poder es muy corto.");
            return;
        }
        this._poder = nuevoPoder;
    }
    
    // 4. Métodos Estáticos: Pertenecen a la Clase, no al objeto. Utilería.
    static definicion() {
        return "Un héroe es alguien que protege a los demás.";
    }
}

const spiderman = new Heroe("Peter Parker", "Telarañas");
spiderman.entrenar();              // Uso de método
console.log(spiderman.info);       // Uso de Getter (sin paréntesis)
spiderman.cambiarPoder = "Fuerza"; // Uso de Setter (como asignación)
console.log(Heroe.definicion());   // Uso de Static (desde la clase)


console.log("\n🟦 --- 4. PILARES DE LA POO: HERENCIA ---");

// extends: Hereda todas las propiedades y métodos de la clase padre
class Vengador extends Heroe {
    constructor(nombre, poder, armadura) {
        // super(): Llama al constructor de la clase Padre (Heroe)
        // OBLIGATORIO antes de usar 'this'
        super(nombre, poder); 
        this.armadura = armadura;
    }

    // SOBRESCRITURA (Polimorfismo): Modificar un comportamiento heredado
    entrenar() {
        // Podemos llamar al método original con super.entrenar() si queremos
        super.entrenar(); 
        console.log(`...y además ha mejorado su armadura ${this.armadura}.`);
    }
}

const warMachine = new Vengador("Rhodey", "Fuego", "Mark II");
warMachine.entrenar(); // Ejecuta la versión sobrescrita


console.log("\n🟦 --- 5. ENCAPSULAMIENTO REAL (CAMPOS PRIVADOS #) ---");

// Desde ES2020/2022, JavaScript tiene privacidad real usando '#'
// Estos datos NO son accesibles desde fuera de la clase.

class CuentaBancaria {
    #saldo; // Declaración obligatoria del campo privado
    #pin;

    constructor(titular, saldoInicial, pin) {
        this.titular = titular; // Público
        this.#saldo = saldoInicial; // Privado
        this.#pin = pin; // Privado
    }

    depositar(cantidad) {
        this.#saldo += cantidad;
        this.#imprimirSaldo();
    }

    retirar(cantidad, pinIngresado) {
        if (pinIngresado !== this.#pin) {
            console.log("❌ PIN incorrecto.");
            return;
        }
        if (cantidad > this.#saldo) {
            console.log("❌ Fondos insuficientes.");
            return;
        }
        this.#saldo -= cantidad;
        console.log(`✅ Retiro exitoso. Quedan ${this.#saldo}€`);
    }

    // Método privado (Solo usable dentro de la clase)
    #imprimirSaldo() {
        console.log(`Saldo actual: ${this.#saldo}€`);
    }
}

const miCuenta = new CuentaBancaria("Usuario", 1000, 1234);

miCuenta.depositar(500); // Funciona
miCuenta.retirar(200, 1234); // Funciona

// INTENTO DE HACKEO:
try {
    console.log(miCuenta.#saldo); // ❌ ERROR: Private field '#saldo' must be declared
} catch (error) {
    console.log("🔒 BLOQUEADO: No puedes acceder a variables privadas (#saldo) desde fuera.");
}


console.log("\n🟦 --- 6. POLIMORFISMO (EN PROFUNDIDAD) ---");

// Capacidad de objetos diferentes de responder al mismo mensaje (método) de distinta forma.

class Animal {
    hacerSonido() { console.log("Sonido genérico..."); }
}

class Perro extends Animal {
    hacerSonido() { console.log("Guau Guau!"); }
}

class Gato extends Animal {
    hacerSonido() { console.log("Miau Miau!"); }
}

// Función que acepta CUALQUIER animal (Polimorfismo)
function escucharAnimal(animal) {
    animal.hacerSonido();
}

const animales = [new Perro(), new Gato(), new Animal()];

console.log("--- Concierto de animales ---");
animales.forEach(a => escucharAnimal(a));


/* =========================================================================
   RESUMEN FINAL
=========================================================================
   1. Object Literal: Para cosas simples y únicas.
   2. Class: Plantilla para crear múltiples objetos iguales.
   3. constructor: Inicializa los datos.
   4. this: El contexto (el objeto actual).
   5. extends / super: Para herencia.
   6. #propiedad: Para datos verdaderamente privados (seguridad).
*/