%define debug_package %{nil}
%global pname pglinter
%global sname pglinter
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.1.0
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL Database Linting and Analysis Extension
License:	PostgreSQL
URL:		https://github.com/pmpetit/pglinter
Source0:	pglinter-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pglinter is a PostgreSQL Database Linting and Analysis Extension that analyzes databases
for potential issues, performance problems, and best practice violations.
This is a Rust conversion of the original Python dblinter tool, providing native
PostgreSQL extension capabilities for database analysis and linting.

%prep
%setup -q -n %{sname}-%{version}

%build
PATH=%{pginstdir}/bin:~/.cargo/bin:$PATH cargo pgrx package -v

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{pginstdir}/lib %{buildroot}%{pginstdir}/share/extension
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so                  %{buildroot}%{pginstdir}/lib/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/
cp -a %{_builddir}/%{sname}-%{version}/target/release/%{pname}-pg%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}*.sql    %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Mon Feb 09 2026 Vonng <rh@vonng.com> - 1.1.0-1PIGSTY
- https://github.com/pmpetit/pglinter/releases/tag/1.1.0
* Mon Dec 15 2025 Vonng <rh@vonng.com> - 1.0.1-1PIGSTY
* Sun Nov 17 2025 Vonng <rh@vonng.com> - 1.0.0-1PIGSTY
- Initial RPM release, used by PGSTY/PIGSTY <https://pgsty.com>
