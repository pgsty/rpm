\set ON_ERROR_STOP on
\pset format unaligned
\pset tuples_only on
-- Regression for upstream 3f9ee86639f4e494172d843fa13ce8ffd151498d.
-- Run in a disposable database; no pre-existing mobility_input_qa schema.
SET timezone = 'UTC';
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS mobilitydb;
CREATE SCHEMA mobility_input_qa;
CREATE TABLE mobility_input_qa.cases (
    id integer GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    label text UNIQUE NOT NULL,
    typename text NOT NULL,
    input text NOT NULL,
    expression text NOT NULL,
    expected text NOT NULL
);

INSERT INTO mobility_input_qa.cases(label,typename,input,expression,expected)
SELECT 'transform.'||label, 'tgeompoint', input, 'transform(v,4326)',
    'srid(result)=4326 AND ST_Distance(startValue(result),ST_SetSRID(ST_Point(1,0),4326))<1e-10'
FROM (VALUES
    ('instant','SRID=3857;Point(111319.49079327357 0)@2026-01-01'),
    ('sequence','SRID=3857;[Point(111319.49079327357 0)@2026-01-01,Point(222638.98158654714 0)@2026-01-02]'),
    ('discrete','SRID=3857;{Point(111319.49079327357 0)@2026-01-01,Point(222638.98158654714 0)@2026-01-02}'),
    ('sequence_set','SRID=3857;{[Point(111319.49079327357 0)@2026-01-01,Point(222638.98158654714 0)@2026-01-02],[Point(333958.4723798207 0)@2026-01-03]}'),
    ('3d','SRID=3857;[Point(111319.49079327357 0 3)@2026-01-01,Point(222638.98158654714 0 6)@2026-01-02]')
) samples(label,input);

INSERT INTO mobility_input_qa.cases(label,typename,input,expression,expected) VALUES
('transform.geomset','geomset','SRID=3857;{"Point(111319.49079327357 0)","Point(222638.98158654714 0)"}',
 'transform(v,4326)', 'srid(result)=4326 AND (SELECT array_agg(round(ST_X(g)::numeric,8) ORDER BY ST_X(g)) FROM unnest(getValues(result)) g)=ARRAY[1,2]::numeric[]'),
('transform.geogset','geogset','SRID=4326;{"Point(1 1)","Point(2 2)"}',
 'transform(v,4269)', 'srid(result)=4269 AND (SELECT array_agg(round(ST_X(g::geometry)::numeric,6) ORDER BY ST_X(g::geometry)) FROM unnest(getValues(result)) g)=ARRAY[1,2]::numeric[]'),
('transform.geography','tgeogpoint','SRID=4326;[Point(1 1)@2026-01-01,Point(2 2)@2026-01-02]',
 'transform(v,4269)', 'srid(result)=4269 AND abs(ST_X(startValue(result)::geometry)-1)<1e-6'),
('transform.line','tgeometry','SRID=3857;[Linestring(0 0,111319.49079327357 0)@2026-01-01,Linestring(0 0,222638.98158654714 0)@2026-01-02]',
 'transform(v,4326)', 'srid(result)=4326 AND abs(ST_Length(startValue(result))-1)<1e-10'),
('pipeline.geomset','geomset','SRID=3857;{"Point(1 1)","Point(2 2)"}',
 $$transformPipeline(v,'+proj=pipeline +step +proj=affine +xoff=10 +yoff=20',3857)$$,
 $$result='SRID=3857;{"Point(11 21)","Point(12 22)"}'::geomset$$),
('transform.same_srid','tgeompoint','SRID=3857;[Point(1 1)@2026-01-01,Point(2 2)@2026-01-02]',
 'transform(v,3857)', 'result=v');

INSERT INTO mobility_input_qa.cases(label,typename,input,expression,expected)
SELECT operation||'.'||subtype,'tgeompoint',input,expression,
    'ST_Equals(startValue(result),'||expected_point||')'
FROM (VALUES
    ('instant','SRID=3857;Point(1 1)@2026-01-01'),
    ('sequence','SRID=3857;[Point(1 1)@2026-01-01,Point(2 2)@2026-01-02]'),
    ('sequence_set','SRID=3857;{[Point(1 1)@2026-01-01,Point(2 2)@2026-01-02],[Point(3 3)@2026-01-03]}')
) samples(subtype,input)
CROSS JOIN (VALUES
    ('affine','affine(v,1,0,0,0,1,0,0,0,1,10,20,0)','ST_SetSRID(ST_Point(11,21),3857)'),
    ('scale',$$scale(v,'POINT(2 2)'::geometry)$$,'ST_SetSRID(ST_Point(2,2),3857)'),
    ('scale_origin',$$scale(v,'POINT(2 2)'::geometry,'POINT(1 1)'::geometry)$$,'ST_SetSRID(ST_Point(1,1),3857)'),
    ('pipeline',$$transformPipeline(v,'+proj=pipeline +step +proj=affine +xoff=10 +yoff=20',3857)$$,'ST_SetSRID(ST_Point(11,21),3857)')
) operations(operation,expression,expected_point);

INSERT INTO mobility_input_qa.cases(label,typename,input,expression,expected)
SELECT operation||'.line','tgeometry',
    'SRID=3857;[Linestring(1 1,2 2)@2026-01-01,Linestring(1 1,3 3)@2026-01-02]',
    expression,'ST_Equals(startValue(result),'||expected_geom||')'
FROM (VALUES
    ('affine','affine(v,1,0,0,0,1,0,0,0,1,10,20,0)', $$ST_GeomFromText('LINESTRING(11 21,12 22)',3857)$$),
    ('scale', $$scale(v,'POINT(2 2)'::geometry)$$, $$ST_GeomFromText('LINESTRING(2 2,4 4)',3857)$$),
    ('scale_origin', $$scale(v,'POINT(2 2)'::geometry,'POINT(1 1)'::geometry)$$, $$ST_GeomFromText('LINESTRING(1 1,3 3)',3857)$$)
) operations(operation,expression,expected_geom);

-- Persist the original representation in an independent table before executing
-- any mutating library path. Check the entire value, not only its bounding box.
CREATE TABLE mobility_input_qa.snapshots(id integer PRIMARY KEY, value text NOT NULL);
DO $$DECLARE c record;
BEGIN
    FOR c IN SELECT * FROM mobility_input_qa.cases ORDER BY id LOOP
        EXECUTE format('CREATE TABLE mobility_input_qa.input_%s(v %s)',c.id,c.typename);
        EXECUTE format('INSERT INTO mobility_input_qa.input_%s VALUES (%L::%s)',c.id,c.input,c.typename);
        EXECUTE format('INSERT INTO mobility_input_qa.snapshots SELECT %s,v::text FROM mobility_input_qa.input_%s',c.id,c.id);
    END LOOP;
END$$;
CREATE FUNCTION mobility_input_qa.check_case(case_id integer) RETURNS text LANGUAGE plpgsql AS $$
DECLARE c mobility_input_qa.cases; good boolean; before_value text; after_value text;
BEGIN
    SELECT * INTO STRICT c FROM mobility_input_qa.cases WHERE id=case_id;
    SELECT value INTO STRICT before_value FROM mobility_input_qa.snapshots WHERE id=case_id;
    -- MATERIALIZED guarantees exactly one transform evaluation per row.
    EXECUTE format('WITH result_row AS MATERIALIZED (SELECT v,%s AS result FROM mobility_input_qa.input_%s) SELECT %s FROM result_row',
        c.expression,c.id,c.expected) INTO good;
    IF good IS DISTINCT FROM true THEN RAISE EXCEPTION '% returned incorrect coordinates',c.label; END IF;
    EXECUTE format('SELECT v::text FROM mobility_input_qa.input_%s',c.id) INTO after_value;
    IF after_value IS DISTINCT FROM before_value THEN RAISE EXCEPTION '% changed the stored input',c.label; END IF;
    RETURN c.label||': PASS';
END$$;
BEGIN READ ONLY;
SELECT mobility_input_qa.check_case(id) FROM mobility_input_qa.cases ORDER BY id;
COMMIT;
-- The runner repeats this function after a restart to check persisted input.
CREATE FUNCTION mobility_input_qa.check_stored() RETURNS integer LANGUAGE plpgsql SET timezone='UTC' AS $$
DECLARE c record; actual text; checked integer:=0;
BEGIN
    FOR c IN SELECT * FROM mobility_input_qa.snapshots ORDER BY id LOOP
        EXECUTE format('SELECT v::text FROM mobility_input_qa.input_%s',c.id) INTO actual;
        IF actual IS DISTINCT FROM c.value THEN RAISE EXCEPTION 'stored input % changed',c.id; END IF;
        checked:=checked+1;
    END LOOP;
    RETURN checked;
END$$;
SELECT 'preserved cases',mobility_input_qa.check_stored();
