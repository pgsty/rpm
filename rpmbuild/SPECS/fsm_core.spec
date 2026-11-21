%global pname fsm_core
%global sname fsm_core
%global pginstdir /usr/pgsql-%{pgmajorversion}

%if 0%{?pgmajorversion} < 15 || 0%{?pgmajorversion} > 19
%{error:fsm_core only supports PostgreSQL 15 through 19 in PGSTY builds}
%endif

Name:		%{sname}_%{pgmajorversion}
Version:	1.2.0
Release:	1PGSTY%{?dist}
Summary:	Finite state machine core SQL objects for PostgreSQL
License:	Apache-2.0
URL:		https://github.com/pgfsm/fsm
Source0:	%{sname}-%{version}.tar.gz
BuildArch:	noarch
# Normalized official fsm_core-v1.2.0 release ZIP with the upstream LICENSE.

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server
Requires:	postgresql%{pgmajorversion}-contrib
Requires:	pgmq_%{pgmajorversion} >= 1.4.4
Requires:	pg_cron_%{pgmajorversion} >= 1.5.0

%description
fsm_core installs the SQL schema objects for a finite state machine workflow
system. It requires ltree, pgmq and pg_cron at extension creation time.

%prep
%setup -q -n %{sname}-%{version}

%build
# SQL-only extension bundle without PGXS Makefile.

%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
%{__install} -m 644 %{pname}.control %{buildroot}%{pginstdir}/share/extension/
%{__install} -m 644 %{pname}--*.sql %{buildroot}%{pginstdir}/share/extension/

%files
%license LICENSE
%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Sat Nov 21 2026 Ruohang Feng <rh@vonng.com> - 1.2.0-1PGSTY
- Update to upstream 1.2.0.
- Require pg_cron and install the upstream license.

* Thu Jun 11 2026 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- Initial RPM release for upstream PGXN 1.1.0
