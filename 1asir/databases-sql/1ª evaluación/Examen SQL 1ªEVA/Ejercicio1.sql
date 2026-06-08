CREATE DATABASE Ejercicio1;
USE Ejercicio1;

CREATE TABLE origen(
    codigo_origen INT PRIMARY KEY,
    nombre varchar(30) NOT NULL,
    otros_datos varchar(255));
DESCRIBE origen;

CREATE TABLE destino (
    codigo_destino INT PRIMARY KEY,
    nombre varchar(30) NOT NULL,
    otros_datos varchar(255));
DESCRIBE destino;

CREATE TABLE viajero (
    dni char(9) PRIMARY KEY,
    nombre varchar(30) NOT NULL,
    direccion varchar(200),
    tfno char(9) unique);
DESCRIBE viajero;

CREATE TABLE viaje (
    codigo_viaje INT PRIMARY KEY,
    num_plazas INT,
    fecha DATE,
    otros_datos varchar(255),
    dni_viajero varchar(255) REFERENCES viajero(dni),
    codigo_origen INT REFERENCES origen(codigo_origen),
    codigo_destino INT REFERENCES destino(codigo_destino));
DESCRIBE viaje;


ALTER TABLE viaje ADD precio float;
DESCRIBE viaje;
ALTER TABLE viajero modify tfno varchar(15) NOT NULL;
DESCRIBE viajero;

DROP DATABASE Ejercicio1;