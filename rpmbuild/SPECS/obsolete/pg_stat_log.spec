%global pname pg_stat_log
%global sname pg_stat_log
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} != 18
%{error:pg_stat_log only supports PostgreSQL 18 in PGSTY builds}
%endif

%{!?llvm:%global llvm 1}

Name:		%{sname}_%{pgmajorversion}
Version:	0.1
Release:	1PIGSTY%{?dist}
Summary:	Track PostgreSQL log messages with the Custom Cumulative Stats API
License:	PostgreSQL
URL:		https://github.com/fabriziomello/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/fabriziomello/pg_stat_log/archive/refs/tags/0.1.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc make perl
Requires:	postgresql%{pgmajorversion}-server

%description
pg_stat_log collects cumulative PostgreSQL log message statistics grouped by
backend type, database, user, severity and SQLSTATE. It uses the Custom
Cumulative Stats API introduced in PostgreSQL 18 and must be loaded through
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
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} USE_PGXS=1 %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md
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
%endif

%changelog
* Fri Jun 26 2026 Vonng <rh@vonng.com> - 0.1-1PIGSTY
- Initial RPM release for upstream 0.1
