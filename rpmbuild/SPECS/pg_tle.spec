%global pname tle
%global sname pg_tle
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
Version:	1.5.2
Release:	1PGSTY%{?dist}
Summary:	Trusted Language Extensions for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/aws/pg_tle
Source0:	pg_tle-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
Trusted Language Extensions (TLE) for PostgreSQL (pg_tle) is an open source project that lets developers
extend and deploy new PostgreSQL functionality with lower administrative and technical overhead.
Developers can use Trusted Language Extensions for PostgreSQL to create and install extensions on restricted filesystems
and work with PostgreSQL internals through a SQL API.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.5.2-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sun Oct 26 2025 Vonng <rh@vonng.com> - 1.5.2-1PIGSTY
* Fri Sep 05 2025 Vonng <rh@vonng.com> - 1.5.1-2PIGSTY
- pg18 rc1 support with 3c99c51086ae2d1ec7aeb0ecf186a1a29f465d2c
* Thu Mar 20 2025 Vonng <rh@vonng.com> - 1.5.0-1PIGSTY
* Sat Apr 27 2024 Vonng <rh@vonng.com> - 1.4.0-1PIGSTY
* Sat Feb 17 2024 Vonng <rh@vonng.com> - 1.3.4-1PIGSTY
* Wed Sep 13 2023 Vonng <rh@vonng.com> - 1.2.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
