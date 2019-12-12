CREATE OR REPLACE FUNCTION comprobar_fecha() RETURNS TRIGGER AS $$
   BEGIN
		IF NEW.fecha_entrega < now()::date THEN
		   RAISE EXCEPTION 'Fecha de entrega anterior a la fecha actual' USING ERRCODE='22000';	
		END IF;
		RETURN NEW;
   END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER comprobar_fecha_entrega BEFORE INSERT OR UPDATE ON solicitud
FOR EACH ROW EXECUTE PROCEDURE comprobar_fecha()
