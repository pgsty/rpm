\set ON_ERROR_STOP on
\pset format unaligned
\pset tuples_only on
-- Run after postgis37-dependents.sql in a disposable database.
SET statement_timeout = '60s';
SET client_min_messages = warning;
SET timezone = 'UTC';
CREATE SCHEMA qa;
CREATE TABLE qa.results (label text PRIMARY KEY, ok boolean NOT NULL, detail text);
CREATE FUNCTION qa.check_sql(label text, statement text) RETURNS void LANGUAGE plpgsql AS $$
DECLARE result boolean;
BEGIN
    EXECUTE statement INTO result;
    INSERT INTO qa.results VALUES (label, result IS TRUE, NULL);
EXCEPTION WHEN OTHERS THEN
    INSERT INTO qa.results VALUES (label, false, SQLSTATE || ': ' || SQLERRM);
END $$;
CREATE FUNCTION qa.plan(statement text) RETURNS jsonb LANGUAGE plpgsql AS $$
DECLARE result jsonb;
BEGIN
    EXECUTE 'EXPLAIN (ANALYZE, COSTS OFF, TIMING OFF, FORMAT JSON) ' || statement INTO result;
    RETURN result;
END $$;
CREATE TABLE qa.plans (label text PRIMARY KEY, plan jsonb NOT NULL);

SELECT qa.check_sql('postgis.version', $$SELECT postgis_lib_version() LIKE '3.7.%'$$);
SELECT qa.check_sql('postgis.proj_roundtrip', $$SELECT ST_Distance(
    ST_Transform(ST_Transform(ST_SetSRID(ST_Point(12.5, 48.1),4326),3857),4326),
    ST_SetSRID(ST_Point(12.5,48.1),4326)) < 1e-9$$);
SELECT qa.check_sql('postgis.geos_overlay', $$SELECT abs(ST_Area(ST_Intersection(
    ST_MakeEnvelope(0,0,2,2,3857), ST_MakeEnvelope(1,1,3,3,3857)))-1) < 1e-9$$);

CREATE TABLE qa.trips(id integer PRIMARY KEY, trip tgeompoint);
INSERT INTO qa.trips
SELECT i, format('SRID=3857;[Point(%s 0)@2026-01-01, Point(%s 10)@2026-01-02]',i,i)::tgeompoint
FROM generate_series(1,1000) i;
SELECT qa.check_sql('mobility.length', $$SELECT abs(length(trip)-10)<1e-9 FROM qa.trips WHERE id=1$$);
SELECT qa.check_sql('mobility.interpolation', $$SELECT ST_Equals(valueAtTimestamp(trip,'2026-01-01 12:00+00'), ST_SetSRID(ST_Point(1,5),3857)) FROM qa.trips WHERE id=1$$);
SELECT qa.check_sql('mobility.trajectory', $$SELECT ST_Equals(trajectory(trip),ST_GeomFromText('LINESTRING(1 0,1 10)',3857)) FROM qa.trips WHERE id=1$$);
SELECT qa.check_sql('mobility.temporal_restriction', $$SELECT numInstants(atTime(trip,'[2026-01-01 06:00+00,2026-01-01 18:00+00]'::tstzspan))=2 AND abs(length(atTime(trip,'[2026-01-01 06:00+00,2026-01-01 18:00+00]'::tstzspan))-5)<1e-9 FROM qa.trips WHERE id=1$$);
CREATE TABLE qa.transform_before AS SELECT id, asText(trip) AS value, srid(trip) AS srid, length(trip) AS length FROM qa.trips WHERE id=1;
SELECT qa.check_sql('mobility.proj_transform', $$SELECT ST_SRID(trajectory(transform(trip,4326)))=4326 AND ST_IsValid(trajectory(transform(trip,4326))) FROM qa.trips WHERE id=1$$);
SELECT qa.check_sql('mobility.transform_preserves_input', $$SELECT asText(trip)=b.value AND srid(trip)=b.srid AND length(trip)=b.length FROM qa.trips t JOIN qa.transform_before b USING(id)$$);
CREATE TABLE qa.transform_after AS SELECT id, asText(trip) AS value, srid(trip) AS srid, length(trip) AS length FROM qa.trips WHERE id=1;
SELECT qa.check_sql('mobility.datagen', $$SELECT bool_and(random_int(1,10) BETWEEN 1 AND 10) FROM generate_series(1,100)$$);
SELECT qa.check_sql('mobility.seqscan', $$SELECT count(*)=11 FROM qa.trips WHERE trip && ST_MakeEnvelope(20,0,30,10,3857)::stbox$$);
CREATE INDEX qa_trips_gist ON qa.trips USING gist(trip);
ANALYZE qa.trips;
SET enable_seqscan = off;
INSERT INTO qa.plans VALUES ('mobility.gist', qa.plan($$SELECT id FROM qa.trips WHERE trip && ST_MakeEnvelope(20,0,30,10,3857)::stbox$$));
SELECT qa.check_sql('mobility.gist_plan', $$SELECT plan::text LIKE '%qa_trips_gist%' FROM qa.plans WHERE label='mobility.gist'$$);
SELECT qa.check_sql('mobility.gist_results', $$SELECT array_agg(id ORDER BY id)=ARRAY(SELECT generate_series(20,30)) FROM qa.trips WHERE trip && ST_MakeEnvelope(20,0,30,10,3857)::stbox$$);
DROP INDEX qa.qa_trips_gist;
CREATE INDEX qa_trips_spgist ON qa.trips USING spgist(trip);
INSERT INTO qa.plans VALUES ('mobility.spgist', qa.plan($$SELECT id FROM qa.trips WHERE trip && ST_MakeEnvelope(20,0,30,10,3857)::stbox$$));
SELECT qa.check_sql('mobility.spgist_plan', $$SELECT plan::text LIKE '%qa_trips_spgist%' FROM qa.plans WHERE label='mobility.spgist'$$);
SELECT qa.check_sql('mobility.spgist_results', $$SELECT array_agg(id ORDER BY id)=ARRAY(SELECT generate_series(20,30)) FROM qa.trips WHERE trip && ST_MakeEnvelope(20,0,30,10,3857)::stbox$$);
RESET enable_seqscan;

-- Three linked drainage reaches and one square catchment.
INSERT INTO pghydro.pghft_drainage_area(dra_pk,dra_cd_pfafstetterbasin,dra_gm)
VALUES (1,'1',ST_Multi(ST_MakeEnvelope(0,0,100,100,3857)));
INSERT INTO pghydro.pghft_drainage_line(drn_pk,drn_drp_pk_sourcenode,drn_drp_pk_targetnode,drn_dra_pk,drn_gm)
SELECT i,i,i+1,1,ST_Multi(ST_MakeLine(ST_SetSRID(ST_Point((i-1)*10,0),3857),ST_SetSRID(ST_Point(i*10,0),3857)))
FROM generate_series(1,3) i;
SELECT qa.check_sql('pghydro.length_function', $$SELECT pghydro.pghfn_calculatedrainagelinelength(3857,1)='OK'$$);
SELECT qa.check_sql('pghydro.length_result', $$SELECT count(*)=3 AND bool_and(drn_gm_length=10) FROM pghydro.pghft_drainage_line$$);
SELECT qa.check_sql('pghydro.area_function', $$SELECT pghydro.pghfn_calculatedrainageareaarea(3857,1)='OK'$$);
SELECT qa.check_sql('pghydro.area_result', $$SELECT dra_gm_area=10000 FROM pghydro.pghft_drainage_area WHERE dra_pk=1$$);
SELECT qa.check_sql('pghydro.downstream', $$SELECT array_agg(x ORDER BY x)=ARRAY[2,3] FROM pghydro.pghfn_downstream_drainagelines(1) x$$);
SELECT qa.check_sql('pghydro.split_geometry', $$SELECT ST_NumGeometries(pgh_consistency.pghfn_splitdrainagelinemultipoint(ST_GeomFromText('LINESTRING(0 0,30 0)',3857), ST_GeomFromText('MULTIPOINT(10 0,20 0)',3857)))=3$$);
SELECT qa.check_sql('pghydro.valid_lines', $$SELECT pgh_consistency.pghfn_numdrainagelineisnotvalid()=0$$);
INSERT INTO pgh_raster.pghrt_elevation(rid,rast)
VALUES (1,ST_AddBand(ST_MakeEmptyRaster(10,10,0,10,1,-1,0,0,3857),'32BF'::text,123::double precision,-9999::double precision));
SELECT qa.check_sql('pghydro.raster_elevation', $$SELECT pgh_raster.pghfn_elevation_pixel_value(ST_SetSRID(ST_Point(0.5,9.5),3857))=123$$);
SELECT qa.check_sql('pghydro.raster_outside', $$SELECT pgh_raster.pghfn_elevation_pixel_value(ST_SetSRID(ST_Point(50,50),3857)) IS NULL$$);
SELECT qa.check_sql('pghydro.hgm_circularity', $$SELECT abs(circularity-12.57/16)<1e-9 FROM pgh_hgm.pghfn_dra_circularity(1,3857,3857)$$);
SELECT qa.check_sql('pghydro.output_default', $$SELECT pgh_output.pghfn_updateexporttables()='OK'$$);
SELECT qa.check_sql('pghydro.output_en_au', $$SELECT pgh_output_en_au.pghfn_updateexporttables()='OK'$$);
SELECT qa.check_sql('pghydro.output_pt_br', $$SELECT pgh_output_pt_br.pghfn_updateexporttables()='OK'$$);
SELECT qa.check_sql('pghydro.output_default_rows', $$SELECT count(*)=3 FROM pgh_output.geoft_bho_drainage_line WHERE v001 IS NOT NULL$$);
SELECT qa.check_sql('pghydro.output_en_au_rows', $$SELECT count(*)=3 FROM pgh_output_en_au.geoft_bho_drainage_line WHERE drn_id IS NOT NULL$$);
SELECT qa.check_sql('pghydro.output_pt_br_rows', $$SELECT count(*)=3 FROM pgh_output_pt_br.geoft_bho_trecho_drenagem$$);

\if :with_documentdb
SET search_path TO documentdb_api, documentdb_core, documentdb_api_catalog, documentdb_api_internal, public;
SELECT documentdb_api.create_collection('postgis37_qa', 'deep_places');
SELECT count(documentdb_api.insert_one('postgis37_qa','deep_places',
    format('{"_id":%s,"value":%s,"loc":{"type":"Point","coordinates":[%s,0]}}',i,i,i/100.0)::bson))
FROM generate_series(1,200) i;
SELECT documentdb_api_internal.create_indexes_non_concurrently('postgis37_qa',
    '{"createIndexes":"deep_places","indexes":[{"key":{"loc":"2dsphere"},"name":"deep_loc_2dsphere"},{"key":{"value":1},"name":"deep_value"}]}',true);
SELECT qa.check_sql('documentdb.insert_read', $$SELECT count(*)=200 FROM documentdb_api.collection('postgis37_qa','deep_places')$$);
SELECT qa.check_sql('documentdb.bson_filter', $$SELECT count(*)=10 FROM documentdb_api.collection('postgis37_qa','deep_places') WHERE document @@ '{"value":{"$lte":10}}'$$);
SELECT qa.check_sql('documentdb.geo_seq', $$SELECT count(*)=49 FROM documentdb_api.collection('postgis37_qa','deep_places') WHERE document @@ '{"loc":{"$geoWithin":{"$geometry":{"type":"Polygon","coordinates":[[[0,-1],[0.495,-1],[0.495,1],[0,1],[0,-1]]]}}}}'$$);
SET enable_seqscan = off;
INSERT INTO qa.plans VALUES ('documentdb.geo',qa.plan($q$SELECT document FROM documentdb_api.collection('postgis37_qa','deep_places') WHERE document @@ '{"loc":{"$geoWithin":{"$geometry":{"type":"Polygon","coordinates":[[[0,-1],[0.495,-1],[0.495,1],[0,1],[0,-1]]]}}}}'$q$));
SELECT qa.check_sql('documentdb.geo_index_plan', $$SELECT plan::text LIKE '%Index%' AND plan::text NOT LIKE '%Seq Scan%' FROM qa.plans WHERE label='documentdb.geo'$$);
SELECT qa.check_sql('documentdb.geo_index_results', $$SELECT count(*)=49 FROM documentdb_api.collection('postgis37_qa','deep_places') WHERE document @@ '{"loc":{"$geoWithin":{"$geometry":{"type":"Polygon","coordinates":[[[0,-1],[0.495,-1],[0.495,1],[0,1],[0,-1]]]}}}}'$$);
SELECT qa.check_sql('documentdb.geo_intersects', $$SELECT count(*)=1 FROM documentdb_api.collection('postgis37_qa','deep_places') WHERE document @@ '{"loc":{"$geoIntersects":{"$geometry":{"type":"Point","coordinates":[1,0]}}}}'$$);
-- The aggregation API requires a single document column in its projection.
SELECT qa.check_sql('documentdb.geonear', $$WITH docs AS MATERIALIZED (SELECT document FROM documentdb_api_catalog.bson_aggregation_pipeline('postgis37_qa','{"aggregate":"deep_places","pipeline":[{"$geoNear":{"near":{"type":"Point","coordinates":[0,0]},"key":"loc","distanceField":"distance","spherical":true,"maxDistance":100000}}]}')) SELECT count(*)=89 FROM docs$$);
INSERT INTO qa.plans VALUES ('documentdb.value',qa.plan($q$SELECT document FROM documentdb_api.collection('postgis37_qa','deep_places') WHERE document @@ '{"value":{"$lte":10}}'$q$));
SELECT qa.check_sql('documentdb.value_index_plan', $$SELECT plan::text LIKE '%Index%' AND plan::text NOT LIKE '%Seq Scan%' FROM qa.plans WHERE label='documentdb.value'$$);
RESET enable_seqscan;
SELECT documentdb_api.update('postgis37_qa','{"update":"deep_places","updates":[{"q":{"_id":1},"u":{"$set":{"value":999}}}]}');
SELECT qa.check_sql('documentdb.update', $$SELECT count(*)=1 FROM documentdb_api.collection('postgis37_qa','deep_places') WHERE document @@ '{"_id":1,"value":999}'$$);
SELECT documentdb_api.delete('postgis37_qa','{"delete":"deep_places","deletes":[{"q":{"_id":200},"limit":1}]}');
SELECT qa.check_sql('documentdb.delete', $$SELECT count(*)=199 FROM documentdb_api.collection('postgis37_qa','deep_places')$$);
BEGIN;
SELECT documentdb_api.insert_one('postgis37_qa','deep_places','{"_id":201,"value":201}');
ROLLBACK;
SELECT qa.check_sql('documentdb.rollback', $$SELECT count(*)=0 FROM documentdb_api.collection('postgis37_qa','deep_places') WHERE document @@ '{"_id":201}'$$);
SELECT qa.check_sql('documentdb.extension_version', $$SELECT bool_and(extversion='1.0-0') AND count(*)=3 FROM pg_extension WHERE extname LIKE 'documentdb%'$$);
RESET search_path;
\endif

SELECT qa.check_sql('runtime.one_geos_proj', $$SELECT count(DISTINCT substring(line FROM '/[^ ]+$'))=3
FROM regexp_split_to_table(pg_read_file('/proc/self/maps',0,2000000),E'\n') line WHERE line ~ '/lib(geos|proj)'$$);
TABLE qa.results;
SELECT label, plan FROM qa.plans ORDER BY label;
DO $$BEGIN IF EXISTS(SELECT FROM qa.results WHERE NOT ok) THEN RAISE EXCEPTION 'deep QA assertions failed'; END IF; END$$;
