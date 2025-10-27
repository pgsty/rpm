%define debug_package %{nil}
%global pname sparql
%global sname pgsparql
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.0
Release:	1PIGSTY%{?dist}
Summary:	SPARQL utilities for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/lacanoid/pgsparql
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
It helps one query SPARQL datasources. SPARQL queries are compiled into Postgres views, so you can use them nicely in SQL.
It is currently used with Virtuoso, so it is useful with sources like dbpedia. It might or might not work with other RDF backends.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}


%files
%doc README.md
%license LICENSE.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Sun Feb 09 2025 Vonng <rh@vonng.com> - 1.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>