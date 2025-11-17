%global	sname	periods
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	1.2.3
Release:	1PIGSTY%{?dist}
Summary:	PERIODs and SYSTEM VERSIONING for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/xocolatl/%{sname}
Source0:	periods-1.2.3.tar.gz
BuildRequires:	postgresql%{pgmajorversion} postgresql%{pgmajorversion}-devel
BuildRequires:	pgdg-srpm-macros
Requires:	postgresql%{pgmajorversion}

%description
This extension recreates the behavior defined in SQL:2016 (originally in SQL:2011)
around periods and tables with SYSTEM VERSIONING. The idea is to figure out all the
rules that PostgreSQL would like to adopt (there are some details missing in the standard)
and to allow earlier versions of PostgreSQL to simulate the behavior once the feature is finally integrated.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for periods
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?suse_version} >= 1500
BuildRequires:	llvm17-devel clang17-devel
Requires:	llvm17
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm => 19.0
%endif

%description llvmjit
This packages provides JIT support for periods
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} DESTDIR=%{buildroot} install

%files
%defattr(-,root,root,-)
%doc CHANGELOG.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*
%{pginstdir}/doc/extension/README.periods

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/%{sname}*.bc
   %{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Sat Oct 25 2025 Vonng <rh@vonng.com> - 1.2.3
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>