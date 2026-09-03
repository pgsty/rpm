%global pname pg_geohash
%global sname pg_geohash
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

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	4PGSTY%{?dist}
Summary:	Geohashing library for HAWQ, Greenplum DB, PostgreSQL
License:	MIT
URL:		https://github.com/jistok/pg_geohash
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description

%prep
%setup -q -n %{sname}-%{version}
%{__mv} %{pname}-1.0.sql %{pname}--1.0.sql
%{__sed} -i 's/%{pname}-1.0.sql/%{pname}--1.0.sql/' Makefile
%{__sed} -i -e '/^PGXS :=/i PG_CONFIG ?= pg_config' -e 's/pg_config --pgxs/$(PG_CONFIG) --pgxs/' Makefile

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot} PG_CONFIG=%{pginstdir}/bin/pg_config

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Aug 14 2026 Vonng <rh@vonng.com> - 1.0-4PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Honor PG_CONFIG so each package is built against its target PostgreSQL version.

* Fri Aug 14 2026 Vonng <rh@vonng.com> - 1.0-3PGSTY
- Fix the extension SQL filename so CREATE EXTENSION works.

* Fri Aug 14 2026 Vonng <rh@vonng.com> - 1.0-2PGSTY
- Rebuild with corrected license metadata.

* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
