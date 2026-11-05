%global sname pg_stat_plans
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:pg_stat_plans supports PostgreSQL 16 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        2.1.1
Release:        1PGSTY%{?dist}
Summary:        Query plan statistics for PostgreSQL
License:        PostgreSQL
URL:            https://github.com/pganalyze/pg_stat_plans
Source0:        pg_stat_plans-2.1.1.tar.gz
# https://github.com/pganalyze/pg_stat_plans/releases/tag/v2.1.1

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:  gcc make libzstd-devel openssl-devel pkgconfig
Requires:       postgresql%{pgmajorversion}-server

%{!?llvm:%global llvm 1}
%if %llvm
BuildRequires:  llvm-devel >= 19.0 clang-devel >= 19.0
%global with_llvm_arg %{nil}
%else
%global with_llvm_arg with_llvm=no
%endif

%description
pg_stat_plans tracks execution plans and plan statistics for PostgreSQL statements.

%prep
%setup -q -n pg_stat_plans-2.1.1

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}  %{with_llvm_arg}

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make}  %{with_llvm_arg} install DESTDIR=%{buildroot}
rm -rf %{buildroot}%{pginstdir}/doc/extension

%files
%license LICENSE
%doc README.md
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*.sql

%if %llvm
%{pginstdir}/lib/bitcode/*
%endif

%changelog
* Thu Nov 05 2026 Vonng <rh@vonng.com> - 2.1.1-1PGSTY
- Add the upstream 2.1.1 package for PostgreSQL 16 through 18
