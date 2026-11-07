\set ON_ERROR_STOP on
-- Run only in a disposable database as its superuser.
CREATE ROLE permissions_probe NOLOGIN;
CREATE SCHEMA pgdemo;
CREATE TABLE pgdemo.example (id integer);
CREATE VIEW pgdemo.example_view AS SELECT id FROM pgdemo.example;
CREATE SEQUENCE pgdemo.example_seq;
CREATE FUNCTION pgdemo.example_function() RETURNS integer
LANGUAGE sql AS 'SELECT 1';

-- Default installation must reach SQL 1.4 using the official scripts.
CREATE EXTENSION pg_permissions;
\ir pg_permissions-assert.sql
DROP EXTENSION pg_permissions;

-- Reproduce the old schema filter, then exercise the official upgrade.
CREATE EXTENSION pg_permissions VERSION '1.3';
INSERT INTO permission_target
    (role_name, permissions, object_type, schema_name, object_name)
VALUES ('permissions_probe', ARRAY['SELECT','INSERT']::perm_type[],
        'TABLE', 'pgdemo', 'example');
INSERT INTO permission_target
    (role_name, permissions, object_type, schema_name)
VALUES ('permissions_probe', ARRAY['USAGE']::perm_type[], 'SCHEMA', 'pgdemo');
CREATE TEMP TABLE target_before AS SELECT to_jsonb(t) AS value FROM permission_target t;
CREATE TEMP TABLE sequence_before AS SELECT last_value, is_called FROM permission_target_id_seq;
DO $$ BEGIN
    IF EXISTS (SELECT FROM all_permissions WHERE schema_name = 'pgdemo') THEN
        RAISE EXCEPTION 'SQL 1.3 did not reproduce the pgdemo filtering defect';
    END IF;
END $$;

ALTER EXTENSION pg_permissions UPDATE TO '1.4';
\ir pg_permissions-assert.sql
DO $$ BEGIN
    IF EXISTS (
        (SELECT value FROM target_before EXCEPT ALL SELECT to_jsonb(t) FROM permission_target t)
        UNION ALL
        (SELECT to_jsonb(t) FROM permission_target t EXCEPT ALL SELECT value FROM target_before)
    ) THEN
        RAISE EXCEPTION 'permission_target changed during the official upgrade';
    END IF;
    IF EXISTS (
        SELECT last_value, is_called FROM sequence_before
        EXCEPT SELECT last_value, is_called FROM permission_target_id_seq
    ) THEN
        RAISE EXCEPTION 'permission_target sequence changed during upgrade';
    END IF;
END $$;
SELECT 'PASS fresh SQL 1.4, official 1.3-to-1.4 upgrade, schema filters, target preservation' AS result;
