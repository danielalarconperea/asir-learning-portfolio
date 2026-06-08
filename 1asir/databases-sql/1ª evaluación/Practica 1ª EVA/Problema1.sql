CREATE database Problema1;
use Problema1;

CREATE TABLE Maquina (
    ID_maquina INT PRIMARY KEY,
    ubicacion VARCHAR(100),
    tipo_de_juego VARCHAR(100));
DESCRIBE Maquina;

CREATE TABLE Jugador (
    ID_jugador INT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    edad INT NOT NULL);
DESCRIBE Jugador;

CREATE TABLE Partida (
    ID_partida INT PRIMARY KEY,
    puntuaje INT,
    ID_jugador INT REFERENCES Jugador(ID_jugador),
    ID_maquina INT REFERENCES Maquina(ID_maquina));
DESCRIBE Partida;

CREATE TABLE Recompensa (
    ID_recompensa INT PRIMARY KEY,
    puntaje INT);
DESCRIBE Recompensa;

CREATE TABLE Recibe (
    ID_jugador INT REFERENCES Jugador(ID_jugador),
    ID_recompensa INT REFERENCES Recompensa(ID_recompensa),
    PRIMARY KEY (ID_jugador, ID_recompensa));
DESCRIBE Recibe;

DROP DATABASE Problema1;