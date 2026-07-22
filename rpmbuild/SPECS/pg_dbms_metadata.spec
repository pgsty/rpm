%define debug_package %{nil}
%global sname pg_dbms_metadata
%global pginstdir /usr/pgsql-%{pgmajorversion}

Summary:	PostgreSQL extension compatible with Oracle DBMS_METADATA
Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	2PIGSTY%{?dist}
License:	PostgreSQL
URL:		https://github.com/HexaCluster/%{sname}
Source0:	%{sname}-%{version}.tar.gz
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_dbms_metadata extracts DDL for database objects in a way compatible
with Oracle's DBMS_METADATA package. It supports retrieving DDL from SQL
queries and PL/pgSQL code.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md \
	%{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%defattr(-,root,root,-)
%license LICENSE
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%{pginstdir}/share/extension/%{sname}--*.sql
%{pginstdir}/share/extension/%{sname}.control

%changelog
* Wed Jul 22 2026 Vonng <rh@vonng.com> - 1.0.0-2PIGSTY
- Rebuild EL8 aarch64 package for PostgreSQL 18

* Tue Feb 25 2025 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-2PGDG
- Add missing build requirements and dependency

* Thu Jan 11 2024 Devrim Gündüz <devrim@gunduz.org> - 1.0.0-1PGDG
- Initial RPM packaging
