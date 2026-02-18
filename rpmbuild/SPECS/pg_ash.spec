%define debug_package %{nil}
%global pname ash
%global sname pg_ash
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.2
Release:	1PIGSTY%{?dist}
Summary:	Active Session History for PostgreSQL with a pure SQL implementation
License:	Apache-2.0
URL:		https://github.com/NikolayS/pg_ash
Source0:	%{sname}-%{version}.tar.gz
#           https://github.com/NikolayS/pg_ash/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server pg_cron_%{pgmajorversion}

%description
pg_ash (ash extension) provides Active Session History for PostgreSQL as a pure SQL/PLpgSQL implementation.
It samples pg_stat_activity and stores historical wait data without requiring shared_preload_libraries.

%prep
%setup -q -n %{sname}-%{version}

%build
# Pure SQL extension, no compilation required.

%install
%{__rm} -rf %{buildroot}
%{__install} -d %{buildroot}%{pginstdir}/share/extension

# Upstream ships SQL scripts only; map them into extension script names.
%{__install} -m 0644 sql/ash-install.sql %{buildroot}%{pginstdir}/share/extension/%{pname}--%{version}.sql
%{__install} -m 0644 sql/ash-1.0.sql %{buildroot}%{pginstdir}/share/extension/%{pname}--1.0.sql
%{__install} -m 0644 sql/ash-1.1.sql %{buildroot}%{pginstdir}/share/extension/%{pname}--1.1.sql
%{__install} -m 0644 sql/ash-1.1.sql %{buildroot}%{pginstdir}/share/extension/%{pname}--1.0--1.1.sql
%{__install} -m 0644 sql/ash-1.1-to-1.2.sql %{buildroot}%{pginstdir}/share/extension/%{pname}--1.1--1.2.sql

cat > %{buildroot}%{pginstdir}/share/extension/%{pname}.control <<'EOF'
comment = 'Active Session History for PostgreSQL'
default_version = '1.2'
relocatable = false
schema = ash
requires = 'pg_cron'
EOF

%files
%doc README.md RELEASE_NOTES.md
%license LICENSE
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Wed Feb 18 2026 Vonng <rh@vonng.com> - 1.2-1PIGSTY
- https://github.com/NikolayS/pg_ash/releases/tag/v1.2
- Package pg_ash as SQL extension scripts with generated control file
