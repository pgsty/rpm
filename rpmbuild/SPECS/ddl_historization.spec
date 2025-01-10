%define debug_package %{nil}
%global pname ddl_historization
%global sname ddl_historization
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.0.7
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL Extension to historize in a table all DDL changes made on a database
License:	GPL-2.0
URL:		https://github.com/rodo/ddl_historization
Source0:	pg_ddl_historization-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
PostgreSQL Extension to historize in a table all DDL changes made on a database

%prep
%setup -q -n pg_ddl_historization-%{version}

%build
PATH=%{pginstdir}/bin:$PATH make

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH make install DESTDIR=%{buildroot}

%files
%doc README.md
%license LICENSE
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Fri Jan 10 2025 Vonng <rh@vonng.com> - 0.0.7-1PIGSTY
- Initial RPM release, used by Pigsty <https://pigsty.io>
