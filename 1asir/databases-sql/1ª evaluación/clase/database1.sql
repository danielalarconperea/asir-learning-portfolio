CREATE DATABASE ejercicio1;
USE ejercicio1;
create table cliente(
    dni CHAR(9) PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    apellidos VARCHAR(50) NOT NULL,
    fecha_nac DATE,
    teléfono CHAR(11));
create table provedor(
    nif CHAR(10) PRIMARY KEY,
    nombre_provedor VARCHAR(30) NOT NULL,
    dirección VARCHAR(100));
CREATE TABLE producto (
    código_producto INT PRIMARY KEY,
    nombre_producto VARCHAR(30) NOT NULL,
    precio FLOAT NOT NULL,
    nif_provedor CHAR(10) REFERENCES provedor(nif));
CREATE TABLE compras (
    dni_cliente CHAR(9) REFERENCES cliente(dni),
    código_producto INT REFERENCES producto(código_producto),
    PRIMARY KEY (dni_cliente, código_producto));
describe cliente;
describe provedor;
describe producto;
describe compras;
ALTER TABLE cliente MODIFY nombre VARCHAR (50) NOT NULL;
describe cliente;
ALTER TABLE cliente MODIFY teléfono INT NOT NULL;
describe cliente;
ALTER TABLE cliente ADD saldo FLOAT;
describe cliente;
ALTER TABLE cliente DROP apellidos;
describe cliente;
ALTER TABLE cliente add apellidos VARCHAR(100) NOT NULL after nombre;
describe cliente;
ALTER TABLE cliente MODIFY fecha_nac date NOT NULL after teléfono;
describe cliente;
ALTER TABLE cliente ADD apodo VARCHAR (50) FIRST;
describe cliente;
ALTER TABLE producto DROP foreign KEY nif_provedor;