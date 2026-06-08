CREATE database Problema3;
use Problema3;

CREATE TABLE Producto (
    ID_producto INT PRIMARY KEY,
    nombre_producto VARCHAR(200) NOT NULL,
    precio FLOAT);
DESCRIBE Producto;

CREATE TABLE Categoria_de_producto (
    ID_categoria INT PRIMARY KEY,
    nombre_categoria VARCHAR(100) NOT NULL,
    descripcion TEXT,
    ID_producto INT REFERENCES Producto(ID_producto));
DESCRIBE Categoria_de_producto;

CREATE TABLE Simple_ (
    ID_categoria INT REFERENCES Categoria_de_producto(ID_categoria),
    IVA_aplicado FLOAT NOT NULL,
    restricciones_venta VARCHAR(100),
    PRIMARY KEY (ID_categoria));
DESCRIBE Simple_;

CREATE TABLE Especializada (
    ID_categoria INT REFERENCES Categoria_de_producto(ID_categoria),
    requisitos_tecnicos VARCHAR(200),
    garantia_extendida VARCHAR(10),
    PRIMARY KEY (ID_categoria));
DESCRIBE Especializada;

CREATE TABLE Cliente (
    ID_cliente INT PRIMARY KEY,
    nombre_cliente VARCHAR(255) NOT NULL,
    email_cliente VARCHAR(255) NOT NULL unique);
DESCRIBE cliente;

CREATE TABLE Direccion (
    ID_direccion INT PRIMARY KEY,
    codigo_postal VARCHAR(10) NOT NULL,
    calle VARCHAR(255) NOT NULL);
DESCRIBE Direccion;

CREATE TABLE Envio (
    ID_envio INT PRIMARY KEY,
    tipo_envio VARCHAR(255),
    costo FLOAT,
    ID_direccion INT REFERENCES Direccion(ID_direccion));
DESCRIBE Envio;

CREATE TABLE Pedido (
    ID_pedido INT PRIMARY KEY,
    fecha_pedido DATE NOT NULL,
    estado_pedido VARCHAR(30) NOT NULL,
    ID_cliente INT REFERENCES Cliente(ID_cliente),
    ID_envio INT REFERENCES Envio(ID_envio));
DESCRIBE Pedido;

CREATE TABLE Contiene (
    ID_producto INT REFERENCES Producto(ID_producto),
    ID_cliente INT REFERENCES Cliente(ID_cliente),
    PRIMARY KEY (ID_producto, ID_cliente));
DESCRIBE Contiene;

DROP DATABASE Problema3;