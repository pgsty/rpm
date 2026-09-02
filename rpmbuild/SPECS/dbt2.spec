%global debug_package %{nil}
%global sname dbt2
%global pginstdir /usr/pgsql-%{pgmajorversion}

%{!?llvm:%global llvm 1}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:dbt2 0.62.0 supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Summary:	DBT-2 PostgreSQL stored functions
Name:		%{sname}-pg%{pgmajorversion}-extensions
Version:	0.62.0
Release:	1PGSTY%{?dist}
License:	Artistic-2.0
Source0:	%{sname}-%{version}.tar.gz
Patch0:		dbt2-0.62.0.patch
URL:		https://github.com/osdldbt/%{sname}/
Requires:	postgresql%{pgmajorversion}-server
BuildRequires:	gcc make
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27

%description
The C stored functions used by the DBT-2 benchmark. The benchmark driver,
schemas, data generator, and full DBT-2 toolchain are intentionally excluded.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for dbt2-extensions
Requires:	%{name}%{?_isa} = %{version}-%{release}
BuildRequires:	llvm-devel >= 17.0 clang-devel >= 17.0
Requires:	llvm >= 17.0

%description llvmjit
This package provides JIT support for dbt2-extensions.
%endif

%prep
%setup -q -n %{sname}-%{version}
patch -d storedproc/pgsql/c -p1 --fuzz=0 < %{PATCH0}

%build
pushd storedproc/pgsql/c
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}
popd

%install
%{__rm} -rf %{buildroot}
pushd storedproc/pgsql/c
PATH=%{pginstdir}/bin:$PATH %{__make} DESTDIR=%{buildroot} install
popd

%files
%license LICENSE
%doc README
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{sname}*.bc
%{pginstdir}/lib/bitcode/%{sname}/*.bc
%endif

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 0.62.0-1PGSTY
- Bump to 0.62.0
- Package only the PostgreSQL stored functions, matching the narrow DEB scope
- Drop full-kit CMake, driver, datagen and dbt2-common dependencies
- Preserve legacy function OIDs, dependencies, ACLs and comments during the row-shape migration
- Preserve strictness and parse-bind compatibility calls against search-path shadowing

* Tue Jul 21 2026 Vonng <rh@vonng.com> - 0.61.7-1PIGSTY
- Add libev development dependency for EL8 builds

* Thu Jul 10 2025 Devrim Gunduz <devrim@gunduz.org> - 0.61.7-1PGDG
- Update 0.61.7
