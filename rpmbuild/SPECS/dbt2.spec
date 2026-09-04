%global sname dbt2
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:dbt2 0.62.0 supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

%if %llvm
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

Summary:	DBT-2 PostgreSQL stored functions
Name:		%{sname}-pg%{pgmajorversion}-extensions
Version:	0.62.0
Release:	1PGSTY%{?dist}
License:	Artistic-2.0
Source0:	%{sname}-%{version}.tar.gz
Patch0:		dbt2-0.62.0.patch
URL:		https://github.com/osdldbt/%{sname}/
%if %llvm
BuildRequires:	llvm-devel >= 19.0
BuildRequires:	clang-devel >= 19.0
%endif

Requires:	postgresql%{pgmajorversion}-server
BuildRequires:	gcc make
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27

%description
The C stored functions used by the DBT-2 benchmark. The benchmark driver,
schemas, data generator, and full DBT-2 toolchain are intentionally excluded.

%prep
%setup -q -n %{sname}-%{version}
patch -d storedproc/pgsql/c -p1 --fuzz=0 < %{PATCH0}

%build
pushd storedproc/pgsql/c
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} %{?_smp_mflags}
popd

%install
%{__rm} -rf %{buildroot}
pushd storedproc/pgsql/c
PATH=%{pginstdir}/bin:$PATH %{__make} %{with_llvm_arg} DESTDIR=%{buildroot} install
popd

%files
%license LICENSE
%doc README
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%{pginstdir}/lib/bitcode/%{sname}*.bc
%{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 0.62.0-1PGSTY
- Align LLVM dependencies and the PGXS enablement toggle with pgrpms
- Merge extension bitcode into the main package and retire the llvmjit subpackage
- Bump to 0.62.0
- Package only the PostgreSQL stored functions, matching the narrow DEB scope
- Drop full-kit CMake, driver, datagen and dbt2-common dependencies
- Preserve legacy function OIDs, dependencies, ACLs and comments during the row-shape migration
- Preserve strictness and parse-bind compatibility calls against search-path shadowing

* Tue Jul 21 2026 Vonng <rh@vonng.com> - 0.61.7-1PIGSTY
- Add libev development dependency for EL8 builds

* Thu Jul 10 2025 Devrim Gunduz <devrim@gunduz.org> - 0.61.7-1PGDG
- Update 0.61.7
