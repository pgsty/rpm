%global pname session_variable
%global sname session_variable
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
Version:	3.5
Release:	1PGSTY%{?dist}
Summary:	The session_variable Postgres database extension provides a way to create and maintain session scoped variables and constants, more or less like Oracle's global variables.
License:	GPL-3.0-only
URL:		https://github.com/splendiddata/session_variable
Source0:	session_variable-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
The session_variable Postgres database extension provides a way to create and maintain session scoped variables and constants.
This extension can be part of a solution to mimic Oracle's global constants and variables.

%prep
%setup -q -n session_variable-%{version}

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
%{pginstdir}/doc/extension/*
%exclude /usr/lib/.build-id/*
#%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 3.5-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Bump to 3.5

* Thu Oct 17 2024 Vonng <rh@vonng.com> - 3.4
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 3.3
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
