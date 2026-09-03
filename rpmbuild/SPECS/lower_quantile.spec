%global pname lower_quantile
%global sname lower_quantile
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
Version:	1.0.3
Release:	1PGSTY%{?dist}
Summary:	Lower quantile aggregate function
License:	BSD-2-Clause
URL:		https://github.com/tvondra/lower_quantile
Source0:	lower_quantile-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
This implements the "lower quantile" aggregate, defined as
Given a multiset S of size n over R, the q-quantile item xq (in S) is the item x whose rank R(x) in the sorted multiset S is
floor(1 + q(n −1)) for 0 <= q <= 1
where the rank R(x) is the number of elements in S smaller than or equal to x.

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
%exclude %{pginstdir}/doc/extension/README.md

%if %llvm
   %{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.0.3-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Thu Jan 09 2025 Vonng <rh@vonng.com> - 1.0.3
- Bump to v1.0.3 with version correction
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 1.0.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
