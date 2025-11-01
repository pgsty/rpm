%define debug_package %{nil}
%global pname pg_mooncake
%global sname pg_mooncake
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.0
Release:	1PIGSTY%{?dist}
Summary:	Columnstore Table in Postgres
License:	MIT
URL:		https://github.com/Mooncake-Labs/pg_mooncake
SOURCE0:    pg_mooncake-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:   pg_duckdb_%{pgmajorversion} >= 1.1.0

%description
pg_mooncake is a PostgreSQL extension that adds native columnstore tables with DuckDB execution.
Columnstore tables are stored as Iceberg or Delta Lake tables in object storage.
It require pg_duckdb to work.

%prep
%setup -q -n %{sname}-%{version}

%build
PG_VERSION=pg%{pgmajorversion} PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/*.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/*.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/*.sql     %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/*.so
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*.sql
%exclude /usr/lib/.build-id/*

%changelog
* Sat Nov 01 2025 Vonng <rh@vonng.com> - 0.2.0-1PIGSTY
- this is an unpublished release build upon pg_duckdb 1.1.0
* Fri Feb 21 2025 Vonng <rh@vonng.com> - 0.1.2-1PIGSTY
* Tue Feb 11 2025 Vonng <rh@vonng.com> - 0.1.1-1PIGSTY
* Tue Jan 21 2025 Vonng <rh@vonng.com> - 0.1.0-1PIGSTY
* Thu Oct 31 2024 Vonng <rh@vonng.com> - 0.0.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>