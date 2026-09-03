%global pname pg_dirtyread
%global sname pg_dirtyread
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
Version:	2.8
Release:	1PGSTY%{?dist}
Summary:	Read dead but unvacuumed tuples from a PostgreSQL relation
License:	BSD-3-Clause
URL:		https://github.com/df7cb/pg_dirtyread
Source0:	pg_dirtyread-%{version}.tar.gz
#           https://deb.debian.org/debian/pool/main/p/pg-dirtyread/pg-dirtyread_2.8.orig.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
The pg_dirtyread extension provides the ability to read dead but unvacuumed rows from a relation.
Supports PostgreSQL 9.2 and later. (On 9.2, at least 9.2.9 is required.)

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.8-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sat Jun 06 2026 Vonng <rh@vonng.com> - 2.8-1PIGSTY
- https://deb.debian.org/debian/pool/main/p/pg-dirtyread/pg-dirtyread_2.8.orig.tar.gz
* Fri Jun 14 2024 Vonng <rh@vonng.com> - 2.7
* Sun May 05 2024 Vonng <rh@vonng.com> - 2.6
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
