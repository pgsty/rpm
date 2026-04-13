%global pname duckdb_fdw
%global sname duckdb_fdw
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot git20251102-870bc43
%global snapshot_commit 870bc4366ba3a96a2359d3c284934fa16ec6b608
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

Name:		%{sname}_%{pgmajorversion}
Version:	1.4.3
Release:	1PIGSTY%{?dist}
Summary:	DuckDB foreign data wrapper for PostgreSQL via pg_duckdb
License:	MIT
URL:		https://github.com/alitrack/%{sname}
Source0:	%{sname}-%{version}.tar.gz
Source1:	pg_duckdb-%{pg_duckdb_version}.tar.gz
# Source0 is a repacked main-branch snapshot from commit %{snapshot_commit}

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	pg_duckdb_%{pgmajorversion} = %{pg_duckdb_version}
Requires:	postgresql%{pgmajorversion}-server
Requires:	pg_duckdb_%{pgmajorversion} = %{pg_duckdb_version}

%description
DuckDB Foreign Data Wrapper for PostgreSQL.
This package is built from the duckdb_fdw main-branch snapshot %{snapshot_commit}
against the DuckDB %{duckdb_version} headers and libduckdb.so shipped by
pg_duckdb %{pg_duckdb_version}. duckdb_fdw does not install its own copy of
libduckdb.so and instead reuses the runtime provided by pg_duckdb.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} == 7
%ifarch aarch64
Requires:	llvm-toolset-7.0-llvm >= 7.0.1
%else
Requires:	llvm5.0 >= 5.0
%endif
%endif
%if 0%{?suse_version} >= 1315 && 0%{?suse_version} <= 1499
BuildRequires:	llvm6-devel clang6-devel
Requires:	llvm6
%endif
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm15-devel clang15-devel
Requires:	llvm15
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}

mkdir -p duckdb-headers
tar -C duckdb-headers --strip-components=5 -xf %{SOURCE1} \
	pg_duckdb-%{pg_duckdb_version}/third_party/duckdb/src/include/duckdb.h \
	pg_duckdb-%{pg_duckdb_version}/third_party/duckdb/src/include/duckdb.hpp \
	pg_duckdb-%{pg_duckdb_version}/third_party/duckdb/src/include/duckdb
test -f duckdb-headers/duckdb.h
test -f duckdb-headers/duckdb.hpp

patch -p1 --forward -f < %{_specdir}/patches/duckdb_fdw-git20251102-870bc43-duckdb-1.4.3-compat.patch
patch -p1 --forward -f < %{_specdir}/patches/duckdb_fdw-git20251102-870bc43-pg_duckdb-linkage.patch
patch -p1 --forward -f < %{_specdir}/patches/duckdb_fdw-git20251102-870bc43-cxx11-abi.patch

%build
test -f %{pginstdir}/lib/libduckdb.so
ln -sfn %{pginstdir}/lib/libduckdb.so libduckdb.so
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH PG_CPPFLAGS="-I$(pwd)/duckdb-headers" %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
ln -sfn %{pginstdir}/lib/libduckdb.so libduckdb.so
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH PG_CPPFLAGS="-I$(pwd)/duckdb-headers" %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif

%exclude %{pginstdir}/lib/bitcode/*

%changelog
* Mon Apr 13 2026 Vonng <rh@vonng.com> - 1.4.3
- Drop the x86_64 legacy libstdc++ ABI override to match pg_duckdb libduckdb.so
- Standardize package version and source tarball name to 1.4.3
- Keep source fixed to duckdb_fdw main snapshot 870bc43
- Rebase to duckdb_fdw main at 870bc43 for PostgreSQL 18 support
- Build against DuckDB 1.4.3 headers and libduckdb.so from pg_duckdb 1.1.1
- Stop installing a second copy of libduckdb.so from duckdb_fdw
