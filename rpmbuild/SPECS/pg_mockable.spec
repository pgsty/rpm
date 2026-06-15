%define debug_package %{nil}
%global pname pg_mockable
%global sname pg_mockable
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_mockable only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.1.0
Release:	1PIGSTY%{?dist}
Summary:	Mock PostgreSQL functions for testing
License:	PostgreSQL
URL:		https://github.com/bigsmoke/pg_mockable
Source0:	%{sname}-%{version}.tar.gz
#           https://pgxn.org/dist/pg_mockable/1.1.0/

BuildArch:	noarch
BuildRequires:	pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_mockable creates mockable wrapper functions in the mockable schema, so tests
can replace calls to functions such as now() with deterministic values.

%prep
%setup -q -n %{sname}-%{version}

%build
# SQL-only PL/pgSQL extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
%{__install} -m 0644 %{pname}.control %{buildroot}%{pginstdir}/share/extension/
%{__install} -m 0644 sql/%{pname}--*.sql %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENCE.txt
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Mon Jun 15 2026 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- Initial RPM release for upstream PGXN 1.1.0
