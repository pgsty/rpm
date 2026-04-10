%global sname pg_ivm
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	1.14
Release:	1PIGSTY%{?dist}
Summary:	Incremental View Maintenance extension for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/sraoss/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#		https://github.com/sraoss/pg_ivm/archive/refs/tags/v1.14.tar.gz

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
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Apr 10 2026 Vonng <rh@vonng.com> - 1.14-1PIGSTY
- Initial RPM release
- https://github.com/sraoss/pg_ivm/releases/tag/v1.14
