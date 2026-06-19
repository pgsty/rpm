#!/bin/bash

set -euo pipefail

PROG_NAME="$(basename "$0")"
BIN_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${BIN_DIR}/.." && pwd)"
SRC_DIR="${ROOT_DIR}/src"
PATCH_DIR="${ROOT_DIR}/rpmbuild/SPECS/patches"

PG_MAJOR="${PG_MAJOR:-18}"
if [ -z "${PATCHSET:-}" ]; then
    case "${PG_MAJOR}" in
        16) PATCHSET=47 ;;
        17) PATCHSET=20 ;;
        18) PATCHSET=1 ;;
        *)
            echo "unsupported PG_MAJOR for OrioleDB beta16: ${PG_MAJOR}" >&2
            exit 1
            ;;
    esac
fi
SRC_ROOT="postgres-patches${PG_MAJOR}_${PATCHSET}"
SRC_ARCHIVE="${SRC_DIR}/${SRC_ROOT}.tar.gz"
PATCH_FILE="${PATCH_DIR}/oriolepg-postgresql-branding.patch"
WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/${PROG_NAME}.XXXXXX")"

cleanup() {
    rm -rf "${WORKDIR}"
}
trap cleanup EXIT

if [ ! -f "${SRC_ARCHIVE}" ]; then
    echo "missing upstream tarball: ${SRC_ARCHIVE}" >&2
    exit 1
fi

mkdir -p "${PATCH_DIR}" "${WORKDIR}/orig" "${WORKDIR}/mod"

echo "extracting ${SRC_ARCHIVE}"
tar -xzf "${SRC_ARCHIVE}" -C "${WORKDIR}/orig"
tar -xzf "${SRC_ARCHIVE}" -C "${WORKDIR}/mod"

echo "applying OrioleDB branding in three version-string locations"
perl -0pi -e 's/PostgreSQL \$PG_VERSION on/OrioleDB \$PG_VERSION on/' \
    "${WORKDIR}/mod/${SRC_ROOT}/configure" \
    "${WORKDIR}/mod/${SRC_ROOT}/configure.ac"
perl -0pi -e 's/PostgreSQL @0@ on/OrioleDB @0@ on/' \
    "${WORKDIR}/mod/${SRC_ROOT}/meson.build"

echo "writing ${PATCH_FILE}"
{
    cat <<'PATCH'
diff --git a/configure b/configure
--- a/configure
+++ b/configure
@@ -1,3 +1,3 @@
 cat >>confdefs.h <<_ACEOF
-#define PG_VERSION_STR "PostgreSQL $PG_VERSION on $host, compiled by $cc_string, `expr $ac_cv_sizeof_void_p \* 8`-bit"
+#define PG_VERSION_STR "OrioleDB $PG_VERSION on $host, compiled by $cc_string, `expr $ac_cv_sizeof_void_p \* 8`-bit"
 _ACEOF
diff --git a/configure.ac b/configure.ac
--- a/configure.ac
+++ b/configure.ac
@@ -1,3 +1,3 @@
 AC_DEFINE_UNQUOTED(PG_VERSION_STR,
-                   ["PostgreSQL $PG_VERSION on $host, compiled by $cc_string, `expr $ac_cv_sizeof_void_p \* 8`-bit"],
+                   ["OrioleDB $PG_VERSION on $host, compiled by $cc_string, `expr $ac_cv_sizeof_void_p \* 8`-bit"],
                    [A string containing the version number, platform, and C compiler])
diff --git a/meson.build b/meson.build
--- a/meson.build
+++ b/meson.build
@@ -1,3 +1,3 @@
 cdata.set_quoted('PG_VERSION_STR',
-  'PostgreSQL @0@ on @1@-@2@, compiled by @3@-@4@, @5@-bit'.format(
+  'OrioleDB @0@ on @1@-@2@, compiled by @3@-@4@, @5@-bit'.format(
     pg_version, host_machine.cpu_family(), host_system,
PATCH
} > "${PATCH_FILE}"

echo "done"
grep -n 'OrioleDB .* on' \
    "${WORKDIR}/mod/${SRC_ROOT}/configure" \
    "${WORKDIR}/mod/${SRC_ROOT}/configure.ac" \
    "${WORKDIR}/mod/${SRC_ROOT}/meson.build"
