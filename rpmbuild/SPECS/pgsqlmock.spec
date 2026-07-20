%define debug_package %{nil}
%global pname pgsqlmock
%global sname pgsqlmock
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgsqlmock only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.1
Release:	1PIGSTY%{?dist}
Summary:	Mocking and faking functions for PostgreSQL unit tests
License:	PostgreSQL
URL:		https://github.com/v-maliutin/pgSQLMock
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pgsqlmock/1.0.1/pgsqlmock-1.0.1.zip
Patch0:		pgsqlmock-1.0.1-pgtap-name.patch

BuildArch:	noarch
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	pgtap_%{pgmajorversion} >= 1.3.4

%description
pgSQLMock extends pgTAP with helpers for mocking functions, faking tables and
views, and restoring database objects after unit tests.

%prep
%setup -q -n %{sname}-%{version}
patch -p1 --forward -f < %{PATCH0}

%build
# SQL-only PL/pgSQL extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%doc README.md doc/pgsqlmock.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Mon Jul 20 2026 Vonng <rh@vonng.com> - 1.0.1-1PIGSTY
- Initial RPM release for upstream PGXN 1.0.1
- Correct the pgTAP control-file dependency name and require pgTAP 1.3.4+
