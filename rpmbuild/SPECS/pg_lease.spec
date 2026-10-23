%global pname pg_lease
%global sname pg_lease
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:           %{sname}_%{pgmajorversion}
Version:        0.1.0
Release:        1PGSTY%{?dist}
Summary:        PostgreSQL leases with TTL expiry and fencing epochs
License:        MIT
URL:            https://pgxn.org/dist/pg_lease/
Source0:        %{sname}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  make postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:       postgresql%{pgmajorversion}-server

%description
pg_lease implements time-bounded ownership of named resources using SQL
and PL/pgSQL, with acquire, renew, release and inspect operations. This
upstream testing release uses lazy expiry and monotonically increasing
fencing epochs. It does not provide fencing across database failover.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make}

%install
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}

%files
%license LICENSE
%doc README.md CHANGELOG.md specs/
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Fri Oct 23 2026 Vonng <rh@vonng.com> - 0.1.0-1PGSTY
- Package the upstream testing release for PostgreSQL 14 through 18.
- Preserve the pure SQL payload as an architecture-independent package.
