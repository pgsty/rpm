%define debug_package %{nil}
%global pname ddl_historization
%global sname ddl_historization
%global pginstdir /usr/pgsql-%{pgmajorversion}
%global commit 18eb9a47467873c78a82585a0cb4a7392147e293
%global gitdate 20241205
%global shortcommit 18eb9a4

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:ddl_historization supports PostgreSQL 14 through 18 in Pigsty}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1.git%{gitdate}.%{shortcommit}PGSTY%{?dist}
Summary:	PostgreSQL Extension to historize in a table all DDL changes made on a database
License:	GPL-2.0-only
URL:		https://github.com/rodo/pg_ddl_historization
Source0:	pg_ddl_historization-%{version}+git%{gitdate}.%{shortcommit}.tar.gz
Patch0:		ddl-historization-1.0.0.patch
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
PostgreSQL Extension to historize in a table all DDL changes made on a database

%prep
%autosetup -p1 -n pg_ddl_historization-%{commit}

%build
PATH=%{pginstdir}/bin:$PATH %{__make}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Mon Aug 31 2026 Vonng <rh@vonng.com> - 1.0.0-1.git20241205.18eb9a4PGSTY
- Update to upstream main snapshot 18eb9a4 with extension version 1.0.0
- Bridge the historical 0.2 line into the complete upstream update graph

* Sun Apr 12 2026 Vonng <rh@vonng.com> - 0.2-1PIGSTY
- https://github.com/rodo/pg_ddl_historization/releases/tag/0.2
* Fri Jan 10 2025 Vonng <rh@vonng.com> - 0.0.7-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
