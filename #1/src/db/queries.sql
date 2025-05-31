CREATE DATABASE cinema;
USE cinema;

CREATE TABLE sala (
    numero INT PRIMARY KEY,
    numPosti INT NOT NULL,
    dim INT NOT NULL,
    numFile INT NOT NULL,
    numPostiPerFila INT NOT NULL,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('3-D', 'tradizionale'))
);

CREATE TABLE film (
    codice INT PRIMARY KEY AUTO_INCREMENT,
    titolo VARCHAR(100) NOT NULL,
    anno INT NOT NULL,
    durata INT NOT NULL CHECK (durata > 0),
    lingua VARCHAR(30) NOT NULL
);

CREATE TABLE proiezione (
    numProiezione INT PRIMARY KEY,
    sala INT NOT NULL,
    filmProiettato INT NOT NULL,
    data DATE NOT NULL,
    ora TIME NOT NULL,
    FOREIGN KEY (sala) REFERENCES sala(numero) ON DELETE CASCADE,
    FOREIGN KEY (filmProiettato) REFERENCES film(codice) ON DELETE CASCADE
);

CREATE TABLE biglietto (
    numProiezione INT,
    numFila INT,
    numPosto INT,
    dataVendita DATE NOT NULL,
    prezzo DECIMAL(6,2) NOT NULL CHECK (prezzo >= 0),
    PRIMARY KEY (numProiezione, numFila, numPosto),
    FOREIGN KEY (numProiezione) REFERENCES proiezione(numProiezione) ON DELETE CASCADE
);