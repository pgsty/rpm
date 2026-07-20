%define debug_package %{nil}
%global pname cron_utils
%global sname cron_utils
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:cron_utils only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1PIGSTY%{?dist}
Summary:	Parse cron expressions and compute trigger times
License:	MIT
URL:		https://github.com/Myshkouski/pg-cron-utils
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/cron_utils/0.1.0/cron_utils-0.1.0.zip

BuildArch:	noarch
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
cron_utils provides SQL functions to parse cron expressions, test whether a
timestamp matches an expression, and compute previous or next trigger times.

%prep
%setup -q -n %{sname}-%{version}

%build
# SQL-only PL/pgSQL extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}
%{__rm} -f %{buildroot}%{pginstdir}/doc/extension/README.md

%files
%license LICENSE
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Mon Jul 20 2026 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
- Initial RPM release for the upstream PGXN unstable distribution 0.1.0
