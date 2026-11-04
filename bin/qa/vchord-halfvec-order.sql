-- Run in a disposable database with vchord preloaded.
-- vchord 1.2.0: two-row halfvec cosine ordering reproduction.
\set ON_ERROR_STOP on
CREATE EXTENSION IF NOT EXISTS vchord CASCADE;
CREATE TABLE cosine_order_probe(id int PRIMARY KEY,h halfvec(64));
INSERT INTO cosine_order_probe
SELECT i,ARRAY(SELECT (('x'||substr(md5((i*64+j)::text),1,8))::bit(32)::bigint/2147483648.0-1)::real FROM generate_series(1,64)j)::halfvec
FROM unnest(ARRAY[6661,231])i;
SELECT ARRAY(SELECT (('x'||substr(md5((7203*64+j)::text),1,8))::bit(32)::bigint/2147483648.0-1)::real FROM generate_series(1,64)j)::halfvec::text AS q \gset
CREATE INDEX cosine_order_rq ON cosine_order_probe USING vchordrq(h halfvec_cosine_ops);
SET enable_seqscan=off;
\echo RQ cosine: the distance for ID 6661 precedes the smaller distance for ID 231.
EXPLAIN(COSTS OFF) SELECT id,h <=> :'q'::halfvec d FROM cosine_order_probe ORDER BY h <=> :'q'::halfvec;
SELECT id,h <=> :'q'::halfvec d FROM cosine_order_probe ORDER BY h <=> :'q'::halfvec;
\echo Sequential reference.
SET enable_indexscan=off;
SET enable_seqscan=on;
SELECT id,h <=> :'q'::halfvec d FROM cosine_order_probe ORDER BY h <=> :'q'::halfvec;
SET enable_indexscan=on;
SET enable_seqscan=off;
DROP INDEX cosine_order_rq;
CREATE INDEX cosine_order_rq ON cosine_order_probe USING vchordrq(h halfvec_cosine_ops) WITH(options='rerank_in_table=true');
\echo RQ with heap reranking.
SELECT id,h <=> :'q'::halfvec d FROM cosine_order_probe ORDER BY h <=> :'q'::halfvec;
\echo Explicit sorting of RQ candidates.
WITH candidate AS MATERIALIZED (SELECT id,h <=> :'q'::halfvec d FROM cosine_order_probe ORDER BY h <=> :'q'::halfvec LIMIT 100)
SELECT * FROM candidate ORDER BY d+0 LIMIT 20;
DROP INDEX cosine_order_rq;
CREATE INDEX cosine_order_g ON cosine_order_probe USING vchordg(h halfvec_cosine_ops);
\echo Graph index: this two-row sample is correctly ordered.
SELECT id,h <=> :'q'::halfvec d FROM cosine_order_probe ORDER BY h <=> :'q'::halfvec;
