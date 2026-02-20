#!/usr/bin/env bash
#==============================================================#
# File      :   babelfish.sh
# Desc      :   build babelfish source tarball + antlr source zip
# Ctime     :   2026-02-18
# Path      :   bin/babelfish.sh
#==============================================================#
set -euo pipefail

BIN_DIR="$(cd "$(dirname "$0")" && pwd)"
SRC_DIR="$(cd "${BIN_DIR}/../src" && pwd)"

PG_VERSION="${1:-17.8}"
BBF_VERSION="${2:-5.5.0}"
PG_REF="${3:-BABEL_5_5_STABLE__PG_17_8}"
EXT_REF="${4:-BABEL_5_5_STABLE}"
ANTLR_VERSION="${5:-4.13.2}"

PG_DIR_PREFIX="postgresql_modified_for_babelfish"
EXT_DIR_PREFIX="babelfish_extensions"
PACKAGE_NAME="babelfishpg-${PG_VERSION}-${BBF_VERSION}"
PG_TARBALL_URL="https://codeload.github.com/babelfish-for-postgresql/postgresql_modified_for_babelfish/tar.gz/refs/heads/${PG_REF}"
EXT_TARBALL_URL="https://codeload.github.com/babelfish-for-postgresql/babelfish_extensions/tar.gz/refs/heads/${EXT_REF}"
ANTLR_ZIP="antlr4-cpp-runtime-${ANTLR_VERSION}-source.zip"
ANTLR_URL="https://www.antlr.org/download/${ANTLR_ZIP}"

PROXY_URL="${BABELFISH_PROXY:-${HTTPS_PROXY:-${https_proxy:-${HTTP_PROXY:-${http_proxy:-${ALL_PROXY:-${all_proxy:-}}}}}}}"

if command -v gtar >/dev/null 2>&1; then
  TAR_BIN="gtar"
else
  TAR_BIN="tar"
fi

TMP_DIR="$(mktemp -d)"
cleanup() {
  rm -rf "${TMP_DIR}"
}
trap cleanup EXIT

if [[ -z "${PROXY_URL}" ]]; then
  V2RAY_CFG="/opt/homebrew/etc/v2ray/config.json"
  if [[ -r "${V2RAY_CFG}" ]]; then
    V2RAY_PROXY="$(perl -0777 -ne 'if (/"inbounds"\s*:\s*\[\s*\{.*?"port"\s*:\s*([0-9]+).*?"protocol"\s*:\s*"([^"]+)"/s) { print "$2://127.0.0.1:$1\n" }' "${V2RAY_CFG}")"
    case "${V2RAY_PROXY}" in
      http://*|https://*) PROXY_URL="${V2RAY_PROXY}" ;;
      socks://*|socks5://*) PROXY_URL="${V2RAY_PROXY}" ;;
      socks) PROXY_URL="socks5h://127.0.0.1:1080" ;;
    esac
  fi
fi

echo "[INFO] source dir: ${SRC_DIR}"
echo "[INFO] pg ref: ${PG_REF}"
echo "[INFO] ext ref: ${EXT_REF}"
echo "[INFO] pg version: ${PG_VERSION}"
echo "[INFO] babelfish version: ${BBF_VERSION}"
echo "[INFO] antlr version: ${ANTLR_VERSION}"
if [[ -n "${PROXY_URL}" ]]; then
  echo "[INFO] proxy: ${PROXY_URL}"
else
  echo "[WARN] no proxy configured; download may be slow" >&2
fi

download_archive() {
  local url="$1"
  local out="$2"
  local attempt=1
  local max_attempt=5
  local use_proxy=0
  if [[ -n "${PROXY_URL}" ]]; then
    use_proxy=1
  fi
  while (( attempt <= max_attempt )); do
    local -a curl_args=( -fL --http1.1 --silent --show-error --retry 5 --retry-all-errors --retry-delay 2 --connect-timeout 30 -o "${out}" "${url}" )
    if (( use_proxy == 1 )); then
      curl_args=( --proxy "${PROXY_URL}" "${curl_args[@]}" )
    fi
    if curl "${curl_args[@]}"; then
      return 0
    fi
    if (( use_proxy == 1 )); then
      echo "[WARN] proxy download failed; retrying direct connection: ${url}" >&2
      use_proxy=0
      continue
    fi
    echo "[WARN] download failed (attempt ${attempt}/${max_attempt}): ${url}" >&2
    sleep 2
    attempt=$((attempt + 1))
  done
  return 1
}

echo "[INFO] downloading upstream archives..."
download_archive "${PG_TARBALL_URL}" "${TMP_DIR}/pg.tar.gz"
download_archive "${EXT_TARBALL_URL}" "${TMP_DIR}/ext.tar.gz"
download_archive "${ANTLR_URL}" "${TMP_DIR}/${ANTLR_ZIP}"

${TAR_BIN} -xzf "${TMP_DIR}/pg.tar.gz" -C "${TMP_DIR}"
${TAR_BIN} -xzf "${TMP_DIR}/ext.tar.gz" -C "${TMP_DIR}"

PG_DIR="$(find "${TMP_DIR}" -maxdepth 1 -type d -name "${PG_DIR_PREFIX}-*" | head -n 1)"
EXT_DIR="$(find "${TMP_DIR}" -maxdepth 1 -type d -name "${EXT_DIR_PREFIX}-*" | head -n 1)"
if [[ -z "${PG_DIR}" || -z "${EXT_DIR}" ]]; then
  echo "[FAIL] cannot locate extracted upstream directories (${PG_REF}, ${EXT_REF})" >&2
  exit 1
fi

PACKAGE_ROOT="${SRC_DIR}/${PACKAGE_NAME}"
rm -rf "${PACKAGE_ROOT}" "${SRC_DIR}/${PACKAGE_NAME}.tar.gz"
mkdir -p "${PACKAGE_ROOT}/postgresql_modified_for_babelfish" \
         "${PACKAGE_ROOT}/babelfish_extensions" \
         "${PACKAGE_ROOT}/third_party"

cp -a "${PG_DIR}/." "${PACKAGE_ROOT}/postgresql_modified_for_babelfish/"
cp -a "${EXT_DIR}/." "${PACKAGE_ROOT}/babelfish_extensions/"
cp -f "${TMP_DIR}/${ANTLR_ZIP}" "${PACKAGE_ROOT}/third_party/${ANTLR_ZIP}"
cp -f "${TMP_DIR}/${ANTLR_ZIP}" "${SRC_DIR}/${ANTLR_ZIP}"

echo "[INFO] applying branding edits (PostgreSQL -> Babelfish in version string)..."
perl -0pi -e 's/PostgreSQL \$PG_VERSION on/Babelfish \$PG_VERSION on/g' "${PACKAGE_ROOT}/postgresql_modified_for_babelfish/configure.ac"
perl -0pi -e "s/'PostgreSQL \@0\@ on \@1\@-\@2\@, compiled by \@3\@-\@4\@, \@5\@-bit'/'Babelfish \@0\@ on \@1\@-\@2\@, compiled by \@3\@-\@4\@, \@5\@-bit'/g" "${PACKAGE_ROOT}/postgresql_modified_for_babelfish/meson.build"
perl -0pi -e 's/PostgreSQL \$PG_VERSION on \$host, compiled by/Babelfish \$PG_VERSION on \$host, compiled by/g' "${PACKAGE_ROOT}/postgresql_modified_for_babelfish/configure"

echo "[INFO] applying babelfish tsql build fix (antlr4 runtime include path)..."
perl -0pi -e 's/PG_CPPFLAGS \+= -I\$\(TSQLSRC\) -I\$\(PG_SRC\) -DFAULT_INJECTOR -Wfloat-conversion/PG_CPPFLAGS += -I\$(ANTLR4_RUNTIME_INCLUDE_DIR) -I\$(TSQLSRC) -I\$(PG_SRC) -DFAULT_INJECTOR -Wfloat-conversion/g' "${PACKAGE_ROOT}/babelfish_extensions/contrib/babelfishpg_tsql/Makefile"

echo "[INFO] applying babelfish tds build fix (exclude fault injection test source)..."
if ! grep -q 'fault_injection/fault_injection_tests.c' "${PACKAGE_ROOT}/babelfish_extensions/contrib/babelfishpg_tds/Makefile"; then
  cat >> "${PACKAGE_ROOT}/babelfish_extensions/contrib/babelfishpg_tds/Makefile" <<'EOS'

# Exclude fault injection test source; it fails with strict -Werror flags on PG17 builds.
tds_exclude_files += $(tds_top_dir)/src/backend/fault_injection/fault_injection_tests.c
EOS
fi

BUILD_DATE_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
cat > "${PACKAGE_ROOT}/SOURCE_MANIFEST" <<EOS
name=babelfishpg
pg_version=${PG_VERSION}
babelfish_version=${BBF_VERSION}
build_date_utc=${BUILD_DATE_UTC}
core_url=${PG_TARBALL_URL}
core_ref=${PG_REF}
ext_url=${EXT_TARBALL_URL}
ext_ref=${EXT_REF}
antlr_runtime_source=${ANTLR_ZIP}
EOS

echo "[INFO] patch verification:"
grep -n 'Babelfish .*\$PG_VERSION on' "${PACKAGE_ROOT}/postgresql_modified_for_babelfish/configure.ac"
grep -n "Babelfish @0@ on @1@-@2@" "${PACKAGE_ROOT}/postgresql_modified_for_babelfish/meson.build"
grep -n 'Babelfish \$PG_VERSION on \$host' "${PACKAGE_ROOT}/postgresql_modified_for_babelfish/configure"
grep -n 'PG_CPPFLAGS += -I\$(ANTLR4_RUNTIME_INCLUDE_DIR)' "${PACKAGE_ROOT}/babelfish_extensions/contrib/babelfishpg_tsql/Makefile"
grep -n 'fault_injection/fault_injection_tests.c' "${PACKAGE_ROOT}/babelfish_extensions/contrib/babelfishpg_tds/Makefile"

find "${PACKAGE_ROOT}" -type f -name '._*' -delete
COPYFILE_DISABLE=1 ${TAR_BIN} -czf "${SRC_DIR}/${PACKAGE_NAME}.tar.gz" -C "${SRC_DIR}" "${PACKAGE_NAME}"
rm -rf "${PACKAGE_ROOT}"

echo "[ OK ] created ${SRC_DIR}/${PACKAGE_NAME}.tar.gz"
echo "[ OK ] created ${SRC_DIR}/${ANTLR_ZIP}"
