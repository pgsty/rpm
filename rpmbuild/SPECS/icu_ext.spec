%global pname icu_ext
%global sname icu_ext
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

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
Version:	1.11.0
Release:	1PGSTY%{?dist}
Summary:	PostgreSQL extension (in C) to expose functionality from the ICU library
License:	PostgreSQL
URL:		https://github.com/dverite/icu_ext
Source0:	icu_ext-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
An extension to expose functionality from ICU to PostgreSQL applications.
It requires PostgreSQL version 11 or newer, configured with ICU (--with-icu).
Note: this text is in GitHub Flavored Markdown format. Please see the version on github if it's rendered weirdly elsewhere.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} LLVM_BINPATH=%{llvm_binpath}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot} LLVM_BINPATH=%{llvm_binpath}

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
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.11.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Tue Jun 30 2026 Vonng <rh@vonng.com> - 1.11.0-1PIGSTY
- Bump to upstream PGXN 1.11.0

* Wed Sep 04 2024 Vonng <rh@vonng.com> - 1.10.0-1PIGSTY
* Mon Oct 14 2024 Vonng <rh@vonng.com> - 1.9.0-1PIGSTY
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 1.8.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
