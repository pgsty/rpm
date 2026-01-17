%global pname pg_ttl_index
%global sname pg_ttl_index
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	2.0.0
Release:	1PIGSTY%{?dist}
Summary:	Automatic data expiration with TTL indexes
License:	PostgreSQL
URL:		https://github.com/ibrahimkarimeddin/postgres-extensions-pg_ttl
Source0:	postgres-extensions-pg_ttl-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_ttl_index provides automatic data expiration with TTL (Time-To-Live) indexes.
It allows PostgreSQL to automatically delete expired rows based on TTL index definitions.

%prep
%setup -q -n postgres-extensions-pg_ttl-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/doc/extension/README.md
%{pginstdir}/doc/extension/CONTRIBUTING.md

%changelog
* Sat Jan 17 2026 Vonng <rh@vonng.com> - 2.0.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
