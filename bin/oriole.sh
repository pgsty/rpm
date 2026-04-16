#!/bin/bash

set -euo pipefail

PROG_NAME="$(basename "$0")"
BIN_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "${BIN_DIR}/.." && pwd)"
SRC_DIR="${ROOT_DIR}/src"
PATCH_DIR="${ROOT_DIR}/rpmbuild/SPECS/patches"

PG_MAJOR="${PG_MAJOR:-17}"
PATCHSET="${PATCHSET:-18}"
SRC_ROOT="postgres-patches${PG_MAJOR}_${PATCHSET}"
SRC_ARCHIVE="${SRC_DIR}/${SRC_ROOT}.tar.gz"
PATCH_FILE="${PATCH_DIR}/oriolepg-postgresql-branding.patch"
WORKDIR="$(mktemp -d "${TMPDIR:-/tmp}/${PROG_NAME}.XXXXXX")"

cleanup() {
    rm -rf "${WORKDIR}"
}
trap cleanup EXIT

emit_diff() {
    local relpath="$1"
    local tmpfile="${WORKDIR}/$(echo "${relpath}" | tr '/' '_').patch"
    local status=0

    diff -u "${WORKDIR}/orig/${SRC_ROOT}/${relpath}" "${WORKDIR}/mod/${SRC_ROOT}/${relpath}" > "${tmpfile}" || status=$?
    if [ "${status}" -ne 0 ] && [ "${status}" -ne 1 ]; then
        echo "failed to diff ${relpath}" >&2
        exit 1
    fi

    sed \
        -e "1s|${WORKDIR}/orig/${SRC_ROOT}/${relpath}|a/${relpath}|" \
        -e "2s|${WORKDIR}/mod/${SRC_ROOT}/${relpath}|b/${relpath}|" \
        "${tmpfile}"
}

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
    emit_diff configure
    emit_diff configure.ac
    emit_diff meson.build
} > "${PATCH_FILE}"

echo "done"
grep -n 'OrioleDB .* on' \
    "${WORKDIR}/mod/${SRC_ROOT}/configure" \
    "${WORKDIR}/mod/${SRC_ROOT}/configure.ac" \
    "${WORKDIR}/mod/${SRC_ROOT}/meson.build"
