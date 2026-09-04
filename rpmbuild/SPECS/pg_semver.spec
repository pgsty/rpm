%global sname semver
%global pginstdir /usr/pgsql-%{pgmajorversion}
%{!?llvm:%global llvm 1}

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Summary:	A semantic version data type for PostgreSQL
Name:		%{sname}_%{pgmajorversion}
Version:	0.41.0
Release:	1PGSTY%{?dist}
License:	PostgreSQL
Source0:	pg-semver-%{version}.tar.gz
URL:		https://github.com/theory/pg-%{sname}/
BuildRequires:	postgresql%{pgmajorversion}-devel
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server

Obsoletes:	%{sname}%{pgmajorversion} < 0.31.0-2

%description
This library contains a single PostgreSQL extension, a data type called "semver".
It's an implementation of the version number format specified by the Semantic
Versioning 2.0.0 Specification.

%prep
%setup -q -n pg-%{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{with_llvm_arg} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%defattr(644,root,root,755)
%doc %{pginstdir}/doc/extension/%{sname}.md
%license LICENSE
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}*sql
%{pginstdir}/share/extension/%{sname}.control

%if %llvm
   %{pginstdir}/lib/bitcode/src/%{sname}*.bc
   %{pginstdir}/lib/bitcode/src/%{sname}/src/*.bc
%endif

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 0.41.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage

* Wed Dec 24 2025 Vonng <rh@vonng.com> - 0.41.0-1PIGSTY
* Sun Oct 26 2025 Vonng <rh@vonng.com> - 0.40.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
