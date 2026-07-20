%define debug_package %{nil}
%global pname fbsql
%global sname fbsql
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 16 || 0%{?pgmajorversion} > 18
%{error:fbsql 0.1.0 only supports PostgreSQL 16 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1PIGSTY%{?dist}
Summary:	Formula-based statistical modeling in SQL
License:	MIT
URL:		https://github.com/dsc-chiba-u/FbSQL
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/fbsql/0.1.0/fbsql-0.1.0.zip

BuildArch:	noarch
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	plr_%{pgmajorversion} >= 8.4.0

%description
FbSQL provides a relation-oriented statistical modeling DSL for PostgreSQL.
It fits Gaussian and binomial generalized linear models through PL/R and
scores relations from the resulting model relation.

%prep
%setup -q -n %{sname}-%{version}

%build
# SQL and PL/R extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md Changes TODO.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Mon Jul 20 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release for upstream PGXN 0.1.0
- Require PL/R 8.4.0 or newer and PostgreSQL 16 through 18
