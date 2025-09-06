%define debug_package %{nil}
%global pname plprql
%global sname plprql
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.0.0
Release:	1PIGSTY%{?dist}
Summary:	Use PRQL in PostgreSQL
License:	Apache-2.0
URL:		https://github.com/kaspermarstal/plprql
SOURCE0:    plprql-%{version}.tar.gz
#           https://github.com/kaspermarstal/plprql/archive/refs/tags/v1.0.0.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
PL/PRQL is a PostgreSQL extension that lets you write functions with PRQL. The extension supports PostgreSQL v12-16 on Linux and macOS.

PRQL (Pipelined Relational Query Language) is an open source query language for data manipulation and analysis that compiles to SQL.
PRQL introduces a pipeline concept (similar to Unix pipes) that transforms data line-by-line. The sequential series of transformations
 reduces the complexity often encountered with nested SQL queries and makes your data manipulation logic easier to read and write.

%prep
%setup -q -n %{sname}-%{version}

%build
cd %{pname}
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
* Sun May 05 2024 Vonng <rh@vonng.com> - 1.0.0
- Initial RPM release, used by Pigsty <https://pigsty.io>