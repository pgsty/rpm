%define debug_package %{nil}
%global pname pg_idkit
%global sname pg_idkit
%global pginstdir /usr/pgsql-%{pgmajorversion}

Name:		%{sname}_%{pgmajorversion}
Version:	0.2.3
Release:	1PIGSTY%{?dist}
Summary:	pg_idkit is a Postgres extension for generating many popular types of identifiers
License:	Apache-2.0
URL:		https://github.com/VADOSWARE/pg_idkit
#           https://github.com/VADOSWARE/pg_idkit/archive/refs/tags/v0.2.3.tar.gz

BuildRequires:	postgresql%{pgmajorversion}-devel pgdg-srpm-macros >= 1.0.27
Requires:	postgresql%{pgmajorversion}-server

%description
pg_idkit is a Postgres extension for generating many popular types of identifiers:
uuidv6, uuidv7, nanoid, ksuid, ulid, timeflake, pushid, xid, cuid, cuid2

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
* Sun May 5 2024 Vonng <rh@vonng.com> - 0.2.3
- Initial RPM release, used by Pigsty <https://pigsty.io>