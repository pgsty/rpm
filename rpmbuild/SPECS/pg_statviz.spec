%global pname pg_statviz
%global sname pg_statviz_extension
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_statviz is packaged for PostgreSQL 14 through 18}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.2.1
Release:        1PGSTY%{?dist}
Summary:        Capture PostgreSQL statistics snapshots for visualization
License:        PostgreSQL
URL:            https://github.com/vyruss/pg_statviz
Source0:        %{pname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

%description
pg_statviz captures PostgreSQL statistics snapshots in a fixed schema for
time-series analysis and visualization. This package contains only the SQL
extension; the optional Python command-line client is not included.

%prep
%setup -q -n %{pname}-%{version}

%build
# Pure SQL/PLpgSQL PGXS extension; there is nothing to compile.

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot} PG_CONFIG=%{pginstdir}/bin/pg_config
%{__rm} -rf %{buildroot}%{pginstdir}/doc/extension

%files
%license LICENSE
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Fri Sep 04 2026 Vonng <rh@vonng.com> - 1.2.1-1PGSTY
- Add the extension-only pg_statviz 1.2.1 PGDG gap package for PostgreSQL 14-18
