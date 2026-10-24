\set ON_ERROR_STOP on
-- Prerequisites: smoke.sql completed; official v2.0.0 httpfs at the path below;
-- an HTTP server serves /tmp on loopback port 18080, in the disposable container.
BEGIN;
SELECT duckdb_execute('fdw_test', $$INSTALL '/tmp/httpfs.duckdb_extension'; LOAD httpfs;$$);
SELECT duckdb_execute('fdw_test', $$CREATE TABLE http_result AS SELECT id, d, s FROM read_parquet('http://127.0.0.1:18080/pgsty_duckdb_fdw.parquet')$$);
SELECT duckdb_execute('fdw_test', $$CREATE TABLE plugin_state AS SELECT extension_name, loaded, installed, extension_version FROM duckdb_extensions() WHERE extension_name='httpfs'$$);
CREATE FOREIGN TABLE http_result (id integer, d numeric(18,3), s text)
  SERVER fdw_test OPTIONS (table 'http_result');
CREATE FOREIGN TABLE plugin_state (extension_name text, loaded boolean, installed boolean, extension_version text)
  SERVER fdw_test OPTIONS (table 'plugin_state');
TABLE plugin_state;
TABLE http_result;
-- Keep actual ELF paths from this same backend while the plugin is loaded.
SELECT line AS loaded_duckdb_module
  FROM regexp_split_to_table(pg_read_file('/proc/self/maps', 0, 1048576), E'\n') AS maps(line)
  WHERE line LIKE '%duckdb_fdw.so%' OR line LIKE '%httpfs.duckdb_extension%';
DO $$ BEGIN
  IF NOT EXISTS (SELECT FROM plugin_state WHERE extension_name='httpfs' AND loaded AND installed)
     OR (SELECT count(*) FROM http_result) <> 2
     OR (SELECT sum(d) FROM http_result) <> 12345.553 THEN
    RAISE EXCEPTION 'official httpfs load/HTTP Parquet read failed';
  END IF;
END $$;
COMMIT;
SELECT 'official httpfs plugin passed' AS result;
