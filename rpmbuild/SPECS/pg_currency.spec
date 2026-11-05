%global pname currency
%global sname pg_currency
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global source_commit 6c91875373f5edfbf38670d12809ece88231a609
%global source_snapshot git20261006.6c91875

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
Version:	0.0.6
Release:	1.%{source_snapshot}PGSTY%{?dist}
Summary:	1 Byte Currency ISO type for PostgreSQL
License:	MIT
URL:		https://github.com/adjust/pg-currency
Source0:	pg-currency-%{version}+%{source_snapshot}.tar.gz
# https://github.com/adjust/pg-currency/archive/6c91875373f5edfbf38670d12809ece88231a609.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
A 1-byte ISO 4217 Currency Code data-type for PostgreSQL.

%prep
%setup -q -n pg-currency-%{source_commit}

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
* Thu Nov 05 2026 Vonng <rh@vonng.com> - 0.0.6-1.git20261006.6c91875PGSTY
- Update to upstream control version 0.0.6 at commit 6c91875373f5
- Include the upstream MRU currency addition and supplied SQL files

* Mon Aug 31 2026 Vonng <rh@vonng.com> - 0.0.4-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Bump to PGXN stable 0.0.4

* Sat Aug 10 2024 Vonng <rh@vonng.com> - 0.0.3-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
