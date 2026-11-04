#!/usr/bin/env python3
"""Exercise installed pg_parquet streaming COPY and check temporary-file cleanup.

Run as the PostgreSQL OS user against a disposable, preloaded cluster:
  pg-parquet-smoke.py --pg-bin /usr/pgsql-18/bin --port 56118
"""

import argparse
import json
import os
from pathlib import Path
import subprocess
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pg-bin", required=True)
    parser.add_argument("--port", required=True)
    parser.add_argument("--host", default="127.0.0.1")
    args = parser.parse_args()
    command = [str(Path(args.pg_bin) / "psql"), "-X", "-qAt", "-v",
               "ON_ERROR_STOP=1", "-h", args.host, "-p", args.port,
               "-d", "postgres"]
    env = dict(os.environ)

    def sql(statement, data=None):
        result = subprocess.run(command + ["-c", statement], input=data,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                env=env, timeout=90)
        if result.returncode:
            raise RuntimeError(result.stderr.decode(errors="replace"))
        return result.stdout

    def literal(value):
        return "'" + str(value).replace("'", "''") + "'"

    sql("CREATE EXTENSION IF NOT EXISTS pg_parquet;")
    version = sql("SELECT extversion FROM pg_extension WHERE extname='pg_parquet';").decode().strip()
    assert version == "0.5.1", version
    data_dir = Path(sql("SHOW data_directory;").decode().strip())
    sql("CREATE TABLE parquet_smoke (a int, b text, c numeric(10,1), d boolean);")
    query = ("SELECT i AS a, CASE WHEN i % 7 = 0 THEN NULL ELSE 'row-' || i END AS b, "
             "(i::numeric / 10)::numeric(10,1) AS c, i % 2 = 0 AS d FROM generate_series(1, 1000) i")
    results = []
    with tempfile.TemporaryDirectory(prefix="parquet-smoke-") as scratch:
        tablespace = Path(scratch) / "tablespace"
        tablespace.mkdir()
        sql("CREATE TABLESPACE parquet_smoke_ts LOCATION " + literal(tablespace) + ";")

        def check_temp_files():
            roots = [data_dir / "base" / "pgsql_tmp"]
            roots.extend(tablespace.glob("PG_*/pgsql_tmp"))
            leftovers = [str(p) for root in roots if root.exists()
                         for p in root.rglob("*") if p.is_file()]
            assert not leftovers, "temporary files leaked: " + repr(leftovers)

        def check_rows():
            result = sql("SELECT count(*), count(*) FILTER (WHERE b IS DISTINCT FROM "
                         "CASE WHEN a % 7 = 0 THEN NULL ELSE 'row-' || a END "
                         "OR c IS DISTINCT FROM a::numeric / 10 "
                         "OR d IS DISTINCT FROM (a % 2 = 0)) FROM parquet_smoke;")
            assert result.strip() == b"1000|0", result

        for mode in ("default", "tablespace"):
            env["PGOPTIONS"] = "-c temp_tablespaces=parquet_smoke_ts" if mode == "tablespace" else ""
            for iteration in range(3):
                parquet = sql("COPY (" + query + ") TO STDOUT WITH (FORMAT parquet);")
                assert parquet.startswith(b"PAR1") and parquet.endswith(b"PAR1"), "invalid Parquet stream"
                check_temp_files()
                sql("TRUNCATE parquet_smoke;")
                sql("COPY parquet_smoke FROM STDIN WITH (FORMAT parquet);", parquet)
                check_rows()
                check_temp_files()
                results.append({"mode": mode, "iteration": iteration + 1,
                                "stream_bytes": len(parquet), "rows": 1000})

            program_file = Path(scratch) / (mode + ".parquet")
            sql("COPY (" + query + ") TO PROGRAM " + literal("cat > " + str(program_file)) +
                " WITH (FORMAT parquet);")
            check_temp_files()
            sql("TRUNCATE parquet_smoke;")
            sql("COPY parquet_smoke FROM PROGRAM " + literal("cat " + str(program_file)) +
                " WITH (FORMAT parquet);")
            check_rows()
            check_temp_files()

        env["PGOPTIONS"] = ""
        sql("DROP TABLE parquet_smoke;")
        sql("DROP TABLESPACE parquet_smoke_ts;")
    print(json.dumps({"extension_version": version, "server_version":
                      sql("SHOW server_version;").decode().strip(),
                      "stream_roundtrips": results, "program_roundtrips": 2,
                      "temporary_files_remaining": 0, "status": "passed"}))


if __name__ == "__main__":
    main()
