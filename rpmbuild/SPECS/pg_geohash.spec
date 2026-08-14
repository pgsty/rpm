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

Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	4PGSTY%{?dist}
Summary:	Geohashing library for HAWQ, Greenplum DB, PostgreSQL
License:	MIT
URL:		https://github.com/jistok/pg_geohash
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description


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
Requires:	llvm => 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}
%{__mv} %{pname}-1.0.sql %{pname}--1.0.sql
%{__sed} -i 's/%{pname}-1.0.sql/%{pname}--1.0.sql/' Makefile
%{__sed} -i -e '/^PGXS :=/i PG_CONFIG ?= pg_config' -e 's/pg_config --pgxs/$(PG_CONFIG) --pgxs/' Makefile

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} PG_CONFIG=%{pginstdir}/bin/pg_config

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Fri Aug 14 2026 Vonng <rh@vonng.com> - 1.0-4PGSTY
- Honor PG_CONFIG so each package is built against its target PostgreSQL version.

* Fri Aug 14 2026 Vonng <rh@vonng.com> - 1.0-3PGSTY
- Fix the extension SQL filename so CREATE EXTENSION works.

* Fri Aug 14 2026 Vonng <rh@vonng.com> - 1.0-2PGSTY
- Rebuild with corrected license metadata.

* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
