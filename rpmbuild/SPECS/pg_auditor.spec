%define debug_package %{nil}
%global pname pg_auditor
%global sname pg_auditor
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.2
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL extension to log each DML statement and flashback transactions
License:	BSD-3
URL:		https://github.com/kouber/pg_auditor
Source0:	pg_auditor-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
PostgreSQL auditing extension that records each data modification statement of specific tables,
and allows partial or complete flashback of transactions.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
#%doc README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id/*
#%exclude %{pginstdir}/doc/extension/README.md

%changelog
* Sat Aug 10 2024 Vonng <rh@vonng.com> - 0.2
- Initial RPM release, used by Pigsty <https://pigsty.io>