-- Run with psql -X -v ON_ERROR_STOP=1 in a disposable, empty database.
-- Both installations are rolled back; no existing extension is modified.
\set ON_ERROR_STOP on

BEGIN;
CREATE EXTENSION uint128;

DO $$
DECLARE
    op record;
    actual text;
    actual_type oid;
    expected text;
    checked integer := 0;
BEGIN
    IF (SELECT extversion FROM pg_extension WHERE extname = 'uint128') <> '1.2.0' THEN
        RAISE EXCEPTION 'unexpected uint128 extension version';
    END IF;

    IF EXISTS (
        SELECT 1
        FROM pg_operator o
        JOIN pg_depend d ON d.classid = 'pg_operator'::regclass AND d.objid = o.oid
        JOIN pg_extension e ON d.refclassid = 'pg_extension'::regclass AND d.refobjid = e.oid
        JOIN pg_operator c ON c.oid = o.oprcom
        WHERE e.extname = 'uint128' AND d.deptype = 'e'
          AND (o.oprresult <> c.oprresult OR c.oprcom <> o.oid
               OR o.oprleft <> c.oprright OR o.oprright <> c.oprleft)
    ) THEN
        RAISE EXCEPTION 'inconsistent uint128 commutator pair';
    END IF;

    FOR op IN
        SELECT o.*, format_type(o.oprleft, NULL) AS left_type,
               format_type(o.oprright, NULL) AS right_type
        FROM pg_operator o
        JOIN pg_depend d ON d.classid = 'pg_operator'::regclass AND d.objid = o.oid
        JOIN pg_extension e ON d.refclassid = 'pg_extension'::regclass AND d.refobjid = e.oid
        WHERE e.extname = 'uint128' AND d.deptype = 'e' AND o.oprname IN ('+', '-')
    LOOP
        IF (op.oprname = '-' OR op.oprleft <> op.oprright) AND op.oprcom <> 0 THEN
            RAISE EXCEPTION 'invalid arithmetic commutator: %', op.oid::regoperator;
        END IF;
        IF op.oprname = '+' AND op.oprleft = op.oprright AND op.oprcom <> op.oid THEN
            RAISE EXCEPTION 'missing same-type addition commutator: %', op.oid::regoperator;
        END IF;
        EXECUTE format(
            'SELECT (12::%s %s 3::%s)::text, pg_typeof(12::%s %s 3::%s)::oid',
            op.left_type, op.oprname, op.right_type,
            op.left_type, op.oprname, op.right_type
        ) INTO actual, actual_type;
        expected := CASE op.oprname WHEN '+' THEN '15' ELSE '9' END;
        IF actual IS DISTINCT FROM expected OR actual_type <> op.oprleft THEN
            RAISE EXCEPTION 'arithmetic changed for %: value %, type %',
                op.oid::regoperator, actual, actual_type::regtype;
        END IF;
        checked := checked + 1;
    END LOOP;
    IF checked <> 182 THEN
        RAISE EXCEPTION 'expected 182 arithmetic operators, checked %', checked;
    END IF;

    BEGIN
        PERFORM '65535'::uint2 + '1'::int16;
        RAISE EXCEPTION 'uint2 overflow was not detected';
    EXCEPTION WHEN numeric_value_out_of_range THEN
        NULL;
    END;
    IF ('1'::int16 + '65535'::uint2)::text <> '65536' THEN
        RAISE EXCEPTION 'reverse addition no longer preserves the wider left type';
    END IF;
END
$$;

-- Check every comparison against PostgreSQL numeric, including signed/unsigned
-- extrema. Inspect links independently of the expression optimizer.
DO $$
DECLARE
    op record;
    bounds jsonb := '{"int1":[-128,127],"int2":[-32768,32767],"int4":[-2147483648,2147483647],"int8":[-9223372036854775808,9223372036854775807],"int16":[-170141183460469231731687303715884105728,170141183460469231731687303715884105727],"uint1":[0,255],"uint2":[0,65535],"uint4":[0,4294967295],"uint8":[0,18446744073709551615],"uint16":[0,340282366920938463463374607431768211455]}';
    x numeric;
    y numeric;
    actual boolean;
    expected boolean;
    pairs integer := 0;
    cases integer := 0;
BEGIN
    IF EXISTS (SELECT 1 FROM pg_operator WHERE oprnamespace = 'public'::regnamespace AND oprcode = 0) THEN
        RAISE EXCEPTION 'undefined operator shell remains';
    END IF;
    FOR op IN
        SELECT o.*, l.typname AS lt, r.typname AS rt,
               c.oprname AS comm, n.oprname AS neg,
               n.oprnegate AS backneg, n.oprleft AS nl, n.oprright AS nr, n.oprresult AS resultneg
        FROM pg_operator o
        JOIN pg_depend d ON d.classid = 'pg_operator'::regclass AND d.objid = o.oid AND d.deptype = 'e'
        JOIN pg_extension e ON d.refclassid = 'pg_extension'::regclass AND d.refobjid = e.oid
        JOIN pg_type l ON l.oid = o.oprleft JOIN pg_type r ON r.oid = o.oprright
        LEFT JOIN pg_operator c ON c.oid = o.oprcom
        LEFT JOIN pg_operator n ON n.oid = o.oprnegate
        WHERE e.extname = 'uint128' AND o.oprname IN ('=', '<>', '<', '<=', '>', '>=')
    LOOP
        IF op.comm IS DISTINCT FROM (CASE op.oprname WHEN '<' THEN '>' WHEN '>' THEN '<' WHEN '<=' THEN '>=' WHEN '>=' THEN '<=' ELSE op.oprname END)
           OR op.neg IS DISTINCT FROM (CASE op.oprname WHEN '<' THEN '>=' WHEN '>' THEN '<=' WHEN '<=' THEN '>' WHEN '>=' THEN '<' WHEN '=' THEN '<>' ELSE '=' END)
           OR op.backneg IS DISTINCT FROM op.oid OR op.nl <> op.oprleft OR op.nr <> op.oprright
           OR op.resultneg <> 'boolean'::regtype THEN
            RAISE EXCEPTION 'invalid comparison links: %', op.oid::regoperator;
        END IF;
        FOR x IN SELECT DISTINCT unnest(ARRAY[(bounds->op.lt->>0)::numeric, 0, 1, (bounds->op.lt->>1)::numeric]) LOOP
            FOR y IN SELECT DISTINCT unnest(ARRAY[(bounds->op.rt->>0)::numeric, 0, 1, (bounds->op.rt->>1)::numeric]) LOOP
                EXECUTE format('SELECT %L::%I %s %L::%I', x, op.lt, op.oprname, y, op.rt) INTO actual;
                expected := CASE op.oprname WHEN '=' THEN x=y WHEN '<>' THEN x<>y WHEN '<' THEN x<y WHEN '<=' THEN x<=y WHEN '>' THEN x>y ELSE x>=y END;
                IF actual IS DISTINCT FROM expected THEN
                    RAISE EXCEPTION 'comparison %: % versus %, got %, expected %', op.oid::regoperator, x, y, actual, expected;
                END IF;
                cases := cases + 1;
            END LOOP;
        END LOOP;
        pairs := pairs + 1;
    END LOOP;
    IF pairs <> 546 THEN RAISE EXCEPTION 'expected 546 comparison operators, got %', pairs; END IF;
    RAISE NOTICE 'comparison operators: %, numeric-oracle boundary cases: %', pairs, cases;
END
$$;

-- Cross-type predicates may use an index filter instead of an index condition.
-- These cases check results; the same-type tests below assert the actual plan.
CREATE TEMP TABLE uint128_index_probe (v uint2);
INSERT INTO uint128_index_probe VALUES (1), (2), (3);
CREATE INDEX ON uint128_index_probe (v);
SET LOCAL enable_seqscan = off;
DO $$
DECLARE
    actual text;
    lhs_type text;
    comparison text;
    expected text;
BEGIN
    FOREACH lhs_type IN ARRAY ARRAY['uint1', 'uint2', 'int16'] LOOP
        FOREACH comparison IN ARRAY ARRAY['<', '<=', '>', '>='] LOOP
            expected := CASE comparison
                WHEN '<' THEN '3' WHEN '<=' THEN '2,3'
                WHEN '>' THEN '1' WHEN '>=' THEN '1,2'
            END;
            EXECUTE format(
                'SELECT string_agg(v::text, '','' ORDER BY v) FROM uint128_index_probe WHERE ''2''::%s %s v',
                lhs_type, comparison
            ) INTO actual;
            IF actual IS DISTINCT FROM expected THEN
                RAISE EXCEPTION 'reversed comparison % % uint2 returned %, expected %',
                    lhs_type, comparison, actual, expected;
            END IF;
        END LOOP;
    END LOOP;
END
$$;

DO $$
DECLARE
    typ text;
    comparison text;
    query text;
    plan json;
    seq_result text;
    index_result text;
    expected text;
    cases integer := 0;
BEGIN
    FOREACH typ IN ARRAY ARRAY['int1', 'int16', 'uint1', 'uint2', 'uint4', 'uint8', 'uint16'] LOOP
        EXECUTE format('CREATE TEMP TABLE index_probe_%s (v %I)', typ, typ);
        EXECUTE format('INSERT INTO index_probe_%s VALUES (1), (2), (3)', typ);
        EXECUTE format('CREATE INDEX ON index_probe_%s (v)', typ);
        FOREACH comparison IN ARRAY ARRAY['<', '<=', '>', '>='] LOOP
            query := format('SELECT v FROM index_probe_%s WHERE ''2''::%I %s v', typ, typ, comparison);
            expected := CASE comparison WHEN '<' THEN '3' WHEN '<=' THEN '2,3' WHEN '>' THEN '1' ELSE '1,2' END;
            PERFORM set_config('enable_seqscan','on',true);
            PERFORM set_config('enable_indexscan','off',true);
            PERFORM set_config('enable_indexonlyscan','off',true);
            PERFORM set_config('enable_bitmapscan','off',true);
            EXECUTE 'EXPLAIN (FORMAT JSON) ' || query INTO plan;
            IF plan->0->'Plan'->>'Node Type' <> 'Seq Scan' THEN RAISE EXCEPTION 'expected sequential plan: %', plan; END IF;
            EXECUTE 'SELECT string_agg(v::text, '','' ORDER BY v) FROM (' || query || ') s' INTO seq_result;
            PERFORM set_config('enable_seqscan','off',true);
            PERFORM set_config('enable_indexscan','on',true);
            PERFORM set_config('enable_indexonlyscan','on',true);
            EXECUTE 'EXPLAIN (FORMAT JSON) ' || query INTO plan;
            IF plan->0->'Plan'->>'Node Type' NOT IN ('Index Scan', 'Index Only Scan')
               OR plan->0->'Plan'->>'Index Cond' IS NULL THEN
                RAISE EXCEPTION 'missing index condition for %: %', query, plan;
            END IF;
            EXECUTE 'SELECT string_agg(v::text, '','' ORDER BY v) FROM (' || query || ') s' INTO index_result;
            IF seq_result IS DISTINCT FROM expected OR index_result IS DISTINCT FROM expected THEN
                RAISE EXCEPTION 'scan mismatch for %: seq %, index %, expected %', query, seq_result, index_result, expected;
            END IF;
            RAISE NOTICE 'index comparison: % %; %', typ, comparison, plan->0->'Plan'->>'Index Cond';
            cases := cases + 1;
        END LOOP;
    END LOOP;
    IF cases <> 28 THEN RAISE EXCEPTION 'index case count %', cases; END IF;
END
$$;

SELECT extname, extversion FROM pg_extension WHERE extname = 'uint128';
ROLLBACK;

BEGIN;
CREATE SCHEMA uint128_qa;
CREATE EXTENSION uint128 WITH SCHEMA uint128_qa;
SET LOCAL search_path = uint128_qa, pg_catalog;
DO $$
BEGIN
    IF ('7'::uint2 + '9'::int16)::text <> '16'
       OR pg_typeof('7'::uint2 + '9'::int16) <> 'uint2'::regtype
       OR pg_typeof('9'::int16 + '7'::uint2) <> 'int16'::regtype THEN
        RAISE EXCEPTION 'custom-schema arithmetic failed';
    END IF;
END
$$;
ROLLBACK;
