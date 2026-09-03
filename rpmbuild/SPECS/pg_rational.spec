%global pname pg_rational
%global sname pg_rational
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_rational only supports PostgreSQL 14 through 18 in PGSTY builds}
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
Version:	0.0.3
Release:	1PGSTY%{?dist}
Summary:	Precise fractional arithmetic for PostgreSQL
License:	MIT
URL:		https://github.com/begriffs/pg_rational
Source0:	pg_rational-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
An efficient custom type. Perfect for exact arithmetic or user-specified table row ordering. Holds values as big as an integer, with matching precision in the denominator.
Features:
Stores fractions in exactly 64 bits (same size as float)
Written in C for high performance
Detects and halts arithmetic overflow for correctness
Uses native CPU instructions for fast overflow detection
Defers GCD calculation until requested or absolutely required
Supports btree and hash indices
Implements Stern-Brocot trees for finding intermediate points
Coercion from integer/bigint/tuple
Custom aggregate

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
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.0.3-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sat Aug 08 2026 Vonng <rh@vonng.com> - 0.0.3-1PIGSTY
- Bump to 0.0.3

* Mon Jul 29 2024 Vonng <rh@vonng.com> - 0.0.2
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
