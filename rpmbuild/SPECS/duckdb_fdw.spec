%global pname duckdb_fdw
%global sname duckdb_fdw
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global duckdb_version 2.0.0
%{!?duckdb_core_jobs:%global duckdb_core_jobs 2}
%{!?llvm:%global llvm 1}

# Upstream 2.0.2 uses boolVal/makeBoolean, which PG14 does not provide.
%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 18
%{error:duckdb_fdw 2.0.2 currently targets PostgreSQL 15 through 18}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        2.0.2
Release:        1PGSTY%{?dist}
Summary:        DuckDB foreign data wrapper with an embedded DuckDB engine
License:        MIT AND Apache-2.0 AND BSD-2-Clause AND BSD-3-Clause AND BSL-1.0 AND Zlib AND Unicode-DFS-2015
URL:            https://github.com/alitrack/duckdb_fdw
Source0:        duckdb_fdw-%{version}.tar.gz
Source1:        duckdb-%{duckdb_version}.tar.gz
Patch0:         duckdb_fdw-2.0.2-static.patch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc gcc-c++ make cmake ninja-build python3
%if %llvm
BuildRequires:  llvm-devel >= 19.0
BuildRequires:  clang-devel >= 19.0
%endif
Requires:       postgresql%{pgmajorversion}-server
# Keep DuckDB's public symbols available to dynamic plugins. This does not
# isolate an incompatible peer core in PostgreSQL's global loader namespace.
Conflicts:      pg_duckdb_%{pgmajorversion}

%description
DuckDB Foreign Data Wrapper for PostgreSQL, using an independently built,
statically embedded DuckDB %{duckdb_version}. Includes Parquet, JSON and ICU,
and retains dynamic DuckDB plugin loading. No external libduckdb
or pg_duckdb package is required. Select one DuckDB extension package per
PostgreSQL major and restart PostgreSQL after changing preload configuration
or switching packages; a package replacement cannot unload existing libraries.

%prep
# Official release tag archives; do not substitute the old 2.0.1 snapshot.
echo '1ed7935b009211915434fd65083b0562389e3faf1722865f81633d70a0c0fc8b  %{SOURCE0}' | sha256sum -c -
echo '7e89053255046bfb26afbd7f524a2fb84df7dbef496aa911ea35e4a1182fdc00  %{SOURCE1}' | sha256sum -c -
%setup -q -n duckdb_fdw-%{version}
mkdir duckdb
tar -xf %{SOURCE1} -C duckdb --strip-components=1
%patch -P 0 -p1

%build
%set_build_flags
# GCC 11 LTO linking breaks file-backed INSERT (PhysicalBatchInsert NULL state).
# Linking the same archives as native objects passes. This does not disable
# PGXS Clang bitcode, its thin index, or PostgreSQL LLVM JIT.
export PG_LDFLAGS="$LDFLAGS -fno-lto"
DUCKDB_BUILD_JOBS=%{duckdb_core_jobs} sh ./build-duckdb.sh
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE duckdb-licenses
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%{pginstdir}/lib/bitcode/%{pname}/
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%endif

%changelog
* Sat Oct 24 2026 Vonng <rh@vonng.com> - 2.0.2-1PGSTY
- Package the official duckdb_fdw 2.0.2 release with DuckDB 2.0.0 PIC archives
- Remove pg_duckdb headers and shared runtime dependencies
- Retain built-in Parquet/JSON/ICU, dynamic plugins, LLVM and debug packages
- Conflict with pg_duckdb for the same PostgreSQL major; require restart on switch
- Replace obsolete snapshot fixes with a static build and runtime guard patch

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 2.0.1-1.git20260529.9354241PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Upgrade to the duckdb_fdw 2.0.1 main snapshot at 9354241
- Consolidate the packaging fixes into a single duckdb_fdw-2.0.1.patch
- Switch from the SQLite compatibility layer to the native DuckDB C API
- Build against DuckDB 1.4.3 headers from pg_duckdb 1.1.1
- Reuse the DuckDB 1.4.3 runtime shipped by pg_duckdb 1.1.1 per PG major
- Resolve libduckdb.so from the extension directory with an $ORIGIN RUNPATH
- Preserve and repair the upstream 1.4.1 to 2.0.1 extension migration chain
- Stop installing a private libduckdb.so into PostgreSQL's library directory
- Preserve legacy servers without user mappings and harden error cleanup
- Keep scalar aggregate results in native DuckDB types for safe conversion
- Align regression expectations with the current insert-only FDW callback policy
- Initialize projected virtual slots before PG17 materializes aggregate rows
- Allow peer-loaded pg_duckdb when both extensions resolve the same libduckdb

* Mon Apr 13 2026 Vonng <rh@vonng.com> - 1.4.3
- Drop the x86_64 legacy libstdc++ ABI override to match pg_duckdb libduckdb.so
- Standardize package version and source tarball name to 1.4.3
- Keep source fixed to duckdb_fdw main snapshot 870bc43
- Rebase to duckdb_fdw main at 870bc43 for PostgreSQL 18 support
- Build against DuckDB 1.4.3 headers and libduckdb.so from pg_duckdb 1.1.1
- Stop installing a second copy of libduckdb.so from duckdb_fdw
