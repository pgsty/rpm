#!/usr/bin/env bash
#==============================================================#
# File      :   pgtde-runtime-test.sh
# Desc      :   runtime QA for the Pigsty Percona pg_tde build
# Ctime     :   2026-07-22
# Path      :   bin/pgtde-runtime-test.sh
#==============================================================#
set -Eeuo pipefail

PGROOT="${PGTDE_ROOT:-/usr/pgtde-18}"
TEST_ROOT="${PGTDE_TEST_ROOT:-/var/tmp/pgtde-runtime-test}"
PRIMARY_PORT="${PGTDE_TEST_PORT:-56432}"
STANDBY_PORT="$((PRIMARY_PORT + 1))"
PRIMARY_DATA="${TEST_ROOT}/primary"
STANDBY_DATA="${TEST_ROOT}/standby"
LOG_DIR="${TEST_ROOT}/log"
KEYRING="${TEST_ROOT}/keyring.per"
MARKER="PIGSTY_PGTDE_QA_7f71c06e"

fail() {
  printf '[FAIL] %s\n' "$*" >&2
  exit 1
}

[[ "$(id -u)" -eq 0 ]] || fail 'run this test as root'
[[ ! -e "${TEST_ROOT}" ]] || fail "test root already exists: ${TEST_ROOT}"

for program in \
  initdb pg_ctl postgres psql pg_config pg_basebackup pg_verifybackup \
  pg_rewind pg_controldata; do
  [[ -x "${PGROOT}/bin/${program}" ]] || fail "missing executable: ${PGROOT}/bin/${program}"
done

for mapping in \
  pg_tde_basebackup:pg_basebackup \
  pg_tde_checksums:pg_checksums \
  pg_tde_resetwal:pg_resetwal \
  pg_tde_rewind:pg_rewind \
  pg_tde_waldump:pg_waldump \
  pg_tde_upgrade:pg_upgrade; do
  alias_name=${mapping%%:*}
  canonical_name=${mapping##*:}
  [[ -L "${PGROOT}/bin/${alias_name}" ]] || fail "${alias_name} is not a compatibility symlink"
  [[ "$(readlink "${PGROOT}/bin/${alias_name}")" == "${canonical_name}" ]] || \
    fail "${alias_name} does not point to ${canonical_name}"
done

server_version=$("${PGROOT}/bin/postgres" --version)
basebackup_version=$("${PGROOT}/bin/pg_basebackup" --version)
rewind_version=$("${PGROOT}/bin/pg_rewind" --version)
[[ "${server_version}" == *'Percona Server for PostgreSQL 18.4.2'* ]] || \
  fail "unexpected server version: ${server_version}"
[[ "${basebackup_version}" == *'Percona Server for PostgreSQL 18.4.2'* ]] || \
  fail "unexpected pg_basebackup version: ${basebackup_version}"
[[ "${rewind_version}" == *'Percona Server for PostgreSQL 18.4.2'* ]] || \
  fail "unexpected pg_rewind version: ${rewind_version}"

unresolved=0
while IFS= read -r module; do
  if ldd "${module}" | grep -q 'not found'; then
    printf '[FAIL] unresolved dependency in %s\n' "${module}" >&2
    ldd "${module}" | grep 'not found' >&2
    unresolved=$((unresolved + 1))
  fi
done < <(find "${PGROOT}/lib/postgresql" -maxdepth 1 -type f -name '*.so' | sort)
[[ "${unresolved}" -eq 0 ]] || fail "${unresolved} modules have unresolved dependencies"

install -d -o postgres -g postgres "${TEST_ROOT}"
install -d -o postgres -g postgres "${PRIMARY_DATA}" "${LOG_DIR}"
runuser -u postgres -- "${PGROOT}/bin/initdb" -D "${PRIMARY_DATA}" \
  --data-checksums --no-locale --encoding=UTF8 \
  --auth-local=trust --auth-host=trust >"${LOG_DIR}/initdb.log" 2>&1
{
  printf "listen_addresses = '127.0.0.1'\n"
  printf 'port = %s\n' "${PRIMARY_PORT}"
  printf "shared_preload_libraries = 'pg_tde'\n"
  printf "wal_level = replica\n"
  printf "max_wal_senders = 10\n"
  printf "max_replication_slots = 10\n"
  printf "hot_standby = on\n"
} >>"${PRIMARY_DATA}/postgresql.conf"

primary_started=0
standby_started=0
stop_clusters() {
  if [[ "${primary_started}" -eq 1 ]]; then
    runuser -u postgres -- "${PGROOT}/bin/pg_ctl" -D "${PRIMARY_DATA}" \
      -m fast -w stop >"${LOG_DIR}/primary-stop.log" 2>&1 || true
  fi
  if [[ "${standby_started}" -eq 1 ]]; then
    runuser -u postgres -- "${PGROOT}/bin/pg_ctl" -D "${STANDBY_DATA}" \
      -m fast -w stop >"${LOG_DIR}/standby-stop.log" 2>&1 || true
  fi
}
trap stop_clusters EXIT

runuser -u postgres -- "${PGROOT}/bin/pg_ctl" -D "${PRIMARY_DATA}" \
  -l "${LOG_DIR}/primary.log" -w start
primary_started=1
PRIMARY_PSQL=("${PGROOT}/bin/psql" -h 127.0.0.1 -p "${PRIMARY_PORT}" \
  -U postgres -d postgres -X -v ON_ERROR_STOP=1)

printf '[PHASE] create every packaged extension\n'
"${PRIMARY_PSQL[@]}" -c 'CREATE SCHEMA _pg_tde' >/dev/null
"${PRIMARY_PSQL[@]}" -c 'CREATE EXTENSION pg_tde SCHEMA _pg_tde' \
  >"${LOG_DIR}/create-pg_tde.log" 2>&1
mapfile -t extensions < <("${PRIMARY_PSQL[@]}" -Atc \
  "SELECT name FROM pg_available_extensions WHERE name <> 'pg_tde' ORDER BY name")
[[ "${#extensions[@]}" -ge 60 ]] || fail "only ${#extensions[@]} non-pg_tde extensions are available"

declare -a first_failures=()
for extension in "${extensions[@]}"; do
  if "${PRIMARY_PSQL[@]}" -c \
      "CREATE EXTENSION IF NOT EXISTS \"${extension}\" CASCADE" \
      >"${LOG_DIR}/create-${extension}.log" 2>&1; then
    printf '[EXT-OK] %s\n' "${extension}"
  else
    first_failures+=("${extension}")
  fi
done

declare -a final_failures=()
for extension in "${first_failures[@]}"; do
  if "${PRIMARY_PSQL[@]}" -c \
      "CREATE EXTENSION IF NOT EXISTS \"${extension}\" CASCADE" \
      >"${LOG_DIR}/retry-${extension}.log" 2>&1; then
    printf '[EXT-OK] %s retry\n' "${extension}"
  else
    final_failures+=("${extension}")
    printf '[EXT-FAIL] %s\n' "${extension}" >&2
  fi
done
[[ "${#final_failures[@]}" -eq 0 ]] || fail "extensions failed: ${final_failures[*]}"

installed_extensions=$("${PRIMARY_PSQL[@]}" -Atc 'SELECT count(*) FROM pg_extension')
expected_extensions=$("${PRIMARY_PSQL[@]}" -Atc 'SELECT count(*) FROM pg_available_extensions')
[[ "${installed_extensions}" -eq "${expected_extensions}" ]] || \
  fail "installed extensions=${installed_extensions}, available=${expected_extensions}"

printf '[PHASE] configure TDE and verify encrypted storage\n'
"${PRIMARY_PSQL[@]}" <<SQL >"${LOG_DIR}/tde-smoke.log"
SELECT _pg_tde.pg_tde_add_database_key_provider_file('qa_file', '${KEYRING}');
SELECT _pg_tde.pg_tde_create_key_using_database_key_provider('qa_main', 'qa_file');
SELECT _pg_tde.pg_tde_set_key_using_database_key_provider('qa_main', 'qa_file');
CREATE TABLE tde_qa(id bigint PRIMARY KEY, payload text) USING tde_heap;
ALTER TABLE tde_qa ALTER COLUMN payload SET STORAGE PLAIN;
INSERT INTO tde_qa
SELECT g, repeat('${MARKER}_' || g || '_', 32) FROM generate_series(1,1000) AS g;
SELECT _pg_tde.pg_tde_is_encrypted('tde_qa');
SQL
encrypted=$("${PRIMARY_PSQL[@]}" -Atc \
  "SELECT _pg_tde.pg_tde_is_encrypted('tde_qa')")
[[ "${encrypted}" == 't' ]] || fail 'tde_qa is not encrypted'

printf '[PHASE] standard pg_basebackup creates and verifies a standby\n'
runuser -u postgres -- "${PGROOT}/bin/pg_basebackup" \
  -h 127.0.0.1 -p "${PRIMARY_PORT}" -U postgres \
  -D "${STANDBY_DATA}" -Fp -X stream -R -c fast \
  >"${LOG_DIR}/basebackup.log" 2>&1
runuser -u postgres -- "${PGROOT}/bin/pg_verifybackup" "${STANDBY_DATA}" \
  >"${LOG_DIR}/verifybackup.log" 2>&1
runuser -u postgres -- "${PGROOT}/bin/pg_ctl" -D "${STANDBY_DATA}" \
  -l "${LOG_DIR}/standby.log" -o "-p ${STANDBY_PORT}" -w start
standby_started=1
STANDBY_PSQL=("${PGROOT}/bin/psql" -h 127.0.0.1 -p "${STANDBY_PORT}" \
  -U postgres -d postgres -X -v ON_ERROR_STOP=1)

for unused in $(seq 1 30); do
  replayed=$("${STANDBY_PSQL[@]}" -Atc \
    "SELECT pg_is_in_recovery() AND count(*) = 1000 FROM tde_qa")
  [[ "${replayed}" == 't' ]] && break
  sleep 1
done
[[ "${replayed:-f}" == 't' ]] || fail 'standby did not replay the base backup state'

printf '[PHASE] create a timeline fork and run standard pg_rewind\n'
runuser -u postgres -- "${PGROOT}/bin/pg_ctl" -D "${PRIMARY_DATA}" \
  -m fast -w stop >"${LOG_DIR}/primary-pre-fork-stop.log" 2>&1
primary_started=0
runuser -u postgres -- "${PGROOT}/bin/pg_ctl" -D "${STANDBY_DATA}" \
  -w promote >"${LOG_DIR}/standby-promote.log" 2>&1
"${STANDBY_PSQL[@]}" -c \
  "INSERT INTO tde_qa VALUES (2001, repeat('${MARKER}_SOURCE_TIMELINE_', 16)); CHECKPOINT" \
  >"${LOG_DIR}/source-divergence.log" 2>&1

runuser -u postgres -- "${PGROOT}/bin/pg_ctl" -D "${PRIMARY_DATA}" \
  -l "${LOG_DIR}/primary-diverged.log" -w start
primary_started=1
"${PRIMARY_PSQL[@]}" -c \
  "INSERT INTO tde_qa VALUES (2002, repeat('${MARKER}_TARGET_TIMELINE_', 16)); CHECKPOINT" \
  >"${LOG_DIR}/target-divergence.log" 2>&1
runuser -u postgres -- "${PGROOT}/bin/pg_ctl" -D "${PRIMARY_DATA}" \
  -m fast -w stop >"${LOG_DIR}/primary-rewind-stop.log" 2>&1
primary_started=0

runuser -u postgres -- "${PGROOT}/bin/pg_rewind" \
  --target-pgdata="${PRIMARY_DATA}" \
  --source-server="host=127.0.0.1 port=${STANDBY_PORT} user=postgres dbname=postgres" \
  --write-recovery-conf --progress \
  >"${LOG_DIR}/rewind.log" 2>&1

runuser -u postgres -- "${PGROOT}/bin/pg_ctl" -D "${PRIMARY_DATA}" \
  -l "${LOG_DIR}/primary-rewound.log" -w start
primary_started=1
"${STANDBY_PSQL[@]}" -c \
  "INSERT INTO tde_qa VALUES (2003, repeat('${MARKER}_POST_REWIND_', 16))" \
  >"${LOG_DIR}/post-rewind-source.log" 2>&1

for unused in $(seq 1 30); do
  rewind_state=$("${PRIMARY_PSQL[@]}" -Atc \
    "SELECT pg_is_in_recovery()::int || '|' ||
            (SELECT count(*) FROM tde_qa WHERE id IN (2001,2003)) || '|' ||
            (SELECT count(*) FROM tde_qa WHERE id = 2002) || '|' ||
            _pg_tde.pg_tde_is_encrypted('tde_qa')::int")
  [[ "${rewind_state}" == '1|2|0|1' ]] && break
  sleep 1
done
[[ "${rewind_state:-}" == '1|2|0|1' ]] || \
  fail "rewound cluster state is ${rewind_state:-unavailable}, expected 1|2|0|1"

relation_path=$("${STANDBY_PSQL[@]}" -Atc \
  "SELECT current_setting('data_directory') || '/' || pg_relation_filepath('tde_qa')")
runuser -u postgres -- "${PGROOT}/bin/pg_ctl" -D "${PRIMARY_DATA}" \
  -m fast -w stop >"${LOG_DIR}/primary-final-stop.log" 2>&1
primary_started=0
runuser -u postgres -- "${PGROOT}/bin/pg_ctl" -D "${STANDBY_DATA}" \
  -m fast -w stop >"${LOG_DIR}/standby-final-stop.log" 2>&1
standby_started=0

if LC_ALL=C grep -aF "${MARKER}" "${relation_path}"* >/dev/null 2>&1; then
  fail 'plaintext marker found in the encrypted relation files'
fi

printf '[RESULT] server=%s extensions=%s/%s encrypted=1 basebackup=pass rewind=pass plaintext=absent\n' \
  "${server_version}" "${installed_extensions}" "${expected_extensions}"
