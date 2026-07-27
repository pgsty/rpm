%global pname pgmp
%global sname pgmp
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global llvm_binpath /usr/bin

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgmp only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.6
Release:	1PIGSTY%{?dist}
Summary:	Multiple precision arithmetic types for PostgreSQL
License:	LGPL-3.0-or-later
URL:		https://github.com/dvarrazzo/pgmp
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pgmp/1.0.6/pgmp-1.0.6.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc gmp-devel python3
Requires:	postgresql%{pgmajorversion}-server

%description
pgmp adds integer and rational PostgreSQL data types backed by the GNU Multiple
Precision Arithmetic Library.

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
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} LLVM_BINPATH=%{llvm_binpath}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot} LLVM_BINPATH=%{llvm_binpath}

%files
%license COPYING
%doc README.rst
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/%{pname}/
%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{pname}.index.bc
%{pginstdir}/lib/bitcode/%{pname}/
%endif
%exclude /usr/lib/.build-id/*

%changelog
* Mon Jul 27 2026 Vonng <rh@vonng.com> - 1.0.6-1PIGSTY
- Add RPM package for upstream PGXN 1.0.6
