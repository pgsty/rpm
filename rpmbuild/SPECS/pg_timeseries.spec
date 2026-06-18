%define debug_package %{nil}
%global pname timeseries
%global sname pg_timeseries
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.1
Release:	1PIGSTY%{?dist}
Summary:	Simple and focused time-series tables for PostgreSQL
License:	PostgreSQL
URL:		https://github.com/ChuckHend/pg_timeseries
SOURCE0:    pg_timeseries-%{version}.tar.gz
#           normalized from https://api.pgxn.org/dist/timeseries/0.2.1/timeseries-0.2.1.zip
BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server pg_cron_%{pgmajorversion} pg_partman_%{pgmajorversion}

%description
The purpose of this extension is to provide a cohesive user experience around the creation, maintenance,
and use of time-series tables. It requires pg_cron and pg_partman to work.

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
* Thu Jun 18 2026 Vonng <rh@vonng.com> - 0.2.1-1PIGSTY
- Update to upstream PGXN 0.2.1 using the normalized source tarball

* Fri Jan 16 2026 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
* Wed Dec 24 2025 Vonng <rh@vonng.com> - 0.1.8-1PIGSTY
* Sat Oct 25 2025 Vonng <rh@vonng.com> - 0.1.7-1PIGSTY
* Fri Jan 10 2025 Vonng <rh@vonng.com> - 0.1.6-2PIGSTY
* Mon Oct 14 2024 Vonng <rh@vonng.com> - 0.1.6-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
