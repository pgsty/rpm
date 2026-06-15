%global pname pg_stat_backtrace
%global sname pg_stat_backtrace
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_stat_backtrace only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PIGSTY%{?dist}
Summary:	Capture C-level backtraces of PostgreSQL processes
License:	PostgreSQL
URL:		https://github.com/Nickyoung0/pg_stat_backtrace
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/Nickyoung0/pg_stat_backtrace/archive/refs/tags/v1.0.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	gcc make pkgconf-pkg-config libunwind-devel
Requires:	postgresql%{pgmajorversion}-server
Requires:	libunwind

%description
pg_stat_backtrace exposes SQL functions to capture or log the C-level stack
backtrace of PostgreSQL processes on Linux using ptrace and libunwind. Runtime
use depends on host ptrace policy such as kernel.yama.ptrace_scope.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/pg-stat-backtrace-%{version}-libunwind-ptrace-linktest.patch

%build
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} PG_CONFIG=%{pginstdir}/bin/pg_config with_llvm=no

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install PG_CONFIG=%{pginstdir}/bin/pg_config with_llvm=no DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md CHANGELOG.md SECURITY.md
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%exclude /usr/lib/.build-id
%exclude /usr/lib/.build-id/*
%exclude /usr/lib/.build-id/*/*

%changelog
* Sun Jun 14 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release for upstream v1.0.0
