%global pname pgmb
%global sname pgmb
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	2PGSTY%{?dist}
Summary:	A simple PostgreSQL Message Broker system
License:	PostgreSQL
URL:		https://github.com/fraruiz/pgmb
Source0:	%{sname}-%{version}.tar.gz
Patch0:		pgmb-1.0.0-extension-schema.patch
BuildArch:	noarch
#           https://github.com/fraruiz/pgmb/archive/refs/tags/release.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server pg_cron_%{pgmajorversion} pgsql_http_%{pgmajorversion}

%description
A lightweight message broker system built inside PostgreSQL. pgmb enables
asynchronous message processing with HTTP-based worker dispatch, automatic
retries, and dead letter queue support. Features include worker management
with HTTP endpoints, queue system with pattern-based routing keys, JSONB
message publishing, and scheduled dispatch via pg_cron.

%prep
%setup -q -n %{sname}-%{version}
%patch -P 0 -p1

%build
PATH=%{pginstdir}/bin:$PATH make

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH make install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql

%changelog
* Wed Oct 28 2026 Vonng <rh@vonng.com> - 1.0.0-2PGSTY
- Require canonical pgsql_http instead of recommending legacy pg_http
- Avoid recreating the schema already declared by the extension control file
- Package the SQL-only extension as noarch

* Thu Feb 12 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
