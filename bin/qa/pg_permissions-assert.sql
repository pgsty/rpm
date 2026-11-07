DO $$
DECLARE kind text;
BEGIN
    IF (SELECT extversion FROM pg_extension WHERE extname = 'pg_permissions') <> '1.4' THEN
        RAISE EXCEPTION 'expected SQL extension version 1.4';
    END IF;
    FOREACH kind IN ARRAY ARRAY['TABLE','VIEW','COLUMN','SEQUENCE','FUNCTION','SCHEMA'] LOOP
        IF NOT EXISTS (
            SELECT FROM all_permissions
            WHERE schema_name = 'pgdemo' AND role_name = 'permissions_probe'
              AND object_type::text = kind
        ) THEN
            RAISE EXCEPTION 'pgdemo missing from % permissions', kind;
        END IF;
    END LOOP;
    IF EXISTS (
        SELECT FROM all_permissions
        WHERE schema_name = 'information_schema' OR schema_name LIKE 'pg\_%'
    ) THEN
        RAISE EXCEPTION 'system schema leaked into permission views';
    END IF;
END $$;
