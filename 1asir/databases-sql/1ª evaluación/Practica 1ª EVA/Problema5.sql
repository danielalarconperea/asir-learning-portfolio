CREATE database Problema5;
use Problema5;

CREATE TABLE Cliente (
    ID_cliente INT PRIMARY KEY,
    nombre_cliente VARCHAR(30) NOT NULL,
    direccion_cliente VARCHAR(150) NOT NULL,
    n_telefono CHAR(9) unique,
    correo_cliente VARCHAR(200) NOT NULL unique);
DESCRIBE Cliente;

CREATE TABLE receta_medica (
    ID_receta_medica INT PRIMARY KEY,
    fecha_de_emision DATE,
    nombre_medico_emitio VARCHAR(30) NOT NULL,
    paciente_para_emitio VARCHAR(255) NOT NULL,
    ID_cliente INT REFERENCES Cliente(ID_cliente));
DESCRIBE receta_medica;

CREATE TABLE Institucion_medica (
    ID_cliente INT REFERENCES Cliente(ID_cliente),
    ID_institucion INT,
    nombre_contacto_principal VARCHAR(30),
    tipo_de_instutucion VARCHAR(40),
    PRIMARY KEY (ID_cliente, ID_institucion));
DESCRIBE Institucion_medica;

CREATE TABLE Individuo (
    ID_cliente INT REFERENCES Cliente(ID_cliente),
    ID_individuo INT,
    PRIMARY KEY (ID_cliente, ID_individuo));
DESCRIBE Individuo;

CREATE TABLE Empleado (
    ID_empleado INT PRIMARY KEY,
    nombre_empleado VARCHAR(30) NOT NULL,
    direccion_empleado VARCHAR(200),
    n_telefono_empleado CHAR(9) NOT NULL unique,
    correo_empleado VARCHAR(150) unique,
    cargo VARCHAR(40),
    salario FLOAT,
    fecha_inicio_empleado DATE);
DESCRIBE Empleado;

CREATE TABLE Producto_farmaceutico (
    ID_producto INT PRIMARY KEY,
    nombre_producto VARCHAR(150) NOT NULL,
    descripcion_producto TEXT,
    precio_venta FLOAT,
    fecha_caducidad DATE,
    cantidad_stock INT,
    sustancia_activa VARCHAR(200));
DESCRIBE Producto_farmaceutico;

CREATE TABLE Promocion (
    ID_promocion INT PRIMARY KEY,
    nombre_promocion VARCHAR(100) NOT NULL,
    descripcion_promocion TEXT,
    fecha_inicio_promocion DATE,
    fecha_finalizacion_promocion DATE,
    producto_en_promocion VARCHAR(100),
    descuento_aplicado FLOAT,
    ID_producto INT REFERENCES Producto_farmaceutico(ID_producto));
DESCRIBE Promocion;

CREATE TABLE Venta (
    ID_venta INT PRIMARY KEY,
    fecha_y_hora_venta DATETIME,
    cliente_que_compro VARCHAR(30),
    empleado_que_proceso_compra VARCHAR(30),
    cantidad_vendida_por_producto INT);
DESCRIBE Venta;

CREATE TABLE Receta_atendida (
    ID_receta_atendida INT PRIMARY KEY,
    producto_dispensado VARCHAR(150),
    cantidad INT);
DESCRIBE Receta_atendida;

CREATE TABLE Provedor (
    ID_provedor INT PRIMARY KEY,
    nombre_empresa VARCHAR(100) NOT NULL,
    direccion_provedor VARCHAR(200),
    n_telefono_provedor CHAR(9) unique,
    correo_provedor VARCHAR(200) NOT NULL unique,
    productos_suministrados_por_provedor VARCHAR(150),
    precio_compra_provedor FLOAT,
    ID_venta INT REFERENCES Venta(ID_venta));
DESCRIBE Provedor;

CREATE TABLE Recepcion_inventario (
    ID_recepcion_inventario INT PRIMARY KEY,
    fecha_recepcion DATE,
    producto_recivido VARCHAR(150),
    cantidad INT,
    precio_compra_inventario FLOAT,
    ID_porvedor INT REFERENCES Provedor(ID_provedor));
DESCRIBE Recepcion_inventario;

CREATE TABLE Atienden (
    ID_empleado INT REFERENCES Empleado(ID_empleado),
    ID_cliente INT REFERENCES Cliente(ID_cliente),
    PRIMARY KEY (ID_empleado, ID_cliente));
DESCRIBE Atienden;

CREATE TABLE Compra (
    ID_producto INT REFERENCES Producto_farmaceutico(ID_producto),
    ID_cliente INT REFERENCES Cliente(ID_cliente),
    PRIMARY KEY (ID_producto, ID_cliente));
DESCRIBE Compra;

CREATE TABLE Incluye (
    ID_venta INT REFERENCES Venta(ID_venta),
    ID_producto INT REFERENCES Producto_farmaceutico(ID_producto),
    PRIMARY KEY (ID_venta, ID_producto));
DESCRIBE Incluye;

CREATE TABLE Abastece (
    ID_producto INT REFERENCES Producto_farmaceutico(ID_producto),
    ID_provedor INT REFERENCES Provedor(ID_provedor),
    PRIMARY KEY (ID_producto, ID_provedor));
DESCRIBE Abastece;

DROP DATABASE Problema5;