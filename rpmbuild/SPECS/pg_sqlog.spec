%define debug_package %{nil}
%global pname pg_sqlog
%global sname pg_sqlog
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.6
Release:	1PIGSTY%{?dist}
Summary:	Extension to export and import json and xml from/to postgres
License:	BSD 3-Clause License
URL:		https://github.com/kouber/pg_sqlog
Source0:	pg_sqlog-1.6.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_sqlog allows to query a foreign table, pointing to a log, recorded in a CSV format.
It has special functions to extract the query duration of each query, as well as to group similar queries together.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH make

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH make install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 1.6
- Initial RPM release, used by Pigsty <https://pigsty.io>