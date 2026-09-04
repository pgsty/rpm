%global pname pg_accumulator
%global sname pg_accumulator
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_accumulator 1.2.0 supports PostgreSQL 14 through 18 in PGSTY builds}
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
Version:	1.2.0
Release:	1PGSTY%{?dist}
Summary:	Balance, turnover and ledger registers for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/Treedo/pg_accumulator
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pg_accumulator-1.2.0.patch
#           official v1.2.0 tag d9b908b9a4dbea8464fb4ecdf0677f03381aa0c8

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_accumulator provides declarative balance, turnover and double-entry ledger
registers with transactional tracking across arbitrary dimensions.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --fuzz=0 < %{PATCH0}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.MD docs/README.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/doc/extension/%{pname}.md
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Tue Sep 01 2026 Vonng <rh@vonng.com> - 1.2.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Upgrade to pg_accumulator 1.2.0 with double-entry ledger registers
- Add the 1.1.3-to-1.2.0 migration preserving existing objects and data

* Sat Apr 25 2026 Vonng <rh@vonng.com> - 1.1.3-1PIGSTY
- Initial RPM release for pg_accumulator 1.1.3 from PGXN
