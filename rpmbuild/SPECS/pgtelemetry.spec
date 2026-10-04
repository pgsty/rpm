%global pname pgtelemetry
%global sname pgtelemetry
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgtelemetry only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        1.7
Release:        1PGSTY%{?dist}
Summary:        Monitoring views and functions for PostgreSQL
License:        PostgreSQL
URL:            https://github.com/adjust/pg-telemetry
Source0:        pgtelemetry-1.7-cac3d192a119.tar.gz
# Source: https://codeload.github.com/adjust/pg-telemetry/tar.gz/cac3d192a119f25dc1964b13624e49b5a5a6a27c
# SHA256: b649abc2ca6b62e30e6bb02385c7a217833444852dce700bb1e7d596504deab3
BuildArch:      noarch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server
Requires:       postgresql%{pgmajorversion}-contrib

%description
Monitoring views and functions for PostgreSQL.

%prep
%setup -q -n pg-telemetry-cac3d192a119f25dc1964b13624e49b5a5a6a27c

%build
# This extension contains only SQL and documentation.

%install
rm -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%{pginstdir}/share/extension/%{pname}-head.sql

%changelog
* Sun Oct 04 2026 Vonng <rh@vonng.com> - 1.7-1PGSTY
- Initial RPM package for the EL9 aarch64 pilot
