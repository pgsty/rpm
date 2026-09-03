%global pname pg_liquid
%global sname pg_liquid
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
Version:	0.1.7
Release:	1PGSTY%{?dist}
Summary:	Liquid-inspired Datalog graph query extension for PostgreSQL
License:	MIT
URL:		https://github.com/michael-golfi/pg_liquid
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_liquid brings Liquid-style graph querying, assertions, recursive closure,
compounds, and row normalizers to PostgreSQL as a native extension.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/pg_liquid-0.1.7.patch

%build
cd %{_builddir}/%{sname}-%{version}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} all

%install
%{__rm} -rf %{buildroot}
cd %{_builddir}/%{sname}-%{version}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.1.7-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Restore automatic debuginfo and debugsource generation with %setup

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 0.1.7-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
