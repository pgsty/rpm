%define debug_package %{nil}
%global pname plprql
%global sname plprql
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.1.0
Release:	1PIGSTY%{?dist}
Summary:	Use PRQL in PostgreSQL
License:	Apache-2.0
URL:		https://github.com/kaspermarstal/plprql
#           https://github.com/kaspermarstal/plprql/archive/refs/tags/v0.1.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
PL/PRQL is a PostgreSQL extension that lets you write functions with PRQL. The extension supports PostgreSQL v12-16 on Linux and macOS.

PRQL (Pipelined Relational Query Language) is an open source query language for data manipulation and analysis that compiles to SQL.
PRQL introduces a pipeline concept (similar to Unix pipes) that transforms data line-by-line. The sequential series of transformations
 reduces the complexity often encountered with nested SQL queries and makes your data manipulation logic easier to read and write.

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
* Sun May 5 2024 Vonng <rh@vonng.com> - 0.1.0
- Initial RPM release, used by Pigsty <https://pigsty.io>