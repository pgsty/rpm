%global pname permuteseq
%global sname permuteseq
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
Version:	1.2.2
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL extension for scalable pseudo-random permutations of sequences
License:	PostgreSQL
URL:		https://github.com/dverite/permuteseq
Source0:	permuteseq-%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
A C PostgreSQL extension to manage scalable pseudo-random permutations of sequences.
It allows to generate unique, non-sequential, random-looking series of numbers without looking up previous values.
The general idea is to encrypt sequence positions with a Feistel cipher and cycle-walking.
The series of numbers are made unique with a secret key and reproducible with the same key.

%prep
%setup -q -n %{sname}-%{version}

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
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.2.2-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Thu Jul 22 2024 Vonng <rh@vonng.com> - 1.2.2
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
