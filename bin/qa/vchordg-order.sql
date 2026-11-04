-- Run in a disposable database with vchord preloaded.
-- vchord 1.2.0: vector L2 ordering with the default graph search settings.
\set ON_ERROR_STOP on
CREATE EXTENSION IF NOT EXISTS vchord CASCADE;
SET max_parallel_workers_per_gather = 0;
CREATE TABLE graph_order_probe(id int PRIMARY KEY, tenant int, v vector(64));
INSERT INTO graph_order_probe
SELECT i, i % 10, ARRAY(
    SELECT (('x' || substr(md5((i * 64 + j)::text), 1, 8))::bit(32)::bigint
        / 2147483648.0 - 1)::real
    FROM generate_series(1, 64) j
)::vector
FROM generate_series(1, 8000) i;
SELECT v::text AS q FROM graph_order_probe WHERE id = 3955 \gset
CREATE INDEX graph_order_g ON graph_order_probe USING vchordg(v vector_l2_ops);
SET vchordg.ef_search = 64;
SET vchordg.beam_search = 1;
SET vchordg.max_scan_tuples = -1;
SET enable_seqscan = off;
\echo Default graph search: inspect the order of IDs 7126 and 2637.
EXPLAIN (COSTS OFF)
SELECT id, v <-> :'q'::vector d FROM graph_order_probe ORDER BY v <-> :'q'::vector LIMIT 20;
SELECT id, v <-> :'q'::vector d FROM graph_order_probe ORDER BY v <-> :'q'::vector LIMIT 20;
\echo Sequential reference.
SET enable_indexscan = off;
SET enable_seqscan = on;
SELECT id, v <-> :'q'::vector d FROM graph_order_probe ORDER BY v <-> :'q'::vector LIMIT 20;
SET enable_indexscan = on;
SET enable_seqscan = off;
\echo Explicit sorting of ANN candidates.
WITH candidates AS MATERIALIZED (
    SELECT id, v <-> :'q'::vector d
    FROM graph_order_probe ORDER BY v <-> :'q'::vector LIMIT 100
)
SELECT * FROM candidates ORDER BY d + 0 LIMIT 20;
\echo Larger search settings on the same index.
SET vchordg.ef_search = 65535;
SET vchordg.beam_search = 65535;
SELECT id, v <-> :'q'::vector d FROM graph_order_probe ORDER BY v <-> :'q'::vector LIMIT 20;
