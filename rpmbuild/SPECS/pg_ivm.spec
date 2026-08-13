%global sname pg_ivm
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	1.15
Release:	1PGSTY%{?dist}
Summary:	Incremental View Maintenance extension for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/sraoss/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#		https://api.github.com/repos/sraoss/pg_ivm/tarball/v1.15

BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

%description
pg_ivm provides Incremental View Maintenance for PostgreSQL by keeping
incrementally maintainable materialized views up to date as base tables change.
For correct maintenance, add pg_ivm to shared_preload_libraries or
session_preload_libraries.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}
%endif

%prep
%setup -q -n sraoss-%{sname}-377a37d

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/bin/pg_ivm_dump_metadata
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Tue Aug 11 2026 Vonng <rh@vonng.com> - 1.15-1PIGSTY
- Update to 1.15
- Package the pg_ivm_dump_metadata utility
- https://github.com/sraoss/pg_ivm/releases/tag/v1.15
* Fri Apr 10 2026 Vonng <rh@vonng.com> - 1.14-1PIGSTY
- Initial RPM release
- https://github.com/sraoss/pg_ivm/releases/tag/v1.14
