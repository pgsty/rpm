%global pname first_last_agg
%global sname first_last_agg
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
Version:	0.1.4
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL extension providing first and last aggregate functions.
License:	PostgreSQL
URL:		https://github.com/wulczer/first_last_agg
Source0:	first_last_agg-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
A simple extension providing two aggregate functions, last and first aggregate functions, operating on any element type and returning the last or the first value of the group.
Since by default the ordering inside groups created by a GROUP BY expression is not defined, it is advisable to use an ORDER BY clause inside the aggregate expression (see the aggregate function syntax). This feature has been added in PostgreSQL 9.0.
This extension is intended to replace the corresponding first and last aggregates from the PostgreSQL wiki.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude %{pginstdir}/doc/extension/first_last_agg.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.1.4-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Mon Jul 29 2024 Vonng <rh@vonng.com> - 0.1.4
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
