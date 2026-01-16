%global pname pg_partman
%global sname pg_partman
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
Version:	5.4.0
Release:	1PIGSTY%{?dist}
Summary:	Partition management extension for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/pgpartman/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/pgpartman/pg_partman/archive/refs/tags/v5.4.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_partman is an extension to create and manage both time-based and number-based
table partition sets. Native partitioning in PostgreSQL 14+ is supported.
Child table & trigger function creation is all managed by the extension itself.
Tables with existing data can also have their data partitioned in easily
managed steps. Optional retention policy can automatically drop partitions
no longer needed. A background worker (BGW) process is included to automatically
run partition maintenance without the need of an external scheduler.

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

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install

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
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Fri Jan 16 2026 Vonng <rh@vonng.com> - 5.4.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
