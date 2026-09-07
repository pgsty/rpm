%global pname duckdb_fdw
%global sname duckdb_fdw
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot_date 20260529
%global snapshot_commit 9354241029df691b695f15428082b7c5cd81e2c7
%global snapshot_short 9354241
%global pg_duckdb_version 1.1.1
%global duckdb_version 1.4.3

%ifarch ppc64 ppc64le s390 s390x armv7hl
 %if 0%{?rhel} && 0%{?rhel} == 7
  %{!?llvm:%global llvm 0}
 %else
  %{!?llvm:%global llvm 1}
 %endif
%else
 %{!?llvm:%global llvm 1}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.0.1
Release:	1.git%{snapshot_date}.%{snapshot_short}PGSTY%{?dist}
Summary:	DuckDB foreign data wrapper for PostgreSQL
License:	MIT
URL:		https://github.com/alitrack/%{sname}
Source0:	%{sname}-%{version}+git%{snapshot_date}.%{snapshot_short}.tar.gz
Source1:	pg_duckdb-%{pg_duckdb_version}.tar.gz
# Source0 is a repacked main-branch snapshot from commit %{snapshot_commit}
Patch0:		duckdb_fdw-2.0.1.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	pg_duckdb_%{pgmajorversion} >= %{pg_duckdb_version}
BuildRequires:	patchelf
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server
Requires:	pg_duckdb_%{pgmajorversion} >= %{pg_duckdb_version}

%description
DuckDB Foreign Data Wrapper for PostgreSQL.
This package is built from the duckdb_fdw main-branch snapshot %{snapshot_commit}
against the DuckDB %{duckdb_version} C API and libduckdb.so shipped by
pg_duckdb %{pg_duckdb_version}. Both extensions use the same per-PostgreSQL-
major runtime, and duckdb_fdw does not install a second copy.

%prep
%setup -q -n %{sname}-%{version}

mkdir -p duckdb-headers
tar -C duckdb-headers --strip-components=5 -xf %{SOURCE1} \
	pg_duckdb-%{pg_duckdb_version}/third_party/duckdb/src/include/duckdb.h \
	pg_duckdb-%{pg_duckdb_version}/third_party/duckdb/src/include/duckdb.hpp \
	pg_duckdb-%{pg_duckdb_version}/third_party/duckdb/src/include/duckdb
test -f duckdb-headers/duckdb.h
test -f duckdb-headers/duckdb.hpp

patch -p1 --fuzz=0 < %{PATCH0}

%build
test -f %{pginstdir}/lib/libduckdb.so
ln -sfn %{pginstdir}/lib/libduckdb.so libduckdb.so
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} PG_CPPFLAGS="-I$(pwd)/duckdb-headers"
patchelf --set-rpath '$ORIGIN' duckdb_fdw.so

%install
%{__rm} -rf %{buildroot}
ln -sfn %{pginstdir}/lib/libduckdb.so libduckdb.so
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} PG_CPPFLAGS="-I$(pwd)/duckdb-headers" install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
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
