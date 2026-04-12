%global pname pg_isok
%global sname pg_isok
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.4.1
Release:	1PIGSTY%{?dist}
Summary:	Query-based data integrity management and soft alerting for PostgreSQL
License:	AGPL-3.0-or-later
URL:		https://codeberg.org/kop/pg_isok
Source0:	%{sname}-%{version}.tar.gz
#           normalized source tarball from the upstream PGXN release archive
#           Supported: PostgreSQL 10+
BuildArch:	noarch

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_isok stores SQL checks as data, executes them in batches, tracks changes in
questionable rows over time, and lets operators defer or accept individual
findings so later runs surface only newly interesting data quality issues.

%prep
%{__rm} -rf %{_builddir}/%{sname}-%{version}
mkdir -p %{_builddir}/%{sname}-%{version}
tar -C %{_builddir}/%{sname}-%{version} --strip-components=1 -xzf %{SOURCE0}

%build
# Pure SQL extension, nothing to compile.

%install
%{__rm} -rf %{buildroot}
cd %{_builddir}/%{sname}-%{version}
%{__mkdir_p} %{buildroot}%{pginstdir}/share/extension
%{__mkdir_p} %{buildroot}%{_docdir}/%{name}
%{__mkdir_p} %{buildroot}%{_licensedir}/%{name}
install -m 0644 pg_isok.control %{buildroot}%{pginstdir}/share/extension/
install -m 0644 sql/pg_isok--*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 0644 doc/index.html %{buildroot}%{_docdir}/%{name}/
install -m 0644 doc/pg_isok.txt %{buildroot}%{_docdir}/%{name}/
install -m 0644 NEWS %{buildroot}%{_docdir}/%{name}/
install -m 0644 LICENSE %{buildroot}%{_licensedir}/%{name}/

%files
%license %{_licensedir}/%{name}/LICENSE
%doc %{_docdir}/%{name}/index.html
%doc %{_docdir}/%{name}/pg_isok.txt
%doc %{_docdir}/%{name}/NEWS
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}--*.sql

%changelog
* Sun Apr 12 2026 Vonng <rh@vonng.com> - 1.4.1-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
