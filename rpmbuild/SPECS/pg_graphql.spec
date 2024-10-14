%define debug_package %{nil}
%global pname pg_graphql
%global sname pg_graphql
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	1.5.9
Release:	1PIGSTY%{?dist}
Summary:	GraphQL support to your PostgreSQL database.
License:	Apache-2.0
URL:		https://github.com/supabase/pg_graphql
Source0:	pg_graphql-%{version}.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_graphql reflects a GraphQL schema from the existing SQL schema.
The extension keeps schema translation and query resolution neatly contained on your database server.
This enables any programming language that can connect to PostgreSQL to query the database via GraphQL with no additional servers, processes, or libraries.

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
* Mon Oct 14 2024 Vonng <rh@vonng.com> - 1.5.9
* Sun Oct 13 2024 Vonng <rh@vonng.com> - 1.5.8
* Thu Jul 18 2024 Vonng <rh@vonng.com> - 1.5.7
* Sat Jun 29 2024 Vonng <rh@vonng.com> - 1.5.6
* Sun May 5 2024 Vonng <rh@vonng.com> - 1.5.4
* Sat Apr 27 2024 Vonng <rh@vonng.com> - 1.5.3
* Sat Feb 17 2024 Vonng <rh@vonng.com> - 1.5.0
* Mon Jan 22 2024 Vonng <rh@vonng.com> - 1.4.4
* Wed Oct 11 2023 Vonng <rh@vonng.com> - 1.4.0
* Mon Sep 18 2023 Vonng <rh@vonng.com> - 1.3.0
- Initial RPM release, used by Pigsty <https://pigsty.io>