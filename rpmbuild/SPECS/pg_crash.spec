%global pname pg_crash
%global sname pg_crash
%global pginstdir /usr/pgsql-%{pgmajorversion}
%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_crash supports PostgreSQL 14 through 18 in Pigsty builds}
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
Epoch:		1
Version:	0.3
Release:	1PGSTY%{?dist}
Summary:	Periodically crash your PostgreSQL database
License:	BSD-3-Clause
URL:		https://github.com/cybertec-postgresql/pg_crash
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pg_crash-0.3.patch

BuildRequires:	gcc make postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
If your database is too reliable, pg_crash can kill it for you. pg_crash is a
PostgreSQL preload module that periodically crashes database infrastructure by
sending configured signals to database processes. It is intended for HA and
failover testing.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --fuzz=0 < %{PATCH0}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1  %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 1:0.3-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Upgrade to the official upstream 0.3 release
- Preserve the historical empty extension catalog with a compatibility edge

* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
