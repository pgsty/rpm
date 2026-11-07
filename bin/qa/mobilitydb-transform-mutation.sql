\set ON_ERROR_STOP on
\pset format unaligned
-- Use a disposable database with only PostGIS and MobilityDB installed.
SET timezone = 'UTC';
CREATE EXTENSION postgis;
CREATE EXTENSION mobilitydb;
CREATE TABLE transform_input(id integer PRIMARY KEY, trip tgeompoint);
INSERT INTO transform_input VALUES (1,
    'SRID=3857;[Point(0 0)@2026-01-01, Point(111319.49079327357 0)@2026-01-02]'::tgeompoint);
SELECT 'before', srid(trip), length(trip), asText(trip) FROM transform_input;
BEGIN READ ONLY;
SELECT 'transformed', asText(transform(trip,4326)) FROM transform_input;
COMMIT;
SELECT 'after', srid(trip), length(trip), asText(trip) FROM transform_input;
SELECT 'libraries', current_setting('shared_preload_libraries');
SELECT extname,extversion FROM pg_extension ORDER BY extname;
-- A read-only SELECT must leave the stored source trajectory intact.
DO $$BEGIN
    IF NOT (SELECT abs(length(trip)-111319.49079327357)<1e-6 FROM transform_input WHERE id=1) THEN
        RAISE EXCEPTION 'transform() mutated the stored input trajectory during a read-only transaction';
    END IF;
END$$;
