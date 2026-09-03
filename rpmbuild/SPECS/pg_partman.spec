%global pname pg_partman
%global sname pg_partman
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_partman only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

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
Version:	5.5.0
Release:	1PGSTY%{?dist}
Summary:	Partition management extension for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/pgpartman/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/pgpartman/pg_partman/archive/refs/tags/v5.5.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server
Requires:	python3
Requires:	python3-psycopg2

%description
pg_partman is an extension to create and manage both time-based and number-based
table partition sets. Native partitioning in PostgreSQL 14+ is supported.
Child table & trigger function creation is all managed by the extension itself.
Tables with existing data can also have their data partitioned in easily
managed steps. Optional retention policy can automatically drop partitions
no longer needed. A background worker (BGW) process is included to automatically
run partition maintenance without the need of an external scheduler.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} DESTDIR=%{buildroot} %{?_smp_mflags} install

# Fix ambiguous python shebang
sed -i 's|#!/usr/bin/env python|#!/usr/bin/env python3|g' %{buildroot}%{pginstdir}/bin/*.py

%files
%defattr(644,root,root,755)
%license LICENSE.txt
%doc README.md CHANGELOG.md
%attr(755,root,root) %{pginstdir}/bin/check_unique_constraint.py
%attr(755,root,root) %{pginstdir}/bin/dump_partition.py
%attr(755,root,root) %{pginstdir}/bin/vacuum_maintenance.py
%{pginstdir}/lib/%{pname}_bgw.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%{pginstdir}/doc/extension/*.md
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 5.5.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Mon Jul 27 2026 Vonng <rh@vonng.com> - 5.5.0-1PIGSTY
- Update to upstream PGXN 5.5.0
- Require Python 3 and psycopg2 for the installed maintenance scripts

* Fri Jan 16 2026 Vonng <rh@vonng.com> - 5.4.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
