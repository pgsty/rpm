%global pname pg_flight_recorder
%global sname pg_flight_recorder
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 18
%{error:pg_flight_recorder supports PostgreSQL 15 through 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        2.29.2
Release:        1PIGSTY%{?dist}
Summary:        Server-side PostgreSQL performance flight recorder
License:        Apache-2.0
URL:            https://github.com/dventimisupabase/pg_flight_recorder
Source0:        %{sname}-%{version}.tar.gz
Patch0:         pg_flight_recorder-2.29.2.patch
BuildArch:      noarch

BuildRequires:  bash gawk
Requires:       postgresql%{pgmajorversion}-server
Requires:       pg_cron_%{pgmajorversion}

%description
pg_flight_recorder continuously captures PostgreSQL performance telemetry via
pg_cron. This package installs the pgfr_record collector and pgfr_analyze
reporting extensions. pg_stat_statements is optional and enables query-level
analysis.

%prep
%autosetup -p1 -n %{sname}-%{version}

%build
bash scripts/build_dbdev_package.sh pgfr_record pgfr_record/pgfr_record--%{version}.sql
bash scripts/build_dbdev_package.sh pgfr_analyze pgfr_analyze/pgfr_analyze--%{version}.sql

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
sed "s/default_version = '0.0.0'/default_version = '%{version}'/" \
    pgfr_record/extension.control > %{buildroot}%{pginstdir}/share/extension/pgfr_record.control
sed "s/default_version = '0.0.0'/default_version = '%{version}'/" \
    pgfr_analyze/extension.control > %{buildroot}%{pginstdir}/share/extension/pgfr_analyze.control
%{__install} -m 0644 pgfr_record/pgfr_record--%{version}.sql %{buildroot}%{pginstdir}/share/extension/
%{__install} -m 0644 pgfr_analyze/pgfr_analyze--%{version}.sql %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE NOTICE
%doc README.md REFERENCE.md PG18_COMPAT.md
%{pginstdir}/share/extension/pgfr_record.control
%{pginstdir}/share/extension/pgfr_record--%{version}.sql
%{pginstdir}/share/extension/pgfr_analyze.control
%{pginstdir}/share/extension/pgfr_analyze--%{version}.sql

%changelog
* Tue Jul 21 2026 Vonng <rh@vonng.com> - 2.29.2-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
- Package pgfr_record and pgfr_analyze for PostgreSQL 15 through 18
