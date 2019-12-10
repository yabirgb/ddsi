CREATE TABLE if not exists cliente (
    dni VARCHAR(9) PRIMARY KEY, 
    nombre VARCHAR(20), 
    telefono VARCHAR(20)
);

create table if not exists coche(
    id_coche integer primary key,
    numero_bastidor varchar(17) unique,
    matricula varchar(7) unique,
    marca varchar(20) not null,
    modelo varchar(20) not null,
    color varchar(12) not null,
    estado varchar(256)
);

CREATE TABLE if not exists alquiler (
    dni varchar(9), 
    id_coche integer ,
    fecha_inicio DATE, 
    fecha_fin DATE,
    precio FLOAT,
    estado VARCHAR(10) check (estado in ('pagado', 'no_pagado')),
    PRIMARY KEY (dni, id_coche, fecha_inicio),

    foreign key (dni) references cliente(dni) on delete cascade,
    foreign key (id_coche) references coche(id_coche) on delete cascade
    
);

create table if not exists proveedores(
       cif varchar(9) not null primary key,
       nombre varchar(64) not null,
       ubicacion varchar(64) not null,
       telefono integer not null,
       correo varchar(64) not null,
       created date not null default CURRENT_TIMESTAMP

);


create table if not exists solicitud(

       cif varchar(9),
       id_coche integer PRIMARY KEY,
       fecha_entrega date,
       punto_recogida varchar(64) not null,
       
       foreign key (id_coche) references coche(id_coche) on delete cascade,
       foreign key (cif) references proveedores(cif) on delete cascade
       
);

INSERT INTO cliente(dni,nombre,telefono) VALUES ('12345678A', 'cliente1', '111');
INSERT INTO cliente(dni,nombre,telefono) VALUES ('12345678B', 'cliente2', '112');
INSERT INTO cliente(dni,nombre,telefono) VALUES ('12345678C', 'cliente3', '113');
INSERT INTO cliente(dni,nombre,telefono) VALUES ('12345678D', 'cliente4', '114');

INSERT INTO coche(id_coche, numero_bastidor, matricula, marca, modelo, color, estado) VALUES ('1', '1', '1', 'marca1', 'modelo1', 'color1', 'estado1');
INSERT INTO coche(id_coche, numero_bastidor, matricula, marca, modelo, color, estado) VALUES ('2', '2', '2', 'marca2', 'modelo1', 'color1', 'estado1');
INSERT INTO coche(id_coche, numero_bastidor, matricula, marca, modelo, color, estado) VALUES ('3', '3', '3', 'marca1', 'modelo1', 'color1', 'estado1');


INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678A', '1', '1/1/2000', '1/1/2000', '2', 'pagado');
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678A', '2', '1/2/2000', '1/2/2000', '2', 'no_pagado');
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678B', '1', '1/1/2000', '1/1/2000', '2', 'pagado');
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678C', '2', '1/1/2000', '1/1/2000', '2', 'pagado');
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678D', '2', '1/1/2000', '1/1/2000', '2', 'pagado');
