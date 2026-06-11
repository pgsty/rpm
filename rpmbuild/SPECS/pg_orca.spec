%define debug_package %{nil}
%global pname pg_orca
%global sname pg_orca
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} != 18
%{error:pg_orca only supports PostgreSQL 18}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PIGSTY%{?dist}
Summary:	ORCA query optimizer as a PostgreSQL extension
License:	Apache-2.0
URL:		https://github.com/quantumiodb/pgorca
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_orca/1.0.0/pg_orca-1.0.0.zip
#           Supported: PostgreSQL 18

BuildRequires:	cmake gcc-c++ ninja-build xerces-c-devel pkgconf-pkg-config
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	xerces-c

%description
pg_orca brings the Apache Cloudberry / Greenplum ORCA optimizer to
PostgreSQL 18 through a planner hook, falling back to the standard planner
when ORCA cannot handle a query.

%prep
%setup -q -n %{sname}-%{version}

%build
cmake -S . -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DPG_CONFIG=%{pginstdir}/bin/pg_config
cmake --build build %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
DESTDIR=%{buildroot} cmake --install build

%files
%doc README.md NOTICE
%license LICENSE
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*.sql
%exclude /usr/lib/.build-id/*

%changelog
* Thu Jun 04 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release for upstream PGXN 1.0.0
