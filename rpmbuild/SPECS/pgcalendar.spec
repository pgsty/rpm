%global pname pgcalendar
%global sname pgcalendar
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.1.0
Release:	1PIGSTY%{?dist}
Summary:	Infinite calendar and recurring schedule extension for PostgreSQL
License:	MIT
URL:		https://github.com/h4kbas/pgcalendar
Source0:	%{sname}-%{version}.zip
#           https://api.pgxn.org/dist/pgcalendar/1.1.0/pgcalendar-1.1.0.zip
#           Supported: PostgreSQL 12+
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	unzip
Requires:	postgresql%{pgmajorversion}-server

%description
pgcalendar is a PostgreSQL extension for recurring events, schedule
projections, and exception handling.

%prep
%{__rm} -rf %{_builddir}/%{sname}-%{version}
cd %{_builddir}
unzip -q %{SOURCE0}
cd %{_builddir}/%{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/pgcalendar-1.1.0-fix-extension-metadata.patch

%build
cd %{_builddir}/%{sname}-%{version}
# Pure SQL extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
cd %{_builddir}/%{sname}-%{version}
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
install -m 644 %{pname}.control %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{pname}--%{version}.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{pname}--%{version}--uninstall.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/README.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--%{version}.sql
%{pginstdir}/share/extension/%{pname}--%{version}--uninstall.sql

%changelog
* Sun Apr 05 2026 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
