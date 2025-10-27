%define debug_package %{nil}
%global pname pg_drop_events
%global sname pg_drop_events
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL extension that logs transaction ids of drop table, drop column, drop materialized view statements to aid point in time recovery
License:	PostgreSQL
URL:		https://github.com/bolajiwahab/pg_drop_events
Source0:	%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_drop_events is a PostgreSQL extension that logs transaction ids of drop table,
drop column, drop materialized view statements to aid point in time recovery.
To perform point in time recovery in case of a disaster whereby a table or a table
column was mistakenly dropped, you simply specify the xact_id you get from the pg_drop_events table as the recovery_target_xid.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH make

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH make install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/share/extension/*.control
%{pginstdir}/share/extension/*sql
%exclude /usr/lib/.build-id/*
%exclude %{pginstdir}/doc/extension/pg_drop_events.md

%changelog
* Thu Jan 23 2024 Vonng <rh@vonng.com> - 0.1.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>