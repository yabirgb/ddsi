--DROP FUNCTION alquilerValidoInsercion() CASCADE;
--DROP FUNCTION alquilerValidoModificacion() CASCADE;

CREATE OR REPLACE FUNCTION alquilerValidoInsercion() RETURNS trigger AS $$
DECLARE name   character varying(255);
BEGIN
	SELECT * INTO name FROM alquiler WHERE id_coche=NEW.id_coche AND ((NEW.fecha_inicio<=fecha_inicio and fecha_inicio<=NEW.fecha_fin) or 
								 (fecha_inicio<NEW.fecha_inicio and NEW.fecha_inicio<=fecha_fin));
	IF name IS NOT NULL THEN
		RAISE EXCEPTION '------------El periodo de alquiler se solapa con otros. No se puede insertar------------';
	END IF;
	RETURN NEW;	
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION alquilerValidoModificacion() RETURNS trigger AS $$
DECLARE name   character varying(255);
BEGIN
	IF NEW.id_coche = OLD.id_coche THEN
		SELECT * INTO name FROM alquiler WHERE id_coche=OLD.id_coche AND ((dni!=OLD.dni or fecha_inicio!=OLD.fecha_inicio) AND 
												((NEW.fecha_inicio<=fecha_inicio and fecha_inicio<=NEW.fecha_fin) OR 
												(fecha_inicio<NEW.fecha_inicio and NEW.fecha_inicio<=fecha_fin)));
	ELSE
		SELECT * INTO name FROM alquiler WHERE id_coche=NEW.id_coche AND ((NEW.fecha_inicio<=fecha_inicio and fecha_inicio<=NEW.fecha_fin) 
								 				or (fecha_inicio<NEW.fecha_inicio and NEW.fecha_inicio<=fecha_fin));
	END IF;
	IF name IS NOT NULL THEN
		RAISE EXCEPTION '------------El periodo de alquiler se solapa con otros. No se puede modificar------------';
	END IF;
	RETURN NEW;	
END;
$$ LANGUAGE plpgsql;


DROP TRIGGER IF EXISTS alquilerInsercion
  ON alquiler;

DROP TRIGGER IF EXISTS alquilerModificacion
  ON alquiler;

CREATE TRIGGER alquilerInsercion BEFORE INSERT ON alquiler FOR EACH ROW EXECUTE PROCEDURE alquilerValidoInsercion();
CREATE TRIGGER alquilerModificacion BEFORE UPDATE ON alquiler FOR EACH ROW EXECUTE PROCEDURE alquilerValidoModificacion();
