CREATE OR REPLACE FUNCTION comprobarMatricula()
	RETURNS TRIGGER AS
$$
BEGIN
	IF NEW.matricula NOT SIMILAR TO '[0-9]{4}[A-Z]{3}' THEN
		RAISE EXCEPTION 'Formato incorrecto de matrícula';
	END IF;
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS matriculaCoche ON coche;

CREATE TRIGGER matriculaCoche
	BEFORE UPDATE ON coche
	FOR EACH ROW
	EXECUTE PROCEDURE comprobarMatricula();
