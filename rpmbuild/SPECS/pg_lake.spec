%define debug_package %{nil}
%global pname pg_lake
%global sname pg_lake
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global vcpkg_version 2025.10.17
%global vcpkg_commit 74e6536215718009aae747d86d84b78376bf9e09
%global source_sha256 fd9fd38b723448a93f3a8265f60655560f8044198cf9c96df26b992cd0b2f2c0

# The bundled runtimes are private implementation details.  Do not let their
# generic SONAMEs satisfy unrelated packages, and do not emit external
# requirements for the two libraries resolved by the package's RUNPATHs.
%global __provides_exclude_from ^%{pginstdir}/lib/pg_lake/.*\\.so.*$
%global __requires_exclude ^(libduckdb\\.so|libavro\\.so\\.24).*$

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:pg_lake 3.4.0 only supports PostgreSQL 16 through 18}
%endif

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        3.4.0
Release:        1PIGSTY%{?dist}
Summary:        PostgreSQL lakehouse extensions powered by DuckDB
License:        Apache-2.0 AND MIT AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND ICU AND ISC AND PostgreSQL AND Unicode-3.0 AND Zlib AND curl AND OpenSSL AND LicenseRef-TPC-EULA-2.2
URL:            https://github.com/Snowflake-Labs/pg_lake
# Repacked upstream release with the pinned Avro, DuckDB, and duckdb-postgres
# submodules required by the build.  SHA256 is verified in %%prep.
Source0:        %{sname}-%{version}.tar.gz
Patch0:         pg_lake-3.4.0-pg-libdir.patch

BuildRequires:  postgresql%{pgmajorversion}-devel
BuildRequires:  pgdg-srpm-macros >= 1.0.27
BuildRequires:  autoconf automake binutils bison ca-certificates cmake curl
BuildRequires:  diffutils file flex gcc gcc-c++ git jq libtool make sed
BuildRequires:  ninja-build patch perl python3 unzip which zip
BuildRequires:  pkgconf-pkg-config
BuildRequires:  jansson-devel krb5-devel libcurl-devel libselinux-devel
BuildRequires:  libxml2-devel libxslt-devel lz4-devel libzstd-devel
BuildRequires:  numactl-devel openssl-devel pam-devel readline-devel
BuildRequires:  snappy-devel xz-devel
%if 0%{?rhel} >= 10
BuildRequires:  zlib-ng-compat-devel
%else
BuildRequires:  zlib-devel
%endif
Requires:       postgresql%{pgmajorversion}-server
Requires:       postgresql%{pgmajorversion}-contrib
Suggests:       awscli2

%description
pg_lake integrates Iceberg tables and Parquet, CSV, and JSON data lake files
with PostgreSQL. It provides transactional Iceberg access and delegates
analytical execution to a bundled DuckDB engine through pgduck_server.

This package is self-contained for one PostgreSQL major version. Its DuckDB
and Avro libraries live in a pg_lake-private directory so that pg_duckdb can
be installed for the same PostgreSQL major without a file collision. Before
use, add pg_extension_base to shared_preload_libraries and start the versioned
pgduck_server binary. Its first start may download the DuckDB spatial extension.

%if %llvm
%package llvmjit
Summary:        Just-in-time compilation support for %{sname}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  clang-devel >= 19.0 llvm-devel >= 19.0
Requires:       llvm >= 19.0
%endif

%description llvmjit
This package provides LLVM bitcode for pg_lake's PostgreSQL modules.
%endif

%prep
test "$(sha256sum %{SOURCE0} | awk '{print $1}')" = "%{source_sha256}"
%autosetup -N -n %{sname}-%{version}
git apply --whitespace=nowarn %{PATCH0}

grep -qx 'version=%{version}' SOURCE_MANIFEST
grep -qx 'upstream_commit=9242798331c415358490587670e4b81a9d4eb4e7' SOURCE_MANIFEST
grep -qx 'avro_commit=2b11dba4fb28c7bb6ff08b40509a6a71fcaf4c21' SOURCE_MANIFEST
grep -qx 'duckdb_commit=6ddac802ffa9bcfbcc3f5f0d71de5dff9b0bc250' SOURCE_MANIFEST
grep -qx 'duckdb_postgres_commit=b63ef4b1eb007320840b6d1760f3c9b139bb3b49' SOURCE_MANIFEST
test "$(git rev-parse HEAD)" = '9242798331c415358490587670e4b81a9d4eb4e7'
test "$(git -C avro rev-parse HEAD)" = '2b11dba4fb28c7bb6ff08b40509a6a71fcaf4c21'
test "$(git -C duckdb_pglake/duckdb rev-parse HEAD)" = '6ddac802ffa9bcfbcc3f5f0d71de5dff9b0bc250'
test "$(git -C duckdb_pglake/duckdb-postgres rev-parse HEAD)" = 'b63ef4b1eb007320840b6d1760f3c9b139bb3b49'
grep -q 'GIT_TAG 13f8a814d41a978c3f19eb1dc76069489652ea6f' duckdb_pglake/extension_config.cmake
grep -q 'GIT_TAG bc15d211f282d1d78fc0d9fda3d09957ba776423' duckdb_pglake/extension_config.cmake
grep -q 'GIT_TAG 7e1ac3333d946a6bf5b4552722743e03f30a47cd' duckdb_pglake/extension_config.cmake

rm -rf .rpm-licenses
mkdir -p .rpm-licenses
cp LICENSE .rpm-licenses/pg_lake-LICENSE
cp avro/lang/c/LICENSE .rpm-licenses/avro-LICENSE
cp avro/lang/c/NOTICE .rpm-licenses/avro-NOTICE
cp duckdb_pglake/LICENSE .rpm-licenses/duckdb-pglake-LICENSE
cp duckdb_pglake/duckdb-postgres/LICENSE .rpm-licenses/duckdb-postgres-LICENSE
find duckdb_pglake/duckdb -type f \( -iname 'LICENSE*' -o -iname 'NOTICE*' \) -print | LC_ALL=C sort | while IFS= read -r license; do
    name="$(printf '%s' "${license#duckdb_pglake/duckdb/}" | tr '/' '-')"
    cp "$license" ".rpm-licenses/duckdb-$name"
done
# TPC EULA 2.2 clause 9 permits redistribution only without charge and
# requires this legend at the top of the distributed label and license.
{
    printf '%s\n\n' 'THE TPC SOFTWARE IS AVAILABLE WITHOUT CHARGE FROM TPC.'
    cat duckdb_pglake/duckdb/extension/tpch/dbgen/LICENSE
} > .rpm-licenses/duckdb-extension-tpch-dbgen-LICENSE
# The vendored miniz license is text despite its executable source mode and
# CRLF line endings. Normalize the packaged documentation only.
sed -i 's/\r$//' .rpm-licenses/duckdb-third_party-miniz-LICENSE

%build
VCPKG_ROOT="$HOME/.cache/pg_lake/vcpkg-%{vcpkg_version}"
VCPKG_BINARY_CACHE="$HOME/.cache/pg_lake/vcpkg-archives"
if [ ! -d "$VCPKG_ROOT/.git" ]; then
    rm -rf "$VCPKG_ROOT"
    mkdir -p "$(dirname "$VCPKG_ROOT")"
    git clone --depth 1 --branch "%{vcpkg_version}" \
        https://github.com/microsoft/vcpkg.git "$VCPKG_ROOT"
fi
test "$(git -C "$VCPKG_ROOT" describe --tags --exact-match)" = "%{vcpkg_version}"
test "$(git -C "$VCPKG_ROOT" rev-parse HEAD)" = "%{vcpkg_commit}"
test -z "$(git -C "$VCPKG_ROOT" status --porcelain --untracked-files=all --ignore-submodules=dirty)"
if [ ! -x "$VCPKG_ROOT/vcpkg" ]; then
    (cd "$VCPKG_ROOT" && ./bootstrap-vcpkg.sh -disableMetrics)
fi
mkdir -p "$VCPKG_BINARY_CACHE"
(cd duckdb_pglake && \
    VCPKG_DISABLE_METRICS=1 \
    VCPKG_DEFAULT_BINARY_CACHE="$VCPKG_BINARY_CACHE" \
    "$VCPKG_ROOT/vcpkg" install)

find duckdb_pglake/vcpkg_installed -path '*/share/*/copyright' -type f -print | LC_ALL=C sort | while IFS= read -r license; do
    component="$(basename "$(dirname "$license")")"
    case "$component" in vcpkg-cmake|vcpkg-cmake-config) continue ;; esac
    cp "$license" ".rpm-licenses/vcpkg-$component-copyright"
done

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/include

VCPKG_ROOT="$HOME/.cache/pg_lake/vcpkg-%{vcpkg_version}"
VCPKG_BINARY_CACHE="$HOME/.cache/pg_lake/vcpkg-archives"
test -f "$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake"
test -d "$VCPKG_BINARY_CACHE"
PG_CPPFLAGS="$(%{pginstdir}/bin/pg_config --cppflags)"
PG_LAKE_PREFIX_MAP="-ffile-prefix-map=%{buildroot}="

# Avro and DuckDB headers/libraries must be staged before their dependants are
# linked, so upstream's build and install are intentionally one ordered step.
%{__make} clean \
    PG_CONFIG=%{pginstdir}/bin/pg_config \
    PG_LIBDIR=%{pginstdir}/lib

CPATH="%{buildroot}%{pginstdir}/include${CPATH:+:$CPATH}" \
LIBRARY_PATH="%{buildroot}%{pginstdir}/lib${LIBRARY_PATH:+:$LIBRARY_PATH}" \
VCPKG_TOOLCHAIN_PATH="$VCPKG_ROOT/scripts/buildsystems/vcpkg.cmake" \
VCPKG_DISABLE_METRICS=1 \
VCPKG_DEFAULT_BINARY_CACHE="$VCPKG_BINARY_CACHE" \
PG_LAKE_GIT_VERSION="v%{version}" \
PG_LAKE_DELTA_SUPPORT=0 \
PGCOMPAT_BUILD_CONFIG=Release \
DUCKDB_BUILD_USE_CACHE=0 \
%{__make} \
    PG_CONFIG=%{pginstdir}/bin/pg_config \
    PG_LIBDIR=%{pginstdir}/lib \
    CPPFLAGS="$PG_CPPFLAGS $PG_LAKE_PREFIX_MAP" \
    EXT_RELEASE_FLAGS="-DBUILD_UNITTESTS=OFF -DBUILD_SHELL=OFF -DCMAKE_SKIP_BUILD_RPATH=ON" \
    DESTDIR=%{buildroot} install

# Headers are only an intermediate dependency for this build. The runtime
# libraries remain self-contained but are isolated from pg_duckdb's SONAME.
rm -rf %{buildroot}%{pginstdir}/include
mkdir -p %{buildroot}%{pginstdir}/lib/pg_lake
mv %{buildroot}%{pginstdir}/lib/libduckdb.so \
   %{buildroot}%{pginstdir}/lib/pg_lake/
mv %{buildroot}%{pginstdir}/lib/libavro.so* \
   %{buildroot}%{pginstdir}/lib/pg_lake/

find duckdb_pglake/build -path '*/_deps/*_extension_fc-src/*' -type f \( -iname 'LICENSE*' -o -iname 'NOTICE*' \) -print | LC_ALL=C sort | while IFS= read -r license; do
    component="$(basename "$(dirname "$license")")"
    cp "$license" ".rpm-licenses/$component-$(basename "$license")"
done
find .rpm-licenses -type f -exec chmod 0644 {} +

%check
private=%{buildroot}%{pginstdir}/lib/pg_lake
server=%{buildroot}%{pginstdir}/bin/pgduck_server
iceberg=%{buildroot}%{pginstdir}/lib/pg_lake_iceberg.so

test -x "$server"
test -f "$private/libduckdb.so"
test -f "$private/libavro.so.24.0.1"
test "$(readlink "$private/libavro.so")" = 'libavro.so.24'
test "$(readlink "$private/libavro.so.24")" = 'libavro.so.24.0.1'
test ! -e %{buildroot}%{pginstdir}/lib/libduckdb.so
test ! -e %{buildroot}%{pginstdir}/lib/libavro.so
test ! -e %{buildroot}%{pginstdir}/include

elf_runpath() {
    readelf -d "$1" | sed -n \
        's/.*Library runpath: \[\(.*\)\].*/\1/p;s/.*Library rpath: \[\(.*\)\].*/\1/p'
}

# PGDG deliberately enables a versioned PostgreSQL RUNPATH in PGXS. Preserve
# that platform convention, while requiring the private runtimes to be found
# first through a relative path and rejecting any build-tree leakage.
server_runpath="$(elf_runpath "$server")"
iceberg_runpath="$(elf_runpath "$iceberg")"
case "$server_runpath" in
    '$ORIGIN/../lib/pg_lake:%{pginstdir}/lib') ;;
    *) echo "unexpected pgduck_server RUNPATH: $server_runpath" >&2; exit 1 ;;
esac
case "$iceberg_runpath" in
    '$ORIGIN/pg_lake:%{pginstdir}/lib') ;;
    *) echo "unexpected pg_lake_iceberg RUNPATH: $iceberg_runpath" >&2; exit 1 ;;
esac

for module in \
    pg_extension_base pg_extension_updater pg_map pg_lake_engine \
    pg_lake_table pg_lake_copy pg_lake; do
    runpath="$(elf_runpath "%{buildroot}%{pginstdir}/lib/$module.so")"
    test "$runpath" = '%{pginstdir}/lib' || {
        echo "unexpected $module RUNPATH: $runpath" >&2
        exit 1
    }
done

for runtime in "$private/libduckdb.so" "$private/libavro.so.24.0.1"; do
    runpath="$(elf_runpath "$runtime")"
    test -z "$runpath" || {
        echo "unexpected private runtime RUNPATH for $runtime: $runpath" >&2
        exit 1
    }
done

for elf in "$server" "$iceberg" "$private/libduckdb.so" \
           "$private/libavro.so.24.0.1" \
           %{buildroot}%{pginstdir}/lib/pg_*.so; do
    runpath="$(elf_runpath "$elf")"
    case "$runpath" in
        *%{buildroot}*|*%{_builddir}*)
            echo "build path leaked into RUNPATH for $elf: $runpath" >&2
            exit 1
            ;;
    esac
    ldd_out="$(ldd "$elf")"
    printf '%s\n' "$ldd_out"
    ! printf '%s\n' "$ldd_out" | grep -q 'not found'
done

duckdb_resolved="$(ldd "$server" | awk '/libduckdb\.so =>/ {print $3}')"
avro_resolved="$(ldd "$iceberg" | awk '/libavro\.so\.24 =>/ {print $3}')"
test "$(readlink -f "$duckdb_resolved")" = "$(readlink -f "$private/libduckdb.so")"
test "$(readlink -f "$avro_resolved")" = "$(readlink -f "$private/libavro.so.24")"

%files
%doc README.md SOURCE_MANIFEST docs/
%license .rpm-licenses/*
%{pginstdir}/bin/pgduck_server
%dir %{pginstdir}/lib/pg_lake
%{pginstdir}/lib/pg_lake/libduckdb.so
%{pginstdir}/lib/pg_lake/libavro.so*
%{pginstdir}/lib/pg_extension_base.so
%{pginstdir}/lib/pg_extension_updater.so
%{pginstdir}/lib/pg_map.so
%{pginstdir}/lib/pg_lake_engine.so
%{pginstdir}/lib/pg_lake_iceberg.so
%{pginstdir}/lib/pg_lake_table.so
%{pginstdir}/lib/pg_lake_copy.so
%{pginstdir}/lib/pg_lake.so
%{pginstdir}/share/extension/pg_extension_base*
%{pginstdir}/share/extension/pg_extension_updater*
%{pginstdir}/share/extension/pg_map*
%{pginstdir}/share/extension/pg_lake_engine*
%{pginstdir}/share/extension/pg_lake_iceberg*
%{pginstdir}/share/extension/pg_lake_table*
%{pginstdir}/share/extension/pg_lake_copy*
%{pginstdir}/share/extension/pg_lake.control
%{pginstdir}/share/extension/pg_lake--*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Jul 10 2026 Vonng <rh@vonng.com> - 3.4.0-1PIGSTY
- Package the complete pg_lake 3.4.0 extension family and pgduck_server
- Bundle pinned DuckDB and Avro runtimes in a PostgreSQL-major private path
