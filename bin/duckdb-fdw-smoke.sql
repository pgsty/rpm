\set ON_ERROR_STOP on
-- Run only in a disposable database/cluster. No pg_duckdb preload is allowed.
CREATE EXTENSION duckdb_fdw;
SELECT extname, extversion FROM pg_extension WHERE extname='duckdb_fdw';
SELECT duckdb_fdw_version(), duckdb_fdw_runtime_fingerprint();
DO $$ BEGIN
  IF (SELECT extversion FROM pg_extension WHERE extname='duckdb_fdw') <> '2.0.2' THEN
    RAISE EXCEPTION 'wrong FDW extension version';
  END IF;
  IF duckdb_fdw_version() <> 'v2.0.0' THEN
    RAISE EXCEPTION 'wrong embedded DuckDB version';
  END IF;
  IF duckdb_fdw_runtime_compatibility_status() <> 'no_peer_loaded' THEN
    RAISE EXCEPTION 'unexpected peer runtime';
  END IF;
END $$;

CREATE SERVER fdw_test FOREIGN DATA WRAPPER duckdb_fdw
  OPTIONS (database '/tmp/pgsty_duckdb_fdw_smoke.db');
-- Deliberately omit user mappings: local files do not need credentials.
SELECT duckdb_execute('fdw_test', 'CREATE TABLE typed (id INTEGER, n INTEGER, d DECIMAL(18,3), ts TIMESTAMPTZ, a INTEGER[], s VARCHAR)');
SELECT duckdb_execute('fdw_test', $$INSERT INTO typed VALUES
  (1, NULL, 12345.678, TIMESTAMPTZ '2026-10-24 12:34:56+08', [1,2,3], '[not an array]'),
  (2, 7, -0.125, TIMESTAMPTZ '2001-01-01 00:00:00+00', [7], '[Description: No-op correction applied to line 42]')$$);
CREATE FOREIGN TABLE typed (id integer, n integer, d numeric(18,3), ts timestamptz, a integer[], s text)
  SERVER fdw_test OPTIONS (table 'typed');
TABLE typed;
DO $$ DECLARE r record; BEGIN
  SELECT * INTO STRICT r FROM typed WHERE id=1;
  IF r.n IS NOT NULL OR r.d IS DISTINCT FROM 12345.678::numeric
      OR r.ts IS DISTINCT FROM '2026-10-24 04:34:56+00'::timestamptz
      OR r.a IS DISTINCT FROM ARRAY[1,2,3] OR r.s IS DISTINCT FROM '[not an array]' THEN
    RAISE EXCEPTION 'typed scan failed';
  END IF;
  IF (SELECT s FROM typed WHERE id=2) <> '[Description: No-op correction applied to line 42]' THEN
    RAISE EXCEPTION 'ordinary text was rewritten as an array';
  END IF;
END $$;

BEGIN;
INSERT INTO typed VALUES (3, NULL, 42.125, '2026-10-24 01:02:03+00', ARRAY[4,5], '[ordinary text]');
DO $$ DECLARE r record; BEGIN
  SELECT * INTO STRICT r FROM typed WHERE id=3;
  IF r.n IS NOT NULL OR r.d IS DISTINCT FROM 42.125::numeric
      OR r.ts IS DISTINCT FROM '2026-10-24 01:02:03+00'::timestamptz
      OR r.a IS DISTINCT FROM ARRAY[4,5] OR r.s IS DISTINCT FROM '[ordinary text]' THEN
    RAISE EXCEPTION 'typed INSERT round trip failed';
  END IF;
END $$;
ROLLBACK;
DO $$ BEGIN
  IF (SELECT count(*) FROM typed) <> 2 THEN
    RAISE EXCEPTION 'typed INSERT rollback failed';
  END IF;
END $$;

SELECT duckdb_execute('fdw_test', 'CREATE TABLE writes (id INTEGER, s VARCHAR)');
CREATE FOREIGN TABLE writes (id integer, s text) SERVER fdw_test OPTIONS (table 'writes');
INSERT INTO writes VALUES (1, 'inserted'), (2, NULL);
BEGIN;
INSERT INTO writes VALUES (3, 'must roll back');
ROLLBACK;
DO $$ BEGIN
  IF (SELECT count(*) FROM writes) <> 2
     OR NOT EXISTS (SELECT FROM writes WHERE id=1 AND s='inserted')
     OR NOT EXISTS (SELECT FROM writes WHERE id=2 AND s IS NULL) THEN
    RAISE EXCEPTION 'INSERT/NULL/ROLLBACK verification failed';
  END IF;
END $$;

SELECT duckdb_execute('fdw_test', $$COPY typed TO '/tmp/pgsty_duckdb_fdw.parquet' (FORMAT PARQUET)$$);
CREATE FOREIGN TABLE parquet_test (id integer, n integer, d numeric(18,3), ts timestamptz, a integer[], s text)
  SERVER fdw_test OPTIONS (table '/tmp/pgsty_duckdb_fdw.parquet');
DO $$ BEGIN
  IF (SELECT count(*) FROM parquet_test) <> 2
     OR (SELECT sum(d) FROM parquet_test) <> 12345.553 THEN
    RAISE EXCEPTION 'Parquet read failed';
  END IF;
END $$;
SELECT 'independent FDW smoke passed' AS result;
