%define debug_package %{nil}
%global pname pg_fkpart
%global sname pg_fkpart
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:    1.7.0
Release:    1PIGSTY%{?dist}
License:    GPLv2
Summary:	Unsigned and other extra integer types for PostgreSQL
URL:		https://github.com/lemoineat/%{sname}
Source0:    %{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_fkpart is a PostgreSQL extension to partition tables following a foreign key of a table.

%prep
%setup -q -n %{sname}-%{version}

%build
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
USE_PGXS=1 PATH=%{pginstdir}/bin/:$PATH %{__make} DESTDIR=%{buildroot} %{?_smp_mflags} install
%{__install} -d %{buildroot}%{pginstdir}/doc/extension
%{__install} -m 644 README.md %{buildroot}%{pginstdir}/doc/extension/README-%{sname}.md

%files
%doc %{pginstdir}/doc/extension/README-%{sname}.md
%license LICENSE
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql

%changelog
* Sat Nov 02 2024 Vonng <rh@vonng.com> - 1.7.0
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>