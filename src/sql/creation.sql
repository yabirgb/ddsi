CREATE TABLE IF NOT EXISTS cliente(
    dni VARCHAR(9) PRIMARY KEY,
    nombre VARCHAR(20), 
    telefono VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS coche(
    id_coche SERIAL PRIMARY KEY,
    numero_bastidor VARCHAR(17) UNIQUE,
    matricula VARCHAR(7) UNIQUE,
    marca VARCHAR(20) NOT NULL,
    modelo VARCHAR(20) NOT NULL,
    color VARCHAR(12) NOT NULL,
    estado VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS alquiler(
    dni VARCHAR(9), 
    id_coche INTEGER,
    fecha_inicio DATE, 
    fecha_fin DATE,
    precio FLOAT,
    estado VARCHAR(10) CHECK (estado IN ('pagado', 'no_pagado')),

    PRIMARY KEY (dni, id_coche, fecha_inicio),
    FOREIGN KEY (dni) REFERENCES cliente(dni) ON DELETE CASCADE,
    FOREIGN KEY (id_coche) REFERENCES coche(id_coche) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS proveedor(
       cif VARCHAR(9) PRIMARY KEY,
       nombre VARCHAR(64) NOT NULL,
       ubicacion VARCHAR(64) NOT NULL,
       telefono INTEGER NOT NULL,
       correo VARCHAR(64) NOT NULL,
       created DATE NOT NULL DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS solicitud(
       cif VARCHAR(9),
       id_coche INTEGER PRIMARY KEY,
       fecha_entrega DATE,
       punto_recogida VARCHAR(64) NOT NULL,
       
       FOREIGN KEY (id_coche) REFERENCES coche(id_coche) ON DELETE CASCADE,
       FOREIGN KEY (cif) REFERENCES proveedor(cif) ON DELETE CASCADE
);
