%define debug_package %{nil}
%global sname postgresql_anonymizer
%global pname anon
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		pg_anon_%{pgmajorversion}
Version:	2.5.1
Release:	1PIGSTY%{?dist}
Summary:	Anonymization & Data Masking for PostgreSQL
License:	PostgreSQL
URL:		https://gitlab.com/dalibo/%{sname}
Source0:	%{sname}-%{version}.tar.gz
#Source0:   https://gitlab.com/dalibo/%{sname}/-/archive/%{version}/%{sname}-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server postgresql%{pgmajorversion}-contrib

%description
postgresql_anonymizer is an extension to mask or replace personally
identifiable information (PII) or commercially sensitive data from a
PostgreSQL database.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension/anon
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/data/*.csv             %{buildroot}%{pginstdir}/share/extension/anon/
cp -a %{_builddir}/%{sname}-%{version}/data/en_US/fake/*.csv  %{buildroot}%{pginstdir}/share/extension/anon/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%{pginstdir}/share/extension/anon/*.csv
%license LICENSE.md
%exclude /usr/lib/.build-id

%changelog
* Mon Dec 15 2025 Vonng <rh@vonng.com> - 2.5.1-1PIGSTY
* Mon Oct 27 2025 Vonng <rh@vonng.com> - 2.4.1-1PIGSTY
* Wed Jul 17 2025 Vonng <rh@vonng.com> - 2.3.0-1PIGSTY
* Wed May 07 2025 Vonng <rh@vonng.com> - 2.1.1-1PIGSTY
* Wed Jan 08 2025 Vonng <rh@vonng.com> - 2.0.0-1PIGSTY
- Rewrite in Rust
* Wed Oct 11 2023 Vonng <rh@vonng.com> - 1.3.2-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>