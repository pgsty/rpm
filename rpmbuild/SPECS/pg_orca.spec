%global pname pg_orca
%global sname pg_orca
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 18 || 0%{?pgmajorversion} > 19
%{error:pg_orca only supports PostgreSQL 18 and 19}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.1.0
Release:	1PGSTY%{?dist}
Summary:	ORCA query optimizer as a PostgreSQL extension
License:	Apache-2.0
URL:		https://github.com/quantumiodb/pgorca
Source0:	%{sname}-%{version}.tar.gz
Patch0:         pg_orca-1.1.0-optional-cpack.patch
Patch1:         pg_orca-1.1.0-static-init-order.patch
#           https://github.com/quantumiodb/pgorca/archive/refs/tags/v1.1.0.tar.gz
#           Supported: PostgreSQL 18 and 19

BuildRequires:	cmake gcc-c++ ninja-build xerces-c-devel pkgconf-pkg-config
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	xerces-c

%description
pg_orca brings the Apache Cloudberry / Greenplum ORCA optimizer to
PostgreSQL 18 and 19 through a planner hook, falling back to the standard planner
when ORCA cannot handle a query.

%prep
%setup -q -n pgorca-%{version}
%patch -P 0 -p1 -F0
%patch -P 1 -p1 -F0

%build
%set_build_flags
cmake -S . -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=Release \
    -DPG_ORCA_BUNDLED_XERCES=OFF -DPG_ORCA_ENABLE_CPACK=OFF \
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
* Sat Nov 21 2026 Vonng <rh@vonng.com> - 1.1.0-1PGSTY
- Bump to 1.1.0 and enable upstream PostgreSQL 19 support
- Avoid cross-translation-unit static initialization in invalid OID checks
- Keep distribution xerces-c and make upstream CPack optional for native packaging

* Thu Jun 04 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release for upstream PGXN 1.0.0
