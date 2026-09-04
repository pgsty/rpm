#!/bin/bash
set -euo pipefail

usage() {
    echo 'usage: verify-rpm-extension-job.sh OUTPUT_DIR SPEC PACKAGE_TEMPLATE PG EXPECTED_ARCH [enabled|disabled]' >&2
    exit 2
}

die() {
    echo "$*" >&2
    exit 1
}

[[ $# -ge 5 && $# -le 6 ]] || usage
OUTPUT_DIR=$1
SPEC=$2
PACKAGE_TEMPLATE=$3
PG=$4
EXPECTED_ARCH=$5
LLVM_MODE=${6:-enabled}
FORBIDDEN_RUNTIME_RE='(^|[[:space:]/])(llvm|clang)[[:alnum:]_.+-]*([[:space:](]|$)|libLLVM|libclang|postgresql[0-9]+-llvmjit'

[[ -d "$OUTPUT_DIR" ]] || die "missing output directory: $OUTPUT_DIR"
[[ -f "$SPEC" ]] || die "missing spec: $SPEC"
SPEC_DIR=$(cd -P "$(dirname "$SPEC")" && pwd)
[[ $(basename "$SPEC_DIR") == SPECS ]] || die "spec must be located under a SPECS directory: $SPEC"
SPEC_TOPDIR=$(cd -P "$SPEC_DIR/.." && pwd)
# The package template must contain a literal token.
# shellcheck disable=SC2016
[[ "$PACKAGE_TEMPLATE" == *'$v'* ]] || die 'package template must contain literal $v'
[[ "$PG" =~ ^(14|15|16|17|18)$ ]] || die "unsupported PostgreSQL major: $PG"
case "$EXPECTED_ARCH" in
    x86_64|aarch64) ;;
    *) die "unsupported expected architecture: $EXPECTED_ARCH" ;;
esac
case "$LLVM_MODE" in
    enabled|disabled) ;;
    *) usage ;;
esac

for command in rpm rpmspec rpm2cpio cpio file readelf; do
    command -v "$command" >/dev/null || die "required command is missing: $command"
done
TMP_ROOT=$(mktemp -d)
trap 'rm -rf "$TMP_ROOT"' EXIT

RPM_ARGS=(--target "$EXPECTED_ARCH" --define "_topdir $SPEC_TOPDIR" --define "pgmajorversion $PG")
if [[ "$LLVM_MODE" == disabled ]]; then
    RPM_ARGS+=(--define 'llvm 0')
fi

MAIN_PACKAGE=${PACKAGE_TEMPLATE//\$v/$PG}
DEBUG_PACKAGE="$MAIN_PACKAGE-debuginfo"
DEBUGSOURCE_PACKAGE="$MAIN_PACKAGE-debugsource"

RPMSPEC_QUERY="$TMP_ROOT/rpmspec-packages.tsv"
if ! rpmspec -q --qf '%{NAME}\t%{EPOCHNUM}:%{VERSION}-%{RELEASE}\t%{ARCH}\n' \
    "${RPM_ARGS[@]}" "$SPEC" >"$RPMSPEC_QUERY"; then
    die 'rpmspec package query failed'
fi
sort -u "$RPMSPEC_QUERY" >"$TMP_ROOT/rpmspec-packages.sorted.tsv" || die 'cannot sort rpmspec package query'

EXPLICIT_PACKAGES=()
declare -A EXPLICIT_EVR=()
declare -A EXPLICIT_ARCH=()
while IFS=$'\t' read -r package evr arch; do
    [[ -n "$package" && -n "$evr" && -n "$arch" ]] || die 'rpmspec returned incomplete package metadata'
    EXPLICIT_PACKAGES+=("$package")
    EXPLICIT_EVR[$package]=$evr
    EXPLICIT_ARCH[$package]=$arch
done <"$TMP_ROOT/rpmspec-packages.sorted.tsv"
[[ ${#EXPLICIT_PACKAGES[@]} -gt 0 ]] || die 'rpmspec generated no binary packages'

for package in "${EXPLICIT_PACKAGES[@]}"; do
    [[ "$package" != *-llvmjit ]] || die "rpmspec still generates extension llvmjit package: $package"
done
EXPECTED_PACKAGES=("${EXPLICIT_PACKAGES[@]}")

declare -A EXPECTED_SET=()
declare -A EXPECTED_EVR=()
declare -A EXPECTED_PACKAGE_ARCH=()
for package in "${EXPECTED_PACKAGES[@]}"; do
    EXPECTED_SET[$package]=1
    if [[ -n ${EXPLICIT_EVR[$package]+x} ]]; then
        EXPECTED_EVR[$package]=${EXPLICIT_EVR[$package]}
        EXPECTED_PACKAGE_ARCH[$package]=${EXPLICIT_ARCH[$package]}
    fi
done
[[ -n ${EXPECTED_SET[$MAIN_PACKAGE]+x} ]] || die "rpmspec lacks main package: $MAIN_PACKAGE"
if [[ "$MAIN_PACKAGE" == "pg_bulkload_$PG" ]]; then
    CLIENT_PACKAGE="$MAIN_PACKAGE-client"
    CLIENT_DEBUG_PACKAGE="$CLIENT_PACKAGE-debuginfo"
    [[ -n ${EXPECTED_SET[$CLIENT_PACKAGE]+x} ]] || die "pg_bulkload rpmspec lacks explicit client package: $CLIENT_PACKAGE"
    if [[ -z ${EXPECTED_SET[$CLIENT_DEBUG_PACKAGE]+x} ]]; then
        EXPECTED_PACKAGES+=("$CLIENT_DEBUG_PACKAGE")
        EXPECTED_SET[$CLIENT_DEBUG_PACKAGE]=1
        EXPECTED_EVR[$CLIENT_DEBUG_PACKAGE]=${EXPECTED_EVR[$CLIENT_PACKAGE]}
        EXPECTED_PACKAGE_ARCH[$CLIENT_DEBUG_PACKAGE]=${EXPECTED_PACKAGE_ARCH[$CLIENT_PACKAGE]}
    fi
fi
[[ -n ${EXPECTED_SET[$DEBUG_PACKAGE]+x} ]] || die "EL rpmspec lacks debuginfo package: $DEBUG_PACKAGE"
[[ -n ${EXPECTED_SET[$DEBUGSOURCE_PACKAGE]+x} ]] || die "EL rpmspec lacks debugsource package: $DEBUGSOURCE_PACKAGE"

shopt -s nullglob
ARTIFACTS=("$OUTPUT_DIR"/*.rpm)
[[ ${#ARTIFACTS[@]} -gt 0 ]] || die "no RPM artifacts in $OUTPUT_DIR"
declare -A ARTIFACT_BY_PACKAGE=()
declare -A ARTIFACT_EVR=()
declare -A ARTIFACT_ARCH=()
artifact_index=0
for artifact in "${ARTIFACTS[@]}"; do
    artifact_index=$((artifact_index + 1))
    metadata="$TMP_ROOT/artifact-$artifact_index.tsv"
    if ! rpm -qp --qf '%{NAME}\t%{EPOCHNUM}:%{VERSION}-%{RELEASE}\t%{ARCH}\n' \
        "$artifact" >"$metadata"; then
        die "cannot query artifact metadata: $artifact"
    fi
    [[ $(wc -l <"$metadata") -eq 1 ]] || die "artifact query returned multiple rows: $artifact"
    IFS=$'\t' read -r package evr arch <"$metadata"
    [[ -n "$package" && -n "$evr" && -n "$arch" ]] || die "incomplete artifact metadata: $artifact"
    [[ "$arch" != src && "$arch" != nosrc ]] || die "source RPM is not a binary artifact: $artifact"
    [[ -z ${ARTIFACT_BY_PACKAGE[$package]+x} ]] || die "duplicate artifact package: $package"
    ARTIFACT_BY_PACKAGE[$package]=$artifact
    ARTIFACT_EVR[$package]=$evr
    ARTIFACT_ARCH[$package]=$arch
    [[ "$package" != *-llvmjit ]] || die "extension llvmjit artifact is forbidden: $artifact"
    [[ "$artifact" != *-llvmjit-*.rpm ]] || die "extension llvmjit filename is forbidden: $artifact"
done

for package in "${EXPECTED_PACKAGES[@]}"; do
    [[ -n ${ARTIFACT_BY_PACKAGE[$package]+x} ]] || die "missing expected artifact: $package"
done
for package in "${!ARTIFACT_BY_PACKAGE[@]}"; do
    [[ -n ${EXPECTED_SET[$package]+x} ]] || die "unexpected artifact package: $package"
    [[ ${ARTIFACT_EVR[$package]} == "${EXPECTED_EVR[$package]}" ]] || \
        die "artifact EVR mismatch: $package=${ARTIFACT_EVR[$package]} expected=${EXPECTED_EVR[$package]}"
    arch=${ARTIFACT_ARCH[$package]}
    [[ "$arch" == "${EXPECTED_PACKAGE_ARCH[$package]}" ]] || \
        die "wrong artifact architecture: $package=$arch expected=${EXPECTED_PACKAGE_ARCH[$package]}"
done

MAIN_RPM=${ARTIFACT_BY_PACKAGE[$MAIN_PACKAGE]}
MAIN_PAYLOAD="$TMP_ROOT/main-payload.txt"
rpm -qpl "$MAIN_RPM" >"$MAIN_PAYLOAD" || die 'cannot query main payload'
BITCODE_COUNT=$(grep -Ec '/lib/bitcode/.*\.bc$' "$MAIN_PAYLOAD" || true)
INDEX_COUNT=$(grep -Ec '/lib/bitcode/.*\.index\.bc$' "$MAIN_PAYLOAD" || true)
if [[ "$LLVM_MODE" == enabled ]]; then
    [[ $BITCODE_COUNT -gt 0 && $INDEX_COUNT -gt 0 ]] || die 'enabled main package lacks bitcode or index'
else
    [[ $BITCODE_COUNT -eq 0 ]] || die 'disabled main package contains bitcode'
fi

for package in "${EXPECTED_PACKAGES[@]}"; do
    [[ "$package" == "$MAIN_PACKAGE" || "$package" == "$DEBUG_PACKAGE" || "$package" == "$DEBUGSOURCE_PACKAGE" ]] && continue
    payload="$TMP_ROOT/payload-${package}.txt"
    rpm -qpl "${ARTIFACT_BY_PACKAGE[$package]}" >"$payload" || die "cannot query companion payload: $package"
    ! grep -Eq '/lib/bitcode/.*\.bc$' "$payload" || die "companion owns extension bitcode: $package"
done

RUNTIME_REQUIRES="$TMP_ROOT/main-requires.txt"
rpm -qp --requires "$MAIN_RPM" >"$RUNTIME_REQUIRES" || die 'cannot query main Requires'
! grep -Eiq "$FORBIDDEN_RUNTIME_RE" "$RUNTIME_REQUIRES" || \
    die 'main package has forbidden LLVM, Clang, or core llvmjit runtime dependency'
PROVIDES="$TMP_ROOT/main-provides.txt"
OBSOLETES="$TMP_ROOT/main-obsoletes.txt"
rpm -qp --provides "$MAIN_RPM" >"$PROVIDES" || die 'cannot query main Provides'
rpm -qp --obsoletes "$MAIN_RPM" >"$OBSOLETES" || die 'cannot query main Obsoletes'
! grep -Eq -- '-llvmjit([ (=]|$)' "$PROVIDES" || die 'main package has forbidden llvmjit Provides'
! grep -Eq -- '-llvmjit([ (<=>]|$)' "$OBSOLETES" || die 'main package has forbidden llvmjit Obsoletes'

mkdir "$TMP_ROOT/main" "$TMP_ROOT/debug" "$TMP_ROOT/source"
(cd "$TMP_ROOT/main" && rpm2cpio "$MAIN_RPM" | cpio -idm --quiet)
(cd "$TMP_ROOT/debug" && rpm2cpio "${ARTIFACT_BY_PACKAGE[$DEBUG_PACKAGE]}" | cpio -idm --quiet)
(cd "$TMP_ROOT/source" && rpm2cpio "${ARTIFACT_BY_PACKAGE[$DEBUGSOURCE_PACKAGE]}" | cpio -idm --quiet)

mapfile -d '' -t MAIN_BITCODE_FILES < <(
    find "$TMP_ROOT/main" -type f -path '*/lib/bitcode/*.bc' -print0
)
if [[ "$LLVM_MODE" == enabled ]]; then
    [[ ${#MAIN_BITCODE_FILES[@]} -eq $BITCODE_COUNT ]] || die 'main bitcode payload count changed after extraction'
    extracted_indexes=0
    for bitcode in "${MAIN_BITCODE_FILES[@]}"; do
        [[ -s "$bitcode" ]] || die "empty bitcode payload: $bitcode"
        [[ "$bitcode" == *.index.bc ]] && extracted_indexes=$((extracted_indexes + 1))
    done
    [[ $extracted_indexes -eq $INDEX_COUNT && $extracted_indexes -gt 0 ]] || die 'main bitcode index payload is missing or empty'
else
    [[ ${#MAIN_BITCODE_FILES[@]} -eq 0 ]] || die 'disabled main package contains extracted bitcode'
fi

mapfile -d '' -t MAIN_ELFS < <(
    while IFS= read -r -d '' candidate; do
        file -b "$candidate" | grep -q '^ELF ' && printf '%s\0' "$candidate"
    done < <(find "$TMP_ROOT/main" -type f -size +0c -print0)
)
[[ ${#MAIN_ELFS[@]} -gt 0 ]] || die 'main package contains no native ELF'
for elf in "${MAIN_ELFS[@]}"; do
    notes=$(mktemp "$TMP_ROOT/notes.XXXXXX")
    readelf -n "$elf" >"$notes"
    mapfile -t build_ids < <(sed -n 's/.*Build ID:[[:space:]]*//p' "$notes")
    [[ ${#build_ids[@]} -eq 1 && ${build_ids[0]} =~ ^[0-9a-f]{40}$ ]] || die "invalid Build ID: $elf"
    build_id=${build_ids[0]}
    debuglink_dump=$(mktemp "$TMP_ROOT/debuglink.XXXXXX")
    debuglink=''
    if readelf --string-dump=.gnu_debuglink "$elf" >"$debuglink_dump" 2>/dev/null; then
        mapfile -t debuglink_values < <(sed -n 's/^[[:space:]]*\[[^]]*\][[:space:]]*//p' "$debuglink_dump")
        debuglink=${debuglink_values[0]:-}
    fi
    if [[ -n "$debuglink" ]]; then
        [[ "$debuglink" != */* && "$debuglink" != . && "$debuglink" != .. ]] || \
            die "unsafe .gnu_debuglink: $elf -> $debuglink"
        relative_elf=${elf#"$TMP_ROOT/main"}
        [[ "$relative_elf" == /* ]] || die "cannot map main ELF path: $elf"
        debug_file="$TMP_ROOT/debug/usr/lib/debug$(dirname "$relative_elf")/$debuglink"
        [[ -f "$debug_file" && ! -L "$debug_file" && -s "$debug_file" ]] || \
            die "missing matching debuglink file: $elf -> $debug_file"
    else
        debug_file="$TMP_ROOT/debug/usr/lib/debug/.build-id/${build_id:0:2}/${build_id:2}.debug"
    fi
    [[ -s "$debug_file" ]] || die "missing matching debug file: $elf"
    debug_notes=$(mktemp "$TMP_ROOT/debug-notes.XXXXXX")
    readelf -n "$debug_file" >"$debug_notes"
    mapfile -t debug_build_ids < <(sed -n 's/.*Build ID:[[:space:]]*//p' "$debug_notes")
    [[ ${#debug_build_ids[@]} -eq 1 && ${debug_build_ids[0]} == "$build_id" ]] || \
        die "debug file Build ID mismatch: $elf -> $debug_file"
    sections=$(mktemp "$TMP_ROOT/sections.XXXXXX")
    readelf -SW "$debug_file" >"$sections"
    grep -Fq .debug_info "$sections" || die "debug file lacks .debug_info: $debug_file"
done

SOURCE_FILE=$(find "$TMP_ROOT/source/usr/src/debug" -type f -size +0c -print -quit 2>/dev/null || true)
[[ -n "$SOURCE_FILE" ]] || die 'debugsource package has no non-empty source file'

printf 'verified main=%s mode=%s arch=%s bitcode=%s index=%s elf=%s packages=%s\n' \
    "$MAIN_PACKAGE" "$LLVM_MODE" "$EXPECTED_ARCH" "$BITCODE_COUNT" "$INDEX_COUNT" \
    "${#MAIN_ELFS[@]}" "${#EXPECTED_PACKAGES[@]}"
