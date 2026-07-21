#!/usr/bin/env bash
#==============================================================#
# File      :   ivorysql-contrib-test.sh
# Desc      :   clean-install and runtime test IvorySQL contrib
# Ctime     :   2026-07-20
# Path      :   bin/ivorysql-contrib-test.sh
#==============================================================#
set -Eeuo pipefail

RPM_PATH="${1:?usage: ivorysql-contrib-test.sh /path/to/contrib.rpm}"
PGROOT="${IVORYSQL_ROOT:-/usr/ivory-18}"
PORT="${IVORYSQL_TEST_PORT:-55432}"
TEST_ROOT="${IVORYSQL_TEST_ROOT:-/var/tmp/ivorysql-contrib-clean-test}"

[[ -f "${RPM_PATH}" ]] || { printf '[FAIL] missing RPM: %s\n' "${RPM_PATH}" >&2; exit 1; }
[[ ! -e "${TEST_ROOT}" ]] || { printf '[FAIL] test root already exists: %s\n' "${TEST_ROOT}" >&2; exit 1; }

dnf -y --nogpgcheck --setopt=repo_gpgcheck=0 install "${RPM_PATH}"
dnf check

rpm -q ivorysql-18 ivorysql-18-contrib
rpm -V ivorysql-18-contrib
rpm -q --requires ivorysql-18-contrib | \
  grep -Eq '^ivorysql-18(\([^)]*\))?[[:space:]]+>=[[:space:]]+5[.]0$'
rpm -q --requires ivorysql-18-contrib | \
  grep -Eq '^ivorysql-18(\([^)]*\))?[[:space:]]+<[[:space:]]+6[.]0$'

[[ "$(rpm -ql ivorysql-18-contrib | grep -c '[.]control$')" -eq 29 ]]
[[ "$(rpm -ql ivorysql-18-contrib | grep -E -c '/lib/postgresql/[^/]+[.]so$')" -eq 31 ]]

while IFS= read -r module; do
  if ldd "${module}" | grep -q 'not found'; then
    ldd "${module}" >&2
    printf '[FAIL] unresolved dependency in %s\n' "${module}" >&2
    exit 1
  fi
done < <(find "${PGROOT}/lib/postgresql" -maxdepth 1 -type f -name '*.so' | sort)

mkdir -p "${TEST_ROOT}/data" "${TEST_ROOT}/log"
chown -R postgres:postgres "${TEST_ROOT}"
runuser -u postgres -- "${PGROOT}/bin/initdb" -D "${TEST_ROOT}/data" \
  --no-locale --encoding=UTF8 --auth-local=trust --auth-host=trust \
  >"${TEST_ROOT}/log/initdb.log" 2>&1
{
  printf "listen_addresses = '127.0.0.1'\n"
  printf 'port = %s\n' "${PORT}"
  printf "shared_preload_libraries = 'pgaudit,pg_cron,pg_hint_plan,pg_jieba,pg_show_plans,pg_stat_monitor,pg_textsearch'\n"
  printf "cron.database_name = 'postgres'\n"
  printf "wal_level = logical\n"
  printf "max_replication_slots = 10\n"
} >>"${TEST_ROOT}/data/postgresql.conf"

started=0
stop_server() {
  if [[ "${started}" -eq 1 ]]; then
    runuser -u postgres -- "${PGROOT}/bin/pg_ctl" -D "${TEST_ROOT}/data" \
      -m fast -w stop >"${TEST_ROOT}/log/stop.log" 2>&1 || true
  fi
}
trap stop_server EXIT

runuser -u postgres -- "${PGROOT}/bin/pg_ctl" -D "${TEST_ROOT}/data" \
  -l "${TEST_ROOT}/log/postgresql.log" -w start
started=1

PSQL=("${PGROOT}/bin/psql" -h 127.0.0.1 -p "${PORT}" -U postgres \
  -d postgres -X -v ON_ERROR_STOP=1)
"${PSQL[@]}" -c 'CREATE EXTENSION fuzzystrmatch' >/dev/null

extensions=(
  postgis address_standardizer address_standardizer_data_us postgis_raster
  postgis_sfcgal postgis_topology postgis_tiger_geocoder pgrouting age ddlx
  http pgagent pgaudit pg_bigm pg_cron pg_curl pg_hint_plan pg_jieba
  pg_partman pgroonga pgroonga_database pg_show_plans pg_stat_monitor
  pg_textsearch plpgsql_check redis_fdw system_stats vector zhparser
)
for extension in "${extensions[@]}"; do
  "${PSQL[@]}" -c "CREATE EXTENSION \"${extension}\"" \
    >"${TEST_ROOT}/log/create-${extension}.log" 2>&1
  printf '[ OK ] CREATE EXTENSION %s\n' "${extension}"
done

count=$("${PSQL[@]}" -Atc \
  "SELECT count(*) FROM pg_extension WHERE extname = ANY (ARRAY['address_standardizer','address_standardizer_data_us','age','ddlx','http','pgagent','pgaudit','pg_bigm','pg_cron','pg_curl','pg_hint_plan','pg_jieba','pg_partman','pgroonga','pgroonga_database','pgrouting','pg_show_plans','pg_stat_monitor','pg_textsearch','plpgsql_check','postgis','postgis_raster','postgis_sfcgal','postgis_tiger_geocoder','postgis_topology','redis_fdw','system_stats','vector','zhparser']);")
[[ "${count}" -eq 29 ]]

"${PSQL[@]}" -Atc "SELECT postgis_lib_version(), postgis_sfcgal_version();"
"${PSQL[@]}" -Atc 'SELECT pgr_version();'
"${PSQL[@]}" -Atc "SELECT '[1,2,3]'::vector <-> '[3,2,1]'::vector;"
"${PSQL[@]}" -c \
  "CREATE TABLE pgroonga_smoke (id integer, content text); INSERT INTO pgroonga_smoke VALUES (1, 'IvorySQL extension test'), (2, 'unrelated row'); CREATE INDEX pgroonga_smoke_idx ON pgroonga_smoke USING pgroonga (content); SET enable_seqscan = off; SELECT id FROM pgroonga_smoke WHERE content &@ 'IvorySQL';"
"${PSQL[@]}" -c \
  "CREATE FUNCTION plpgsql_check_smoke() RETURNS integer LANGUAGE plpgsql AS \$\$ BEGIN RETURN 1; END \$\$; SELECT count(*) FROM plpgsql_check_function_tb('plpgsql_check_smoke()');"
"${PSQL[@]}" -Atc \
  "SELECT * FROM pg_create_logical_replication_slot('ivory_wal2json_test', 'wal2json', true);"

printf '[ OK ] clean dependency install, server startup, 29 extensions, and functional smoke tests\n'
