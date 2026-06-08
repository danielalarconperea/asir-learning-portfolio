CREATE database Problema6;
USE Problema6;

CREATE TABLE Categoria (
    ID_categoria INT PRIMARY KEY,
    descripcion TEXT);
DESCRIBE Categoria;

CREATE TABLE Nuevo (
    ID_categoria INT REFERENCES Categoria(ID_categoria),
    ID_nuevo INT,
    fecha_de_fabricacion DATE,
    PRIMARY key (ID_categoria, ID_nuevo));
DESCRIBE Nuevo;

CREATE TABLE Usado (
    ID_categoria INT REFERENCES Categoria(ID_categoria),
    ID_usado INT,
    kilometraje INT,
    PRIMARY key (ID_categoria, ID_usado));
DESCRIBE Usado;

CREATE TABLE Servicio_adicional (
    ID_servicio INT PRIMARY KEY,
    nombre_servicio VARCHAR(30) NOT NULL,
    precio FLOAT);
DESCRIBE Servicio_adicional;

CREATE TABLE Personal (
    ID_tecnico INT PRIMARY KEY,
    nombre_personal VARCHAR(30) NOT NULL,
    nivel_experiencia VARCHAR(50));
DESCRIBE Personal;

CREATE TABLE Vehiculo (
    ID_vehiculo INT PRIMARY KEY,
    marca VARCHAR(30) NOT NULL,
    precio FLOAT,
    ID_categoria INT REFERENCES Categoria(ID_categoria),
    ID_tecnico INT REFERENCES Personal(ID_tecnico),
    ID_servicio INT REFERENCES Servicio_adicional(ID_servicio));
DESCRIBE Vehiculo;

CREATE TABLE Cliente (
    ID_cliente INT PRIMARY KEY,
    nombre_cliente VARCHAR(30) NOT NULL,
    n_telefono CHAR(9) NOT NULL unique);
DESCRIBE Cliente;

CREATE TABLE Venta (
    ID_venta INT PRIMARY KEY,
    fecha_venta DATE,
    importe_total FLOAT,
    ID_cliente INT REFERENCES Cliente(ID_cliente));
DESCRIBE Venta;

CREATE TABLE Incluyen (
    ID_vehiculo INT REFERENCES Vehiculo(ID_vehiculo),
    ID_venta INT REFERENCES Venta(ID_venta),
    PRIMARY KEY (ID_vehiculo, ID_venta));
DESCRIBE Incluyen;

DROP DATABASE Problema6;