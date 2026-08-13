%define debug_package %{nil}
%global pname pg_relation_sql
%global sname pg_relation_sql
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_relation_sql only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.2
Release:	1PGSTY%{?dist}
Summary:	Join PostgreSQL relations through generated foreign-key functions
License:	PostgreSQL
URL:		https://github.com/asmgit/pg_relation_sql
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_relation_sql/0.2.2/pg_relation_sql-0.2.2.zip
BuildArch:	noarch

BuildRequires:	pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_relation_sql turns every foreign key into a pair of set-returning SQL
functions for navigating declared relations. Upstream intentionally ships a
standalone SQL script instead of a CREATE EXTENSION package so it also works
with managed PostgreSQL services.

%prep
%setup -q -n %{sname}-%{version}

%build
# Standalone SQL script, nothing to compile.

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/share/%{pname}
%{__install} -m 0644 relation_sql.sql %{buildroot}%{pginstdir}/share/%{pname}/

%files
%license LICENSE
%doc README.md CHANGELOG.md EXPLAIN.md
%dir %{pginstdir}/share/%{pname}
%{pginstdir}/share/%{pname}/relation_sql.sql

%changelog
* Fri Aug 14 2026 Vonng <rh@vonng.com> - 0.2.2-1PGSTY
- Add the upstream PGXN 0.2.2 standalone SQL package
