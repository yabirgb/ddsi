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
