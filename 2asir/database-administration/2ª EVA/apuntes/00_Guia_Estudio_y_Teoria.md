# Guía de Estudio y Teoría de Bases de Datos (MySQL)

Este documento complementa los archivos SQL prácticos con los conceptos teóricos fundamentales que no se explican directamente con código, así como comandos de sistema vitales para la administración.

## Índice
1. [Diseño de Bases de Datos (Modelo E/R)](#1-diseño-de-bases-de-datos)
2. [Normalización](#2-normalización)
3. [Tipos de Datos en MySQL](#3-tipos-de-datos-en-mysql)
4. [Transacciones (ACID)](#4-transacciones-acid)
5. [Comandos de Sistema (Backups y Restauración)](#5-comandos-de-sistema)

---

## 1. Diseño de Bases de Datos

Antes de escribir una sola línea de SQL, es crucial diseñar la base de datos correctamente.

### Entidades y Relaciones
*   **Entidad**: Objeto del mundo real (ej: *Alumno*, *Asignatura*). Se convierte en **Tabla**.
*   **Atributo**: Característica de la entidad (ej: *Nombre*, *DNI*). Se convierte en **Columna**.
*   **Relación**: Asociación entre entidades.
    *   **1:1 (Uno a Uno)**: Un usuario tiene un único perfil extendido. (Poco común, suele fusionarse en una tabla).
    *   **1:N (Uno a Muchos)**: Un profesor imparte varias asignaturas. Se implementa propagando la Clave Primaria (PK) del lado "1" como Clave Foránea (FK) al lado "N".
    *   **N:M (Muchos a Muchos)**: Un alumno cursa muchas asignaturas y una asignatura tiene muchos alumnos. **Requiere una tabla intermedia** que contiene las FK de ambas entidades.

### Claves
*   **Primary Key (PK)**: Identificador único e irrepetible de una fila. Recomendado: `INT AUTO_INCREMENT`.
*   **Foreign Key (FK)**: Columna que referencia a una PK de otra tabla para mantener la **Integridad Referencial**.

---

## 2. Normalización

Proceso para eliminar redundancia y dependencias incoherentes.

*   **1FN (Primera Forma Normal)**: 
    *   No hay grupos repetitivos (ej: no tener `telefono1`, `telefono2`).
    *   Todos las columnas contienen valores atómicos (indivisibles).
*   **2FN (Segunda Forma Normal)**: 
    *   Cumple 1FN.
    *   Todos los atributos dependen de la clave principal completa (no solo de una parte, importante en claves compuestas).
*   **3FN (Tercera Forma Normal)**: 
    *   Cumple 2FN.
    *   No hay dependencias transitivas (ningún atributo depende de otro atributo que no sea la clave principal). Ej: Si tienes `CP` y `Ciudad`, `Ciudad` depende de `CP`, no del usuario directamente -> Separar en tabla de Direcciones.

---

## 3. Tipos de Datos en MySQL

Elegir el tipo correcto ahorra espacio y mejora el rendimiento.

### Numéricos
*   `INT`: Números enteros estándar (±2 mil millones). `UNSIGNED` para solo positivos.
*   `TINYINT`: Muy pequeño (0-255). Usado para booleanos (`TINYINT(1)`).
*   `DECIMAL(M, D)`: Exacto para dinero. `DECIMAL(10,2)` almacena hasta 99999999.99.
*   `FLOAT/DOUBLE`: Aproximado para cálculos científicos. **No usar para dinero**.

### Texto
*   `VARCHAR(n)`: Longitud variable. Solo usa lo que necesita (+1 byte). Ej: Nombres, emails.
*   `CHAR(n)`: Longitud fija. Rellena con espacios. Bueno para códigos fijos (ej: DNI, códigos de país 'ES', 'FR').
*   `TEXT`: Para textos largos (> 65KB).

### Fecha y Hora
*   `DATE`: Solo fecha (`YYYY-MM-DD`).
*   `DATETIME`: Fecha y hora (`YYYY-MM-DD HH:MM:SS`). Rango 1000 a 9999.
*   `TIMESTAMP`: Fecha y hora UTC. Rango 1970 a 2038. Se actualiza solo con `current_timestamp`.

---

## 4. Transacciones (ACID)

Fundamental para la integridad en sistemas multiusuario (2º ASIR).

*   **A - Atomicidad**: Todo o nada. Si una parte falla, se deshace todo (`ROLLBACK`).
*   **C - Consistencia**: La transacción lleva la BD de un estado válido a otro válido.
*   **I - Aislamiento**: Las transacciones concurrentes no se interfieren (ver niveles de aislamiento).
*   **D - Durabilidad**: Una vez confirmado (`COMMIT`), el cambio es permanente incluso si se va la luz.

---

## 5. Comandos de Sistema

Estos comandos se ejecutan en la terminal (PowerShell o Bash), no dentro del cliente MySQL.

### Copias de Seguridad (Backup)
Hacer un volcado de la estructura y datos a un archivo `.sql`.

**Sintaxis completa:**
```bash
mysqldump -u [usuario] -p [nombre_base_datos] > [archivo_destino.sql]
```

**Opciones útiles:**
*   `--routines`: Incluye procedimientos almacenados y funciones.
*   `--triggers`: Incluye disparadores (activado por defecto).
*   `--events`: Incluye eventos programados.
*   `--add-drop-table`: Añade `DROP TABLE` antes de `CREATE` (útil para sobreescribir).

**Ejemplo completo (Backup de 'colegio'):**
```bash
mysqldump -u root -p --routines --events colegio > C:\backups\colegio_full.sql
```

### Restauración
Importar un archivo `.sql` a la base de datos.

**Método 1: Desde terminal (Sistema)**
```bash
mysql -u root -p [nombre_base_datos] < [archivo_origen.sql]
```
*Nota: La base de datos debe existir previamente (`CREATE DATABASE...`).*

**Método 2: Desde dentro de MySQL (Source)**
```sql
USE nombre_base_datos;
SOURCE C:/ruta/al/archivo/archivo_origen.sql;
```

### Conexión Remota
Para conectarse a un servidor MySQL en otra máquina.

```bash
mysql -h [IP_SERVIDOR] -P [PUERTO] -u [USUARIO] -p
# Ejemplo:
mysql -h 192.168.1.50 -P 3306 -u admin -p
```
