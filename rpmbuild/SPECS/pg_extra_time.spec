%define debug_package %{nil}
%global pname pg_extra_time
%global sname pg_extra_time
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_extra_time only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	2.1.0
Release:	1PIGSTY%{?dist}
Summary:	Extra date-time functions and operators for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/bigsmoke/pg_extra_time
Source0:	%{sname}-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/pg_extra_time/2.1.0/pg_extra_time-2.1.0.zip

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_extra_time provides date-time functions and operators that complement the
standard PostgreSQL date-time feature set.

%prep
%setup -q -n %{sname}-%{version}

%build
# SQL-only PGXS extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%license LICENCE.txt
%doc README.md CHANGELOG.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Thu Jun 11 2026 Vonng <rh@vonng.com> - 2.1.0-1PIGSTY
- Initial RPM release for upstream PGXN 2.1.0
