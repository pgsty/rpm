%global pname duckdb_fdw
%global sname duckdb_fdw
%global pginstdir /usr/pgsql-%{pgmajorversion}

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
Version:	1.1.2
Release:	1PIGSTY%{?dist}
Summary:	DuckDB Foreign data wrapper extension for PostgreSQL.
License:	MIT License
URL:		https://github.com/alitrack/%{sname}
Source0:	%{sname}-%{version}.tar.gz
# https://github.com/alitrack/duckdb_fdw/archive/refs/tags/v1.1.2.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}-server libduckdb = %{version}

%description
DuckDB Foreign Data Wrapper for PostgreSQL
This is a foreign data wrapper (FDW) to connect PostgreSQL to DuckDB database file.
This FDW works with PostgreSQL 9.6 ... 17 and compiled with exact same version of libduckdb.

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
BuildRequires:  llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm => 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
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
* Sun Nov 03 2024 Vonng <rh@vonng.com> - 1.1.2
- Bump libduckdb to 1.1.2 with PostgreSQL 17 support
* Sat Jun 29 2024 Vonng <rh@vonng.com> - 1.0.0
- Changing version schema to keep in sync with libduckdb
* Mon Jan 29 2024 Vonng <rh@vonng.com> - 1.1
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>