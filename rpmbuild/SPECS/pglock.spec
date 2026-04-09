%global pname pglock
%global sname pglock
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PIGSTY%{?dist}
Summary:	Lightweight distributed lock service inside PostgreSQL
License:	PostgreSQL
URL:		https://github.com/fraruiz/pglock
Source0:	%{sname}-%{version}.zip
#           https://api.pgxn.org/dist/pglock/1.0.0/pglock-1.0.0.zip
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
BuildRequires:	unzip
Requires:	postgresql%{pgmajorversion}-server
Requires:	pg_cron_%{pgmajorversion}

%description
pglock provides a lightweight distributed lock service on top of PostgreSQL
using SQL functions and a lock table with TTL cleanup through pg_cron.

%prep
%{__rm} -rf %{_builddir}/%{sname}-%{version}
cd %{_builddir}
unzip -q %{SOURCE0}
%{__rm} -rf %{_builddir}/__MACOSX
cd %{_builddir}/%{sname}-%{version}
patch -p1 --forward -f < %{_specdir}/patches/pglock-1.0.0-add-pglock-control-file.patch

%build
# Pure SQL extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
cd %{_builddir}/%{sname}-%{version}
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
PATH=%{pginstdir}/bin:$PATH %{__make} install DESTDIR=%{buildroot}
install -m 644 README.md %{buildroot}%{_docdir}/%{name}/
install -m 644 CHANGELOG.md %{buildroot}%{_docdir}/%{name}/

%files
%doc %{_docdir}/%{name}/README.md
%doc %{_docdir}/%{name}/CHANGELOG.md
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql

%changelog
* Mon Apr 06 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Drop duplicate CREATE SCHEMA from extension SQL to fix CREATE EXTENSION

* Sun Apr 05 2026 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
