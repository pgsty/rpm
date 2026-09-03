%global pname pgnodemx
%global sname pgnodemx
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
Version:	2.0.1
Release:	1PGSTY%{?dist}
Summary:	Capture node OS metrics via SQL queries
License:	Apache-2.0 AND BSD-3-Clause
URL:		https://github.com/pgnodemx/pgnodemx
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pgnodemx-2.0.1.patch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
SQL functions that allow capture of node OS metrics from PostgreSQL
Executing role must have been granted pg_monitor membership (pgmonitor for PostgreSQL version 9.6 and below - see Compatibility section below).

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/share/extension/pg_proctab*
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.0.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Thu Jul 23 2026 Vonng <rh@vonng.com> - 2.0.1-1PIGSTY
- https://github.com/pgnodemx/pgnodemx/releases/tag/v2.0.1
- Prevent connection failures when cgroup support is disabled or unavailable
* Mon Oct 14 2024 Vonng <rh@vonng.com> - 1.7
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.6
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
