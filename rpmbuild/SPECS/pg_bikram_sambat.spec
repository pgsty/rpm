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

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1PIGSTY%{?dist}
Summary:	Bikram Sambat date type and conversion functions
License:	PostgreSQL
URL:		https://github.com/LeohangRai/pg_bikram_sambat
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_bikram_sambat/0.1.0/pg_bikram_sambat-0.1.0.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc
Requires:	postgresql%{pgmajorversion}-server

%description
pg_bikram_sambat adds a bs_date type for the Nepali Bikram Sambat calendar,
including Gregorian AD to BS conversion functions, BS date formatting,
operators, casts, and index support.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Requires:	llvm >= 19.0
%endif

%description llvmjit
This package provides JIT support for %{sname}.
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} DEBUG_FLAGS="$RPM_OPT_FLAGS"

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} DEBUG_FLAGS="$RPM_OPT_FLAGS"

%files
%doc readme.md todos.txt
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/*
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Thu Apr 30 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release for upstream PGXN 0.1.0
- Package the bs_date type and Bikram Sambat conversion functions
