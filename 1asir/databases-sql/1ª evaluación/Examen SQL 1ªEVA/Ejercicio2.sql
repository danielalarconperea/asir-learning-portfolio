CREATE DATABASE Ejercicio2;
USE Ejercicio2;

CREATE TABLE cliente (
    codigo_c INT PRIMARY KEY,
    num_social INT NOT NULL NOT NULL,
    domicilio varchar(200),
    tfno char(9));
DESCRIBE cliente;

CREATE TABLE proyecto(
    codigo_p INT PRIMARY KEY,
    descripcion TEXT,
    fecha_inicio DATE,
    fecha_fin DATE,
    cuantia INT,
    codigo_cliente INT REFERENCES cliente(codigo_c));
DESCRIBE proyecto;

CREATE TABLE colaborador (
    nif char(9) PRIMARY KEY,
    nombre varchar(30) NOT NULL,
    domicilio varchar(200),
    banco varchar(100),
    numero_cuenta INT unique,
    tfno char(9));
DESCRIBE colaborador;

CREATE TABLE participan (
    nif_colaborador char(9) REFERENCES colaborador(nif),
    codigo_proyecto INT REFERENCES proyecto(codigo_p),
    PRIMARY KEY (nif_colaborador, codigo_proyecto));
DESCRIBE participan;

CREATE TABLE tipo_pago (
    codigo_pago INT PRIMARY KEY,
    descripcion TEXT);
DESCRIBE tipo_pago;

CREATE TABLE pago (
    numero INT PRIMARY KEY,
    concepto TEXT,
    cantidad INT,
    fecha_pago DATE,
    nif_colaborador char(9) REFERENCES colaborador(nif),
    codigo_tipo_pago INT REFERENCES tipo_pago(codigo_pago));
DESCRIBE pago;

ALTER TABLE cliente modify num_social INT unique;
DESCRIBE cliente;
DROP TABLE pago;
DESCRIBE pago;

DROP DATABASE Ejercicio2;