CREATE database Problema2;
use Problema2;

CREATE TABLE Servicios_de_seguridad (
    ID_servicio INT PRIMARY KEY,
    descripcion_detallada TEXT,
    precio_asociado FLOAT NOT NULL);
DESCRIBE Servicios_de_seguridad;

CREATE TABLE Registro_de_incidentes (
    ID_incidente INT PRIMARY KEY,
    detalles_sobre_el_incidente TEXT,
    fecha_y_hora DATETIME NOT NULL,
    cliente_afectado VARCHAR(30) NOT NULL,
    técnico_asegurado VARCHAR(30) NOT NULL,
    ID_servicio INT REFERENCES Servicios_de_seguridad(ID_servicio));
DESCRIBE Registro_de_incidentes;

CREATE TABLE Tecnico_de_seguridad (
    ID_tecnico INT PRIMARY KEY,
    nombre_tecnico VARCHAR(30) NOT NULL,
    apellido_tecnico VARCHAR(60) NOT NULL,
    direccion_tecnico VARCHAR(30),
    direccion_correo_elec_tecnico VARCHAR(150) NOT NULL unique,
    n_telefono_tecnico CHAR(9) unique,
    nivel_experiencia VARCHAR(50));
DESCRIBE Tecnico_de_seguridad;

CREATE TABLE Contrato (
    ID_contrato INT PRIMARY KEY,
    fecha_inicio DATE NOT NULL,
    fecha_finalizacion DATE NOT NULL,
    coste_total FLOAT);
DESCRIBE Contrato;

CREATE TABLE Cliente (
    ID_cliente INT PRIMARY KEY,
    nombre_empresa VARCHAR(150) NOT NULL,
    nombre_contacto_principal VARCHAR(100),
    direccion_cliente VARCHAR(200) NOT NULL,
    direccion_correo_elec_cliente VARCHAR(150) unique,
    n_telefono_cliente CHAR(9) unique);
DESCRIBE cliente;

CREATE TABLE Informe_de_seguridad (
    ID_informe INT PRIMARY KEY,
    estado_seguridad VARCHAR(200),
    actividades_realizadas_tecnicos TEXT,
    recomendaciones_seguridad TEXT);
DESCRIBE Informe_de_seguridad;

CREATE TABLE Reportado (
    ID_cliente INT REFERENCES Cliente(ID_cliente),
    ID_incidente INT REFERENCES Registro_de_incidentes(ID_incidente),
    PRIMARY KEY (ID_cliente, ID_incidente));
DESCRIBE Reportado;

CREATE TABLE Presta (
    ID_servicio INT REFERENCES Servicios_de_seguridad(ID_servicio),
    ID_tecnico INT REFERENCES Tecnico_de_seguridad(ID_tecnico),
    PRIMARY KEY (ID_servicio, ID_tecnico));
DESCRIBE Presta;

CREATE TABLE Asignado (
    ID_tecnico INT REFERENCES Tecnico_de_seguridad(ID_tecnico),
    ID_contrato INT REFERENCES Contrato(ID_contrato),
    PRIMARY KEY (ID_tecnico, ID_contrato));
DESCRIBE Asignado;

CREATE TABLE Firma (
    ID_contrato INT REFERENCES Contrato(ID_contrato),
    ID_cliente INT REFERENCES Cliente(ID_cliente),
    PRIMARY KEY (ID_contrato, ID_cliente));
DESCRIBE Firma;

CREATE TABLE Informa (
    ID_cliente INT REFERENCES Cliente(ID_cliente),
    ID_informe INT REFERENCES Informe_de_seguridad(ID_informe),
    PRIMARY KEY (ID_cliente, ID_informe));
DESCRIBE Informa;

DROP database Problema2;