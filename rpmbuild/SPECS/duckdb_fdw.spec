%global pname duckdb_fdw
%global sname duckdb_fdw
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global snapshot_date 20260529
%global snapshot_commit 9354241029df691b695f15428082b7c5cd81e2c7
%global snapshot_short 9354241
%global duckdb_version 1.5.5

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
Version:	2.0.1
Release:	1.git%{snapshot_date}.%{snapshot_short}PGSTY%{?dist}
Summary:	DuckDB foreign data wrapper for PostgreSQL
License:	MIT
URL:		https://github.com/alitrack/%{sname}
Source0:	%{sname}-%{version}+git%{snapshot_date}.%{snapshot_short}.tar.gz
Source1:	duckdb-%{duckdb_version}-headers.tar.gz
# Source0 is a repacked main-branch snapshot from commit %{snapshot_commit}
Patch0:		duckdb_fdw-2.0.1.patch
Patch1:		duckdb_fdw-2.0.1-types.patch
Patch2:		duckdb_fdw-2.0.1-tests.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	libduckdb >= %{duckdb_version}
BuildRequires:	patchelf
Requires:	postgresql%{pgmajorversion}-server
Requires:	libduckdb >= %{duckdb_version}

%description
DuckDB Foreign Data Wrapper for PostgreSQL.
This package is built from the duckdb_fdw main-branch snapshot %{snapshot_commit}
against the standalone DuckDB %{duckdb_version} C API and shared library.
duckdb_fdw does not install a private copy of libduckdb.so into PostgreSQL's
library directory.

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

tar -C . --strip-components=1 -xf %{SOURCE1}

patch -p1 --fuzz=0 < %{PATCH0}
patch -p1 --fuzz=0 < %{PATCH1}
patch -p1 --fuzz=0 < %{PATCH2}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}
patchelf --set-rpath %{_libdir} duckdb_fdw.so

%install
%{__rm} -rf %{buildroot}
export QA_RPATHS=1
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

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

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 2.0.1-1.git20260529.9354241PGSTY
- Upgrade to the duckdb_fdw 2.0.1 main snapshot at 9354241
- Switch from the SQLite compatibility layer to the native DuckDB C API
- Build and run against the standalone libduckdb 1.5.5 package
- Preserve and repair the upstream 1.4.1 to 2.0.1 extension migration chain
- Stop installing a private libduckdb.so into PostgreSQL's library directory
- Replace the PostgreSQL-library RPATH with the system libdir runtime
- Preserve legacy servers without user mappings and harden error cleanup
- Keep scalar aggregate results in native DuckDB types for safe conversion
- Align regression expectations with the current insert-only FDW callback policy
- Ship PostgreSQL bitcode in the llvmjit subpackage instead of an empty RPM

* Mon Apr 13 2026 Vonng <rh@vonng.com> - 1.4.3
- Drop the x86_64 legacy libstdc++ ABI override to match pg_duckdb libduckdb.so
- Standardize package version and source tarball name to 1.4.3
- Keep source fixed to duckdb_fdw main snapshot 870bc43
- Rebase to duckdb_fdw main at 870bc43 for PostgreSQL 18 support
- Build against DuckDB 1.4.3 headers and libduckdb.so from pg_duckdb 1.1.1
- Stop installing a second copy of libduckdb.so from duckdb_fdw
