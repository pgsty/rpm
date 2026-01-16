%define debug_package %{nil}
%global pname timeseries
%global sname pg_timeseries
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.0
Release:	1PIGSTY%{?dist}
Summary:	Simple and focused time-series tables for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/ChuckHend/pg_timeseries
SOURCE0:    pg_timeseries-%{version}.tar.gz
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server pg_cron_%{pgmajorversion} pg_partman_%{pgmajorversion}

%description
The purpose of this extension is to provide a cohesive user experience around the creation, maintenance,
and use of time-series tables. require pg_cron, pg_partman, hydra, and pg_ivm to work

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH make

%install
%{__rm} -rf %{buildroot}
# Remove generated file to avoid conflict with source file during install
%{__rm} -f sql/timeseries--0.1.6.sql
PATH=%{pginstdir}/bin:$PATH make install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/doc/extension/*.md
%exclude /usr/lib/.build-id/*

%changelog
* Fri Jan 16 2026 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
* Wed Dec 24 2025 Vonng <rh@vonng.com> - 0.1.8-1PIGSTY
* Sat Oct 25 2025 Vonng <rh@vonng.com> - 0.1.7-1PIGSTY
* Fri Jan 10 2025 Vonng <rh@vonng.com> - 0.1.6-2PIGSTY
* Mon Oct 14 2024 Vonng <rh@vonng.com> - 0.1.6-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>