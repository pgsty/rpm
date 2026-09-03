%global pname pg_bikram_sambat
%global sname pg_bikram_sambat
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
Version:	0.1.0
Release:	1PGSTY%{?dist}
Summary:	Bikram Sambat date type and conversion functions
License:	PostgreSQL
URL:		https://github.com/LeohangRai/pg_bikram_sambat
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_bikram_sambat/0.1.0/pg_bikram_sambat-0.1.0.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

%description
pg_bikram_sambat adds a bs_date type for the Nepali Bikram Sambat calendar,
including Gregorian AD to BS conversion functions, BS date formatting,
operators, casts, and index support.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} DEBUG_FLAGS="$RPM_OPT_FLAGS"

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} install DESTDIR=%{buildroot} DEBUG_FLAGS="$RPM_OPT_FLAGS"

%files
%doc readme.md todos.txt
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%exclude /usr/lib/.build-id/*

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.1.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Thu Apr 30 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release for upstream PGXN 0.1.0
- Package the bs_date type and Bikram Sambat conversion functions
