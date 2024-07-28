%define debug_package %{nil}
%global pname pgdd
%global sname pgdd
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.5.2
Release:	1PIGSTY%{?dist}
Summary:	PostgreSQL Data Dictionary, Inspect data dictionary via SQL
License:	Apache-2.0
URL:		https://github.com/rustprooflabs/pgdd
#           https://github.com/rustprooflabs/pgdd/archive/refs/tags/0.5.2.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
The PostgreSQL Data Dictionary (PgDD) is an in-database solution to provide introspection via standard SQL query syntax.
This extension makes it easy to provide a usable data dictionary to all users of a PostgreSQL database.
See the full project documentation: https://rustprooflabs.github.io/pgdd/ for more information.

%install
%{__rm} -rf %{buildroot}
install -d %{buildroot}%{pginstdir}/lib/
install -d %{buildroot}%{pginstdir}/share/extension/
install -m 755 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/lib/%{pname}.so %{buildroot}%{pginstdir}/lib/
install -m 644 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}-*.sql %{buildroot}%{pginstdir}/share/extension/
install -m 644 %{_sourcedir}/%{pname}_%{pgmajorversion}/usr/pgsql-%{pgmajorversion}/share/extension/%{pname}.control %{buildroot}%{pginstdir}/share/extension/

%files
%{pginstdir}/lib/%{pname}.so
%{pginstdir}/share/extension/%{pname}.control
%{pginstdir}/share/extension/%{pname}*sql
%exclude /usr/lib/.build-id

%changelog
* Sun May 5 2024 Vonng <rh@vonng.com> - 0.5.2
- Initial RPM release, used by Pigsty <https://pigsty.io>