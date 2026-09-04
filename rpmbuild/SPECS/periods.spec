%global	sname	periods
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.2.3
Release:	1PGSTY%{?dist}
Summary:	PERIODs and SYSTEM VERSIONING for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/xocolatl/%{sname}
Source0:	periods-1.2.3.tar.gz
BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
BuildRequires:	pgdg-srpm-macros
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}
Requires:	postgresql%{pgmajorversion}-contrib

%description
This extension recreates the behavior defined in SQL:2016 (originally in SQL:2011)
around periods and tables with SYSTEM VERSIONING. The idea is to figure out all the
rules that PostgreSQL would like to adopt (there are some details missing in the standard)
and to allow earlier versions of PostgreSQL to simulate the behavior once the feature is finally integrated.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*
%{pginstdir}/doc/extension/README.periods

%if %llvm
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.2.3-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Sat Oct 25 2025 Vonng <rh@vonng.com> - 1.2.3
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
