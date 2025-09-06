%define debug_package %{nil}
%global pname pgdd
%global sname pgdd
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.6.0
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL Data Dictionary, Inspect data dictionary via SQL
License:	Apache-2.0
URL:		https://github.com/rustprooflabs/pgdd
SOURCE0:    pgdd-%{version}.tar.gz
#           https://github.com/rustprooflabs/pgdd/archive/refs/tags/0.6.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
The PostgreSQL Data Dictionary (PgDD) is an in-database solution to provide introspection via standard SQL query syntax.
This extension makes it easy to provide a usable data dictionary to all users of a PostgreSQL database.
See the full project documentation: https://rustprooflabs.github.io/pgdd/ for more information.

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
* Mon May 26 2025 Vonng <rh@vonng.com> - 0.6.0
- Add PostgreSQL 17 support with pgrx 0.14.1
* Sun May 05 2024 Vonng <rh@vonng.com> - 0.5.2
- Initial RPM release, used by Pigsty <https://pigsty.io>