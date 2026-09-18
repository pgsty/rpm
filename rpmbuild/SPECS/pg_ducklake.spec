%global pname pg_ducklake
%global sname pg_ducklake
%global pginstdir /usr/pgsql-%{pgmajorversion}
# DuckDB's nested Ninja build is substantially more memory-intensive than the
# PGXS bridge. Keep its own concurrency below the outer RPM build parallelism.
# Override with --define 'duckdb_core_jobs N' on builders with more memory.
%{!?duckdb_core_jobs:%global duckdb_core_jobs 2}

%if 0%{?rhel} && 0%{?rhel} < 9
%{error:pg_ducklake 1.0.2 is currently supported on EL9 and later; EL8 GCC8 filesystem compatibility is not validated}
%endif

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_ducklake 1.0.2 only supports PostgreSQL 14 through 18}
%endif

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.2
Release:	1PGSTY%{?dist}
Summary:	DuckLake lakehouse extension for PostgreSQL
License:	MIT
URL:		https://github.com/relytcloud/pg_ducklake
# Source0 is a normalized v1.0.2 release tarball with all build-time sources:
# pg_ducklake b7da9fc28f4845a7c84c026ca6569d2d289ea303
# duckdb 9a64d338f2fa1d3c1d43c016b09c538b529dd397
# pg_ducklake/third_party/ducklake 93cc490d9b5554f6fd5322dbef23f41d4fa91bb8
# pg_ducklake/third_party/duckdb-postgres c89234f0b1985f4ee0f52f16e742a1ab2d4ae4f0
# pg_ducklake/third_party/duckdb-postgres/database-connector 746b56c4063f3682f4eb4facdc49408ed1885555
# pg_ducklake/third_party/duckdb-postgres/postgres REL_15_13
Source0:	%{sname}-%{version}.tar.gz
# Upstream v1.0.2 CI pins vcpkg 84bab45d, whose roaring port is 4.5.0.
# Keep Pigsty's already-validated 4.7.1; CRoaring 5 is a separate major upgrade.
Source1:	CRoaring-4.7.1-amalgamation.tar.gz
Patch0:		pg_ducklake-1.0.2.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc gcc-c++ make cmake ninja-build patch pkgconf-pkg-config ccache
BuildRequires:	bison flex zlib-devel readline-devel libxml2-devel libxslt-devel
BuildRequires:	openssl-devel libcurl-devel lz4-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_ducklake is a PostgreSQL extension for managed DuckLake tables, backed by
DuckDB and Parquet files. It requires shared_preload_libraries = 'pg_ducklake'
before CREATE EXTENSION.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --fuzz=0 < %{PATCH0}
tar -xzf %{SOURCE1}
mkdir -p .rpm-licenses
cp LICENSE .rpm-licenses/%{sname}-LICENSE
cp CRoaring-4.7.1/LICENSE .rpm-licenses/CRoaring-LICENSE
cp pg_ducklake/third_party/duckdb-postgres/LICENSE .rpm-licenses/duckdb-postgres-LICENSE
cp pg_ducklake/third_party/duckdb-postgres/database-connector/LICENSE .rpm-licenses/database-connector-LICENSE
cp pg_ducklake/third_party/duckdb-postgres/postgres/COPYRIGHT .rpm-licenses/postgresql-COPYRIGHT

%build
%set_build_flags
# PGXS also feeds C/C++ flags to Clang when producing extension bitcode.
# Keep generic LTO there, while bounding GCC's bundled DuckDB LTO workers.
# The bundled DuckDB keeps function and line-table DWARF only (-g1); the PGXS
# bridge keeps the full distribution -g so the debuginfo package stays tractable.
pg_cflags="${CFLAGS//-flto=auto/-flto}"
pg_cxxflags="${CXXFLAGS//-flto=auto/-flto}"
duckdb_cflags="${CFLAGS//-flto=auto/-flto=1} -g1"
duckdb_cxxflags="${CXXFLAGS//-flto=auto/-flto=1} -g1"
duckdb_ldflags="${LDFLAGS//-flto=auto/-flto=1}"
croaring_prefix="$(pwd)/.croaring"
croaring_src="$(pwd)/CRoaring-4.7.1"
mkdir -p "$croaring_prefix/include/roaring" "$croaring_prefix/lib/cmake/roaring" "$croaring_src/build"
cp -a "$croaring_src/include/roaring/." "$croaring_prefix/include/roaring/"
cp -a "$croaring_src/cpp/roaring/." "$croaring_prefix/include/roaring/"
for src in $(find "$croaring_src/src" -name '*.c' | sort); do
	obj="$(echo "${src#$croaring_src/}" | tr '/.' '__').o"
	%{__cc} %{optflags} -fPIC -I"$croaring_src/include" -c "$src" -o "$croaring_src/build/$obj"
done
ar cr "$croaring_prefix/lib/libroaring.a" "$croaring_src"/build/*.o
cat > "$croaring_prefix/lib/cmake/roaring/roaringConfig.cmake" <<'EOF'
get_filename_component(_roaring_prefix "${CMAKE_CURRENT_LIST_DIR}/../../.." ABSOLUTE)
add_library(roaring::roaring STATIC IMPORTED)
set_target_properties(roaring::roaring PROPERTIES
  IMPORTED_LOCATION "${_roaring_prefix}/lib/libroaring.a"
  INTERFACE_INCLUDE_DIRECTORIES "${_roaring_prefix}/include")
add_library(roaring::roaring-headers INTERFACE IMPORTED)
set_target_properties(roaring::roaring-headers PROPERTIES
  INTERFACE_INCLUDE_DIRECTORIES "${_roaring_prefix}/include")
add_library(roaring::roaring-headers-cpp INTERFACE IMPORTED)
set_target_properties(roaring::roaring-headers-cpp PROPERTIES
  INTERFACE_INCLUDE_DIRECTORIES "${_roaring_prefix}/include")
EOF
cp "$croaring_prefix/lib/cmake/roaring/roaringConfig.cmake" "$croaring_prefix/lib/cmake/roaring/roaring-config.cmake"

CMAKE_PREFIX_PATH="$croaring_prefix" PATH=%{pginstdir}/bin:$PATH PG_CONFIG=%{pginstdir}/bin/pg_config \
	CMAKE_BUILD_PARALLEL_LEVEL=%{duckdb_core_jobs} \
	CCACHE_DIR="$HOME/.cache/pg_ducklake/ccache" CCACHE_COMPILERCHECK=content CCACHE_MAXSIZE=16G \
	%{__make} -j%{duckdb_core_jobs} %{with_llvm_arg} COMPILER_LAUNCHER=ccache ROARING_LIB_DIR="$croaring_prefix/lib" \
	PG_CFLAGS="$pg_cflags" PG_CXXFLAGS="$pg_cxxflags" LDFLAGS="$duckdb_ldflags" \
	DUCKDB_C_FLAGS="$duckdb_cflags" DUCKDB_CXX_FLAGS="$duckdb_cxxflags"

# DuckDB's checked-in Bison/Flex output uses relative #line paths.  GCC resolves
# those paths against the CMake build directory, while the authoritative inputs
# remain under duckdb/third_party/libpg_query.  Materialize only that source
# subtree at the recorded location so RPM debugedit can copy the real sources.
mapfile -t duckdb_release_dirs < <(find duckdb/build -mindepth 1 -maxdepth 1 -type d -name 'release-*' -print)
test "${#duckdb_release_dirs[@]}" -eq 1
debug_pgquery_dir="${duckdb_release_dirs[0]}/third_party/libpg_query"
mkdir -p "$debug_pgquery_dir"
cp -a duckdb/third_party/libpg_query/grammar "$debug_pgquery_dir/"
cp -a duckdb/third_party/libpg_query/scan.l "$debug_pgquery_dir/"
cp -a duckdb/third_party/libpg_query/src_backend_parser_scan.cpp "$debug_pgquery_dir/"

# Bison creates grammar_out.hpp beside grammar_out.cpp.  The generator then
# renames it byte-for-byte into the checked-in parser include tree.
cp -a duckdb/third_party/libpg_query/include/parser/gram.hpp \
	"$debug_pgquery_dir/grammar/grammar_out.hpp"

# generate_grammar.py renames grammar_out.cpp to src_backend_parser_gram.cpp,
# then replaces an include and the yynerrs assignment.  In the bundled 1.0.2
# parser both include spellings are absent, so that replacement is a no-op;
# only the single yynerrs edit must be reversed to reproduce the pre-rename
# Bison output referenced by its own DWARF line table.
parser_gram=duckdb/third_party/libpg_query/src_backend_parser_gram.cpp
test "$(grep -Fc '#include "grammar_out.hpp"' "$parser_gram")" -eq 0
test "$(grep -Fc '#include "include/parser/gram.hpp"' "$parser_gram")" -eq 0
test "$(grep -Fc 'yynerrs = 0; (void)yynerrs;' "$parser_gram")" -eq 1
sed 's/yynerrs = 0; (void)yynerrs;/yynerrs = 0;/' "$parser_gram" > "$debug_pgquery_dir/grammar/grammar_out.cpp"
test -s "$debug_pgquery_dir/grammar/grammar_out.cpp"

%install
%set_build_flags
pg_cflags="${CFLAGS//-flto=auto/-flto}"
pg_cxxflags="${CXXFLAGS//-flto=auto/-flto}"
duckdb_cflags="${CFLAGS//-flto=auto/-flto=1} -g1"
duckdb_cxxflags="${CXXFLAGS//-flto=auto/-flto=1} -g1"
duckdb_ldflags="${LDFLAGS//-flto=auto/-flto=1}"
%{__rm} -rf %{buildroot}
CMAKE_PREFIX_PATH="$(pwd)/.croaring" PATH=%{pginstdir}/bin:$PATH PG_CONFIG=%{pginstdir}/bin/pg_config \
	CMAKE_BUILD_PARALLEL_LEVEL=%{duckdb_core_jobs} \
	%{__make} -j%{duckdb_core_jobs} %{with_llvm_arg} ROARING_LIB_DIR="$(pwd)/.croaring/lib" install DESTDIR=%{buildroot} \
	PG_CFLAGS="$pg_cflags" PG_CXXFLAGS="$pg_cxxflags" LDFLAGS="$duckdb_ldflags" \
	DUCKDB_C_FLAGS="$duckdb_cflags" DUCKDB_CXX_FLAGS="$duckdb_cxxflags"

%files
%doc README.md SOURCE_MANIFEST pg_ducklake/docs
%license .rpm-licenses/*
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 1.0.2-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Keep LLVM and PGXS bitcode enabled by default on every supported PG major
- Upgrade to pg_ducklake 1.0.2 with a checksummed complete source bundle
- Retain CRoaring 4.7.1 after validating the 5.1.1 API and serialization
- Build PostgreSQL LLVM bitcode into the main package on supported EL9 builders
- Limit the nested DuckDB Ninja build to two memory-safe jobs
- Pass distribution debug flags into the nested DuckDB CMake build
- Cache nested DuckDB compilation using full command and compiler-content keys
- Ignore only PostgreSQL's unrelated package-build debug map in that cache key
- Keep Clang bitcode on generic LTO and each bundled GCC link to one worker
- Build the bundled DuckDB core with line-table debug information only (-g1)
- Feed distribution flags to the PGXS bridge through PG_CFLAGS and PG_CXXFLAGS
- Merge the DuckDB flag plumbing into pg_ducklake-1.0.2.patch

* Sat Jul 11 2026 Vonng <rh@vonng.com> - 1.0.0-2PIGSTY
- Mark the current package as EL9+ pending EL8 GCC8 filesystem support
- Enforce the supported PostgreSQL 14 through 18 range

* Fri Jun 19 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release for pg_ducklake 1.0.0
