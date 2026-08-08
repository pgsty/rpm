%define debug_package %{nil}
%global pname cat_tools
%global sname cat_tools
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:cat_tools only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.3.0
Release:        1PIGSTY%{?dist}
Summary:        Tools for interfacing with the PostgreSQL catalog
License:        MIT
URL:            https://github.com/decibel/cat_tools
Source0:        %{sname}-%{version}.tar.gz
#               normalized from https://api.pgxn.org/dist/cat_tools/0.3.0/cat_tools-0.3.0.zip
BuildArch:      noarch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

%description
cat_tools provides SQL functions and views for inspecting and working with
PostgreSQL system catalogs. Version 0.3.0 supports PostgreSQL 12 and later;
PGSTY packages it for the active PostgreSQL 14 through 18 releases.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} PG_CONFIG=%{pginstdir}/bin/pg_config

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot} PG_CONFIG=%{pginstdir}/bin/pg_config

%files
%license LICENSE
%doc README.asc HISTORY.asc
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Fri Aug 07 2026 Vonng <rh@vonng.com> - 0.3.0-1PIGSTY
- Initial RPM release for upstream PGXN 0.3.0
