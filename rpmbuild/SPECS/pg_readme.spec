%define debug_package %{nil}
%global pname pg_readme
%global sname pg_readme
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 14 || 0%{?pgmajorversion} > 18
%{error:pg_readme only supports PostgreSQL 14 through 18 in PGSTY builds}
%endif

Name:           %{sname}_%{pgmajorversion}
Version:        0.7.1
Release:        1PGSTY%{?dist}
Summary:        Generate Markdown documentation from PostgreSQL comments
License:        PostgreSQL
URL:            https://github.com/bigsmoke/pg_readme
Source0:        %{sname}-%{version}.tar.gz
#               normalized from https://api.pgxn.org/dist/pg_readme/0.7.1/pg_readme-0.7.1.zip
BuildArch:      noarch

BuildRequires:  postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server
Requires:       postgresql%{pgmajorversion}-contrib

%description
pg_readme generates Markdown documentation for PostgreSQL extensions and
schemas from COMMENT objects stored in the pg_description system catalog.

%prep
%setup -q -n %{sname}-%{version}

%build
# SQL-only PGXS extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot} PG_CONFIG=%{pginstdir}/bin/pg_config

%files
%license LICENCE.txt
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql
%{pginstdir}/share/extension/%{pname}_test_extension.control
%{pginstdir}/share/extension/%{pname}_test_extension--*.sql

%changelog
* Fri Aug 07 2026 Vonng <rh@vonng.com> - 0.7.1-1PIGSTY
- Initial RPM release for upstream PGXN 0.7.1
