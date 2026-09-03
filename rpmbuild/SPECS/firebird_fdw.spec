%global pname firebird_fdw
%global sname firebird_fdw
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
Version:	1.4.2
Release:	1PGSTY%{?dist}
Summary:	A PostgreSQL foreign data wrapper (FDW) for Firebird
License:	PostgreSQL
URL:		https://github.com/ibarwick/firebird_fdw
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27 libfq >= 0.6.2 firebird-devel >= 2.0.0
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server libfq >= 0.6.2

%description
This is a foreign data wrapper (FDW) to connect PostgreSQL to Firebird.
It provides both read (SELECT) and write (INSERT/UPDATE/DELETE) support, as well as pushdown of some operations.
While it appears to be working reliably, please be aware this is still very much work-in-progress; USE AT YOUR OWN RISK.
firebird_fdw is designed to be compatible with PostgreSQL 9.5 ~ 19.
The range of firebird_fdw options available for a particular PostgreSQL version depends on the state of the Foreign Data Wrapper (FDW) API
for that version; the more recent the version, the more features will be available. However, not all FDW API features are currently supported.

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

%if %llvm
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.4.2-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Add the complete LLVM toolchain and package its bitcode payload explicitly

* Sun Jul 05 2026 Vonng <rh@vonng.com> - 1.4.2-2PIGSTY
- Rebuild firebird_fdw 1.4.2 against libfq 0.6.2
* Sat Jun 06 2026 Vonng <rh@vonng.com> - 1.4.2-1PIGSTY
- https://github.com/ibarwick/firebird_fdw/releases/tag/1.4.2
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 1.4.1-1PIGSTY
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.4.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
