INSERT INTO cliente(dni,nombre,telefono) VALUES ('12345678A', 'cliente1', '111') ON CONFLICT DO NOTHING;
INSERT INTO cliente(dni,nombre,telefono) VALUES ('12345678B', 'cliente2', '112') ON CONFLICT DO NOTHING;
INSERT INTO cliente(dni,nombre,telefono) VALUES ('12345678C', 'cliente3', '113') ON CONFLICT DO NOTHING;
INSERT INTO cliente(dni,nombre,telefono) VALUES ('12345678D', 'cliente4', '114') ON CONFLICT DO NOTHING;

INSERT INTO coche(marca, modelo, color) VALUES ('marca1', 'modelo1', 'color2');
INSERT INTO coche(marca, modelo, color) VALUES ('marca2', 'modelo1', 'color1');
INSERT INTO coche(marca, modelo, color) VALUES ('marca1', 'modelo2', 'color1');


INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678A', '1', '1/1/2000', '1/1/2000', '2', 'pagado') ON CONFLICT DO NOTHING;
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678B', '1', '1/1/2000', '1/1/2000', '2', 'pagado') ON CONFLICT DO NOTHING;
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678C', '2', '1/1/2000', '1/1/2000', '2', 'pagado') ON CONFLICT DO NOTHING;
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678D', '2', '1/1/2000', '1/1/2000', '2', 'pagado') ON CONFLICT DO NOTHING;

INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678A', '2', '1/2/2000', '1/2/2000', '2', 'no_pagado') ON CONFLICT DO NOTHING;
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678A', '3', '1/2/2000', '1/2/2000', '2', 'no_pagado') ON CONFLICT DO NOTHING;
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678B', '1', '1/2/2000', '1/2/2000', '2', 'no_pagado') ON CONFLICT DO NOTHING;
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678B', '2', '1/2/2000', '1/2/2000', '2', 'no_pagado') ON CONFLICT DO NOTHING;
INSERT INTO alquiler(dni,id_coche,fecha_inicio, fecha_fin, precio, estado) VALUES ('12345678C', '1', '1/2/2000', '1/2/2000', '2', 'no_pagado') ON CONFLICT DO NOTHING;

INSERT INTO proveedor(cif, nombre, ubicacion, telefono, correo) VALUES ('12345678A', 'autoslocos', 'pulianas', 660816891, 'example@example.com')
