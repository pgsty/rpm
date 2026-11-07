\set ON_ERROR_STOP on
CREATE EXTENSION postgis;
CREATE EXTENSION postgis_raster;
CREATE EXTENSION mobilitydb;
CREATE EXTENSION mobilitydb_datagen;
CREATE EXTENSION pghydro;
CREATE EXTENSION pgh_raster;
CREATE EXTENSION pgh_hgm;
CREATE EXTENSION pgh_output;
CREATE EXTENSION pgh_output_en_au;
CREATE EXTENSION pgh_output_pt_br;
CREATE EXTENSION pgh_consistency;

DO $$
DECLARE
    trip tgeompoint := 'SRID=4326;[Point(0 0)@2026-01-01, Point(1 1)@2026-01-02]'::tgeompoint;
BEGIN
    IF postgis_lib_version() NOT LIKE '3.7.%' THEN
        RAISE EXCEPTION 'expected PostGIS 3.7, got %', postgis_lib_version();
    END IF;
    IF numInstants(trip) <> 2 OR NOT ST_IsValid(ST_Buffer(trajectory(trip), 0.1)) THEN
        RAISE EXCEPTION 'MobilityDB/PostGIS trajectory check failed';
    END IF;
    IF abs(ST_X(ST_Transform(ST_SetSRID(ST_MakePoint(1, 1), 4326), 3857)) - 111319.490793) > 0.001 THEN
        RAISE EXCEPTION 'PostGIS PROJ transform check failed';
    END IF;
END
$$;

\if :with_documentdb
CREATE EXTENSION documentdb_core;
CREATE EXTENSION documentdb CASCADE;
CREATE EXTENSION documentdb_extended_rum;
SET search_path TO documentdb_api, documentdb_core, documentdb_api_catalog, documentdb_api_internal, public;
SELECT documentdb_api.create_collection('postgis37_qa', 'places');
SELECT documentdb_api_internal.create_indexes_non_concurrently(
    'postgis37_qa',
    '{"createIndexes":"places","indexes":[{"key":{"loc":"2dsphere"},"name":"loc_2dsphere"}]}',
    true
);
SELECT documentdb_api.insert_one('postgis37_qa', 'places', '{"_id":1,"loc":{"type":"Point","coordinates":[0,0]}}');
SELECT documentdb_api.insert_one('postgis37_qa', 'places', '{"_id":2,"loc":{"type":"Point","coordinates":[40,40]}}');
DO $$
DECLARE
    matching bigint;
BEGIN
    SELECT count(*) INTO matching
    FROM documentdb_api.collection('postgis37_qa', 'places')
    WHERE document @@ '{"loc":{"$geoWithin":{"$geometry":{"type":"Polygon","coordinates":[[[-10,-10],[10,-10],[10,10],[-10,10],[-10,-10]]]}}}}';
    IF matching <> 1 THEN
        RAISE EXCEPTION 'DocumentDB/PostGIS geospatial check returned % rows', matching;
    END IF;
END
$$;
RESET search_path;
\endif

SELECT extname, extversion FROM pg_extension ORDER BY extname;
SELECT postgis_full_version();
SELECT DISTINCT substring(line FROM '/[^ ]+$') AS gis_library
FROM regexp_split_to_table(pg_read_file('/proc/self/maps', 0, 2000000), E'\n') AS line
WHERE line ~ '/lib(geos|proj)'
ORDER BY 1;
