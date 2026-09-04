%global pname pg_bigm
%global sname pg_bigm
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
Version:	1.2
Release:	1PGSTY%{?dist}
Summary:	Full text search capability with create 2-gram (bigram) index.
License:	PostgreSQL
URL:		https://github.com/pgbigm/pg_bigm
Source0:	pg_bigm-%{version}-20250903.tar.gz
#           https://github.com/pgbigm/pg_bigm/archive/refs/tags/v1.2-20250903.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
The pg_bigm module provides full text search capability in PostgreSQL.
This module allows a user to create 2-gram (bigram) index for faster full text search.
pg_bigm is released under the PostgreSQL License, a liberal Open Source license,
 similar to the BSD or MIT licenses.

%prep
%setup -q -n pg_bigm-1.2-20250903

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

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
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.2-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Mon Feb 09 2026 Vonng <rh@vonng.com> - 1.2-2PIGSTY
- https://github.com/pgbigm/pg_bigm/releases/tag/v1.2-20250903
* Sun Jul 28 2024 Vonng <rh@vonng.com> - v1.2-20240606
* Mon Oct 16 2023 Vonng <rh@vonng.com> - 1.2.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
