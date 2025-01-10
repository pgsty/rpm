%define debug_package %{nil}
%global pname timeseries
%global sname pg_timeseries
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.6
Release:	2PIGSTY%{?dist}
Summary:	Simple and focused time-series tables for PostgreSQL, from Tembo
License:	PostgreSQL
URL:		https://github.com/tembo-io/pg_timeseries
SOURCE0:    pg_timeseries-%{version}.tar.gz
#           https://github.com/tembo-io/pg_timeseries/archive/refs/tags/v0.1.6.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server pg_cron_%{pgmajorversion}  pg_ivm_%{pgmajorversion}
%if 0%{?fedora} || 0%{?rhel} >= 8
Recommends: pg_partman_%{pgmajorversion} hydra_%{pgmajorversion}
%else
Requires: pg_partman_%{pgmajorversion} hydra_%{pgmajorversion}
%endif

%description
The purpose of this extension is to provide a cohesive user experience around the creation, maintenance,
and use of time-series tables. require pg_cron, pg_partman, hydra, and pg_ivm to work

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH make

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH make install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/doc/extension/*.md
%exclude /usr/lib/.build-id/*

%changelog
* Fri Jan 10 2025 Vonng <rh@vonng.com> - 0.1.6-2PIGSTY
* Mon Oct 14 2024 Vonng <rh@vonng.com> - 0.1.6
- Initial RPM release, used by Pigsty <https://pigsty.io>