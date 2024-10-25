%define debug_package %{nil}
%global sname ddlx
%global pname pgddl
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.28
Release:	1PIGSTY%{?dist}
Summary:	DDL eXtractor functions for PostgreSQL (ddlx)
License:	PostgreSQL
URL:		https://github.com/lacanoid/pgddl
Source0:	%{pname}-%{version}.tar.gz
#           https://github.com/michelp/ddlx/archive/refs/heads/master.zip
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
This is an SQL-only extension for PostgreSQL that provides uniform functions
for generating SQL Data Definition Language (DDL) scripts for objects created
in a database. It contains a bunch of SQL functions to convert PostgreSQL
system catalogs to nicely formatted snippets of SQL DDL, such as CREATE TABLE.

%prep
%setup -q -n %{pname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}
%{__mkdir} -p %{buildroot}%{pginstdir}/doc/extension/
%{__cp} README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%license LICENSE.md
%defattr(644,root,root,755)
%{pginstdir}/share/extension/%{sname}*.sql
%{pginstdir}/share/extension/%{sname}.control
%doc %{pginstdir}/doc/extension/README-%{sname}.md

%changelog
* Fri Oct 25 2023 Vonng <rh@vonng.com> - 0.28
- Initial RPM release, used by Pigsty <https://pigsty.io>