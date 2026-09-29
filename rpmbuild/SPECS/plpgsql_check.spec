%global pname plpgsql_check
%global sname plpgsql_check
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:plpgsql_check only supports PostgreSQL 14 through 18 in PGSTY builds}
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
Version:	2.10.11
Release:	1PGSTY%{?dist}
Summary:	Additional tools for PL/pgSQL function validation
License:	MIT
URL:		https://github.com/okbob/plpgsql_check
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
plpgsql_check provides direct and indirect validation, profiling, tracing, and
dependency inspection tools for PL/pgSQL functions.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md TODO.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}*
%endif

%changelog
* Tue Sep 29 2026 Vonng <rh@vonng.com> - 2.10.11-1PGSTY
- Update to 2.10.11

* Sat Sep 19 2026 Vonng <rh@vonng.com> - 2.10.10-1PGSTY
- Update to 2.10.10

* Fri Sep 04 2026 Vonng <rh@vonng.com> - 2.10.4-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Fri Aug 07 2026 Vonng <rh@vonng.com> - 2.10.4-1PIGSTY
- Update to latest upstream PGXN 2.10.4

* Mon Jul 27 2026 Vonng <rh@vonng.com> - 2.10.3-1PIGSTY
- Update to latest upstream PGXN 2.10.3

* Sun Jul 19 2026 Vonng <rh@vonng.com> - 2.10.1-1PIGSTY
- Update to latest upstream PGXN 2.10.1

* Wed Jul 01 2026 Vonng <rh@vonng.com> - 2.9.2-1PIGSTY
- Update to upstream PGXN 2.9.2

* Thu Jun 04 2026 Vonng <rh@vonng.com> - 2.9.1-1PIGSTY
- Update to upstream PGXN 2.9.1

* Sun May 24 2026 Vonng <rh@vonng.com> - 2.9.0-1PIGSTY
- Initial RPM release for upstream PGXN 2.9.0
