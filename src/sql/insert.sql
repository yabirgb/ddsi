INSERT INTO cliente(dni,nombre,telefono) VALUES ('12345678A', 'cliente1', '111') ON CONFLICT DO NOTHING;
INSERT INTO cliente(dni,nombre,telefono) VALUES ('12345678B', 'cliente2', '112') ON CONFLICT DO NOTHING;
INSERT INTO cliente(dni,nombre,telefono) VALUES ('12345678C', 'cliente3', '113') ON CONFLICT DO NOTHING;
INSERT INTO cliente(dni,nombre,telefono) VALUES ('12345678D', 'cliente4', '114') ON CONFLICT DO NOTHING;

INSERT INTO coche(id_coche, numero_bastidor, matricula, marca, modelo, color, estado) VALUES ('1', '1', '1', 'marca1', 'modelo1', 'color1', 'estado1') ON CONFLICT DO NOTHING;
INSERT INTO coche(id_coche, numero_bastidor, matricula, marca, modelo, color, estado) VALUES ('2', '2', '2', 'marca2', 'modelo1', 'color1', 'estado1') ON CONFLICT DO NOTHING;
INSERT INTO coche(id_coche, numero_bastidor, matricula, marca, modelo, color, estado) VALUES ('3', '3', '3', 'marca1', 'modelo1', 'color1', 'estado1') ON CONFLICT DO NOTHING;


INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678A', '1', '1/1/2000', '1/1/2000', '2', 'pagado') ON CONFLICT DO NOTHING;
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678B', '1', '1/1/2000', '1/1/2000', '2', 'pagado') ON CONFLICT DO NOTHING;
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678C', '2', '1/1/2000', '1/1/2000', '2', 'pagado') ON CONFLICT DO NOTHING;
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678D', '2', '1/1/2000', '1/1/2000', '2', 'pagado') ON CONFLICT DO NOTHING;

INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678A', '2', '1/2/2000', '1/2/2000', '2', 'no_pagado') ON CONFLICT DO NOTHING;
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678A', '3', '1/2/2000', '1/2/2000', '2', 'no_pagado') ON CONFLICT DO NOTHING;
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678B', '1', '1/2/2000', '1/2/2000', '2', 'no_pagado') ON CONFLICT DO NOTHING;
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678B', '2', '1/2/2000', '1/2/2000', '2', 'no_pagado') ON CONFLICT DO NOTHING;
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678C', '1', '1/2/2000', '1/2/2000', '2', 'no_pagado') ON CONFLICT DO NOTHING;