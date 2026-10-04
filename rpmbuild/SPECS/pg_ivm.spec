%global sname pg_ivm
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.16
Release:	1PGSTY%{?dist}
Summary:	Incremental View Maintenance extension for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/sraoss/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#		https://github.com/sraoss/pg_ivm/archive/refs/tags/v1.16.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_ivm provides Incremental View Maintenance for PostgreSQL by keeping
incrementally maintainable materialized views up to date as base tables change.
For correct maintenance, add pg_ivm to shared_preload_libraries or
session_preload_libraries.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/bin/pg_ivm_dump_metadata
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Oct 02 2026 Ruohang Feng <rh@vonng.com> - 1.16-1PGSTY
- Update to 1.16.

* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.15-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Tue Aug 11 2026 Vonng <rh@vonng.com> - 1.15-1PIGSTY
- Update to 1.15
- Package the pg_ivm_dump_metadata utility
- https://github.com/sraoss/pg_ivm/releases/tag/v1.15
* Fri Apr 10 2026 Vonng <rh@vonng.com> - 1.14-1PIGSTY
- Initial RPM release
- https://github.com/sraoss/pg_ivm/releases/tag/v1.14
