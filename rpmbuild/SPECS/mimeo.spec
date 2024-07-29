%define debug_package %{nil}
%global pname mimeo
%global sname mimeo
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.5.1
Release:	1PIGSTY%{?dist}
Summary:	Extension for specialized, per-table replication between PostgreSQL instances
License:	BSD 2-Clause
URL:		https://github.com/omniti-labs/mimeo
Source0:	mimeo-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
Mimeo is an extension that provides specialized, per-table replication between PostgreSQL instances. It currently provides snapshot (whole table copy), incremental (based on an incrementing timestamp or id), and DML (inserts, updates and deletes).
Also installing the pg_jobmon extension (see other repositories in omniti-labs) to log all replication activity and provide monitoring is highly recommended.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
PATH=%{pginstdir}/bin:$PATH %{__make} %{?_smp_mflags} install DESTDIR=%{buildroot}

%files
%doc README.md
%{pginstdir}/bin/run_refresh.py
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/doc/extension/*.md

%changelog
* Mon Jul 29 2024 Vonng <rh@vonng.com> - 1.5.1
- Initial RPM release, used by Pigsty <https://pigsty.io>