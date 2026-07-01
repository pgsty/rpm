%global pname pg_stat_plans
%global sname pg_stat_plans
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:pg_stat_plans only supports PostgreSQL 16 through 18 in PGSTY builds}
%endif

%if 0%{?pgmajorversion} <= 17
%{!?llvm:%global llvm 0}
%else
%{!?llvm:%global llvm 1}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.1.0
Release:	1PIGSTY%{?dist}
Summary:	Track per-plan call counts, execution times and EXPLAIN texts
License:	PostgreSQL
URL:		https://github.com/pganalyze/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/pganalyze/pg_stat_plans/archive/refs/tags/v2.1.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc make pkgconf-pkg-config libzstd-devel openssl-devel
Requires:	postgresql%{pgmajorversion}-server
Requires:	libzstd openssl-libs

%description
pg_stat_plans tracks aggregate plan statistics in PostgreSQL by hashing plan
trees with a plan ID calculation. It helps identify plan regressions and stores
example EXPLAIN texts for queries. The extension must be loaded through
shared_preload_libraries.

%if %llvm
%package llvmjit
Summary:	Just-in-time compilation support for %{sname}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:	llvm-devel >= 19.0 clang-devel >= 19.0
Requires:	llvm => 19.0
%endif

%description llvmjit
This packages provides JIT support for %{sname}
%endif

%prep
%setup -q -n %{sname}-%{version}

%build
%if %llvm
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}
%else
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 with_llvm=no %{?_smp_mflags}
%endif

%install
%{__rm} -rf %{buildroot}
%if %llvm
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}
%else
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 with_llvm=no %{?_smp_mflags} install DESTDIR=%{buildroot}
%endif

%files
%license LICENSE
%doc README.md CHANGELOG.md
%{pginstdir}/lib/%{sname}.so
%{pginstdir}/share/extension/%{sname}.control
%{pginstdir}/share/extension/%{sname}--*.sql
%exclude /usr/lib/.build-id
%exclude /usr/lib/.build-id/*
%exclude /usr/lib/.build-id/*/*

%if %llvm
%files llvmjit
%{pginstdir}/lib/bitcode/%{sname}*.bc
%{pginstdir}/lib/bitcode/%{sname}/*.bc
%if 0%{?pgmajorversion} <= 17
%{pginstdir}/lib/bitcode/%{sname}/compat_16_17/*.bc
%endif
%endif

%changelog
* Fri Jun 26 2026 Vonng <rh@vonng.com> - 2.1.0-1PIGSTY
- Initial RPM release for upstream v2.1.0
