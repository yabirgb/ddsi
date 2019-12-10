DROP FUNCTION funcion1() CASCADE;
CREATE OR REPLACE FUNCTION funcion1() RETURNS trigger AS $$
DECLARE name   character varying(255);
BEGIN
	SELECT * INTO name FROM alquiler where (NEW.fecha_inicio<=fecha_inicio and fecha_inicio<=NEW.fecha_fin) or 
								 (fecha_inicio<NEW.fecha_inicio and NEW.fecha_inicio<=fecha_fin);
	 IF name IS NOT NULL THEN
     	RAISE EXCEPTION '------------El periodo de alquiler se solapa con otros------------';
     END IF;
	RETURN NEW;	
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER alquilerValido BEFORE INSERT ON alquiler FOR EACH ROW EXECUTE PROCEDURE funcion1();

