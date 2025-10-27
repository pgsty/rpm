%define debug_package %{nil}
%global pname db_migrator
%global sname db_migrator
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PIGSTY%{?dist}
Summary:	migrating databases from other data sources to PostgreSQL
License:	BSD-3
URL:		https://github.com/cybertec-postgresql/db_migrator
Source0:	db_migrator-RELEASE_1_0_0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
db_migrator is a PostgreSQL extension that provides functions for migrating databases from other data sources to PostgreSQL. This requires a foreign data wrapper for the data source you want to migrate.
You also need a plugin for db_migrator that contains the code specific to the targeted data source. Currently, plugins exist for the following data sources:

%prep
%setup -q -n db_migrator-RELEASE_1_0_0

%build
PATH=%{pginstdir}/bin:$PATH make

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH make install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/doc/extension/README.db_migrator
%exclude /usr/lib/.build-id/*

%changelog
* Mon Sep 18 2023 Vonng <rh@vonng.com> - 1.0.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>