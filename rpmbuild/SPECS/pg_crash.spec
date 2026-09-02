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

Name:		%{sname}_%{pgmajorversion}
Epoch:		1
Version:	0.3
Release:	1PGSTY%{?dist}
Summary:	Periodically crash your PostgreSQL database
License:	BSD-3-Clause
URL:		https://github.com/cybertec-postgresql/pg_crash
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pg_crash-0.3.patch

BuildRequires:	gcc make postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 clang llvm
Requires:	postgresql%{pgmajorversion}-server

%description
If your database is too reliable, pg_crash can kill it for you. pg_crash is a
PostgreSQL preload module that periodically crashes database infrastructure by
sending configured signals to database processes. It is intended for HA and
failover testing.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}
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
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --fuzz=0 < %{PATCH0}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1  %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 1:0.3-1PGSTY
- Upgrade to the official upstream 0.3 release
- Preserve the historical empty extension catalog with a compatibility edge

* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
