#!/usr/bin/env bash
#==============================================================#
# File      :   ivorysql-pair-test.sh
# Desc      :   replacement-install test for IvorySQL kernel + contrib
# Ctime     :   2026-07-20
# Path      :   bin/ivorysql-pair-test.sh
#==============================================================#
set -Eeuo pipefail

CONTRIB_RPM="${1:?usage: ivorysql-pair-test.sh CONTRIB_RPM EL ARCH}"
TARGET_EL="${2:?missing EL major (8, 9, or 10)}"
TARGET_ARCH="${3:?missing architecture (x86_64 or aarch64)}"
PGROOT="${IVORYSQL_ROOT:-/usr/ivory-18}"
PORT="${IVORYSQL_TEST_PORT:-55432}"
TEST_ROOT="${IVORYSQL_TEST_ROOT:-/var/tmp/ivorysql-pair-test}"
KERNEL_NEVRA="ivorysql-18-5.4-1PIGSTY.el${TARGET_EL}.${TARGET_ARCH}"
TARGET="el${TARGET_EL}.${TARGET_ARCH}"

fail() {
  printf '[FAIL] %s: %s\n' "${TARGET}" "$*" >&2
  exit 1
}

[[ -f "${CONTRIB_RPM}" ]] || fail "missing contrib RPM: ${CONTRIB_RPM}"
[[ ! -e "${TEST_ROOT}" ]] || fail "test root already exists: ${TEST_ROOT}"
[[ "$(uname -m)" == "${TARGET_ARCH}" ]] || \
  fail "container architecture $(uname -m), expected ${TARGET_ARCH}"
grep -Eq "^VERSION_ID=\"?${TARGET_EL}([.]|\"|$)" /etc/os-release || \
  fail "container is not EL${TARGET_EL}"

printf '[PHASE] %s baseline and PostgreSQL removal\n' "${TARGET}"
baseline_pg=$(rpm -qa --qf '%{NAME}\n' | grep -Ec '^postgresql([0-9]+)?($|-)' || true)
printf '[INFO] %s baseline_postgresql_packages=%s\n' "${TARGET}" "${baseline_pg}"

# Exercise the actual replacement path even when the minimal base image has no
# PostgreSQL package initially: install PGDG 18, then remove every installed
# PostgreSQL package before IvorySQL is introduced.
dnf -y --nogpgcheck --setopt=repo_gpgcheck=0 install postgresql18-server
"/usr/pgsql-18/bin/postgres" --version
mapfile -t pg_packages < <(
  rpm -qa --qf '%{NAME}\n' | grep -E '^postgresql([0-9]+)?($|-)' | sort -u
)
[[ "${#pg_packages[@]}" -gt 0 ]] || fail 'PGDG PostgreSQL installation was not detected'
printf '[INFO] %s removing_postgresql_packages=%s names=%s\n' \
  "${TARGET}" "${#pg_packages[@]}" "${pg_packages[*]}"
dnf -y remove "${pg_packages[@]}"
remaining_pg=$(rpm -qa --qf '%{NAME}\n' | grep -Ec '^postgresql([0-9]+)?($|-)' || true)
[[ "${remaining_pg}" -eq 0 ]] || fail "PostgreSQL packages remain after removal"
[[ ! -x /usr/pgsql-18/bin/postgres ]] || fail 'PGDG postgres binary remains after removal'
printf '[ OK ] %s PostgreSQL packages removed completely\n' "${TARGET}"

printf '[PHASE] %s explicit IvorySQL kernel + contrib installation\n' "${TARGET}"
dnf -y --nogpgcheck --setopt=repo_gpgcheck=0 install \
  "${KERNEL_NEVRA}" "${CONTRIB_RPM}"
dnf check

kernel_nevra=$(rpm -q --qf '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}' ivorysql-18)
contrib_nevra=$(rpm -q --qf '%{NAME}-%{VERSION}-%{RELEASE}.%{ARCH}' ivorysql-18-contrib)
[[ "${kernel_nevra}" == "${KERNEL_NEVRA}" ]] || \
  fail "unexpected kernel: ${kernel_nevra}"
[[ "${contrib_nevra}" == "ivorysql-18-contrib-5.4-2PIGSTY.el${TARGET_EL}.${TARGET_ARCH}" ]] || \
  fail "unexpected contrib: ${contrib_nevra}"
rpm -V ivorysql-18
rpm -V ivorysql-18-contrib

rpm -q --requires ivorysql-18-contrib | \
  grep -Eq '^ivorysql-18(\([^)]*\))?[[:space:]]+>=[[:space:]]+5[.]0$' || \
  fail 'missing IvorySQL >= 5.0 dependency'
rpm -q --requires ivorysql-18-contrib | \
  grep -Eq '^ivorysql-18(\([^)]*\))?[[:space:]]+<[[:space:]]+6[.]0$' || \
  fail 'missing IvorySQL < 6.0 dependency'

post_install_pg=$(rpm -qa --qf '%{NAME}\n' | grep -Ec '^postgresql([0-9]+)?($|-)' || true)
[[ "${post_install_pg}" -eq 0 ]] || fail 'IvorySQL installation pulled PostgreSQL packages back in'

kernel_controls=$(rpm -ql ivorysql-18 | grep -c '[.]control$')
contrib_controls=$(rpm -ql ivorysql-18-contrib | grep -c '[.]control$')
available_controls=$(find "${PGROOT}/share/postgresql/extension" -maxdepth 1 \
  -type f -name '*.control' -exec basename {} .control \; | sort -u | wc -l)
kernel_modules=$(rpm -ql ivorysql-18 | grep -E -c '/lib/postgresql/[^/]+[.]so$')
contrib_modules=$(rpm -ql ivorysql-18-contrib | grep -E -c '/lib/postgresql/[^/]+[.]so$')
available_modules=$(find "${PGROOT}/lib/postgresql" -maxdepth 1 \
  -type f -name '*.so' | wc -l)
[[ "${kernel_controls}" -eq 66 ]] || fail "kernel controls=${kernel_controls}, expected 66"
[[ "${contrib_controls}" -eq 29 ]] || fail "contrib controls=${contrib_controls}, expected 29"
[[ "${available_controls}" -eq 95 ]] || fail "combined controls=${available_controls}, expected 95"
[[ "${kernel_modules}" -eq 98 ]] || fail "kernel modules=${kernel_modules}, expected 98"
[[ "${contrib_modules}" -eq 31 ]] || fail "contrib modules=${contrib_modules}, expected 31"
[[ "${available_modules}" -eq 129 ]] || fail "combined modules=${available_modules}, expected 129"

unresolved=0
while IFS= read -r module; do
  if ldd "${module}" | grep -q 'not found'; then
    printf '[FAIL] unresolved dependency in %s\n' "${module}" >&2
    ldd "${module}" | grep 'not found' >&2
    unresolved=$((unresolved + 1))
  fi
done < <(find "${PGROOT}/lib/postgresql" -maxdepth 1 -type f -name '*.so' | sort)
[[ "${unresolved}" -eq 0 ]] || fail "${unresolved} modules have unresolved dependencies"
printf '[ OK ] %s package_inventory kernel=66+98 contrib=29+31 combined=95+129\n' "${TARGET}"

printf '[PHASE] %s initialize server and create all extensions\n' "${TARGET}"
mkdir -p "${TEST_ROOT}/data" "${TEST_ROOT}/log"
chown -R postgres:postgres "${TEST_ROOT}"
runuser -u postgres -- "${PGROOT}/bin/initdb" -D "${TEST_ROOT}/data" \
  --no-locale --encoding=UTF8 --auth-local=trust --auth-host=trust \
  >"${TEST_ROOT}/log/initdb.log" 2>&1
{
  printf "listen_addresses = '127.0.0.1'\n"
  printf 'port = %s\n' "${PORT}"
  printf "shared_preload_libraries = 'gb18030_2022,liboracle_parser,ivorysql_ora,pg_stat_statements,pgaudit,pg_cron,pg_hint_plan,pg_jieba,pg_show_plans,pg_stat_monitor,pg_textsearch'\n"
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

server_version=$("${PSQL[@]}" -Atc 'SELECT version();')
[[ "${server_version}" == *'IvorySQL 5.4'* ]] || fail "unexpected server: ${server_version}"
mapfile -t extensions < <("${PSQL[@]}" -Atc \
  'SELECT name FROM pg_available_extensions ORDER BY name;')
[[ "${#extensions[@]}" -eq 95 ]] || \
  fail "pg_available_extensions=${#extensions[@]}, expected 95"

declare -a first_failures=()
for extension in "${extensions[@]}"; do
  if "${PSQL[@]}" -c "CREATE EXTENSION IF NOT EXISTS \"${extension}\" CASCADE" \
      >"${TEST_ROOT}/log/create-${extension}.log" 2>&1; then
    printf '[EXT-OK] %s %s\n' "${TARGET}" "${extension}"
  else
    first_failures+=("${extension}")
    printf '[EXT-RETRY] %s %s\n' "${TARGET}" "${extension}"
  fi
done

declare -a final_failures=()
for extension in "${first_failures[@]}"; do
  if "${PSQL[@]}" -c "CREATE EXTENSION IF NOT EXISTS \"${extension}\" CASCADE" \
      >"${TEST_ROOT}/log/retry-${extension}.log" 2>&1; then
    printf '[EXT-OK] %s %s retry\n' "${TARGET}" "${extension}"
  else
    final_failures+=("${extension}")
    printf '[EXT-FAIL] %s %s\n' "${TARGET}" "${extension}" >&2
  fi
done

installed_extensions=$("${PSQL[@]}" -Atc 'SELECT count(*) FROM pg_extension;')
[[ "${#final_failures[@]}" -eq 0 ]] || \
  fail "extensions failed: ${final_failures[*]}"
[[ "${installed_extensions}" -eq 95 ]] || \
  fail "installed extensions=${installed_extensions}, expected 95"

printf '[PHASE] %s functional smoke tests\n' "${TARGET}"
postgis_result=$("${PSQL[@]}" -Atc \
  "SELECT postgis_lib_version() || '|' || postgis_sfcgal_version();")
pgrouting_result=$("${PSQL[@]}" -Atc 'SELECT pgr_version();')
vector_result=$("${PSQL[@]}" -Atc \
  "SELECT '[1,2,3]'::vector <-> '[3,2,1]'::vector;")
uuid_result=$("${PSQL[@]}" -Atc 'SELECT sys.uuid_generate_v4() IS NOT NULL;')
trgm_result=$("${PSQL[@]}" -Atc \
  "SELECT similarity('ivorysql', 'ivory') > 0;")
stats_result=$("${PSQL[@]}" -Atc 'SELECT count(*) >= 0 FROM pg_stat_statements;')
cron_result=$("${PSQL[@]}" -Atc 'SELECT count(*) >= 0 FROM cron.job;')
[[ "${postgis_result}" == 3.5.4'|'* ]] || fail "PostGIS result: ${postgis_result}"
[[ "${pgrouting_result}" == '3.8.0' ]] || fail "pgRouting result: ${pgrouting_result}"
[[ "${vector_result}" == '2.8284271247461903' ]] || fail "vector result: ${vector_result}"
[[ "${uuid_result}" == 't' && "${trgm_result}" == 't' && \
   "${stats_result}" == 't' && "${cron_result}" == 't' ]] || \
  fail 'kernel extension smoke test returned false'

"${PSQL[@]}" -c \
  "CREATE TABLE pgroonga_smoke (id integer, content text); INSERT INTO pgroonga_smoke VALUES (1, 'IvorySQL extension test'), (2, 'unrelated row'); CREATE INDEX pgroonga_smoke_idx ON pgroonga_smoke USING pgroonga (content); SET enable_seqscan = off; SELECT id FROM pgroonga_smoke WHERE content &@ 'IvorySQL';" \
  >"${TEST_ROOT}/log/pgroonga-smoke.log"
grep -Eq '^[[:space:]]*1[[:space:]]*$' \
  "${TEST_ROOT}/log/pgroonga-smoke.log" || fail 'PGroonga match did not return row 1'
"${PSQL[@]}" -c \
  "CREATE FUNCTION plpgsql_check_smoke() RETURNS integer LANGUAGE plpgsql AS \$\$ BEGIN RETURN 1; END \$\$; SELECT count(*) FROM plpgsql_check_function_tb('plpgsql_check_smoke()');" \
  >"${TEST_ROOT}/log/plpgsql-check-smoke.log"
grep -q '^CREATE FUNCTION$' "${TEST_ROOT}/log/plpgsql-check-smoke.log" || \
  fail 'plpgsql_check test function was not created'
grep -Eq '^[[:space:]]*0[[:space:]]*$' \
  "${TEST_ROOT}/log/plpgsql-check-smoke.log" || \
  fail 'plpgsql_check reported diagnostics for the valid test function'
"${PSQL[@]}" -Atc \
  "SELECT * FROM pg_create_logical_replication_slot('ivory_wal2json_test', 'wal2json', true);" \
  >"${TEST_ROOT}/log/wal2json-smoke.log"
grep -Eq '^ivory_wal2json_test[|]' "${TEST_ROOT}/log/wal2json-smoke.log" || \
  fail 'wal2json logical slot was not returned'
"${PSQL[@]}" -c \
  "LOAD 'age'; SET search_path = ag_catalog, \"\$user\", public; SELECT create_graph('ivory_pair_graph'); SELECT * FROM cypher('ivory_pair_graph', \$\$ CREATE (n:Smoke {name: 'ok'}) RETURN n \$\$) AS (n agtype);" \
  >"${TEST_ROOT}/log/age-smoke.log"
grep -Fq '"name": "ok"' "${TEST_ROOT}/log/age-smoke.log" || \
  fail 'AGE Cypher result did not contain the test vertex'

printf '[RESULT] target=%s pg_removed=1 kernel=%s contrib=%s controls=66+29=95 modules=98+31=129 available=95 installed=95 failed=0 postgis=%s pgrouting=%s vector=%s\n' \
  "${TARGET}" "${kernel_nevra}" "${contrib_nevra}" "${postgis_result}" \
  "${pgrouting_result}" "${vector_result}"
