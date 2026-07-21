%define debug_package %{nil}
%global pname pgmemento
%global sname pgmemento
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pgmemento only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.7.4
Release:        1PIGSTY%{?dist}
Summary:        Audit trail with schema versioning for PostgreSQL
License:        LGPL-3.0-only
URL:            https://github.com/pgMemento/pgMemento
Source0:        %{sname}-%{version}.tar.gz

BuildArch:      noarch
BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

%description
pgMemento provides transaction-based row auditing, DDL tracking, schema
versioning, and restoration helpers implemented in PL/pgSQL.

%prep
%setup -q -n pgMemento-%{version}

%build
bash extension/compile.sh > %{pname}--%{version}.sql

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
%{__install} -m 0644 extension/%{pname}.control \
    %{buildroot}%{pginstdir}/share/extension/
%{__install} -m 0644 %{pname}--%{version}.sql \
    %{buildroot}%{pginstdir}/share/extension/
for oldversion in 0.7 0.7.1 0.7.2 0.7.3; do
    %{__install} -m 0644 UPGRADE_v07_to_v074.sql \
        "%{buildroot}%{pginstdir}/share/extension/%{pname}--${oldversion}--%{version}.sql"
done

%files
%license LICENSE
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Tue Jul 21 2026 Vonng <rh@vonng.com> - 0.7.4-1PIGSTY
- Initial RPM release for upstream 0.7.4
