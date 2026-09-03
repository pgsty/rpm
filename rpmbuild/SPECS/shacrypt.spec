%global pname shacrypt
%global sname shacrypt
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
Version:	1.1
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL extension to generate SHA256-CRYPT and SHA512-CRYPT password hashes
License:	PostgreSQL
URL:		https://github.com/dverite/postgres-shacrypt
Source0:	postgres_shacrypt-%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
A PostgreSQL extension to generate SHA256-CRYPT and SHA512-CRYPT password hashes.
See https://www.akkadia.org/drepper/SHA-crypt.txt for the specification and upstream code by Ulrich Drepper.

%prep
%setup -q -n postgres_shacrypt-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH make %{with_llvm_arg} USE_PGXS=1 install DESTDIR=%{buildroot}

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/*sql

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.1-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Thu Jul 22 2024 Vonng <rh@vonng.com> - 1.1-2PIGSTY
* Thu Jul 22 2024 Vonng <rh@vonng.com> - 1.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
