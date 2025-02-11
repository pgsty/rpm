%define debug_package %{nil}
%global pname pg_mooncake
%global sname pg_mooncake
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.1
Release:	1PIGSTY%{?dist}
Summary:	Columnstore Table in Postgres
License:	MIT
URL:		https://github.com/Mooncake-Labs/pg_mooncake
SOURCE0:    pg_mooncake-%{version}.tar.gz
#           https://github.com/pg_mooncake/pg_mooncake/archive/refs/tags/v0.1.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
# we will use pg_duckdb's libduckdb instead to avoid conflict later

%description
pg_mooncake is a PostgreSQL extension that adds native columnstore tables with DuckDB execution.
Columnstore tables are stored as Iceberg or Delta Lake tables in object storage.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} release

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%{pginstdir}/lib/%{pname}*.so
%{pginstdir}/lib/libduckdb.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*

%changelog
* Tue Feb 11 2025 Vonng <rh@vonng.com> - 0.1.1
* Tue Jan 21 2025 Vonng <rh@vonng.com> - 0.1.0
* Thu Oct 31 2024 Vonng <rh@vonng.com> - 0.0.1
- Initial RPM release, used by Pigsty <https://pigsty.io>