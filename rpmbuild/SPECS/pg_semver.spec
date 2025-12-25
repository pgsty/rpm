%global sname semver
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}

Summary:	A semantic version data type for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.41.0
Release:	1PIGSTY%{?dist}
License:	PostgreSQL
Source0:	pg-semver-%{version}.tar.gz
URL:		https://github.com/theory/pg-%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel
Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 0.31.0-2

%description
This library contains a single PostgreSQL extension, a data type called "semver".
It's an implementation of the version number format specified by the Semantic
Versioning 2.0.0 Specification.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for semver
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
This package provides JIT support for semver
%endif

%prep
%setup -q -n pg-%{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
%files llvmjit
   %{pginstdir}/lib/bitcode/src/%{sname}*.bc
   %{pginstdir}/lib/bitcode/src/%{sname}/src/*.bc
%endif

%changelog
* Wed Dec 24 2025 Vonng <rh@vonng.com> - 0.41.0-1PIGSTY
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 0.40.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
