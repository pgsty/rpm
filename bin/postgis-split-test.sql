-- Run after bin/postgis-test.sql in a disposable database.
-- TIGER is included only on PostgreSQL 16 and newer.
\set ON_ERROR_STOP on
CREATE EXTENSION address_standardizer;
CREATE EXTENSION address_standardizer_data_us;
DO $$
DECLARE parsed record; normalized record;
BEGIN
  SELECT * INTO parsed FROM parse_address('385 Landgrove Rd Landgrove VT 05148');
  IF parsed.num IS DISTINCT FROM '385' OR parsed.state IS DISTINCT FROM 'VT' OR parsed.zip IS DISTINCT FROM '05148' THEN
    RAISE EXCEPTION 'address parser mismatch: %', parsed;
  END IF;
  SELECT * INTO normalized FROM standardize_address('us_lex','us_gaz','us_rules','1 Devonshire Place, Boston, MA 02109');
  IF normalized.house_num IS DISTINCT FROM '1' OR normalized.name IS DISTINCT FROM 'DEVONSHIRE' OR normalized.postcode IS DISTINCT FROM '02109' THEN
    RAISE EXCEPTION 'US standardizer mismatch: %', normalized;
  END IF;
END $$;
SELECT current_setting('server_version_num')::int >= 160000 AS has_tiger \gset
\if :has_tiger
CREATE EXTENSION postgis_tiger_geocoder CASCADE;
SET search_path = public,tiger;
DO $$
DECLARE normalized record;
BEGIN
  SELECT * INTO normalized FROM normalize_address('1 Devonshire Place, Boston, MA 02109');
  IF normalized.address IS DISTINCT FROM 1 OR normalized.streetname IS DISTINCT FROM 'Devonshire' OR normalized.zip IS DISTINCT FROM '02109' THEN
    RAISE EXCEPTION 'TIGER normalize mismatch: %', normalized;
  END IF;
  IF position('CREATE SCHEMA IF NOT EXISTS tiger_data' in loader_generate_script(ARRAY['RI'],'sh'))=0 THEN
    RAISE EXCEPTION 'TIGER loader script missing data schema';
  END IF;
END $$;
\endif
SELECT extname,extversion FROM pg_extension ORDER BY extname;
SELECT 'PostGIS split extension smoke tests passed';
