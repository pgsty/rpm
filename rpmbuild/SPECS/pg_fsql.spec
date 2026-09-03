%global pname pg_fsql
%global sname pg_fsql
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
Version:	1.1.0
Release:	1PGSTY%{?dist}
Summary:	Recursive SQL template engine for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/yurc/pg_fsql
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_fsql is a recursive SQL template engine for PostgreSQL.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/pg_fsql-1.1.0.patch

%build
cd %{_builddir}/%{sname}-%{version}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} all %{pname}--1.0.sql

%install
%{__rm} -rf %{buildroot}
cd %{_builddir}/%{sname}-%{version}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} %{pname}--1.0.sql install DESTDIR=%{buildroot}

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.1.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Restore automatic debuginfo and debugsource generation with %setup

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
